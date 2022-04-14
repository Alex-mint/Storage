from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import RegisterUserForm, LoginUserForm, OrderForm
from .mixins import CartMixin
from .models import Item, CartProduct, Customer, Order, Cart
from .utils import recalc_cart


class Home(CartMixin, View):
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


@login_required
def edit_address(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        customer.city = request.POST.get('city')
        customer.street = request.POST.get('street')
        customer.number = request.POST.get('number')
        customer.save()
        return redirect('account')
    return render(request, 'main/account.html')


@login_required
def edit_account(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.phone = request.POST.get('phone')
        customer.save()
        return redirect('account')
    return render(request, 'main/account.html')


class AccountView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        context = {
            'customer': customer,
            'cart': self.cart,
        }
        return render(request, 'main/account.html', context)


class StaffView(View):

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all
        context = {
            'orders': orders
        }
        return render(request, 'main/staff.html', context)


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    context = {
        'order': order,
        'first_image': order.images.all()[:1],
        'images': [image.image.url for image in order.images.all()[1:]],
        'all_images': [image.image.url for image in order.images.all()],
    }

    return render(request, 'main/order-details.html', context=context)


class Checkout(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        form = OrderForm(request.POST or None)
        context = {
            'customer': customer,
            'cart': self.cart,
            'form': form
        }
        return render(request, 'main/checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            customer.first_name = form.cleaned_data['first_name']
            customer.last_name = form.cleaned_data['last_name']
            customer.phone = form.cleaned_data['phone']
            customer.save()
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


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
