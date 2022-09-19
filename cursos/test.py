from datetime import datetime, date, timedelta, time


initDate = '07/28/2022'
print('initDate: ',initDate)
replace = initDate.replace('/','-')
print('replace: ',replace)
date = datetime.strptime(replace, '%m-%d-%Y').date()
print('date: ',date)