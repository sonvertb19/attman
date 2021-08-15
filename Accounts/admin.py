from django.contrib import admin
from Accounts.models import Student,Subject,Timetable,Attendance, SemDetails
# Register your models here.

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Timetable)
admin.site.register(Attendance)
admin.site.register(SemDetails)
