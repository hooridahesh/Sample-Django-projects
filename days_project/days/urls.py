from django.urls import path
from . import views

urlpatterns = [
    path("", views.days_list, name="day_list"),
    path('<int:day>', views.check_int),
    path('<str:day>', views.check_str, name='day_unic'),
]
