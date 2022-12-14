from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect, render


# Create your views here.
def loginUser(request):
    template_name = 'accounts/pages/login.html'
    if request.method == 'GET':
        return render(request, template_name)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('balancecontrol:home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request, template_name)


def register(request):
    template_name = 'accounts/pages/register.html'

    if request.method != 'POST':
        return render(request, template_name)

    fistname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    if fistname == '' or lastname == '' or username == '' or email == '' \
            or password == '' or password2 == '':
        messages.info(request, 'Please fill all the fields')
        return render(request, template_name)
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail invalid!')
        return render(request, template_name)

    if len(password) < 6:
        messages.error(
            request, 'Password must be greater than 6 characters!')
        return render(request, template_name)
    if password == password2:
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return render(request, template_name)
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return render(request, template_name)
        else:
            user = User.objects.create_user(
                first_name=fistname, last_name=lastname, username=username,
                email=email, password=password)
            user.save()
            messages.success(request, 'user created successfully')
            return redirect('accounts:loginUser')
    else:
        messages.info(request, 'Passwords not matching...')
        return render(request, template_name)


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
    return redirect('accounts:loginUser')
