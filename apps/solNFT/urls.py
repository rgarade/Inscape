from rest_framework import routers
from django.urls import path
from django.conf.urls import url 
from apps.solNFT import views 

urlpatterns = [
    url(r'mint_token', views.mint_token, name = "mint_token")
]
