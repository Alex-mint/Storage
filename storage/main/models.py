import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Storage(models.Model):
    name = models.CharField('Nombre de dueño', max_length=255)
    phone = models.CharField('Telefono', max_length=255, null=True, blank=True)
    email = models.EmailField('Correo', null=True, blank=True)
    city = models.CharField('Ciudad', max_length=100, null=True, blank=True)
    street = models.CharField('Calle', max_length=100, null=True, blank=True)
    number = models.CharField('Numero', max_length=10, null=True, blank=True)
    iban = models.CharField('Iban', max_length=255, null=True, blank=True)
    banco = models.CharField('Banco', max_length=255, null=True, blank=True)
    address = models.CharField('Direccion de Banco', max_length=255, null=True,
                               blank=True)
    image = models.ImageField('Fotos de pedido', null=True, blank=True)
    lat = models.FloatField('latitud', blank=True, null=True)
    lon = models.FloatField('longitud', blank=True, null=True)
    send_email_to_owner = models.BooleanField('Mandar email a dueño', default=False)
    send_email_to_customer = models.BooleanField('Mandar email a cliente', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Dueño'


class Item(models.Model):
    title = models.CharField('Nombre', max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField('Imagen')
    description = models.TextField('Descripcion', null=True)
    price = models.DecimalField('Precio', max_digits=9, decimal_places=2)
    extra = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Cliente',
                             on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Pedido',
                             on_delete=models.CASCADE,
                             related_name='related_products')
    item = models.ForeignKey(Item, verbose_name='Objeto',
                             on_delete=models.CASCADE)
    qty = models.PositiveIntegerField('Cantidad', default=1)
    month = models.PositiveIntegerField('Meses', default=1)
    final_price = models.DecimalField('Precio final', max_digits=9,
                                      decimal_places=2)

    def __str__(self):
        return f'{self.item.title} '

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.item.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Dueño',
                              on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True,
                                      related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField('Precio de pedido', max_digits=9,
                                      default=0, decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)
    month = models.PositiveIntegerField('Meses', default=1)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name='Usuario',
                                on_delete=models.CASCADE)
    phone = models.CharField('telefono', max_length=20, null=True, blank=True)
    city = models.CharField('Ciudad', max_length=100, null=True, blank=True)
    street = models.CharField('Calle', max_length=100, null=True, blank=True)
    number = models.CharField('Numero', max_length=10, null=True, blank=True)
    first_name = models.CharField('Nombre', max_length=255, null=True, blank=True)
    last_name = models.CharField('Apellidos', max_length=255, null=True, blank=True)
    email = models.CharField('Email', max_length=10, null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Pedidos',
                                    related_name='related_order')

    def __str__(self):
        return f'{self.user.username}'


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Nuevo pedido'),
        (STATUS_IN_PROGRESS, 'En proceso'),
        (STATUS_READY, 'Recibido'),
        (STATUS_COMPLETED, 'Entregado')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Sin transporte'),
        (BUYING_TYPE_DELIVERY, 'Con transporte')
    )

    customer = models.ForeignKey(Customer, verbose_name='Cliente',
                                 related_name='related_orders',
                                 on_delete=models.CASCADE)
    first_name = models.CharField('Nombre', max_length=255)
    last_name = models.CharField('Apellidos', max_length=255)
    phone = models.CharField('Telefono', max_length=20)
    city = models.CharField('Ciudad', max_length=100)
    street = models.CharField('Calle', max_length=100)
    number = models.CharField('Numero', max_length=10)
    email = models.CharField('Email', max_length=100)
    cart = models.ForeignKey(Cart, verbose_name='Pedido',
                             on_delete=models.CASCADE,
                             null=True, blank=True)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        'Transporte?',
        max_length=100,
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField('Comentario de cliente', null=True, blank=True)
    staff_comment = models.TextField('Comentario mio', null=True, blank=True)
    month = models.PositiveIntegerField('Meses', default=1)
    created_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Fecha de pedido')
    order_start = models.DateField(verbose_name='comenso de pedido',
                                  default=timezone.now)
    order_finish = models.DateField(verbose_name='comenso de pedido',
                                   default=timezone.now)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('order', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        self.order_finish = self.order_start + datetime.timedelta(days=30*self.month)
        super().save(*args, **kwargs)



class Image(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='images',
        verbose_name="Localizacion"
    )
    image = models.ImageField('Fotos de pedido')

    def __str__(self):
        return f'{self.id}. {self.order.id}'

    class Meta(object):
        verbose_name = "Imagen"


class PageMessage(models.Model):
    title = models.CharField('Nombre', max_length=255)
    text = models.TextField('Mensaje')

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = "Mensaje"
