from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Product, Customer, Order, OrderItem
from users.models import User_Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from pos.forms import BalanceUpdateForm, FetchCustomerForm
from django.shortcuts import render, redirect
from decimal import Decimal

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def billing(request):
    if request.method == 'GET':
        return render(request, 'billing.html')
    else:
        cid = request.POST.get('customerID', None)
        customer = Customer.objects.get(pk=cid)
        products = list(Product.objects.all())

        #the code below ni very long but inawork the same way as the one above, 
        # context = { 'cust' : customer.identity,
        #             'name' : customer.name,
        #             'balance' : customer.balance,
        #             'products': products, }
        return render(request, 'billing_details.html', {'customer': customer, 'products': products})

@login_required
def order(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        if data is None:
            raise AttributeError
        print(data)
        customer = Customer.objects.get(pk=data['customer_id'])
        order = Order.objects.create(customer=customer,
                                    total_price=data['total_price'],
                                    success=False)
        for product_id in data['product_ids']:
            OrderItem(product=Product.objects.get(pk=product_id), order=order).save()
        if data['total_price'] <= customer.balance:
            customer.balance -= int(data['total_price'])
            customer.save()
            order.success = True
        order.save()
        return render(request, 'order.html', {'success' : order.success})

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price']
    template_name = 'new_product.html'
    success_url = reverse_lazy('product_list')  # Assuming you have a URL named 'product_list' for the list view

    def form_valid(self, form):
        # Set the current user as the creator of the product
        form.instance.user = self.request.user

        # Call the parent class's form_valid method to save the form and get the response
        response = super().form_valid(form)

        # Return the response
        return response
    

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['identity', 'name', 'balance', 'photo']
    template_name = 'new_customer.html'
    reverse_lazy = 'customer_list'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response
    
class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'

class BalanceUpdateView(UpdateView):
    model = Customer
    form_class = BalanceUpdateForm
    template_name = 'update_balance.html'
    success_url = reverse_lazy('customer_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_balance'] = self.object.balance
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def fetch_customer_id(self, request, *args, **kwargs):
        if request.method == 'GET':
            return render(request, 'fetch_customer_id.html')
        elif request.method == 'POST':
            try:
                cid = request.POST.get('customerID', None)
                customer = get_object_or_404(Customer, pk=cid)
                return render(request, 'update_balance.html', {'customer': customer})
            except Customer.DoesNotExist:
                return HttpResponse("Customer not found")
        else:
            return HttpResponse("Invalid request method")

    def dispatch(self, *args, **kwargs):
        if 'fetch_customer_id' in self.request.path:
            return self.fetch_customer_id(*args, **kwargs)
        return super().dispatch(*args, **kwargs)
    

class UpdateBalanceView(View):
    template_name = 'update_balance.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        identity = request.POST.get('identity', None)
        amount = request.POST.get('amount', None)

        try:
            customer = Customer.objects.get(identity=identity)
            amount_decimal = Decimal(amount)
            customer.balance += amount_decimal
            customer.save()
            return redirect('update_balance_success', identity=identity)
        except Customer.DoesNotExist:
            return render(request, self.template_name, {'error_message': 'Customer not found.'})
        except ValueError:
            return render(request, self.template_name, {'error_message': 'Invalid amount.'})
        
class UpdateBalanceSuccessView(View):
    template_name = 'update_balance_success.html'

    def get(self, request, identity):
        try:
            customer = Customer.objects.get(identity=identity)
            return render(request, self.template_name, {'customer': customer})
        except Customer.DoesNotExist:
            return render(request, self.template_name, {'error_message': 'Customer not found.'})
        

class CustomerDetailsView(UpdateView):
    model = Customer
    form_class = BalanceUpdateForm
    template_name = 'update_balance.html'
    success_url = reverse_lazy('customer_list')
    
    def customer_details(request):
        if request.method == 'GET':
            return render(request, 'billing.html')
        else:
            cid = request.POST.get('customerID', None)
            customer = Customer.objects.get(pk=cid)
            return render(request, 'billing_details.html', {'customer': customer})
