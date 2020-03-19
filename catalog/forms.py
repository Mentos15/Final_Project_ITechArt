from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegForm(forms.Form):
    email = forms.EmailField(required=True)
    login = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=5)
    repeat_password = forms.CharField(widget=forms.PasswordInput(), min_length=5)

    def clean_email(self):
        email = self.data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Mail уже занят")
        else:
            return email

    def clean_login(self):
        login = self.data['login']
        if User.objects.filter(username = login).exists():
            raise ValidationError("Имя пользователя уже занято")
        else:
            return login
    def clean_repeat_password(self):
        password = self.data['password']
        ret_password = self.data['repeat_password']

        if password != ret_password:
            raise ValidationError("Пароли не совпадают")
        else:
            return ret_password

class ChangePasswordForm(forms.Form):
    last_password = forms.CharField(widget=forms.PasswordInput(), min_length=5)
    new_password = forms.CharField(widget=forms.PasswordInput(), min_length=5)
    rep_password = forms.CharField(widget=forms.PasswordInput(), min_length=5)

    def clean_rep_new_password(self):
        new_password = self.data['new_password']
        rep_password = self.data['rep_new_password']
        if new_password != rep_password:
            raise ValidationError("Пароли не совпадают")
        else:
            return rep_password




class LoginForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=5)



class CategoryConfirence(forms.Form):
    IT = 'IT'
    Since = 'Since'
    Football = 'Football'
    Ecology = 'Ecology'
    conf_list = [
        (IT, 'IT'),
        (Since, 'Since'),
        (Football, 'Football'),
        (Ecology, 'Ecology'),
    ]
    category = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=conf_list,
    )




