from datetime import date, timedelta
import shutil
import imgkit
import os   
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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
        start -= timedelta(days=start.weekday()) #change the starting day of the week to monday
        end += timedelta(days=6-end.weekday())  #change the ending day of the week to sunday
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
        if len(info) == 2: #if event ends on the same day, only event start date is required
            end = start
        else:
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
        temp = name.split(":")
        veh = temp[0]
        eventinfo = [startdate, enddate, veh, name]
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
        currdate.append(start.strftime("%d %b")) #format into a readable date
        currdate.append(svc.copy()) # list of veh
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
            calendar[i][2].append(event[3]) # add name of event to list of event on that day
            if event[2] in calendar[i][1]: # if vehicle under servicing is one of the veh being tracked
                calendar[i][1].remove(event[2])
    return calendar


def scheduler(message, chatid, context):
    # Input will be start date, end date of calendars
    # monday is the first day of the week
    # months "jan feb mar apr may jun jul aug sept oct nov dec"
    # TODO: Merge cells if they have the same event

    script_dir = os.path.dirname(os.path.realpath("__file__"))
    rel_dir = "results"
    filepath = os.path.join(script_dir, rel_dir)
    # create results folder if it does not exisit
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    data = message.split("\n")

    data.pop(0) #remove '/make'

    if len(data) <= 2:
        context.bot.send_message(chat_id=chatid, text="Error: Message invalid, are you missing the list of vehicles?")
        return False

    # get the actual start and end date of the calendar
    start, end = caldates(data[0])
    if not start:
        context.bot.send_message(chat_id=chatid, text="Error: Calendar Start/End date is invalid or missing")
        return False
    
    if start > end : # if calendar start date is after its end date
        context.bot.send_message(chat_id=chatid, text="Error: Calendar start date is after its end date")
        return False

    if (end-start).days > 105: # to ensure gap between calendar start and end date is within 3 months
        context.bot.send_message(chat_id=chatid, text="Error: Calendar start date and end date differ by more than 3 months")
        return False

    # get the veh
    svc = [a.strip() for a in data[1].split(',')]

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
        
        # write the available veh
        file.write("<tr>")
        for day in range(7): 
            if calendar[week+day][1] == "": # if no veh
                file.write(f"<td>  </td>")
            else:
                veh = ", ".join(calendar[week+day][1]) # join the list of veh into a string
                file.write(f"<td> {veh} </td>")
        file.write("</tr>") 

    file.write("</table>")
    file.write("</table>")
    file.write("</body>")
    file.write("</html>")
    file.close()       

    imgkit.from_file(f'{filepath}/table{chatid}.html', f'{filepath}/out{chatid}.jpg')
    return filepath