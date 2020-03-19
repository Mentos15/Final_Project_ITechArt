from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import RegForm, LoginForm, CategoryConfirence, ChangePasswordForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import ConfirenceList, Records
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.mail import send_mail
import datetime
import hashlib


def index(request):
    qwery = request.GET.getlist('category')
    forms2 = CategoryConfirence(request.GET)
    if not qwery:
        tupl = list(reversed(ConfirenceList.objects.all()))
    else:
        tupl = list(reversed(ConfirenceList.objects.filter(category__in=qwery)))
    paginator = Paginator(tupl, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    # if request.is_ajax():
    #  return render(request, 'Conferences/_list_ajax.html', {'forms2': forms2, 'page_obj': page_obj})
    return render_to_response('Conferences.html', {'forms2': forms2, 'page_obj': page_obj})
    # return render(request, 'Conferences.html', {'forms2': forms2, 'page_obj': page_obj})


def print_errors(request, errors):
    for field in errors:
        for error in field.errors:
            messages.error(request, error)


def More_info(request, id):
    tupl = get_object_or_404(ConfirenceList, id=id)
    more_info = {'more_info': tupl}
    return render(request, 'More_details.html', more_info)


def RegisterUser(request):
    if request.method == 'POST':
        forms = RegForm(request.POST)
        if forms.is_valid():
            forms = forms.cleaned_data
            user = User.objects.create_user(forms['login'], forms['email'], forms['password'])
            hash = hashlib.sha1(user.username.encode('utf-8')).hexdigest()
            send_mail('Активация аккаунта', f'Нажмите: http://127.0.0.1:8000/catalog/activate/{hash}',
                      'vitalyya1510@gmail.com', [user.email], False)
            user.is_active = False
            user.save()
            return redirect('catalog:Confirences')
        else:
            for error in forms.errors.items():
                messages.error(request, error[1])

    forms = RegForm()

    context = {'forms': forms}
    return render(request, 'register.html', context)


def ChangePassword(request):
    user = request.user
    if request.method == 'POST':
        forms = ChangePasswordForm(request.POST)
        if forms.is_valid():
            forms = forms.cleaned_data
            if not (check_password(forms['last_password'], user.password)):
                messages.error(request, "Неверный старый пароль")
            else:
                user.set_password(forms['new_password'])
                user.save()
                login(request, user)
                messages.info(request, "Пароль успешно именен")
            return redirect('catalog:change_password')
        else:
            for error in forms.errors.items():
                messages.error(request, error[1])
    forms = ChangePasswordForm()
    return render(request, 'ChangePassword.html', {'forms': forms})


def Logout(request):
    logout(request)
    return redirect('catalog:Confirences')


def LoginToAccount(request):
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            forms = forms.cleaned_data
            try:
                u = User.objects.get(username=forms['login'])
                user = authenticate(request, username=forms['login'], password=forms['password'])
            except:
                messages.error(request, "Неверно введен логин или пароль")
                forms = LoginForm()
                return render(request, 'Login_to_account.html', {'login_forms': forms})
            if user is not None:
                if u.is_active:
                    login(request, user)
                    return redirect('catalog:Confirences')
                else:
                    messages.error(request, "Аккаунт не активирован")
            else:
                messages.error(request, "Неверно введен логин или пароль")
        else:
            for error in forms.errors.items():
                messages.error(request, error[1])
    forms = LoginForm()
    return render(request, 'Login_to_account.html', {'login_forms': forms})


def RegisterOnConfirence(request, id):
    users = request.user
    tupl = get_object_or_404(ConfirenceList, pk=id)
    if request.user.is_authenticated:
        regconf = Records(conference=tupl)
        name_conf = Records.objects.filter(conference=tupl)
        for i in name_conf:
            if i.user.get() == users:
                messages.error(request, "Вы уже зарегестрированы на конференцию")
                return redirect('catalog:More_info', id=id)
        regconf.save()
        regconf.user.add(request.user)

        return redirect('catalog:More_info', id=id)
    return redirect('catalog:login')


def activate(request, hashuser):
    if not request.user.is_authenticated:
        users = User.objects.filter(is_active=False)
        for user in users:
            if hashuser == hashlib.sha1(user.username.encode('utf-8')).hexdigest():
                user.last_login = datetime.datetime.now()
                user.is_active = True
                user.save()
                messages.info(request, 'Аккаунт активирован')
                return render(request, 'activate.html')
        else:
            messages.error(request, 'Ошибка')
            return render(request, 'activate.html')
    else:
        messages.error(request, 'Вы уже авторизованы')
        return render(request, 'activate.html')
