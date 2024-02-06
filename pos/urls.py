from django.urls import path
from pos.views import (order, billing, dashboard, ProductCreateView, ProductListView, CustomerCreateView, 
                            CustomerListView, BalanceUpdateView, UpdateBalanceView,  UpdateBalanceSuccessView, CustomerDetailsView)


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('billing/', billing, name='billing'),
    path('billing/order', order, name='order'),
    path('new_product/', ProductCreateView.as_view(), name="new_product"),
    path('product_list/', ProductListView.as_view(), name = "product_list"),
    path('new_customer/', CustomerCreateView.as_view(), name="new_customer"),
    path('customer_list/', CustomerListView.as_view(), name = "customer_list"),
    path('update-balance/', UpdateBalanceView.as_view(), name='update_balance'),
    path('customer_details/', CustomerDetailsView.as_view(), name = 'customer_details'),
    path('update-balance/success/<int:identity>/', UpdateBalanceSuccessView.as_view(), name='update_balance_success'),
]
