import stripe
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.conf import settings

from .forms import RegisterUserForm, LoginUserForm, OrderForm, AddImageForm, \
    StatusForm, PageInfo
from .mixins import CartMixin
from .models import Cart, Item, CartProduct, Customer, Order, Image, PageMessage
from .utils import recalc_cart, send_message, get_map


class Home(CartMixin, View):
    def get(self, request, *args, **kwargs):
        items = Item.objects.filter(category__name='items')
        boxes = Item.objects.filter(category__name='box')
        context = {
            'storage': self.storage,
            'items': items,
            'boxes': boxes,
            'cart': self.cart,
        }
        return render(request, 'main/index.html', context)


class AboutUs(CartMixin, View):
    def get(self, request, *args, **kwargs):
        text = PageInfo.objects.filter(title_es='about').first()
        context = {
            'storage': self.storage,
            'cart': self.cart,
            'text': text
        }
        return render(request, 'main/about_us.html', context)


class ContactUs(CartMixin, View):
    def get(self, request, *args, **kwargs):
        text = PageInfo.objects.filter(title_es='contacto').first()
        folium_map = get_map(self.storage)
        context = {
            'storage': self.storage,
            'cart': self.cart,
            'text': text,
            'map': folium_map._repr_html_()
        }
        return render(request, 'main/contact_us.html', context)


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {
                'storage': self.storage,
                'cart': self.cart,
            }
            return render(request, 'main/cart.html', context)
        else:
            send_message('login', request)
            return redirect('home')


class CartVueView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        cart_vue = []#Cart.objects.filter(id=self.cart.id).values()
        items = []
        for item in self.cart.products.all():
            a = {
                'id': item.item.id,
                'title': item.item.title,
                'price':item.item.price,
                'qty': item.qty,
                'final_price': item.final_price
            }
            items.append(a)
        
        cart_vue = {'items': items, 
                    'month': self.cart.month, 
                    'total': self.cart.final_price
                    }
        
            #print(item.item.title)

        if request.user.is_authenticated:
            context = {
                'storage': self.storage,
                'cart': self.cart,
                'cart_vue': cart_vue,
            }
            print(cart_vue)
            return render(request, 'main/cart_vue.html', context)
        else:
            send_message('login', request)
            return redirect('home')


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            item_slug = kwargs.get('slug')
            item = Item.objects.get(slug=item_slug)
            cart_product, created = CartProduct.objects.get_or_create(
                user=self.cart.owner, cart=self.cart, item=item
            )
            if created:
                self.cart.products.add(cart_product)
            recalc_cart(self.cart)
            send_message('add_to_cart', request)
            return HttpResponseRedirect('/')
        else:
            send_message('login', request)
            return redirect('home')


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
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        send_message('update_price', request)
        return HttpResponseRedirect('/cart/')


class ChangeMonthsView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        cart = self.cart
        cart.month = int(request.POST.get('months'))
        cart.save()
        recalc_cart(cart)
        send_message('update_price', request)
        return HttpResponseRedirect('/cart/')


def edit_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            customer = Customer.objects.get(user=request.user)
            customer.city = request.POST.get('city')
            customer.street = request.POST.get('street')
            customer.number = request.POST.get('number')
            customer.save()
            send_message('edit_address', request)
            return redirect('account')
        return render(request, 'main/account.html')
    else:
        return redirect('home')


def edit_account(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            customer = Customer.objects.get(user=request.user)
            customer.first_name = request.POST.get('first_name')
            customer.last_name = request.POST.get('last_name')
            customer.phone = request.POST.get('phone')
            customer.email = request.POST.get('email')
            customer.save()
            send_message('edit_account', request)
            return redirect('account')
        return render(request, 'main/account.html')
    else:
        return redirect('home')


def edit_status(request, id):
    if request.user.is_staff:
        if request.method == 'POST':
            order = Order.objects.get(id=id)
            order.status = request.POST.get('status')
            order.save()
            return redirect(f'/order-details/{id}')
        return render(request, '/')
    else:
        return redirect('home')


def edit_staff_comment(request, id):
    if request.user.is_staff:
        if request.method == 'POST':
            order = Order.objects.get(id=id)
            order.staff_comment = request.POST.get('comment')
            order.save()
            return redirect(f'/order-details/{id}')
        return render(request, '/')
    else:
        return redirect('home')


def order_cancel(request, id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)
        order.delete()
        send_message('cancel', request)
        if request.user.is_staff:
            return redirect('staff')
        else:
            return redirect('account')
    else:
        return redirect('home')


class AccountView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            text = PageMessage.objects.filter(title='dashboad').first()
            context = {
                'storage': self.storage,
                'customer': customer,
                'cart': self.cart,
                'text': text
            }
            return render(request, 'main/account.html', context)
        else:
            return redirect('home')


class StaffView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            orders = Order.objects.all
            context = {
                'storage': self.storage,
                'orders': orders,
            }
            return render(request, 'main/staff.html', context)
        else:
            return redirect('home')


def order_detail(request, id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=id)
        form = AddImageForm(request.POST, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                Image.objects.create(
                    order=get_object_or_404(Order, id=id),
                    image=request.FILES.get('image')
                )
                return redirect(f'/order-details/{id}')
        else:
            form = AddImageForm()
        context = {
            'order': order,
            'first_image': order.images.all()[:1],
            'images': [image.image.url for image in order.images.all()[1:]],
            'all_images': [image.image.url for image in order.images.all()],
            'form': form,
            'status_form': StatusForm(request.POST)
        }

        return render(request, 'main/order-details.html', context=context)
    else:
        return redirect('home')


def order_view(request, id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=id)
        context = {
            'order': order,
        }
        return render(request, 'main/order-view.html', context=context)
    else:
        return redirect('home')


class Checkout(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            form = OrderForm(request.POST or None)
            context = {
                'storage': self.storage,
                'customer': customer,
                'cart': self.cart,
                'form': form,
                'pub_key': settings.STRIPE_API_KEY_PUBLIC
            }
            return render(request, 'main/checkout.html', context)
        else:
            return redirect('home')


class StripeView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        line_items = [
            {
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f'Storage x {self.cart.month}/mo',
                    },
                    'unit_amount': int(self.cart.final_price * 100),
                },
                'quantity': 1
            }
        ]

        stripe.api_key = self.storage.secret_key
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/error/'
        )
        payment_intent = session.payment_intent
        request.session['payment_intent'] = payment_intent
        return JsonResponse({'session': session, 'order': payment_intent})


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            customer.first_name = form.cleaned_data['first_name']
            customer.last_name = form.cleaned_data['last_name']
            customer.phone = form.cleaned_data['phone']
            customer.email = form.cleaned_data['email']
            customer.city = form.cleaned_data['city']
            customer.street = form.cleaned_data['street']
            customer.number = form.cleaned_data['number']
            customer.save()
            request.session['order_date'] = str(
                form.cleaned_data['order_date'])
            request.session['comment'] = form.cleaned_data['comment']
            return HttpResponseRedirect('/pre-pay/')
        send_message('fields', request)
        return HttpResponseRedirect('/checkout/')


class PrePay(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            order_date = request.session['order_date']
            comment = request.session['comment']
            context = {
                'storage': self.storage,
                'customer': customer,
                'cart': self.cart,
                'order_date': order_date,
                'comment': comment,
                'pub_key': self.storage.public_key
            }
            return render(request, 'main/pre-pay.html', context)
        else:
            return redirect('home')


class Success(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.cart.final_price:
                customer = Customer.objects.get(user=request.user)
                new_order = Order()
                new_order.customer = customer
                new_order.first_name = customer.first_name
                new_order.last_name = customer.last_name
                new_order.phone = customer.phone
                new_order.email = customer.email
                new_order.city = customer.city
                new_order.street = customer.street
                new_order.number = customer.number
                new_order.month = self.cart.month
                new_order.cart = self.cart
                new_order.order_start = request.session['order_date']
                new_order.commit = request.session['comment']
                new_order.payment_intent = request.session['payment_intent']
                self.cart.in_order = True
                self.cart.save()
                new_order.cart = self.cart
                new_order.save()
                customer.orders.add(new_order)

                text = PageMessage.objects.get(title='pay-success')
                context = {
                    'text': text,
                }
                return render(request, 'main/success.html', context=context)
            else:
                return redirect('account')
        else:
            return redirect('home')


class RegisterUser(CartMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['storage'] = self.storage
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(CartMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['storage'] = self.storage
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')

