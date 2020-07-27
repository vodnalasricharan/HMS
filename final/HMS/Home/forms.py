from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class studentprofileForm(ModelForm):
	class Meta:
		model=Student
		fields='__all__'
		exclude=['user','date_created','rollno','branch','student_status']
class staffprofileForm(ModelForm):
	class Meta:
		model=Staff
		fields='__all__'
		exclude=['user','designation']

# class createappealForm(ModelForm):
# 	class Meta:
# 		model=Appeal
# 		fields=['type','out_date','in_date','out_time','in_time','reason']
# 		exclude = ['student','staff','status']
#
# class createapealForm2(forms.Form):
# 	TYPES=(
# 		('home-out','Home-Out'),
# 		('day-out','Day-Out'),
# 		   )
# 	type=forms.CharField(widget=forms.Select(choices=TYPES))
# 	room_no=forms.IntegerField()
# 	out_date=forms.DateField(widget=forms.SelectDateWidget,input_formats=['%Y-%m-%d'])
# 	in_date = forms.DateField(widget=forms.SelectDateWidget,input_formats=['%Y-%m-%d'])
# 	out_time=forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
# 	in_time= forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
# 	reason = forms.CharField()
