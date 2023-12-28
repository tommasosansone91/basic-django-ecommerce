from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.conf import settings


# Create your models here.

User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)  # User instance
    # we set the user to this view

    ip_address = models.CharField(max_length=220, blank=True, null=True)  # ip field

    # these two fields must handle every possible model
    # like products, order, cart address .....
    content_type = models.ForeignKey(ContentType, 
                                     # content type there allows a shade menu in admin section
                                     on_delete=models.CASCADE)  #  products, order, cart address .....
    
    object_id = models.PositiveBigIntegerField()   #  product id, order id, cart id, address id.....
    content_object = GenericForeignKey('content_type', 'object_id')  # rpoduct instance
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} viewed on {}".format(self.content_object, self.timestamp)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'