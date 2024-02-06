# forms.py
from django import forms
from .models import Customer

class BalanceUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['balance']

    def __init__(self, *args, **kwargs):
        current_balance = kwargs.pop('current_balance', None)
        super().__init__(*args, **kwargs)
        self.fields['balance'].initial = current_balance

    def clean_balance(self):
        current_balance = self.fields['balance'].initial
        new_balance = self.cleaned_data['balance']
        updated_balance = current_balance + new_balance
        return updated_balance

class FetchCustomerForm(forms.Form):
    customerID = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        label='Customer ID',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def clean_customerID(self):
        customer_id = self.cleaned_data['customerID']
        # Add any custom validation logic for customer ID here if needed
        return customer_id