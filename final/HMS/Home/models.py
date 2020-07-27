from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import *

def validate_image(image):
    file_size = image.file.size
    # limit_kb = 150
    # if file_size > limit_kb * 1024:
    #     raise ValidationError("Max size of file is %s KB" % limit)

    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
       raise ValidationError("Max size of file is %s MB" % limit_mb)
# Create your models here.
class Student(models.Model):
    HNAMES = (
        ('Godavari','Godavari Boys Hostel'),
        ('krishna','Krishna Boys Hostel'),
        ('sharadha','Sharadha Girls Hostel'),
        ('saraswathi','Saraswathi Girls Hostel'),
    )
    BRANCHES=(
        ('CSE','CSE'),
        ('IT','IT'),
        ('EEE','EEE'),
        ('MECH','MECH'),
        ('ECE','ECE'),
    )
    STD_STATUS=(
        ('In','Inside Hostel'),
        ('Out','Outside Hostel'),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    # we set null=True just for any other exception errors..but this name field cannot be empty
    email = models.CharField(max_length=200, null=True,validators=[validate_email])
    branch = models.CharField(max_length=200, null=True,choices=BRANCHES)
    hostel = models.CharField(max_length=200, null=True,choices=HNAMES)
    rollno = models.CharField(max_length=200,primary_key=True)
    father_name = models.CharField(max_length=200, null=True)
    father_mobile_no = models.CharField(max_length=200, null=True)
    mobile_no = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True,default='Specify correct address')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic= models.ImageField(null=True,default='default.png',validators=[validate_image])
    student_status=models.CharField(max_length=200,null=True,choices=STD_STATUS)
    # this __str__ function represents the name in database
    def __str__(self):
        return self.rollno

class Staff(models.Model):
    DESIG=(
        ('HM','Hostel Manager'),
        ('Caretaker','Caretaker'),
        ('maintainance','Maintainance'),
    )
    HNAMES = (
        ('Godavari', 'Godavari Boys Hostel'),
        ('krishna', 'Krishna Boys Hostel'),
        ('sharadha', 'Sharadha Girls Hostel'),
        ('saraswathi', 'Saraswathi Girls Hostel'),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True,validators=[validate_email])
    designation = models.CharField(max_length=200,null=True,choices=DESIG)
    hostel= models.CharField(max_length=200,null=True,choices=HNAMES)
    profile_pic = models.ImageField(null=True, default='default.png',validators=[validate_image])

    def __str__(self):
        return self.name

class Appeal(models.Model):
    TYPES=(
        ('home-out','Home-Out'),
        ('day-out','Day-Out'),
    )
    STATUS=(
        ('pending','Pending'),
        ('approved','Approved'),
        ('used','Used'),
    )
    student = models.ForeignKey(Student,null=True,on_delete=models.SET_NULL)
    staff = models.CharField(max_length=500,null=True,default='To be allocated')
    type = models.CharField(max_length=200,default='home-out',choices=TYPES)
    room_no = models.IntegerField(null=True)
    out_datetime = models.DateTimeField('Out Date&Time (yyyy-mm-dd 24hr:60min)',null=False)
    in_datetime = models.DateTimeField('In Date&Time(yyyy-mm-dd 24hr:60min)',null=False)
    reason = models.CharField(max_length=500,null=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS,default='pending')

    def __str__(self):
        return self.type