from django.db import models

from carts.models import Cart

from python_ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save

import math

from billing.models import BillingProfile

from addresses.models import Address

# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),

)



class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile, 
            cart=cart_obj, 
            active=True
            )        

        if qs.count()==1:
            created = False
            obj = qs.first()
        else:
            obj = Order.objects.create(
                billing_profile=billing_profile, 
                cart=cart_obj)   
            created = True     
        return obj, created
        

class Order(models.Model):
    # corretto abbia piu foreign key
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, blank=True)
    
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True, on_delete=models.CASCADE)
     #visto che uso 2 foreign key associate llo stesso modello devo usare dei related name diversi per indicarle
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.order_id

    objects = OrderManager()

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total]) #fsum= sommatoria
        # new_total = cart_total + shipping_total
        print("eseguita somma nel checkout:")
        formatted_total = format(new_total, '.2f')
        print(formatted_total)
        # self.total = new_total #errato nel video
        self.total = new_total
        self.save()
        return new_total


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)

    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)

        if qs.count() ==1:
            order_obj = qs.first()
            print("updating")
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    print("running")
    if created:
        print("updating")
        instance.update_total()

post_save.connect(post_save_order, sender=Order)