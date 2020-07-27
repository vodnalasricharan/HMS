from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .decorators import *

# Create your views here.

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

    return render(request,'Home/Home.html')
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
@allowed_users(allowed_roles=['student'])
def studenthome(request):
    createappealFormset = inlineformset_factory(Student, Appeal,fields=('type','room_no','out_datetime','in_datetime', 'reason'),extra=1)
    user=request.user
    student=Student.objects.get(user=user)
    form = createappealFormset(queryset=Appeal.objects.none(),instance=student)
    #form= createapealForm2()
    if request.method == 'POST':

        form = createappealFormset(request.POST,instance=student)
        if request.POST['appeal_set-0-reason'] :
            #print(request.POST['appeal_set-0-reason'])

            if form.is_valid():
                form.save()
                messages.success(request,'Request Placed')
                return redirect('studenthome')

            messages.warning(request, 'Request Not Placed Please fill Form correctly')
            return redirect('studenthome')
        else:
            messages.warning(request, 'Request Not Placed Please fill Form correctly')
            return redirect('studenthome')
    context = {'student': student, 'form': form}
    return render(request, 'Home/studenthome.html', context)



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
@allowed_users(allowed_roles=['HM'])
def HMhome(request):
    user=request.user
    HM=Staff.objects.get(user=user)
    context={'HM':HM}
    return render(request, 'Home/HMhome.html',context)



@allowed_users(allowed_roles=['staff'])
def caretakerhome(request):
    user=request.user
    staff=Staff.objects.get(user=user)
    context={'staff': staff}
    return render(request, 'Home/caretakerhome.html',context)


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
                branch=request.POST.get('branch')

            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('studentlogin')

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
            user = request.user
            HM = Staff.objects.get(user=user)
            context = {'HM': HM}

            return redirect('AddCaretaker',context)
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
            user = request.user
            HM = Staff.objects.get(user=user)
            context = {'HM': HM}

            return redirect('AddHM',context)
    user = request.user
    HM = Staff.objects.get(user=user)

    context = {'form': form,'HM': HM}
    return render(request, 'Home/AddHM.html',context)
@allowed_users(allowed_roles=['student'])
def studentprofile(request,pk):
    student=Student.objects.get(rollno=pk)  # getting student information
    context={'student': student}
    return render(request,'Home/studentprofile.html',context)

@allowed_users(allowed_roles=['student'])
def studentupdateprofile(request,pk):
    student = Student.objects.get(rollno=pk)  # getting student information

    form = studentprofileForm(instance=student)  # passing form

    if request.method == 'POST':
        form = studentprofileForm(request.POST, request.FILES, instance=student)
        # request.FILES used because we are passing media files
        if form.is_valid():
            form.save()
    context = {'student': student, 'form': form}
    return render(request, 'Home/studentupdateprofile.html', context)

@allowed_users(allowed_roles=['student'])
def studentpendingrequests(request,pk):
    student = Student.objects.get(rollno=pk)
    pending = student.appeal_set.filter(status='pending')
    context = {'student': student , 'pending': pending }
    return render(request,'Home/studentpendingrequests.html',context)
@allowed_users(allowed_roles=['student'])
def deleterequest(request,pk):
    student=Student.objects.get(user=request.user)
    appeal = Appeal.objects.get(id=pk)
    if request.method == "POST":
        appeal.delete()
        return redirect('/')

    context = {'item': appeal,'student':student}
    return render(request,'Home/deleterequest.html',context)




@allowed_users(allowed_roles=['staff'])
def caretakerprofile(request,pk):
    staff=Staff.objects.get(name=pk)
    context={'staff': staff}
    return render(request,'Home/caretakerprofile.html',context)
@allowed_users(allowed_roles=['staff'])
def caretakerupdateprofile(request,pk):
    staff=Staff.objects.get(name=pk)
    form = staffprofileForm(instance=staff)  # passing form

    if request.method == 'POST':
        form = staffprofileForm(request.POST, request.FILES, instance=staff)
        # request.FILES used because we are passing media files
        if form.is_valid():
            form.save()

    context={'staff': staff,'form': form}
    return render(request,'Home/caretakerupdateprofile.html',context)


@allowed_users(allowed_roles=['HM'])
def HMprofile(request,pk):
    HM=Staff.objects.get(name=pk)
    context={'HM':HM }
    return render(request, 'Home/HMprofile.html', context)
@allowed_users(allowed_roles=['HM'])
def HMupdateprofile(request,pk):
    HM=Staff.objects.get(name=pk)
    form = staffprofileForm(instance=HM)  # passing form

    if request.method == 'POST':
        form = staffprofileForm(request.POST, request.FILES, instance=HM)
        # request.FILES used because we are passing media files
        if form.is_valid():
            form.save()
    context={'HM':HM ,'form': form}
    return render(request, 'Home/HMupdateprofile.html', context)


@unauthenticated_user
def godavari(request):
    return render(request, 'Home/godavari.html')
@unauthenticated_user
def krishna(request):
    return render(request, 'Home/krishna.html')
@unauthenticated_user
def sharadha(request):
    return render(request, 'Home/sharadha.html')
@unauthenticated_user
def saraswathi(request):
    return render(request, 'Home/saraswathi.html')

def logoutUser(request):
	logout(request)
	return redirect('Home')