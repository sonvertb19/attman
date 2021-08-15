import csv

from Accounts import models
from django.db.models import Sum
from datetime import timedelta
import datetime

sno = 1
dates = []
attendence = [["SNo", "Date", "Classes Attended", "Classes Held"],]

u = models.User
s = u.objects.get(username = "sonvert")

# Creating attendence for added time table.
x = models.SemDetails.objects.get(user = s)

start_date = x.sem_start
end_date = x.sem_end

present_date = datetime.datetime.now().date()

if end_date < present_date:
	end_date = sem_end
else:
	end_date = present_date

number_of_days_till_date = int ((end_date - start_date).days)

# Reading every date between sem_start and sem_end

for x in range(0,number_of_days_till_date + 1):
	single_date = start_date + timedelta(x)
	date = single_date.strftime("%Y-%m-%d")

	print("\n\n" + date + "\n")

	attended = 0
	bunked = 0

	day_int = single_date.weekday()

	timetable = models.Timetable.objects.filter(day = day_int, user = s)

	for x in timetable:
		val_str = ""

		# print(x);
		a = models.Attendance.objects.get(timetable = x, user = s, Date = single_date)
		# x.value_int = int(a.value_int)

		if a.value_int == 1:
			attended = attended + 1
			val_str = "Present"

		elif a.value_int == 0:
			val_str = "Absent"
			bunked = bunked + 1

		elif a.value_int == 2:
			val_str = "Cancelled"

		elif a.value_int == -1:
			val_str = "Not Marked"

		print("\t" + a.timetable.subject.title + ": " + str(a.value_int) + " (" + val_str + ")")

	print("\n\tTotal Classes attended: " + str(attended))
	print("\n\tTotal Classes held: " + str(attended + bunked))

	row = [sno, date, attended, attended + bunked]

	attendence.append(row)

	sno = sno + 1

csv.register_dialect('myDialect', quoting = csv.QUOTE_ALL, skipinitialspace=True)

with open('date_wise_attendance.csv', 'w') as f:
	writer = csv.writer(f, dialect='myDialect')
	for row in attendence:
		writer.writerow(row)

f.close()