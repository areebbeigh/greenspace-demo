from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, RedirectView, View, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from ecomm.models import Product, Order
from ecomm.forms import ProductForm


class UserIsNurseryManagerMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_nursery_manager()

    def get_permission_denied_message(self):
        return "You're not a nursery manager."


class UserOwnsProductMixin(UserPassesTestMixin):
    def test_func(self):
        return (self.request.user.is_nursery_manager() and
                self.get_product().owner == self.request.user)

    def get_permission_denied_message(self):
        return 'You do not own this product.'


class UserIsOrderSellerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_order().seller == self.request.user

    def get_permission_denied_message(self):
        return 'You are not the seller.'


class UserIsOrderBuyerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_order().buyer == self.request.user

    def get_permission_denied_message(self):
        return 'Not your order'


class Home(RedirectView):
    pattern_name = 'product-list'


class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/list.html'
    title = None


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product/detail.html'


class ProductCreate(UserIsNurseryManagerMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create_form.html'
    success_url = reverse_lazy('nursery-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': Product(owner=self.request.user)})
        return kwargs


class ProductUpdate(UserOwnsProductMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/update_form.html'
    success_url = reverse_lazy('nursery-list')

    def get_product(self):
        return Product.objects.get(id=self.kwargs['pk'])


class ProductDelete(UserOwnsProductMixin, DeleteView):
    model = Product
    template_name = 'product/confirm_delete.html'
    success_url = reverse_lazy('nursery-list')

    def get_product(self):
        return Product.objects.get(id=self.kwargs['id'])


class NurseryList(UserIsNurseryManagerMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'manager/nursery.html'

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('customer-order-list')

    def post(self, *args, **kwargs):
        self.product = Product.objects.get(id=kwargs.get('pk'))
        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': Order(buyer=self.request.user,
                                         product=self.product, seller=self.product.owner)})
        return kwargs


class NurseryOrderList(UserIsNurseryManagerMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'manager/orders.html'

    def get_queryset(self):
        return Order.objects.filter(seller=self.request.user)


class NurseryOrderDone(UserIsOrderSellerMixin, View):

    def post(self, request, *args, **kwargs):
        order = self.get_order()
        if 'complete' in request.POST:
            order.status = 'Delivered'
        elif 'cancel' in request.POST:
            order.status = 'Failed'
        else:
            return redirect('nursery-order-list')
        order.save()
        return redirect('nursery-order-list')

    def get_order(self):
        return Order.objects.get(id=self.kwargs['pk'])


class CustomerOrderDone(UserIsOrderBuyerMixin, View):

    def post(self, request, *args, **kwargs):
        order = self.get_order()
        if 'cancel' in request.POST:
            order.status = 'Failed'
        else:
            return redirect('customer-order-list')
        order.save()
        return redirect('customer-order-list')

    def get_order(self):
        return Order.objects.get(id=self.kwargs['pk'])


class CustomerOrderList(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'customer/orders.html'

    def get_queryset(self):
        return self.request.user.orders_placed.all()
