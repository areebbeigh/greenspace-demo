from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from users.forms import LoginForm
from users.views import RegistrationView
from ecomm.views import (ProductList, ProductCreate, ProductDetail,
                         Home, OrderCreate, NurseryList, ProductUpdate, ProductDelete,
                         NurseryOrderList, NurseryOrderDone, CustomerOrderDone, CustomerOrderList,)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/register/', RegistrationView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        extra_context={'title': 'Login'},
        authentication_form=LoginForm,
        redirect_authenticated_user=True,
    ), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('customer/products/', ProductList.as_view(), name='product-list'),
    path('customer/products/<slug:pk>/',
         ProductDetail.as_view(), name='product-detail'),
    path('customer/products/<slug:pk>/buy',
         OrderCreate.as_view(), name='order-create'),
    path('customer/orders/', CustomerOrderList.as_view(), name='customer-order-list'),
    path('customer/orders/<slug:pk>/done', CustomerOrderDone.as_view(), name='customer-order-done'),

    path('manager/products', NurseryList.as_view(), name='nursery-list'),
    path('manager/products/new', ProductCreate.as_view(), name='product-create'),
    path('manager/products/<slug:pk>/edit', ProductUpdate.as_view(), name='product-edit'),
    path('manager/products/<slug:pk>/delete', ProductDelete.as_view(), name='product-delete'),
    path('manager/orders/', NurseryOrderList.as_view(), name='nursery-order-list'),
    path('manager/orders/<slug:pk>/done', NurseryOrderDone.as_view(), name='nursery-order-done'),

    path('', Home.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
