from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .forms import contactUsForms, contactUsFormModel, profileForms
from .models import ContactUs, profilemodel

# Create your views here.

# def contact_us(request):
#         if request.method == 'POST':
#             # contact_us_forms = contactUsForms(request.POST)
#             contact_forms = contactUsFormModel(request.POST)
#             if contact_forms.is_valid():
#                 # print(contact_us_forms.cleaned_data)
#                 # contact = ContactUs(
#                 #     title=contact_us_forms.cleaned_data.get('subject'),
#                 #     email=contact_us_forms.cleaned_data.get('email'),
#                 #     full_name=contact_us_forms.cleaned_data.get('full_name'),
#                 #     message=contact_us_forms.cleaned_data.get('message')
#                 # )
#                 # contact.save()
#                 contact_forms.save()
#                 return redirect('home_page')
#         else:
#             # contact_us_forms = contactUsForms()
#             contact_forms = contactUsFormModel()
#         return render(request, 'contact_us/contact_us_form.html', {'contact_forms': contact_forms})

# ---------------------------------------------------------------------------#

# class contactUsView(View):  # این کلاس بیس ویو است
#     def get(self, request):
#         contact_forms = contactUsFormModel()
#         return render(request, 'contact_us/contact_us_form.html', {'contact_forms': contact_forms})
#
#     def post(self, request):
#         contact_forms = contactUsFormModel(request.POST)
#         if contact_forms.is_valid():
#             contact_forms.save()
#             return redirect('home_page')
#         return render(request, 'contact_us/contact_us_form.html', {'contact_forms': contact_forms})

# --------------------------------------------------------------------------------#

"""
می تونیم از FormView استفاده کنیم به جای اینکه مثل بالا پیش بریم
چون دیگه نیاز نیست get , post توی حالت پایین داشته باشیم
"""


class contactUsView(FormView):
    template_name = 'contact_us/contact_us_form.html'
    form_class = contactUsFormModel
    success_url = 'contact-us'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class createProfileView(View):
    def get(self, request):
        form = profileForms()
        return render(request, 'contact_us/create_profile.html', {'form': form})

    def post(self, request):
        submittedFile = profileForms(request.POST, request.FILES)
        if submittedFile.is_valid():
            profile = profilemodel(image=request.FILES['upload_image'])
            profile.save()
            return redirect('creat-profile')
        return render(request, 'contact_us/create_profile.html', {'form': submittedFile})


class imagesView(ListView):
    template_name = 'contact_us/file_list.html'
    model = profilemodel
    context_object_name = 'profiles'
