
from django.urls import path

app_name = "products"


from products.views import (
    ProductListView, 
    # product_list_view, 
    # ProductDetailView, 
    ProductDetailSlugView,
    # product_detail_view,
    # ProductFeaturedListView,
    # ProductFeaturedDetailView,
    
)


urlpatterns = [
    
    # path('admin/', admin.site.urls),

    # path('', home_page, name="home"),
    # path('about/', about_page, name="about"),
    # path('contact/', contact_page, name="contact"),
    # path('login/', login_page, name="login"),
    # path('register/', register_page, name="register"),

    path('products/', ProductListView.as_view(), name="list"), #spostato nell altro urls
    # path('products-fbv/', product_list_view),

# posso chiamarli id o pk a mio piacimento
    # path('products/<int:pk>', ProductDetailView.as_view()),
    path('products/<str:slug>', ProductDetailSlugView.as_view(), name="detail"), #spostato nell altro urls
    # path('products-fbv/<int:pk>', product_detail_view),

    # path('featured/', ProductFeaturedListView.as_view()),
    # path('featured/<int:pk>', ProductFeaturedDetailView.as_view()),


    
]
