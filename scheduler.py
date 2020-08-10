import datetime

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
dates = data[0].split()
months ={"JAN":1, "FEB":2, "MAR":3, "APR":4, "MAY":5, "JUN":6, "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}
years = ['20' + dates[2], '20' + dates[5]]
umonths = [months[dates[1].upper()], months[dates[4].upper()]]
days = [dates[0], dates[3]]
start = datetime.date(int(years[0]),int(umonths[0]),int(days[0]))
end = datetime.date(int(years[1]),int(umonths[1]),int(days[1]))
start -= datetime.timedelta(days=start.weekday()) #change the starting date to the week monday
end += datetime.timedelta(days=6-end.weekday())  #change the ending date to the week sunday
print(start,end)
svc = [a.strip() for a in data[1].split(',')] #get the svc ***REMOVED***
print(svc)