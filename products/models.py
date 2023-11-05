import random
from django.db.models import Q
from django.db import models
import os

from django.db.models.signals import pre_save, post_save
from mainapp_ecommerce.utils import unique_slug_generator

from django.urls import reverse

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename, 
        final_filename=final_filename
        )

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):        
        lookups = (
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(tag__title__icontains=query)
            ) 


        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()
        
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() ==1:
            return qs.first()        
        return None

    def search(self, query):
        # lookups = Q(title__icontains=query) | Q(description__icontains=query) # ho sostituito con .searc e quindi ho cancellato
        return self.get_queryset().active().search(query) # ho sostituito
        # return self.get_queryset().ative().filter(lookups).distinct() # ho sostituito con .search(query)

# Create your models here.
# name as single item, not plural
class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=10, default=39.99)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True) # requires pip install pillow
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    # sovrascrive objects
    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug":self.slug})



    # modifica il nome con cui appaiono i prodotti nel modello
    def __str__(self):
        return self.title

# per django dpo il v1
    # def __unicode__(self):
    #     return self.title

    @property
    def name(self):
        return self.title
        # è una spece di alias, creo name che hs lo stesso valore di title


def product_pre_save_receiver(sender, instance, *arge, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)