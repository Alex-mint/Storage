from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from .forms import RegisterUserForm, LoginUserForm
from .mixins import CartMixin
from .models import Item, CartProduct
from .utils import recalc_cart


class Home(CartMixin, View):
    # model = Item
    # template_name = 'main/index.html'
    # context_object_name = 'products'
    def get(self, request, *args, **kwargs):
        products = Item.objects.all()
        context = {
            'products': products,
            'cart': self.cart
        }
        return render(request, 'main/index.html', context)


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
        }
        return render(request, 'main/cart.html', context)


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        item_slug = kwargs.get('slug')
        item = Item.objects.get(slug=item_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, item=item
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        return HttpResponseRedirect('/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        item_slug = kwargs.get('slug')
        item = Item.objects.get(slug=item_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, item=item
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        item = Item.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, item=item
        )
        qty = int(request.POST.get('qty'))
        month = int(request.POST.get('month'))
        cart_product.month = month
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class Checkout(CartMixin, View):

    def get(self, request, *args, **kwargs):
        #form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            #'form': form
        }
        return render(request, 'main/checkout.html', context)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')



class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')

