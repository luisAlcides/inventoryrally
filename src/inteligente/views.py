from webbrowser import get
from django.shortcuts import render, redirect
from .models import Product, Category, Sale, Client
from django.db.models import Sum, F
from .models import Supplier, Unit
from .forms import SupplierForm, UnitForm, ClientForm, ProductForm, CategoryForm, ForecastForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib, base64
import re
from django.urls import reverse
from django.http import JsonResponse
from time import sleep
from django.shortcuts import render, get_object_or_404




def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_product")
    else:
        form = CategoryForm()
    return render(request, "add_category.html", {"form": form})


def product_list(request):
    products = Product.objects.all()

    return render(
        request,
        "product_list.html",
        {
            "products": products,
        },
    )


def vendedor_interface(request):
    products = Product.objects.all()
    clients = Client.objects.all()


    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))

        product = Product.objects.get(id=product_id)
        product.current_stock -= quantity
        product.save()

        Sale.objects.create(product=product, quantity=quantity)


        return redirect("vendedor_interface")

    return render(request, "vendedor_interface.html", {"products": products, "clients": clients})


def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_suppliers")
    else:
        form = SupplierForm()
    return render(request, "add_supplier.html", {"form": form})


def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, "list_suppliers.html", {"suppliers": suppliers})


def add_unit(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_units")
    else:
        form = UnitForm()
    return render(request, "add_unit.html", {"form": form})


def list_units(request):
    units = Unit.objects.all()
    return render(request, "list_units.html", {"units": units})

def add_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_client")
    else:
        form = ClientForm()
    return render(request, "add_client.html", {"form": form})

def list_clients(request):
    clients = Client.objects.all()
    return render(request, "list_clients.html", {"clients": clients})


def demand():
    product_match = re.search(r"(?i)pronostico de demanda para el (\w+)", user_message)
    months_match = re.search(r"en (\d+) meses?", user_message, re.IGNORECASE)

    # Aquí estableces el producto y el número de meses por defecto
    forecast_url = reverse("forecast_demand")

    # Construye la respuesta con el enlace a la página de pronóstico
    response_message = f"""
    <p style='color:green;'>
    Puedes ver el pronóstico de demanda en el siguiente enlace:
    <a href='{forecast_url}' style='color: red;' onmouseover="this.style.color='#0056b3';" onmouseout="this.style.color='#007bff';">
        Pronóstico de Demanda
    </a></p>
    """
    return response_message

def product_purchase(request, product_id):
    # Obtén el producto por su ID
    product = get_object_or_404(Product, id=product_id)

    # Obtén el proveedor del producto
    supplier = get_object_or_404(Supplier, id=product.supplier_id)

    # Renderiza la plantilla con los detalles del producto y del proveedor
    return render(request, 'product_purchase.html', {
        'product': product,
        'supplier': supplier
    })

def get_product_less_10():
    products = Product.objects.filter(current_stock__lt=10)
    if not products:
        return "<p>No hay productos con menos de 10 unidades en stock.</p>"

    response_message = """
    <table style="border-collapse: collapse; width: 100%; border: 1px solid black;">
        <thead>
            <tr>
                <th style="border: 1px solid black; padding: 8px; text-align: left;">Producto</th>
                <th style="border: 1px solid black; padding: 8px; text-align: left;">Stock Actual</th>
                <th style="border: 1px solid black; padding: 8px; text-align: left;">Acción</th>
            </tr>
        </thead>
        <tbody>
    """

    for product in products:
        # Genera la URL para la vista de compra del producto
        purchase_url = reverse('product_purchase', args=[product.id])
        response_message += f"""
        <tr>
            <td style="border: 1px solid black; padding: 8px;">{product.name}</td>
            <td style="border: 1px solid black; padding: 8px;">{product.current_stock}</td>
            <td style="border: 1px solid black; padding: 8px;">
                <a href="{purchase_url}" style="color: red;" onmouseover="this.style.color='#0056b3';" onmouseout="this.style.color='#007bff';">Comprar</a>
            </td>
        </tr>
        """

    response_message += """
        </tbody>
    </table>
    <p style="margin-top: 10px;">¿Deseas comprar más productos? <a href="{% url 'product_list' %}">Haz clic aquí para ver más productos</a>.</p>
    """

    return response_message


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        response_message = get_product_less_10()
        sleep(2)
        return JsonResponse({"response": response_message})



def forecast_demand(request):
    return render(request, "forecast_demand.html")
