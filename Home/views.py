from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .decorators import *
import qrcode
from django.conf import settings
import os
from datetime import datetime
import pytz
from .filters import *
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

utc=pytz.UTC

# Create your views here.
#################################################   HOMEPAGE   #########################################
def home(request):
    if request.user.is_authenticated:
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'student':
                return redirect('studenthome')
            if group == 'HM':
                return redirect('HMhome')
            if group == 'staff':
                return redirect('caretakerhome')
            if group == 'security':
                return redirect('securitylogin')

    total=Student.objects.all().count()
    inside=Student.objects.filter(student_status='In').count()
    context={'total':total,'inside':inside}
    return render(request,'Home/Home.html',context)

@unauthenticated_user
def godavari(request):
    total=Student.objects.filter(hostel='Godavari')
    if total:
        inside=Student.objects.filter(student_status='In',hostel='Godavari').count()
    else:
        inside=0
    total=total.count()
    context={'total':total,'inside':inside}
    return render(request, 'Home/godavari.html',context)
@unauthenticated_user
def krishna(request):
    total=Student.objects.filter(hostel='krishna')
    print()
    if total:
        inside=Student.objects.filter(student_status='In',hostel='krishna').count()
    else:
        inside=0
    total=total.count()
    context={'total':total,'inside':inside}
    return render(request, 'Home/krishna.html',context)
@unauthenticated_user
def sharadha(request):
    total=Student.objects.filter(hostel='sharadha')
    if total:
        inside=Student.objects.filter(student_status='In',hostel='sharadha').count()
    else:
        inside=0
    total=total.count()
    context={'total':total,'inside':inside}
    return render(request, 'Home/sharadha.html',context)
@unauthenticated_user
def saraswathi(request):
    total=Student.objects.filter(hostel='saraswathi')
    if total:
        inside=Student.objects.filter(student_status='In',hostel='saraswathi').count()
    else:
        inside=0
    total=total.count()
    context={'total':total,'inside':inside}
    return render(request, 'Home/saraswathi.html',context)


#################################################   REGISTRATION PAGES   ##########################################

@unauthenticated_user
def studentregister(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.username = request.POST.get('username')
            form.email = request.POST.get('email')
            form.password1 = request.POST.get('password1')
            form.password2 = request.POST.get('password2')
            user = form.save()
            username = form.cleaned_data.get('username')

            group,create = Group.objects.get_or_create(name='student')

            user.groups.add(group)

            Student.objects.create(
                user=user,
                rollno= request.POST.get('username'),
                email = request.POST.get('email'),
                hostel=request.POST.get('hostel'),
                branch=request.POST.get('branch'),
                student_status='In'

            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('studentregister')

    context = {'form': form}
    return render(request, 'Home/Registration.html',context)
@allowed_users(allowed_roles=['HM'])
def AddCaretaker(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.username = request.POST.get('username')
            form.email = request.POST.get('email')
            form.password1 = request.POST.get('password1')
            form.password2 = request.POST.get('password2')
            user = form.save()
            username = form.cleaned_data.get('username')

            group,create = Group.objects.get_or_create(name='staff')

            user.groups.add(group)

            Staff.objects.create(
                user=user,
                name= form.username,
                email = form.email,
                designation='Caretaker',
                hostel=request.POST.get('hostel'),
            )

            messages.success(request, 'Account was created for ' + username)
            # user = request.user
            #              HM = Staff.objects.get(user=user)
            #              context = {'HM': HM}

            return redirect('AddCaretaker')
    user = request.user
    HM = Staff.objects.get(user=user)

    context = {'form': form,'HM':HM}
    return render(request, 'Home/AddCaretaker.html',context)

@allowed_users(allowed_roles=['HM'])
def AddHM(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.username = request.POST.get('username')
            form.email = request.POST.get('email')
            form.password1 = request.POST.get('password1')
            form.password2 = request.POST.get('password2')
            user = form.save()
            username = form.cleaned_data.get('username')

            group,create = Group.objects.get_or_create(name='HM')

            user.groups.add(group)

            Staff.objects.create(
                user=user,
                name= form.username,
                email = form.email,
                designation='HM',
            )

            messages.success(request, 'Account was created for ' + username)
            #user = request.user
            #HM = Staff.objects.get(user=user)
            #context = {'form':form,'HM': HM}

            return redirect('AddHM')
    user = request.user
    HM = Staff.objects.get(user=user)

    context = {'form': form,'HM': HM}
    return render(request, 'Home/AddHM.html',context)


#################################################   LOGIN PAGES   ##########################################


@unauthenticated_user
def studentlogin(request):
    if request.method == 'POST':
        username = request.POST.get('rollno')

        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.groups.exists():
                group = user.groups.all()[0].name
                if group == 'student':
                    login(request, user)
                    return redirect('studenthome')

        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request,'Home/Student Login.html',context)

@unauthenticated_user
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('name')

        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.groups.exists():
                group = user.groups.all()[0].name
                if group == 'HM':
                    login(request, user)
                    return redirect('HMhome')
                if group == 'staff':
                    login(request,user)
                    return redirect('caretakerhome')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'Home/Admin.html', context)



#################################################   STUDENT PAGES   ##########################################


@allowed_users(allowed_roles=['student'])
def studenthome(request):

    user=request.user
    student=Student.objects.get(user=user)
    # createappealFormset = inlineformset_factory(Student, Appeal,
    #                                             fields=('type', 'room_no', 'out_datetime', 'in_datetime', 'reason'),
    #                                              extra=1)
    #form = createappealFormset(queryset=Appeal.objects.none(),instance=student)
    form= createapealForm2()
    if request.method == 'POST':

        # form = createappealFormset(request.POST,instance=student)
        form=createapealForm2(request.POST)
        print(request.POST)
        # print(form.data)
            #print(request.POST['appeal_set-0-reason'])

        if form.is_valid():
            # print(form.data)
            # obj=form.save(commit=False)
            type=request.POST.get('type')
            room_no=request.POST.get('room_no')
            reason=request.POST.get('reason')
            out_date=request.POST.get('out_date')
            out_time=request.POST.get('out_time')
            in_date=request.POST.get('in_date')
            in_time=request.POST.get('in_time')
            timings=request.POST.get('timings_to_contact')
            out_datetime=datetime.strptime(out_date+' '+out_time,"%Y-%m-%d %H:%M:%S")
            in_datetime=datetime.strptime(in_date+' '+in_time,"%Y-%m-%d %H:%M:%S")
            print(out_datetime)
            print(in_datetime)
            outtime=out_datetime.astimezone(pytz.timezone("Asia/Kolkata")).date()
            intime=in_datetime.astimezone(pytz.timezone("Asia/Kolkata")).date()
            now=datetime.now().date()
            print(outtime)
            print(intime)
            print(now.day)
            if outtime < now:
                messages.warning(request,'Please enter out date&time correctly')
                return redirect('studenthome')
            if intime < outtime:
                messages.warning(request,'Please enter in date&time correctly')
                return redirect('studenthome')


            Appeal.objects.create(
                student=student,
                hostel=student.hostel,
                father_mobile_no=student.father_mobile_no,
                type=type,
                out_datetime=out_datetime,
                in_datetime=in_datetime,
                status='pending',
                room_no=room_no,
                reason=reason,
                branch=student.branch,
                year=student.year,
                timings=timings,
            )
            messages.success(request,'Request Placed')
            return redirect('studenthome')


        else:
            messages.warning(request, 'Request Not Placed Please fill Form correctly')
            return redirect('studenthome')
    context = {'student': student, 'form': form}
    return render(request, 'Home/studenthome.html', context)

@allowed_users(allowed_roles=['student'])
def studentprofile(request):
    student=Student.objects.get(user=request.user)  # getting student information
    context={'student': student}
    return render(request,'Home/studentprofile.html',context)

@allowed_users(allowed_roles=['student'])
def studentupdateprofile(request):
    student = Student.objects.get(user=request.user)  # getting student information

    form = studentprofileForm(instance=student)  # passing form

    if request.method == 'POST':
        form = studentprofileForm(request.POST, request.FILES, instance=student)
        # request.FILES used because we are passing media files
        if form.is_valid():
            form.save()
    context = {'student': student, 'form': form}
    return render(request, 'Home/studentupdateprofile.html', context)

@allowed_users(allowed_roles=['student'])
def studentpendingrequests(request):
    student = Student.objects.get(user=request.user)
    pending = student.appeal_set.filter(status='pending')
    paginator = Paginator(pending, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        pending = paginator.page(page)
    except PageNotAnInteger:
        pending = paginator.page(1)
    except EmptyPage:
        pending = paginator.page(paginator.num_pages)
    context = {'student': student , 'pending': pending }
    return render(request,'Home/studentpendingrequests.html',context)

@allowed_users(allowed_roles=['student'])
def studentapprovedrequests(request):
    student=Student.objects.get(user=request.user)
    approved= student.appeal_set.filter(status='approved')
    context={'student':student,'approved':approved}
    return render(request,'Home/studentapprovedrequests.html',context)

@allowed_users(allowed_roles=['student'])
def studentactiverequests(request):
    student = Student.objects.get(user=request.user)
    active = student.appeal_set.filter(status='used')
    context = {'student': student, 'active': active}
    return render(request, 'Home/studentactiverequests.html', context)

@allowed_users(allowed_roles=['student'])
def studentpastrequests(request):
    student = Student.objects.get(user=request.user)
    expired = student.appeal_set.filter(status='expired')
    myFilter = studentFilter(request.GET, queryset=expired)
    expired = myFilter.qs
    paginator = Paginator(expired, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        expired = paginator.page(page)
    except PageNotAnInteger:
        expired = paginator.page(1)
    except EmptyPage:
        expired = paginator.page(paginator.num_pages)
    context = {'student': student, 'expired': expired,'myFilter':myFilter}
    return render(request, 'Home/studentpastrequests.html', context)

@allowed_users(allowed_roles=['student'])
def studentrejectedrequests(request):
    student = Student.objects.get(user=request.user)
    rejected = student.appeal_set.filter(status='rejected')
    paginator = Paginator(rejected, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        rejected= paginator.page(page)
    except PageNotAnInteger:
        rejected= paginator.page(1)
    except EmptyPage:
        rejected = paginator.page(paginator.num_pages)
    context = {'student': student, 'rejected': rejected}
    return render(request, 'Home/studentrejectedrequests.html', context)

@allowed_users(allowed_roles=['student'])
def deleterequest(request,pk):
    student=Student.objects.get(user=request.user)
    appeal = Appeal.objects.get(id=pk)
    if request.method == "POST":
        if appeal.qr_code :
            path = str(settings.MEDIA_ROOT) + '/' + str(appeal.qr_code)
            os.remove(path)
            appeal.qr_code = None
        appeal.delete()
        return redirect('/')

    context = {'item': appeal,'student':student}
    return render(request,'Home/deleterequest.html',context)

@allowed_users(allowed_roles=['student'])
def studentinstructions(request):
    return render(request,'Home/studentinstructions.html')

#################################################   HOSTEL MANAGER PAGES   ##########################################

@allowed_users(allowed_roles=['HM'])
def HMhome(request):
    user=request.user
    HM=Staff.objects.get(user=user)
    requests=Appeal.objects.filter(status='pending')
    myFilter = CThomeFilter(request.GET, queryset=requests)
    requests = myFilter.qs
    paginator = Paginator(requests, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)
    context={'HM':HM,'requests':requests,'myFilter':myFilter}
    return render(request, 'Home/HMhome.html',context)
@allowed_users(allowed_roles=['HM'])
def HMprofile(request):
    HM=Staff.objects.get(user=request.user)
    context={'HM':HM }
    return render(request, 'Home/HMprofile.html', context)
@allowed_users(allowed_roles=['HM'])
def HMupdateprofile(request):
    HM=Staff.objects.get(user=request.user)
    form = staffprofileForm(instance=HM)  # passing form

    if request.method == 'POST':
        form = staffprofileForm(request.POST, request.FILES, instance=HM)
        # request.FILES used because we are passing media files
        if form.is_valid():
            form.save()
    context={'HM':HM ,'form': form}
    return render(request, 'Home/HMupdateprofile.html', context)
@allowed_users(allowed_roles=['HM'])
def hmapprovedrequests(request):
    requests=Appeal.objects.filter(status='approved')
    HM = Staff.objects.get(user=request.user)
    myFilter = CThomeFilter(request.GET, queryset=requests)
    requests = myFilter.qs
    paginator = Paginator(requests, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)
    context={'HM':HM,'requests':requests,'myFilter':myFilter}
    return render(request,'Home/hmapprovedrequests.html',context)

@allowed_users(allowed_roles=['HM'])
def hmknowstudentstatus(request):
    HM = Staff.objects.get(user=request.user)
    students=Student.objects.all()
    myFilter = knowstudentstatusFilter(request.GET, queryset=students)
    students = myFilter.qs
    paginator = Paginator(students, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    context={'HM':HM,'students': students,'myFilter':myFilter}
    return render(request,'Home/hmstudentstatus.html',context)

@allowed_users(allowed_roles=['HM'])
def HMinstructions(request):
    return render(request,'Home/HMinstructions.html')

#################################################   CARETAKER PAGES   ##########################################

@allowed_users(allowed_roles=['staff'])
def caretakerhome(request):
    user=request.user
    staff=Staff.objects.get(user=user)
    requests= Appeal.objects.filter(status='pending',hostel=staff.hostel)
    myFilter = CThomeFilter(request.GET, queryset=requests)
    requests=myFilter.qs
    paginator=Paginator(requests,10)
    page_request_var="page"
    page=request.GET.get(page_request_var)
    try:
        requests=paginator.page(page)
    except PageNotAnInteger:
        requests=paginator.page(1)
    except EmptyPage:
        requests=paginator.page(paginator.num_pages)

    context={'staff': staff,'requests':requests,'myFilter':myFilter}
    return render(request, 'Home/caretakerhome.html',context)


@allowed_users(allowed_roles=['staff','HM'])
def viewrequest(request,pk):
    appeal=Appeal.objects.get(id=pk)
    student=Student.objects.get(rollno=appeal.student.rollno)
    caretaker=Staff.objects.get(user=request.user)
    crname=caretaker.name

    if request.method == 'POST':
        if request.POST.get('cancel'):
            appeal.status = 'rejected'
            appeal.staff = crname
            appeal.save()
        else:
            appeal.status='approved'
            appeal.staff= crname
            qrcode_img = qrcode.make('http://'+str(request.META['HTTP_HOST'])+'/security_check/'+str(appeal.id))
            fname=str(appeal.id)+'.png'
            qrcode_img.save(settings.MEDIA_ROOT+'/qr_codes/'+fname)
            appeal.qr_code='qr_codes/'+fname
            appeal.save()
        return redirect('/')
    context={'student':student,'staff':caretaker,'appeal':appeal}
    return render(request,'Home/viewrequest.html',context)


@allowed_users(allowed_roles=['staff'])
def caretakerprofile(request):
    staff=Staff.objects.get(user=request.user)
    context={'staff': staff}
    return render(request,'Home/caretakerprofile.html',context)
@allowed_users(allowed_roles=['staff'])
def caretakerupdateprofile(request):
    staff=Staff.objects.get(user=request.user)
    form = staffprofileForm(instance=staff)  # passing form

    if request.method == 'POST':
        form = staffprofileForm(request.POST, request.FILES, instance=staff)
        # request.FILES used because we are passing media files
        if form.is_valid():
            form.save()

    context={'staff': staff,'form': form}
    return render(request,'Home/caretakerupdateprofile.html',context)
@allowed_users(allowed_roles=['staff'])
def crapprovedrequests(request):
    staff=Staff.objects.get(user=request.user)
    requests = Appeal.objects.filter(status='approved', hostel=staff.hostel)
    myFilter = CThomeFilter(request.GET, queryset=requests)
    requests = myFilter.qs
    paginator = Paginator(requests, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)
    context={'staff':staff,'requests':requests,'myFilter':myFilter}
    return render(request,'Home/crapprovedrequests.html',context)

@allowed_users(allowed_roles=['staff'])
def crondayout(request):
    staff=Staff.objects.get(user=request.user)
    requests= Appeal.objects.filter(type='day-out',status='used',hostel=staff.hostel)
    paginator = Paginator(requests, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)
    context={'staff':staff,'requests':requests}
    return render(request,'Home/crondayout.html',context)

@allowed_users(allowed_roles=['staff'])
def crlefttoday(request):
    staff = Staff.objects.get(user=request.user)
    requests=Appeal.objects.filter(type='home-out',hostel=staff.hostel,status='used')
    myFilter = lefttodayFilter(request.GET, queryset=requests)
    requests = myFilter.qs
    paginator = Paginator(requests, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)
    context = {'staff': staff, 'requests': requests,'myFilter':myFilter}
    return render(request, 'Home/crlefttoday.html', context)

@allowed_users(allowed_roles=['staff'])
def crarrivedtoday(request):
    staff = Staff.objects.get(user=request.user)
    requests=Appeal.objects.filter(type='home-out',hostel=staff.hostel,status='expired')
    myFilter = arrivedtodayFilter(request.GET, queryset=requests)
    requests = myFilter.qs
    paginator = Paginator(requests, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)
    context = {'staff': staff, 'requests': requests,'myFilter':myFilter}
    return render(request, 'Home/crarrivedtoday.html', context)

@allowed_users(allowed_roles=['staff'])
def crknowstudentstatus(request):
    staff = Staff.objects.get(user=request.user)
    students=Student.objects.filter(hostel=staff.hostel)
    myFilter = knowstudentstatusFilter(request.GET, queryset=students)
    students = myFilter.qs
    paginator = Paginator(students, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    context = {'staff': staff, 'students': students,'myFilter':myFilter}
    return render(request, 'Home/crstudentstatus.html', context)

@allowed_users(allowed_roles=['staff'])
def crinstructions(request):
    return render(request,'Home/crinstructions.html')

#################################################   LOGOUT   ##########################################
def logoutUser(request):
    if request.user.groups.all()[0].name == 'security':
        logout(request)
        return redirect('securitylogin')
    else :
        logout(request)
        return redirect('Home')


#################################################  SECURITY  ##########################################

@unauthenticated_user
def securitylogin(request):
    if request.method == 'POST':
        username = request.POST.get('name')

        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.groups.exists():
                group = user.groups.all()[0].name
                if group == 'security':
                    login(request, user)
                    return redirect('securityhome')

        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request,'Home/securitylogin.html',context)

@allowed_users(allowed_roles=['security'])
def securityhome(request):
    name = request.user.username
    context={'name':name}
    return render(request,'Home/securityhome.html',context)

@allowed_users(allowed_roles=['security'])
def securitycheck(request,pk):
    try:
        appeal=Appeal.objects.get(id=pk)
        if appeal.status == 'expired':
            messages.warning(request, 'Request expired')
            return redirect('securityhome')
        out=appeal.out_datetime.astimezone(pytz.timezone("Asia/Kolkata"))
        out=out.date()
        now=datetime.now().date()
        #print(out,now)
        student = Student.objects.get(rollno=appeal.student)
        if student.student_status == 'In':
            if now != out :
                message ='You can go out only on '+str(appeal.out_datetime.date())
                messages.warning(request,message)
                return redirect('securityhome')

        if request.method == 'POST':
            print(student.student_status)
            if student.student_status == 'In':
                student.student_status = 'Out'
                student.save()
                appeal.status = 'used'
                appeal.actual_out = datetime.now()
                appeal.save()
                return redirect('securityhome')
            if student.student_status == 'Out':
                student.student_status = 'In'
                student.save()
                appeal.status ='expired'
                path = str(settings.MEDIA_ROOT) + '/' + str(appeal.qr_code)
                os.remove(path)
                appeal.qr_code = None
                appeal.actual_in = datetime.now()
                appeal.save()

                return redirect('securityhome')
    except :
        messages.warning(request,'This request doesnot exists')
        return redirect('securityhome')


    context={'student':student,'appeal':appeal}
    return render(request,'Home/securitycheck.html',context)


######################################## CONTACT US ########################################

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # send email code goes here
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']

            message = "{0} has sent you a new message:\n\n{1} \n\nfrom {2}".format(sender_name, form.cleaned_data['message'],sender_email)
            send_mail('JNTUHCEJ HOSTEL PORTAL', message, sender_email, ['vodnalasricharan@gmail.com','varunteja200025@gmail.com'])
            messages.success(request,'Your Query has been sent')
            return redirect('contactus')
    else:
        form = ContactForm()

    return render(request, 'Home/contact-us.html', {'form': form})