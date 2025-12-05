from django import forms
from django.core.exceptions import ValidationError


class registerForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput()

    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput()
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class loginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput()

    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput()
    )


class forgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput()
    )


class resetPasswordForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput()
    )
