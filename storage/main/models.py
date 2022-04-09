from django.conf import settings
from django.db import models
from django.utils import timezone


class Item(models.Model):
    title = models.CharField('Nombre', max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField('Imagen')
    description = models.TextField('Descripcion', null=True)
    price = models.DecimalField('Precio', max_digits=9, decimal_places=2)

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Cliente', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Pedido', on_delete=models.CASCADE, related_name='related_products')
    item = models.ForeignKey(Item, verbose_name='Objeto', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField('Cantidad', default=1)
    month = models.PositiveIntegerField('Meses', default=1)
    final_price = models.DecimalField('Precio final', max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.item.title} '

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.month * self.item.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Dueño', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField('Precio de pedido', max_digits=9, default=0, decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name='Usuario',
                                on_delete=models.CASCADE)
    phone = models.CharField('telefono', max_length=20, null=True, blank=True)
    address = models.CharField('Dirección', max_length=255, null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Pedidos', related_name='related_order')

    def __str__(self):
        return "Cliente: {} {}".format(self.user.first_name, self.user.last_name)


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

    customer = models.ForeignKey(Customer, verbose_name='Cliente', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField('Nombre', max_length=255)
    last_name = models.CharField('Apellidos', max_length=255)
    phone = models.CharField('Telefono', max_length=20)
    cart = models.ForeignKey(Cart, verbose_name='Pedido', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField('Dirección', max_length=1024, null=True, blank=True)
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
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)