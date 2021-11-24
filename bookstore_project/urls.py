"""django_shop_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from bookstore import views
from bookstore import views as store_views
from bookstore.views import store, ProductDetailView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('bookstore.urls')),
    path('',views.store,name='store'),
    # path('',ProductView.as_view(), name='store'),
    path('update_item/',views.updateitem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    path('contact_us/', store_views.contact, name='contact_us'),
    path('success/', store_views.thank_you, name='thank_you'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    # path('product/<int:pk>',views.productdetails,name='product-detail')
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)