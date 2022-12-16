import os
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string

from .models import PassawordResetToken


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
            if PassawordResetToken.objects.filter(user=user).exists():
                PassawordResetToken.objects.get(user=user).delete()
            token = get_random_string(length=64)
            resert_token = PassawordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timedelta(hours=2)
            )

            subject = 'Password reset request'
            email_template_name = 'accounts/pages/password_message.txt'
            parametrs = {
                'email': user.email,
                'domain': os.environ.get('DOMAIN_NAME'),
                'site_name': 'Balance Control',
                'user': user,
                'token': resert_token,
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


def resetPasswordConfirm(request):
    template_name = 'accounts/pages/resetpasswordconfirm.html'
    token = request.GET.get('token')
    try:
        resert_token = PassawordResetToken.objects.get(token=token)
    except PassawordResetToken.DoesNotExist:
        return render(request, 'accounts/pages/tokeninvalid.html')

    if resert_token.expires_at < timezone.now():
        return render(request, 'accounts/pages/tokenexpired.html')

    if request.method == 'POST':
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
            user = resert_token.user
            user.set_password(password)
            user.save()
            resert_token.delete()
            messages.success(request, 'Password reset successfully')
            return redirect('accounts:resetPasswordComplete')
        else:
            messages.info(request, 'Passwords not matching...')
            return render(request, template_name)
    else:
        return render(request, template_name)


def resetPasswordInvalid(request):
    template_name = 'accounts/pages/resetpasswordinvalid.html'
    if request.method == 'GET':
        return render(request, template_name)


def resetPasswordExpired(request):
    template_name = 'accounts/pages/resetpasswordexpired.html'
    if request.method == 'GET':
        return render(request, template_name)


def resetPasswordComplete(request):
    template_name = 'accounts/pages/resetpasswordcomplete.html'
    if request.method == 'GET':
        return render(request, template_name)
