from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *
from django.contrib.admin import widgets
from bootstrap_datepicker_plus import DateTimePickerInput

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class studentprofileForm(ModelForm):
	class Meta:
		model=Student
		fields='__all__'
		exclude=['user','date_created','rollno','branch','student_status']


class ContactForm(forms.Form):
	name = forms.CharField(max_length=100)
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea(attrs={'rows':8, 'cols':25}))


# class studentstatusForm(ModelForm):
# 	class Meta:
# 		model=Student
# 		fields=['student_status']
class staffprofileForm(ModelForm):
	class Meta:
		model=Staff
		fields='__all__'
		exclude=['user','designation']
# class updaterequestForm(ModelForm):
# 	class Meta:
# 		model=Appeal
# 		fields=['status']
# class createappealForm(ModelForm):
# 	class Meta:
# 		model=Appeal
# 		fields=['type','out_date','in_date','out_time','in_time','reason']
# 		exclude = ['student','staff','status']
#
class DateTimeInput(forms.DateTimeInput):
	input_type = "datetime-local"
	def __init__(self, **kwargs):
		kwargs["format"] = "%Y-%m-%dT%H:%M"
		super().__init__(**kwargs)


class createapealForm2(forms.Form):
	TYPES=(
		('home-out','Home-Out'),
		('day-out','Day-out'),
	)
	type=forms.ChoiceField(choices=TYPES)
	room_no=forms.IntegerField(required=True)
	out_date=forms.DateField(required=True,widget=widgets.AdminDateWidget())
	out_time=forms.TimeField(required=True,widget=widgets.AdminTimeWidget())
	in_date=forms.DateField(required=True,widget=widgets.AdminDateWidget())
	in_time=forms.TimeField(required=True,widget=widgets.AdminTimeWidget())
	timings_to_contact = forms.CharField(required=True)
	reason=forms.CharField(required=True)

