from django.urls import path
from . import views

urlpatterns = [
    # path('', views.contact_us, name='contact-us-page'),
    path('', views.contactUsView.as_view(), name='contact-us-page'),
    # اینجا با as_view کلاس رو به صورت ویو در نظر میگیره
    path('creat-profile/', views.createProfileView.as_view(), name='creat-profile'),
    path('images-list/', views.imagesView.as_view(), name='images-list')

]
