# import os
# from datetime import date, timedelta
#
# start = date(year = 2016, month = 1, day = 1)
#
# for i in range(44, 53):
#     wstart = start + timedelta(days = 7 * (i - 1))
#     wend = start + timedelta(days = 7 * (i - 1) + 6)
#     if i == 52:
#         wend += timedelta(days = 2)
#     command = "scrapy crawl movie -a start=%s -a end=%s -a accept_noscore=True -a week=%d -L WARNING" % (wstart.strftime("%m-%d"), wend.strftime("%m-%d"), i)
#     # os.system(command)
#     print command

import pytz, datetime

timeUTC = datetime.datetime(2013, 5, 23, 19, 27, 50, 0)
print(timeUTC.strftime('%H:%M:%S'))
timezoneLocal = pytz.timezone('Asia/Shanghai')
utc = pytz.utc
timeLocal = utc.localize(timeUTC).astimezone(timezoneLocal)
print(timeLocal.strftime('%H:%M:%S'))