from django import forms
from .models import Product, Category, Supplier, Unit, Client

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "supplier",
            "unit",
            "purchase_price",
            "sale_price",
            "current_stock",
        ]
        labels = {
            "name": "Nombre del Producto",
            "category": "Categoría",
            "supplier": "Proveedor",
            "unit": "Unidad",
            "purchase_price": "Precio de Compra",
            "sale_price": "Precio de Venta",
            "current_stock": "Stock Actual",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["company_name", "provider_name", "phone_number"]
        labels = {
            "company_name": "Nombre de la Empresa",
            "provider_name": "Nombre del Proveedor",
            "phone_number": "Número de Teléfono",
        }
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'provider_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name"]
        labels = {
            "name": "Unidad",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ForecastForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="Producto", widget=forms.Select(attrs={'class': 'form-control'}))
    months = forms.IntegerField(
        min_value=1, max_value=12, initial=3, label="Meses a pronosticar",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["first_name", "last_name", "phone_number", "email", "address"]
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "phone_number": "Número de Teléfono",
            "email": "Correo Electrónico",
            "address": "Dirección",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
