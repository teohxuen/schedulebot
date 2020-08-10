import datetime

def caldates(data):
    dates = data.split()
    months ={"JAN":1, "FEB":2, "MAR":3, "APR":4, "MAY":5, "JUN":6, "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}
    startyear = int('20'+dates[2])
    endyear = int('20'+dates[5])
    startmonth = int(months[dates[1].upper()])
    endmonth = int(months[dates[4].upper()])
    startday = int(dates[0])
    endday = int(dates[3])
    start = datetime.date(startyear, startmonth, startday)
    end = datetime.date(endyear, endmonth, endday)
    start -= datetime.timedelta(days=start.weekday()) #change the starting date to the week monday
    end += datetime.timedelta(days=6-end.weekday())  #change the ending date to the week sunday
    print(start,end)
    return start, end

def event(data, svc, calstart, calend):
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
    startdate = datetime.date(startyear, startmonth, startday)
    enddate = datetime.date(endyear, endmonth, endday)
    ***REMOVED*** = name[0:2] #***REMOVED*** down for event
    eventinfo = [startdate, enddate, ***REMOVED***, name]
    print(eventinfo)
    return eventinfo

def main():
    message = '''10 Aug 20 23 Aug 20
    ***REMOVED***, ***REMOVED***, ***REMOVED***, ***REMOVED***
    10 Aug, ***REMOVED*** Annually, 12 Aug
    11 Aug, ***REMOVED*** ***REMOVED***, 11 Aug 
    13 Aug, ***REMOVED*** PRE AVI, 13 Aug
    13 Aug, ***REMOVED*** AVI, 13 Aug 
    14 Aug, ***REMOVED*** ***REMOVED***, 14 Aug
    17 Aug, ***REMOVED*** ***REMOVED***, 19 Aug
    19 Aug, O1 ***REMOVED***, 20 Aug'''
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

    #get the svc ***REMOVED***
    svc = [a.strip() for a in data[1].split(',')] 
    print(svc)

    events = []

    for i in range(2, len(data)):
        eventinfo = event(data[i], svc, start, end)
        events.append(eventinfo)
    
    events.sort() #sort by date


main()
