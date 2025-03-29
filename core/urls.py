from django.shortcuts import redirect
from django.urls import path
from . import views
from .views import register_view, login_view, logout_view, home, rent_success_view, toggle_favorite_view, \
    delete_car_view

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('add-car/', views.add_car_view, name='add_car'),
    path('filter/', views.car_filter_view, name='car_filter'),
    path('car/<int:car_id>/', views.car_detail_view, name='car_detail'),
    path('rent/<int:car_id>/', views.rent_car_view, name='rent_car'),
    path('rent-success/', rent_success_view, name='rent_success'),
    path('rent/cancel/<int:rent_id>/', views.cancel_rent_view, name='cancel_rent'),
    path('favorite/<int:car_id>/', toggle_favorite_view, name='toggle_favorite'),
    path('notifications/', views.notification_list_view, name='notifications'),
    path('user_profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('verify-email/<int:user_id>/', views.verify_email_view, name='verify_email'),
    path('forgot-password/', views.password_reset_request_view, name='forgot_password'),
    path('reset-password/<int:user_id>/', views.password_reset_verify_view, name='reset_password'),
    path('delete-car/<int:car_id>/', delete_car_view, name='delete_car'),
    path('accounts/login/', lambda request: redirect('login')),

]