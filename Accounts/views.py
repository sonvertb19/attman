from django.shortcuts import render
from  django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
from . import forms
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Accounts.models import Subject, Timetable, Attendance, Student, SemDetails
from datetime import timedelta, date
from datetime import datetime, time
from django.contrib.auth.mixins import LoginRequiredMixin

import json


def check_sem_details(request_passed):
	x = SemDetails.objects.filter(user = request_passed.user)

	if x:
		x = SemDetails.objects.get(user = request_passed.user)
		sem_start = x.sem_start
		sem_end = x.sem_end

		# This is the default value of model fields.
		if str(sem_start) == "1900-01-01":
			if str(sem_end) == "1900-01-01":
				return False

		return True

def Index(request):

	if (request.user.is_authenticated):
		sem_details = check_sem_details(request)
		context = {'sem_details': sem_details}
	else:
		context = {'sem_details': True}

	return render(request, "Accounts/index.html", context)

class add_sem_details(CreateView, LoginRequiredMixin):
	model = SemDetails
	template_name = "Accounts/add_sem_details.html"
	# fields = ['sem_start', 'sem_end']
	form_class = forms.Sem_details_form
	success_url = reverse_lazy('index')

	def get_initial(self):
		initial = super().get_initial()
		initial.update({ 'sem_start': datetime.now(), 'sem_end': datetime.now() })
		return initial

	def form_valid(self,form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class UserRegistration(CreateView):
	model = Student
	template_name = "Accounts/user_reg.html"
	form_class = forms.UserForm
	success_url = reverse_lazy('login')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('logout_user'))

def logout_user(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('index'))
	else:
		return render(request, "Accounts/logout.html")


def user_login(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('index'))
	else:
		if request.method == "GET":
			return render(request, "Accounts/login.html")

		elif request.method == "POST":

			username = request.POST.get('Username')
			password = request.POST.get('Password')

			user = authenticate(username = username, password = password)

			user_info={}
			if user:
				# print("inside if user")
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('index'))
				else:
					return HttpResponse("<h1>Account Not Active</h1>")

			else:
				user_info.update({'errors': "Invalid Credentials!"})

				return render(request, "Accounts/login.html", context = user_info)

def day_int_to_name(day_int):

	if int(day_int)==0:
		day_str= 'Monday'
	elif int(day_int)==1:
		day_str= 'Tuesday'
	elif int(day_int)==2:
		day_str= 'Wednesday'
	elif int(day_int)==3:
		day_str= 'Thursday'
	elif int(day_int)==4:
		day_str= 'Friday'
	elif int(day_int)==5:
		day_str= 'Saturday'
	elif int(day_int)==6:
		day_str= 'Sunday'

	return day_str

def day_int_to_short_name(day_int):

	if int(day_int)==0:
		day_str= 'Mon'
	elif int(day_int)==1:
		day_str= 'Tue'
	elif int(day_int)==2:
		day_str= 'Wed'
	elif int(day_int)==3:
		day_str= 'Thu'
	elif int(day_int)==4:
		day_str= 'Fri'
	elif int(day_int)==5:
		day_str= 'Sat'
	elif int(day_int)==6:
		day_str= 'Sun'

	return day_str

@login_required
def SubjectListView(request):
	if request.method == "GET":

		subject_list = Subject.objects.filter(user = request.user).order_by('title');

		context = {'subject_list': subject_list}

		subject_detailed_list = {}

		for subject in subject_list:
			# print(subject)
			timetable_s = Timetable.objects.filter(user = request.user, subject = subject)

			total_classes_held = 0
			total_classes_attended = 0
			total_classes_bunked = 0

			for timetable in timetable_s:
				attendance_s = Attendance.objects.filter(timetable = timetable)

				for att in attendance_s:
					if att.value_int == 0:
						total_classes_bunked = total_classes_bunked + 1
					if att.value_int == 1:
						total_classes_attended = total_classes_attended + 1

			total_classes_held = total_classes_attended + total_classes_bunked

			# print("Total Classes Attended = " + str(total_classes_attended))
			# print("Total Classes Held     = " + str(total_classes_held))


			if total_classes_held != 0:
				x = total_classes_attended/total_classes_held
				subject.percentage = x * 100
				# print(subject.percentage)


			classes_required = (3 * total_classes_held) - (4 * total_classes_attended)
			bunks_available = ((4 * total_classes_attended) - (3 * total_classes_held) )/ 3

			if classes_required <= 0:
				classes_required = "You are on track."
				bunks_available = str(bunks_available) + " bunks available."

			else:
				classes_required = str(classes_required) + " class required."

			# print(str(subject))
			subject_name = subject.title

			subject_detailed_list.update({
				str(subject_name):{
					'timetable' : [],
					'total_classes_attended': total_classes_attended,
					'total_classes_bunked': total_classes_bunked,
					'total_classes_held': total_classes_held,
					'classes_required': classes_required,
					'bunks_available': bunks_available,
				}
			})
			subject_timetable = Timetable.objects.filter(user = request.user, subject = subject)

			for s in subject_timetable:
				# print(s.day)
				# print(s.period)
				subject_detailed_list[str(subject_name)]['timetable'].append(
					{
						'day': day_int_to_name(s.day),
						'time': str(s.time.strftime('%I:%M %p')),
					}
				)


		subject_detailed_list = json.dumps(subject_detailed_list, sort_keys=True, indent=4)
		# print(subject_detailed_list)

		context.update({'subject_detailed_list': subject_detailed_list})


		return render(request, "Accounts/subject_list.html",context)


	elif request.method == "POST":

		subject_title = request.POST.get('subject_title')

		error = False

		s = Subject.objects.filter(title = subject_title, user = request.user).count()

		if(s > 0):
			error = 'Subject Already Exists.'

		else:
			s = Subject.objects.create(title = subject_title, user = request.user)
			s.save()


		subject_list = Subject.objects.filter(user = request.user).order_by('title');

		context = {'subject_list': subject_list}

		subject_detailed_list = {}

		for subject in subject_list:
			# print(subject)
			timetable_s = Timetable.objects.filter(user = request.user, subject = subject)

			total_classes_held = 0
			total_classes_attended = 0
			total_classes_bunked = 0

			for timetable in timetable_s:
				attendance_s = Attendance.objects.filter(timetable = timetable)

				for att in attendance_s:
					if att.value_int == 0:
						total_classes_bunked = total_classes_bunked + 1
					if att.value_int == 1:
						total_classes_attended = total_classes_attended + 1

			total_classes_held = total_classes_attended + total_classes_bunked

			# print("Total Classes Attended = " + str(total_classes_attended))
			# print("Total Classes Held     = " + str(total_classes_held))

			subject.total_classes_bunked = total_classes_bunked
			subject.total_classes_attended = total_classes_attended
			subject.total_classes_held = total_classes_held

			if total_classes_held != 0:
				x = total_classes_attended/total_classes_held
				subject.percentage = x * 100
				# print(subject.percentage)


			# print(str(subject))
			subject_name = subject.title

			subject_detailed_list.update({
				str(subject_name):{
					'timetable' : [],
					'total_classes_attended': total_classes_attended,
					'total_classes_bunked': total_classes_bunked,
					'total_classes_held': total_classes_held,
				}
			})
			subject_timetable = Timetable.objects.filter(user = request.user, subject = subject)

			for s in subject_timetable:
				# print(s.day)
				# print(s.period)
				subject_detailed_list[str(subject_name)]['timetable'].append({
						'day': day_int_to_name(s.day),
						'time': str(s.time.strftime('%I:%M %p')),
					}
				)


		subject_detailed_list = json.dumps(subject_detailed_list, sort_keys=True, indent=4)

		# print(subject_detailed_list)

		context = {'subject_list': subject_list, 'error': error}

		context.update({'subject_detailed_list': subject_detailed_list})

		return render(request, "Accounts/subject_list.html",context)



class SubjectUpdateView(UpdateView, LoginRequiredMixin):
	model = Subject
	fields = ['title']
	template_name="Accounts/update_subject.html"
	success_url = reverse_lazy('subject_list')


class SubjectDeleteView(DeleteView, LoginRequiredMixin):
	model = Subject
	template_name="Accounts/delete_subject.html"
	success_url = reverse_lazy('subject_list')
	# user_info={}
	# if user:
	# 	print("inside if user")
	# 	if user.is_active:
	# 		login(request, user)

@login_required
def Dayslist(request):
	sem_details = check_sem_details(request)
	context = {'sem_details': sem_details}

	return render (request,"Accounts/days_list.html",context)


# class TimetableCreateView(CreateView):
# 	model=Timetable
# 	template="Accounts/timetable_form.html"
# 	success_url= reverse_lazy('days')


# 	def form_valid(self,form):
# 		form.instance.user = self.request.user
# 		return super().form_valid(form)

@login_required
def TimetableCreateView(request):

	sem_details = check_sem_details(request)
	context = {'sem_details': sem_details}

	if request.method =="POST":

		u = request.user
		day  = request.POST.get('day')
		time = request.POST.get('Time')
		subject_pk = request.POST.get('subject')
		venue = request.POST.get('venue')

		subject = Subject.objects.get(pk=subject_pk)

		c = Timetable.objects.filter(day=day, time=time, user = u).count()


		if(c > 0):
			# A timetable at that time of that day exists.

			error = "You have already entered a class at that time of day."

			# print(form)
			day_int = request.POST.get("day")

			day_str = day_int_to_name(day_int)

			context.update({'error': error, 'day_int': day_int ,'day_str': day_str})

			return render(request, "Accounts/timetable_form.html",context)



		if venue:
			t = Timetable.objects.create(subject = subject, day=day, time=time, user = u, venue = venue)
		else:
			t = Timetable.objects.create(subject = subject, day=day, time=time, user = u, venue = "---")

		t.save()

		day = int(day)

		# print(day)
		# print(type(day))

		# Creating attendence for added time table.
		x = SemDetails.objects.get(user = request.user)

		sem_start = x.sem_start
		sem_end = x.sem_end

		# print(sem_start)
		# print(sem_end)

		start_date = sem_start
		end_date = sem_end

		# Total number of days.
		number_of_days_in_sem = int ((sem_end - sem_start).days)

		# Reading every date between sem_start and sem_end
		for x in range(0,number_of_days_in_sem + 1):
			single_date = start_date + timedelta(x)
			# print(single_date.strftime("%Y-%m-%d"))
			if single_date.weekday() == day:

				# print(single_date.strftime("%A") + " found" + " (" + single_date.strftime("%Y-%m-%d") + ") ")
				a = Attendance.objects.create(Date = single_date, user = request.user, timetable = t)
				a.save()

		if start_date.weekday() == day:
			a = Attendance.objects.create(Date = start_date, user = request.user, timetable = t)
			a.save()

		if end_date.weekday() == day:
			a = Attendance.objects.create(Date = end_date, user = request.user, timetable = t)
			a.save()

		# print(reverse('timetable') + "?day=" + str(day))

		# return HttpResponseRedirect(reverse('timetable') + "?day=" + str(day))
		return HttpResponseRedirect(reverse('days'))

	else:
		# print(form)
		subjects = Subject.objects.filter(user=request.user)

		day_int = request.GET.get("day")

		day_str = day_int_to_name(day_int)

		context.update({'day_int': day_int ,'day_str': day_str, 'subjects': subjects})

		return render(request, "Accounts/timetable_form.html",context)

@login_required
def TimetableList(request):

	sem_details = check_sem_details(request)
	context = {'sem_details': sem_details}

	if request.method == "GET":
		# print(form)
		# day_int = request.GET.get("day")

		timetable_list = Timetable.objects.filter(user = request.user).order_by('day', 'time');
		# print(timetable_list)

		# As day are stored as integers, converting them into Day Names
		for x in timetable_list:

			day_int = x.day

			if int(day_int)==0:
				x.day = 'Monday'
			elif int(day_int)==1:
				x.day = 'Tuesday'
			elif int(day_int)==2:
				x.day = 'Wednesday'
			elif int(day_int)==3:
				x.day = 'Thursday'
			elif int(day_int)==4:
				x.day = 'Friday'
			elif int(day_int)==5:
				x.day = 'Saturday'
			elif int(day_int)==6:
				x.day = 'Sunday'


		context.update({'timetable_list': timetable_list})

		return render(request, "Accounts/timetable_list.html",context)

class TimetableUpdateView(UpdateView, LoginRequiredMixin):
	model = Timetable
	fields = ['subject','time','day', 'venue']
	template_name="Accounts/update_timetable.html"
	success_url = reverse_lazy('timetable_list')

	def get_context_data(self, **kwargs):
		context = super(TimetableUpdateView, self).get_context_data(**kwargs)
		sem_details = check_sem_details(self.request)
		context.update({'sem_details': sem_details})
		return context



class TimetableDeleteView(DeleteView, LoginRequiredMixin):
	model = Timetable
	template_name="Accounts/delete_timetable.html"
	success_url = reverse_lazy('timetable_list')

	def get_context_data(self, **kwargs):
		context = super(TimetableDeleteView, self).get_context_data(**kwargs)
		sem_details = check_sem_details(self.request)
		context.update({'sem_details': sem_details})
		return context

@login_required
def AttendanceView(request):

	sem_details = check_sem_details(request)
	context = {'sem_details': sem_details}

	if sem_details:
		pass
	else:
		return render(request, "Accounts/attendance.html", context)

	error = ""
	date_entered = ""

	if request.method =="GET":
		d = request.GET.get('Date')

		if d:
			pass
		else:
			d = datetime.now()
			d = d.strftime('%Y-%m-%d')

		x = SemDetails.objects.get(user = request.user)
		sem_start = x.sem_start
		sem_end = x.sem_end

		D = datetime.strptime(d, '%Y-%m-%d').date()

		if D < sem_start:
			error = "The semester did not start by then! ;)"
			date_entered = D.strftime('%d-%B-%Y')
			d = sem_start
			d = d.strftime('%Y-%m-%d')

		if D > datetime.now().date():
			error = "Adding/Viewing future attendance not allowed!"
			date_entered = D.strftime('%d-%B-%Y')
			d = datetime.now()
			d = d.strftime('%Y-%m-%d')

		if D > sem_end:
			error = "The semester will be over by then! ;)"
			date_entered = D.strftime('%d-%B-%Y')
			d = sem_end
			d = d.strftime('%Y-%m-%d')


		D = datetime.strptime(d, '%Y-%m-%d')

		yesterday_date = D - timedelta(1)
		tomorrow_date = D + timedelta(1)

		yesterday_string = yesterday_date.strftime('%Y-%m-%d')
		tomorrow_string = tomorrow_date.strftime('%Y-%m-%d')

		# print("yesterday = " + yesterday_string)
		# print("tomorrow = " + tomorrow_string)

		date_readable = D.strftime('%d-%B-%Y')
		day_int = D.weekday()
		day = D.strftime('%A')

		timetable = Timetable.objects.filter(day = day_int, user = request.user).order_by('day', 'time')

		for x in timetable:
			# print(x);
			a = Attendance.objects.get(timetable = x, user = request.user, Date = d)
			# print(a.value_int)
			x.value_int = int(a.value_int)

		# day_attendence_records = {}

		# for x in timetable:

		# 	a = Attendance.objects.get(timetable = x, user = request.user, Date = d)

		# 	subject = str(x.subject)
		# 	time = str(x.time)
		# 	value_str = str(a.value_str)

		# 	day_attendence_records.update({
		# 		str(x.subject): {
		# 			'subject': subject,
		# 			'time': time,
		# 			'value_str': value_str
		# 		}
		# 	})

		# c = {'a': 'aa'}

		# print(c['a'])
		# for x in day_attendence_records:
		# 	print(x)





		# print(timetable)
		# for a in timetable:
			# print(a.user)
			# print(a.subject)
			# print(a.day)
			# print(a.period)
			# print(a.value_int)
		# print("asdasd")
		context.update({'error': error, 'date_entered': date_entered, 'day_timetable': timetable,'yesterday': yesterday_string, 'tomorrow': tomorrow_string, 'date': d, 'date_readable': date_readable, 'day': day})

		return render(request, "Accounts/attendance.html", context)


@login_required
def mark_attendance(request):

	if request.method == "POST":
		HttpResponse("<html><body><h4>Only GET allowed.</h4></body></html>")

	elif request.method == "GET":
		t_pk = request.GET.get("t_pk")
		date = request.GET.get("date")
		# print(date)
		value_int = request.GET.get("value")

		if int(value_int) == 1:
			value_str = "Present"
		elif int(value_int) == 0:
			value_str = "Absent"
		elif int(value_int) == 2:
			value_str = "Cancelled"

		t = Timetable.objects.get(pk = t_pk)
		# print(t)
		a = Attendance.objects.filter(timetable = t, user = request.user, Date = date)
		# print(a)
		a.update(value_int = value_int, value_str = value_str)

		# for x in a:
			# print(str(x) + " -> " + str(x.value_str))
		return HttpResponseRedirect(reverse('attendance') + "?Date=" + str(date))

@login_required
def SubjectWiseAttendanceList(request):

	if request.method == "GET":

		subject_pk = request.GET.get('sub')

		if subject_pk:
			# Find attendance of that subject.
			subject_s = Subject.objects.get(pk = int(subject_pk))

			subject_name = subject_s.title
			context = {'subject_name': subject_name}

			subject_detailed_list = {}

			timetable_s = Timetable.objects.filter(user = request.user, subject = subject_s)

			# print(timetable_s)

			total_classes_held = 0
			total_classes_attended = 0
			total_classes_bunked = 0
			total_classes_cancelled = 0
			percentage = 0

			classes_list = {}

			for timetable in timetable_s:
				attendance_s = Attendance.objects.filter(timetable = timetable).order_by("-Date")

				today = date.today()
				# print(today)

				for att in attendance_s:

					if att.Date <= date.today():
						# print(str(att.pk) + " -> " + str(att.Date) + " -> " + str(att.timetable.time) + " -> " + str(day_int_to_name(att.timetable.day)))

						if att.value_int == 0:
							total_classes_bunked = total_classes_bunked + 1

						if att.value_int == 1:
							total_classes_attended = total_classes_attended + 1

						if att.value_int == 2:
							total_classes_cancelled = total_classes_cancelled + 1

						classes_list.update({
							# Combining date and time of class to convert into epoh
							# so that it can be sorted and also
							# so that a class twice on same day can be recorded.
							datetime.combine(att.Date, att.timetable.time).timestamp():
								{
									'date_yyyy_mm_dd' : str(att.Date.strftime("%Y-%m-%d")),
									'date': str(att.Date.strftime("%d-%b-%Y")),
									'day': str(day_int_to_short_name(att.timetable.day)),
									'time': att.timetable.time.strftime('%I:%M %p'),
									'attendance_value_int': att.value_int,
									'attendance_value_str': att.value_str,
								}
						})

					else:
						pass

			# The key in the objects are the epoch timestamps of the dates.
			# Sort Keys = True sorts the date.
			classes_list = json.dumps(classes_list, sort_keys=True, indent=4)
			# print(classes_list)

			total_classes_held = total_classes_attended + total_classes_bunked

			# print("Total Classes Attended = " + str(total_classes_attended))
			# print("Total Classes Held     = " + str(total_classes_held))

			if total_classes_held != 0:
				x = total_classes_attended/total_classes_held
				percentage = round(x * 100, 2)
				# print(subject.percentage)

			classes_required = (3 * total_classes_held) - (4 * total_classes_attended)
			bunks_available = ((4 * total_classes_attended) - (3 * total_classes_held) )/ 3
			bunks_available = int(bunks_available)

			if classes_required <= 0:
				classes_required = "You are on track."
				if(bunks_available == 0):
					bunks_available = ""
				elif(bunks_available == 1):
					bunks_available = str(bunks_available) + " bunk available!"
				else:
					bunks_available = str(bunks_available) + " bunks available!"

			else:
				# bunks_available = "No bunks available."
				classes_required = str(classes_required) + " class required."

			subject_detailed_list.update({
				str(subject_name):{
					'timetable' : [],
					'total_classes_attended': total_classes_attended,
					'total_classes_bunked': total_classes_bunked,
					'total_classes_cancelled': total_classes_cancelled,
					'total_classes_held': total_classes_held,
					'percentage': percentage,
					'classes_required': classes_required,
					'bunks_available': bunks_available,
				}
			})
			subject_timetable = Timetable.objects.filter(user = request.user, subject = subject_s).order_by('day', 'time')

			for s in subject_timetable:
				# print(s.day)
				# print(s.period)
				subject_detailed_list[str(subject_name)]['timetable'].append(
					{
						'day': day_int_to_name(s.day),
						'time': str(s.time.strftime('%I:%M %p')),
					}
				)

			subject_detailed_list = json.dumps(subject_detailed_list, sort_keys=True, indent=4)

			# print(subject_detailed_list)

			context.update({'subject_detailed_list': subject_detailed_list, 'classes_list': classes_list})

			# print(classes_list)

			return render(request, 'Accounts/subject_wise_attendance_list.html', context)
		else:
			# Render empty form which comtains list of subject.
			subject_list = Subject.objects.filter(user = request.user).order_by('title')

			# for x in subject_list:
				# print(x.title)

			context = {'subject_list': subject_list}

			return render(request, 'Accounts/subject_wise_attendance_list_form.html', context)