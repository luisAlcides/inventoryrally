from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("add_product/", views.add_product, name="add_product"),
    path("add_category/", views.add_category, name="add_category"),
    path("vendedor/", views.vendedor_interface, name="vendedor_interface"),
    path("add_supplier/", views.add_supplier, name="add_supplier"),
    path("list_suppliers/", views.list_suppliers, name="list_suppliers"),
    path("add_unit/", views.add_unit, name="add_unit"),
    path("list_units/", views.list_units, name="list_units"),
    path("chatbot/", views.chatbot_response, name="chatbot_response"),
    path("forecast_demand/", views.forecast_demand, name="forecast_demand"),
    path("chatbot_response/", views.chatbot_response, name="chatbot_response"),
    path("add_client", views.add_client, name="add_client"),
    path("list_clients", views.list_clients, name="list_clients"),
    path('purchase/<int:product_id>/', views.product_purchase, name='product_purchase'),

]
