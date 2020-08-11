from datetime import date, timedelta
import shutil
import imgkit
import os   
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def botinit(update,context):
    # todo explain how to use the bot
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi I'm a bot that help to generate schedules to help you visualise better. Call '/help' for instructions!")

def bothelp(update, context):
    message = 'Please enter your message as shown:\n' +\
            '/make\n'+\
            '<calendar start><calendar end>\n'+\
            '<serviceable ***REMOVED***s>\n'+\
            '<event start>,<***REMOVED*** used><event name>,<event end>'
    example = '/make\n'+\
            '10 Aug 20 24 Aug 20\n'+\
            '***REMOVED***, ***REMOVED***, ***REMOVED***, ***REMOVED***\n'+\
            '11 Aug, ***REMOVED*** ***REMOVED***, 13 Aug\n'+\
            '14 Aug, ***REMOVED*** ***REMOVED***, 14 Aug\n'+\
            '17 Aug, ***REMOVED*** ***REMOVED***, 19 Aug\n'+\
            '20 Aug, O1 ***REMOVED***, 20 Aug\n'+\
            '24 Aug, ***REMOVED***, 24 Aug'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=example)

def caldates(data):
    try:
        dates = data.split()
        months ={"JAN":1, "FEB":2, "MAR":3, "APR":4, "MAY":5, "JUN":6, "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}
        startyear = int('20'+dates[2])
        endyear = int('20'+dates[5])
        startmonth = int(months[dates[1].upper()])
        endmonth = int(months[dates[4].upper()])
        startday = int(dates[0])
        endday = int(dates[3])
        start = date(startyear, startmonth, startday)
        end = date(endyear, endmonth, endday)
        start -= timedelta(days=start.weekday()) #change the starting date to the week monday
        end += timedelta(days=6-end.weekday())  #change the ending date to the week sunday
    except:
        return False, False
    return start, end

def parseevent(data, svc, calstart, calend):
    try:
        data.strip()
        info = [x.strip() for x in data.split(',')]
        months ={"JAN":1, "FEB":2, "MAR":3, "APR":4, "MAY":5, "JUN":6, "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}
        start = info[0].split()
        name = info[1]
        end = info[2].split()
        startday = int(start[0])
        startmonth = int(months[start[1].upper()])
        endday = int(end[0])
        endmonth = int(months[end[1].upper()])
        # attempt to handle the issue of years
        if startmonth < calstart.month:
            startyear = calend.year
        else:
            startyear = calstart.year
        if endmonth < calstart.month:
            endyear = calend.year
        else:
            endyear = calstart.year 
        startdate = date(startyear, startmonth, startday)
        enddate = date(endyear, endmonth, endday)
        temp = name.split()
        ***REMOVED*** = temp[0]
        eventinfo = [startdate, enddate, ***REMOVED***, name]
    except:
        return False
    return eventinfo

def checkdetail(eventinfo, calstart, calend, chatid, context):
    if eventinfo[1] < eventinfo[0]:  # check if event end date is after event start date
        context.bot.send_message(chat_id=chatid, text=f"{eventinfo[3]} is invalid as the event end date is before its start date")
        return False
    if eventinfo[0] > calend: # check if event start date is after calendar end date
        context.bot.send_message(chat_id=chatid, text=f"{eventinfo[3]} is invalid as the event start date is after the calendar end date")
        return False
    return True

def createcal(start, end, svc):
    #create array to imitate calendar
    calendar = []
    while start <= end:
        currdate = []
        #currdate.append(tempdate)
        currdate.append(start.strftime("%d %b")) #format into a readable date
        currdate.append(svc.copy()) # list of svc ***REMOVED***
        currdate.append([]) # list of events
        calendar.append(currdate)
        start += timedelta(days = 1) # increment date
    return calendar

def updatecal(start, end, events, calendar):
    for event in events:
        if event[0] < start: # if event start is before cal start
            startday = 0
        else:
            startday = (event[0] - start).days
        if event[1] > end: # if event end is after event end
            endday = (end - start).days
        else:
            endday = (event[1] - start).days
        for i in range(startday, endday + 1):
            calendar[i][2].append(event[3]) #add name of event to list of event on that day
            if event[2] in calendar[i][1]: # if ***REMOVED*** under servicing is one of the svc ***REMOVED***
                calendar[i][1].remove(event[2])
    return calendar


def scheduler(message, chatid, context):
    #Input will be start date, end date of calendars
    # monday is the first day of the week
    # months "jan feb mar apr may jun jul aug sept oct nov dec"
    # <start date of cal><end date of cal>
    # <serviceable ***REMOVED*** ordered in priority>
    # <start date> <***REMOVED***> <name of event> <end date>
    # for now just generate the image
    # future idea: show 2 weekly and send reminders, ixxf schedule
    # add in options to show aros priority, or when aros is up
    # better error messages and error handling
    # better handling of dates
    # merge cells

    script_dir = os.path.dirname(os.path.realpath("__file__"))
    rel_dir = "results"
    filepath = os.path.join(script_dir, rel_dir)
    # create results folder if it does not exisit
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    data = message.split("\n")

    data.pop(0) #remove /make

    if len(data) <= 2:
        context.bot.send_message(chat_id=chatid, text="Error: Message invalid, are you missing the list of serviceable ***REMOVED***?")
        return False

    # get the actual start and end date of the calendar
    # find if the start date is mon
    start, end = caldates(data[0])
    if not start:
        context.bot.send_message(chat_id=chatid, text="Error: Calendar Start/End date is invalid or missing")
        return False
    
    if start > end : # if calendar start date is after its end date
        context.bot.send_message(chat_id=chatid, text="Error: Calendar start date is after its end date")
        return False

    if (end-start).days > 93:
        context.bot.send_message(chat_id=chatid, text="Error: Calendar start date and end date differ by more than 3 months")
        return False

    # get the svc ***REMOVED***
    svc = [a.strip() for a in data[1].split(',')]
    for i in svc: # check if list of serviceable ***REMOVED*** is valid
        if i[:1] != "A" or len(i) != 2:
            context.bot.send_message(chat_id=chatid, text="List of serviceable ***REMOVED*** is invalid")
            return False

    # list of events
    events = []

    for i in range(2, len(data)):
        eventinfo = parseevent(data[i], svc, start, end)
        if not eventinfo: # if event is invalid
           context.bot.send_message(chat_id=chatid, text=f"Event: '{data[i]}' is invalid") 
        else:
            if checkdetail(eventinfo, start, end, chatid, context): # check if event is valid and append to list of events if valid
                events.append(eventinfo)
    
    events.sort() #sort by date

    calendar = createcal(start, end, svc) # create a calendar

    calendar = updatecal(start, end, events, calendar) # add events to the calendar
    
    shutil.copy('template.html', f'{filepath}/table{chatid}.html') # copy the template html
    file = open(f'{filepath}/table{chatid}.html','a')

    for week in range(0, len(calendar),7):
        # write the days
        file.write("<tr>")
        for day in range(7): 
            file.write(f"<th> {calendar[week+day][0]} </th>")
        file.write("</tr>")

        # write the events
        file.write("<tr>")
        for day in range(7): 
            if calendar[week+day][2] == "": # if no events
                file.write(f"<td>  </td>")
            else:
                file.write("<td>")
                for event in calendar[week+day][2]:
                    file.write(f"<div> {event}</div>")
                file.write("</td>")
        file.write("</tr>")

        # write the svc ***REMOVED***
        file.write("<tr>")
        for day in range(7): 
            if calendar[week+day][1] == "": # if no ***REMOVED***s
                file.write(f"<td>  </td>")
            else:
                ***REMOVED***s = ", ".join(calendar[week+day][1]) # join the list of ***REMOVED*** into a string
                file.write(f"<td> {***REMOVED***s} </td>")
        file.write("</tr>") 

    file.write("</table>")
    file.write("</table>")
    file.write("</body>")
    file.write("</html>")
    file.close()       

    imgkit.from_file(f'{filepath}/table{chatid}.html', f'{filepath}/out{chatid}.jpg')
    return filepath

def botschedule(update,context):
    filepath = scheduler(update.message.text, update.effective_chat.id, context)
    if filepath:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Here's your picture!")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f'{filepath}/out{update.effective_chat.id}.jpg', 'rb'))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Unfortunately we are unable to generate the schedule, check out /help for assistance")

def main():

    updater = Updater(token='***REMOVED***', use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', botinit)
    dispatcher.add_handler(start_handler) 

    help_handler = CommandHandler('help', bothelp)
    dispatcher.add_handler(help_handler) 

    scheduler_handler = CommandHandler('make', botschedule)
    dispatcher.add_handler(scheduler_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()  


main()