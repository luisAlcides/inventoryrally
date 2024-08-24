from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    company_name = models.CharField(max_length=100, verbose_name="Nombre de la Empresa")
    provider_name = models.CharField(
        max_length=100, verbose_name="Nombre del Proveedor"
    )
    phone_number = models.CharField(max_length=15, verbose_name="Número de Teléfono")

    def __str__(self):
        return self.company_name


class Unit(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True
    )
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.IntegerField()

    def __str__(self):
        return self.name


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale of {self.quantity} {self.product.name}(s) on {self.date}"
