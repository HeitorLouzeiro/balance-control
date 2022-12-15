import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

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
    except:  # noqa
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


def resetPassword(request):
    template_name = 'accounts/pages/resetpassword.html'
    if request.method == 'POST':
        email = request.POST.get('email')
        if email == '':
            messages.info(request, 'Please fill the field')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            subject = 'Password reset request'
            email_template_name = 'accounts/pages/password_message.txt'
            parametrs = {
                'email': user.email,
                'domain': '127.0.0.1:8000',
                'site_name': 'Balance Control',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }
            email = render_to_string(email_template_name, parametrs)
            try:
                send_mail(subject, email, '', [
                          user.email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Email sent successfully')
            return redirect('accounts:resetPasswordSent')
        else:
            messages.info(request, 'Email not found')
            return render(request, template_name)
    else:
        return render(request, template_name)


def resetPasswordSent(request):
    template_name = 'accounts/pages/resetpasswordsent.html'
    if request.method == 'GET':
        return render(request, template_name)


def resetPasswordConfirm(request, uidb64, token):
    template_name = 'accounts/pages/resetpasswordconfirm.html'
    if request.method == 'GET':
        return render(request, template_name)

    if request.method == 'POST':
        uid = urlsafe_base64_decode(uidb64).decode()
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == '' or password2 == '':
            messages.info(request, 'Please fill all the fields')
            return render(request, template_name)
        if len(password) < 6:
            messages.error(
                request, 'Password must be greater than 6 characters!')
            return render(request, template_name)
        if password == password2:
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('accounts:resetPasswordComplete')
        else:
            messages.info(request, 'Passwords not matching...')
            return render(request, template_name)


def resetPasswordComplete(request):
    template_name = 'accounts/pages/resetpasswordcomplete.html'
    if request.method == 'GET':
        return render(request, template_name)
