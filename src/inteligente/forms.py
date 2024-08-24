from django import forms
from .models import Product, Category, Supplier, Unit


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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["company_name", "provider_name", "phone_number"]
        labels = {
            "company_name": "Nombre de la Empresa",
            "provider_name": "Nombre del Proveedor",
            "phone_number": "Número de Teléfono",
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name"]
        labels = {
            "name": "Unidad",
        }


class ForecastForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="Producto")
    months = forms.IntegerField(
        min_value=1, max_value=12, initial=3, label="Meses a pronosticar"
    )
