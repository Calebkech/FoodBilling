from django.urls import path
from pos.views import (order, billing, dashboard, ProductCreateView, CutomerDetailsView ,ProductListView, CustomerCreateView, 
                            CustomerListView, CustomerUpdateView, CustomerDeleteView)


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('billing/', billing, name='billing'),
    path('billing/order', order, name='order'),
    path('new_product/', ProductCreateView.as_view(), name="new_product"),
    path('product_list/', ProductListView.as_view(), name = "product_list"),
    path('new_customer/', CustomerCreateView.as_view(), name="new_customer"),
    path('customer_list/', CustomerListView.as_view(), name = "customer_list"),
    path('customer/<int:pk>/details/', CutomerDetailsView.as_view(), name = 'customer_details'),
    path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name = 'customer_delete'),
]
