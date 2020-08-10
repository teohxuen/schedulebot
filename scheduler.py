from datetime import date, timedelta

def caldates(data):
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
    return start, end

def parseevent(data, svc, calstart, calend):
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
    return eventinfo

def checkdetail(eventinfo, calstart, calend):
    if eventinfo[1] < eventinfo[0]:  # check if event end date is after event start date
        print(eventinfo[3], "is invalid as the event end date is before its start date")
        return False
    if eventinfo[0] > calend: # check if event start date is after calendar end date
        print(eventinfo[3], "is invalid as the event start date is after the calendar end date")
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

def main():
    message = '''10 Aug 20 23 Aug 20
    ***REMOVED***, ***REMOVED***, ***REMOVED***, ***REMOVED***
    10 Aug, ***REMOVED*** Annually, 12 Aug
    11 Aug, ***REMOVED*** ***REMOVED***, 11 Aug 
    13 Aug, ***REMOVED*** PRE AVI, 13 Aug
    13 Aug, ***REMOVED*** AVI, 13 Aug 
    14 Aug, ***REMOVED*** ***REMOVED***, 14 Aug
    17 Aug, ***REMOVED*** ***REMOVED***, 19 Aug
    19 Aug, O1 ***REMOVED***, 20 Aug
    19 Aug, ***REMOVED***0 ***REMOVED***, 25 Aug
    19 Jul, ***REMOVED***1 ***REMOVED***, 20 Aug'''
    #Input will be start date, end date of calendar
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
    data = message.split("\n")

    # get the actual start and end date of the calendar
    # find if the start date is mon
    start, end = caldates(data[0])

    # get the svc ***REMOVED***
    svc = [a.strip() for a in data[1].split(',')] 

    # list of events
    events = []

    for i in range(2, len(data)):
        eventinfo = parseevent(data[i], svc, start, end)
        if checkdetail(eventinfo, start, end): # check if event is valid and append to list of events if valid
            events.append(eventinfo)
    
    events.sort() #sort by date

    calendar = createcal(start, end, svc) # create a calendar

    calendar = updatecal(start, end, events, calendar) # add events to the calendar



    for i in calendar:
        print(i)
    

main()
