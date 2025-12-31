from django.urls import path
from .views import register_page,verify_email_confirm
from django.contrib.auth.views import LogoutView


app_name = 'user'

urlpatterns = [
    path('register/',register_page,name='register_page'),
    path('email-confirm/<uidb64>/<token>/',verify_email_confirm,name='verify-email-confirm'),
    path('logout/',LogoutView.as_view(),name='logout')
]
