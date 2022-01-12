
from django.urls import include, re_path

from apps.solNFT import views 

urlpatterns = [
    re_path(r'mint_token', views.mint_token, name = "mint_token"),
    re_path(r'login', views.login, name = "login"),
    re_path(r'get_all_property_filter',views.get_all_property_filtered,name="get_all_proprty"),
    re_path(r'get_all_property',views.get_all_property,name="get_all_proprty"),
    re_path(r'get_property_details',views.get_property_details,name="get_proprty_details"),
    re_path(r'save-user', views.saveUserDetails, name = "saveUserDetails"),
    re_path(r'get-user-details', views.getUserDetails, name = "getUserDetails"),
    re_path(r'logout', views.logout, name = "logout"),


]
