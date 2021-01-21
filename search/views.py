
from django.shortcuts import render
from products.models import Product
from django.views.generic.list import ListView

# Create your views here.
class SearchProductView(ListView):
    # è comunque una lista

    template_name = "search/view.html" 

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q') # va a cercare il form che ha come attributo name="q" e prende quello che ha inserito l'utente
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context


    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        print(query)
        if query is not None:
            # lookups = Q(title__icontains=query) | Q(description__icontains=query)
            return Product.objects.search(query)
            # return Product.objects.filter(lookups).distinct() # distinct per dire che se trova il risultato in anetrambi i campi li riporta una volta sola (nel metaglossario non ho usato distinct e funzionava bene uguale)
        else:
            return Product.objects.featured()


        '''
        django triple multiline comments
        '''