from django import forms
from django.contrib.auth.forms import UserCreationForm
from Accounts.models import Student, Subject, Timetable, Attendance, SemDetails
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import date


class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'password1', 'password2']

	def clean_email(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		if email and User.objects.filter(email=email).count() > 0:
			raise forms.ValidationError('This email address is already registered.')
		return email

class CalenderForm(ModelForm):
	class Meta:
		model = Attendance
		fields = ['Date','timetable','value']

class Sem_details_form(ModelForm):
	
	class Meta:
		model = SemDetails

		fields = ['sem_start', 'sem_end']

		widgets = {
			'sem_start': forms.DateInput(attrs = {'type': 'date', 'class': 'date_field'}),
			'sem_end': forms.DateInput(attrs = {'type': 'date', 'class': 'date_field'}),
			}

	def clean(self):
		cleaned_data=super(Sem_details_form, self).clean()
		
		print(cleaned_data)
		
		sem_start = cleaned_data.get('sem_start')
		sem_end = cleaned_data.get('sem_end')

		print(sem_start)
		print(sem_end)

		if(sem_start >= sem_end):
			raise forms.ValidationError('The start date can not be equal/greater than end date.')
		else:
			return cleaned_data
