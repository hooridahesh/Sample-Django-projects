from django import forms
from .models import ContactUs


class contactUsForms(forms.Form):
    full_name = forms.CharField(
        label='نام و نام خانوادگی',
        max_length=50,
        error_messages={
            'required': 'لطفا نام و نام خانوادگی خود را وارد کنید',
            'max_length': 'مقدار کاراکتر حداکثر 50 می باشد'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی'
        })
    )
    email = forms.EmailField(
        label='ایمیل',
        error_messages={
            'required': 'لطفا ایمیل خود را وارد کنید',
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        })
    )
    subject = forms.CharField(
        label='عنوان',
        error_messages={
            'required': 'لطفا عنوان خود را وارد کنید',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان'
        })
    )
    message = forms.CharField(
        label='متن پیام',
        required=False,
        widget=forms.Textarea(attrs={
            'id': 'message',
            'class': 'form-control',
            'placeholder': 'متن پیام'
        })
    )


class contactUsFormModel(forms.ModelForm):  # این فرم دقیقا به مدل وصل میشه
    class Meta:
        model = ContactUs  # برای این مدل داریم فرم رو میسازیم
        fields = ['full_name', 'title', 'message', 'email']
        # این فرم برای این فیلدها داره تولید میشه و دقیقا هم نام با مدل باید باشه اسم هاشون
        # fields = '__all__'  # این ینی همه فیلدها
        # exclude = ['created_date']  # این یعنی همه فیلدها به جز این created_date
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'title': 'عنوان',
            'message': 'متن پیام',
            'email': 'ایمیل'
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'متن پیام',
                'id': 'message',
            })
        }
        error_messages = {
            'full_name': {
                'required': 'لطفا نام و نام خانوادگی خود را وارد کنید'
            },
            'title': {
                'required': 'لطفا عنوان را وارد کنید'
            },
            'email': {
                'required': 'لطفا ایمیل خود را وارد کنید'
            }
        }


class profileForms(forms.Form):
    upload_image = forms.FileField()
