from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),

    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('postComment/', views.postComment, name="postComment"),
    path('products/<int:myid>', views.productview, name="ProductView"),
    path('checkout/', views.checkout, name="Checkout"),

]