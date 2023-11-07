from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product


from django.http import Http404


from carts.models import Cart

# Create your views here.

# list view

class ProductFeaturedListView(ListView):
    template_name = "products/list.html" #ci deve essere

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all().featured() #ci deve essere
    template_name = "products/fetured-detail.html" #ci deve essere

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all() #ci deve essere



class ProductListView(ListView):
    # queryset = Product.objects.all() #ci deve essere
    template_name = "products/list.html" #ci deve essere

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        request = self.request
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()




def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)

    
# detail view

class ProductDetailView(DetailView):
    # queryset = Product.objects.all() #ci deve essere
    template_name = "products/detail.html" #ci deve essere

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        # print("context")
        print(context)
        # {
        # 'object': <Product: t shirt>, 
        # 'product': <Product: t shirt>, 
        # 'view': <products.views.ProductDetailView object at 0x000002329F0A7A60>
        # }
        
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product does not exist")
        return instance


    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all() #ci deve essere
    template_name = "products/detail.html" #ci deve essere

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        request = self.request
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # instance = get_object_or_404(Product, slug=slug, active=True)

        try:
            instance = Product.objects.get(slug=slug, active=True)

        except Product.DoesNotExist:
            raise Http404("Not found...")

        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()

        except:
            raise Http404("Uhmmm")
         
        return instance    



def product_detail_view(request, pk=None, *args, **kwargs):

    # instance = Product.objects.get(pk=pk)
    # instance = get_object_or_404(Product, pk=pk)

    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print("no product here")
    #     raise Http404("oh, no! Product doesn't exist")
    # except:
    #     print("????")

    
    # instance = Product.objects.get_by_id(pk)
    # print(instance)

    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product does not exist")

    # qs = Product.objects.filter(id=pk)

    # if qs.exists() and qs.count() == 1:   # count è un metodo di queryset + efficiente sul db che ritorna len (qs)
    #     instance = qs.first()
    # else:
    #     raise Http404("oh, no! Product doesn't exist")    

    context = {        
        'object':instance,
    }

    return render(request, "products/detail.html", context)