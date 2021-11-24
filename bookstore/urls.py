from django.urls import path
from django.contrib.auth import views as auth_views
from . import views




urlpatterns = [
    # path('',views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    # # path('login/', views.loginPage, name='login'),
    # # path('register/', views.registerPage, name='register'),
    # # path('logout/', views.logoutUser, name='logout'),
    #
    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name="bookstore/password_reset.html"), name="reset_password"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="bookstore/password_reset_sent.html"), name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="bookstore/password_reset_confirm.html"), name="password_reset_confirm"),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="bookstore/password_reset_complete.html"), name="password_reset_complete"),
    path('search_products', views.search_products, name='search-products'),
    path('search/', views.search, name='search'),
]