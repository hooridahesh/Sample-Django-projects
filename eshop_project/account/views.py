from django.shortcuts import render, redirect
from django.views import View
from .forms import registerForm, loginForm, forgetPasswordForm, resetPasswordForm
from .models import user
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.http import Http404
from django.contrib.auth import login, logout
from utils.email_service import send_email


class registerView(View):
    def get(self, request):
        register_form = registerForm()
        return render(request, 'account/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = registerForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            check_user: bool = user.objects.filter(email__iexact=user_email).exists()
            # برای اینکه ببینه این ایمیل ایا توی دیتابیس هست یا نه و اگر تکراری بود خطا بده بهش
            if check_user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری می باشد')
            else:
                new_user = user(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    username=user_email
                )
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعال سازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/activate_account.html')
                return redirect(reverse('login_page'))

        return render(request, 'account/register.html', {'register_form': register_form})


class loginView(View):
    def get(self, request):
        login_form = loginForm()
        return render(request, 'account/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = loginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            User: user = user.objects.filter(email__iexact=user_email).first()
            if User is not None:
                if User.is_active == False:  # ایا کاربر حساب کاربری رو فعال کرده یا نه
                    login_form.add_error('email', 'حساب کاربری فعال نشده است')
                else:
                    is_password = User.check_password(user_pass)
                    """
                    چون پسورد به صورت هش شده است در دیتابیس به این شکل چکش می کنیم
                    و خروجی به صورت bool است
                    """
                    if is_password:
                        login(request, User)
                        """
                        برای login باید کوکی ست کنیم ینی وقتی که طرف login میکنه
                        براش یه sessionid درست میشه که اطلاعات کاربر رو به طور موقت
                        داخل خودش ذخیره میکنه و برای این کار اومدیم از login رفتیم
                        که خودش اتوماتیک میاد login میکنه
                        """
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('email', 'نام کاربری یا کلمه عبور اشتباه است')

            else:
                login_form.add_error('email', 'نام کاربری یا کلمه عبور اشتباه است')
                """
                این دوتا خط باید ارورشون مثل هم نوشته بشه که کسی نتونه بفهمه که مشکل از
                کلمه عبور است یا ایمیل چون اگر پیغام مشخص بدیم ممکنه ایمیل رو وارد کنه
                و بعد بفهمه مشکل از پسورده و روش کار کنه و اون هم پیدا کنه
                منظورم هکر و اینجور چیزاس
                برای داشتن امنیت باید اینطوری باشه
                """

        return render(request, 'account/login.html', {'login_form': login_form})


class activateAccountView(View):
    def get(self, request, email_active_code):
        User: user = user.objects.filter(email_active_code__iexact=email_active_code).first()
        if User is not None:
            if User.is_active == False:
                User.is_active = True
                User.email_active_code = get_random_string(72)
                User.save()
                return redirect(reverse('login_page'))
            else:
                return redirect(reverse('home_page'))

        raise Http404


class forgetPasswordView(View):
    def get(self, request):
        forget_password = forgetPasswordForm()
        return render(request, 'account/forget_password.html', {'forget_password': forget_password})

    def post(self, request):
        forget_password = forgetPasswordForm(request.POST)
        if forget_password.is_valid():
            user_email = forget_password.cleaned_data.get('email')
            User: user = user.objects.filter(email__iexact=user_email).first()
            if User is not None:
                send_email('بازیابی کلمه عبور', User.email, {'user': User}, 'emails/forgot_password.html')
                return redirect(reverse('home_page'))
        return render(request, 'account/forget_password.html', {'forget_password': forget_password})


class resetPasswordView(View):
    def get(self, request, active_code):
        User: user = user.objects.filter(email_active_code__iexact=active_code)
        if User is None:
            return redirect(reverse('login_page'))

        reset_password = resetPasswordForm()
        return render(request, 'account/reset_password.html', {'reset_password': reset_password})

    def post(self, request, active_code):
        reset_password = resetPasswordForm(request.POST)
        if reset_password.is_valid():
            User: user = user.objects.filter(email_active_code__iexact=active_code).first()
            if User is None:
                return redirect(reverse('login_page'))
            new_pass = reset_password.cleaned_data.get('password')
            User.set_password(new_pass)
            User.email_active_code = get_random_string(72)
            User.is_active = True
            User.save()
            return redirect(reverse('login_page'))

        return render(request, 'account/reset_password.html', {'reset_password': reset_password})


class logoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))
