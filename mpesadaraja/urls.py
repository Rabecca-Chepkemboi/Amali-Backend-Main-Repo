from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('accesstoken/', views.get_access_token, name='get_access_token'),
    path('stkpush/', views.DarajaApiView.as_view(), name='initiate_stk_push'),
    path('callback/', views.process_stk_callback),
    path('webhook/', views.mpesawebhook, name='mpesa_webhook'),

]
