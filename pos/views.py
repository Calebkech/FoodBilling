from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required
from .models import Product, Customer, Order, OrderItem
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


@login_required
def dashboard(request):
    return render(request, 'pos/dashboard.html')

@login_required
def billing(request):
    if request.method == 'GET':
        return render(request, 'pos/billing.html')
    else:
        cid = request.POST.get('customerID', None)
        customer = Customer.objects.get(pk=cid)
        products = list(Product.objects.all())

        #the code below ni very long but inawork the same way as the one above, 
        # context = { 'cust' : customer.identity,
        #             'name' : customer.name,
        #             'balance' : customer.balance,
        #             'products': products, }
        return render(request, 'pos/billing_details.html', {'customer': customer, 'products': products})

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
        return render(request, 'pos/order.html', {'success' : order.success})

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price']
    template_name = 'pos/new_product.html'
    success_url = reverse_lazy('product_list')  # Assuming you have a URL named 'product_list' for the list view

    def form_valid(self, form):
        # Set the current user as the creator of the product
        form.instance.user = self.request.user
        product_name = form.instance.name
        success_message = f'{product_name} save successfully'
        messages.success(self.request, success_message)
        # Call the parent class's form_valid method to save the form and get the response
        response = super().form_valid(form)
        # Return the response
        return response
    

class ProductListView(ListView):
    model = Product
    template_name = 'pos/product_list.html'
    context_object_name = 'page_obj'
    ordering = ['-id']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by(*self.ordering)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context
    
    def test_func(self):

        return True


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['name', 'balance', 'photo']
    template_name = 'pos/new_customer.html'
    success_url = reverse_lazy('customer_list')  # Adjust the URL name if needed

    def form_valid(self, form):
        form.instance.user = self.request.user
        customer_name = form.instance.name
        success_message = f'{customer_name} save successfully'
        messages.success(self.request, success_message)
        return super().form_valid(form)
    
class CustomerListView(ListView):
    model = Customer
    template_name = 'pos/customer_list.html'
    context_object_name = 'page_obj'
    ordering = ['-identity']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by(*self.ordering)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context
    
    def test_func(self):

        return True
        

def customer_info(request):
    if request.method == 'GET':
        return render(request, 'pos/billing.html')
    else:
        cid = request.POST.get('customerID', None)
        customer = Customer.objects.get(pk=cid)
        products = list(Product.objects.all())

        #the code below ni very long but inawork the same way as the one above, 
        # context = { 'cust' : customer.identity,
        #             'name' : customer.name,
        #             'balance' : customer.balance,
        #             'products': products, }
        return render(request, 'pos/customer_info.html', {'customer': customer, 'products': products})

#display details of one item
class CutomerDetailsView(DetailView):
    model = Customer
    template_name = 'pos/customer_info_details.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
    def test_func(self):
        item = self.get_object()
        if self.request.user == item.user:
            return True
        return False
    
class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['name', 'balance', 'photo']
    template_name = 'pos/update_customer.html'
    success_url = reverse_lazy('customer_list')


    def form_valid(self, form):
        form.instance.user = self.request.user
        customer_name = form.instance.name

        try:
            response = super().form_valid(form)
            success_message = f'Customer "{customer_name}" successfully updated'
            messages.success(self.request, success_message)
        except Exception as e:
            error_message = f'Failed to update customer "{customer_name} {str(e)}"'
            messages.error(self.request, error_message)
            # You can log the error or perform any other necessary actions
            response = super().form_invalid(form)
        return response

    def test_func(self):
        trans = self.get_object()
        print(trans)
        if self.request.user == trans.user:
            return True
        return False
    
class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'pos/customer_delete.html'
    success_url = reverse_lazy('customer_list')

    def test_func(self):
        customer = self.get_object()
        return self.request.user == customer.user

    def form_valid(self, form):
        messages.success(self.request, "Customer successfully deleted")
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

# Product Views 

#Product detail view
class ProductDetailView(DeleteView):
    model = Product
    template_name = 'pos/product_details.html'
    
    def get_queryset(self):
        querySet = super().get_queryset()
        return querySet
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.user:
            return True
        return False

#Product Update View
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price']
    template_name = 'pos/product_update.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        product_name = form.instance.name
        product_price = form.instance.price

        try:
            response = super().form_valid(form)
            success_message = f'updated successfully. Name: {product_name}, Price: {product_price} '
            messages.success(self.request, success_message)
        except Exception as e:
            error_message = f'Failed to update "{product_name} {str(e)}"'
            messages.error(self.request, error_message)
            response = super().form_invalid(form)
        return response
    
    def test_func(self):
        prod = self.get_object()
        print(prod)
        if self.request.user == prod.user:
            return True
        return False

#Product Delete View
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'pos/product_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user
    
    def form_valid(self, form):
        success_message = f'Deleted Successfully'
        messages.success(self.request, success_message)
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
