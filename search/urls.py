from django.urls import path

app_name = "search"


from search.views import ( #potrebbe essere aNCHE SOLO .VIEWS

    SearchProductView,

)


urlpatterns = [    

    path('search/', SearchProductView.as_view(), name="query"), 
    
]