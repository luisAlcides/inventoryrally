from django.shortcuts import render, redirect
from .models import Product, Category, Sale
from .forms import ProductForm, CategoryForm, ForecastForm
from django.db.models import Sum, F
from .models import Supplier, Unit
from .forms import SupplierForm, UnitForm
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

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))

        product = Product.objects.get(id=product_id)
        product.current_stock -= quantity
        product.save()

        Sale.objects.create(product=product, quantity=quantity)

        return redirect("vendedor_interface")

    return render(request, "vendedor_interface.html", {"products": products})


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


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()

        # Usar expresiones regulares para buscar el nombre del producto y los meses
        product_match = re.search(r"(?i)pronostico de demanda para el (\w+)", user_message)
        months_match = re.search(r"en (\d+) meses?", user_message, re.IGNORECASE)

        # Aquí estableces el producto y el número de meses por defecto
        forecast_url = reverse("forecast_demand")

        # Construye la respuesta con el enlace a la página de pronóstico
        response_message = f"Puedes ver el pronóstico de demanda en el siguiente enlace: <a href='{forecast_url}'>Pronóstico de Demanda</a>"

        # Enviar la respuesta como JSON
        return JsonResponse({"response": response_message})



def forecast_demand(request):
    return render(request, "forecast_demand.html")
