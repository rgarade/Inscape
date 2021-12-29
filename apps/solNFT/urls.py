
from django.urls import include, re_path

from apps.solNFT import views 

urlpatterns = [
    re_path(r'mint_token', views.mint_token, name = "mint_token")
]
