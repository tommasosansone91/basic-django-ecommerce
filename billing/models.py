from django.db import models
from django.conf import settings

# from python_ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save

from accounts.models import GuestEmail

# Create your models here.

User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user=request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None

        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(
                user=user, 
                email=user.email
                )

        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email
                )

        else:
            print("nè guest nè user")

        return obj


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) #OneToOneField
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # customer is in stripe or brwwin

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print("api request - Send to stripe/braintree")
#         instance.customer_id = newID
#         instance.save()

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)

