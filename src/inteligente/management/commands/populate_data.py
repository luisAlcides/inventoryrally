# inteligente/management/commands/populate_data.py
from django.core.management.base import BaseCommand
from inteligente.models import Product, Sale, Category, Supplier, Unit
from django.utils import timezone
import random


class Command(BaseCommand):
    help = "Poblar la base de datos con 50 productos con categorías, precios y unidades realistas"

    def handle(self, *args, **kwargs):
        # Crear categorías realistas
        categorias = {
            "Alimentos": [
                "Arroz",
                "Frijoles",
                "Pasta",
                "Aceite",
                "Azúcar",
                "Harina",
                "Sal",
                "Cereal",
                "Lentejas",
                "Galletas",
            ],
            "Bebidas": [
                "Jugo de Naranja",
                "Agua Mineral",
                "Refresco",
                "Té",
                "Café",
                "Bebida Energética",
            ],
            "Lácteos": ["Leche", "Queso", "Yogurt", "Mantequilla", "Crema"],
            "Carnes": ["Carne de Res", "Pollo", "Pescado", "Jamón", "Tocino"],
            "Frutas y Verduras": [
                "Manzana",
                "Pera",
                "Plátano",
                "Tomate",
                "Pepino",
                "Zanahoria",
                "Cebolla",
                "Lechuga",
                "Sandía",
                "Mandarina",
            ],
            "Panadería y Dulces": [
                "Pan Integral",
                "Chocolate",
                "Helado",
                "Miel",
                "Gelatina",
            ],
            "Condimentos y Especias": ["Pimienta", "Orégano", "Paprika", "Ajo"],
        }

        # Crear unidades realistas
        unidades = {
            "Kilogramo": [
                "Arroz",
                "Frijoles",
                "Pasta",
                "Azúcar",
                "Harina",
                "Sal",
                "Lentejas",
                "Carne de Res",
                "Pollo",
                "Pescado",
                "Manzana",
                "Pera",
                "Plátano",
                "Tomate",
                "Pepino",
                "Zanahoria",
                "Cebolla",
                "Lechuga",
                "Sandía",
                "Mandarina",
            ],
            "Litro": [
                "Leche",
                "Jugo de Naranja",
                "Agua Mineral",
                "Refresco",
                "Té",
                "Aceite",
                "Café",
            ],
            "Unidad": [
                "Queso",
                "Yogurt",
                "Mantequilla",
                "Crema",
                "Pan Integral",
                "Chocolate",
                "Helado",
                "Galletas",
                "Bebida Energética",
                "Miel",
                "Gelatina",
                "Pimienta",
                "Orégano",
                "Paprika",
                "Ajo",
            ],
            "Paquete": ["Jamón", "Tocino", "Cereal"],
            "Caja": ["Galletas", "Chocolate"],
        }

        # Crear proveedores
        proveedores = [
            {
                "nombre": "Distribuidora Alimentos S.A.",
                "contacto": "Carlos Perez",
                "telefono": "111111111",
            },
            {
                "nombre": "Bebidas Nacionales",
                "contacto": "Ana Lopez",
                "telefono": "222222222",
            },
            {
                "nombre": "Lácteos Frescos",
                "contacto": "Marta Garcia",
                "telefono": "333333333",
            },
            {
                "nombre": "Carnes de Calidad",
                "contacto": "Jose Martinez",
                "telefono": "444444444",
            },
            {
                "nombre": "Frutas y Verduras del Campo",
                "contacto": "Laura Hernandez",
                "telefono": "555555555",
            },
            {
                "nombre": "Panadería Dulce Hogar",
                "contacto": "Pedro González",
                "telefono": "666666666",
            },
            {
                "nombre": "Especias Gourmet",
                "contacto": "María Rodríguez",
                "telefono": "777777777",
            },
        ]
        proveedores_objs = [
            Supplier.objects.create(
                company_name=prov["nombre"],
                provider_name=prov["contacto"],
                phone_number=prov["telefono"],
            )
            for prov in proveedores
        ]

        # Crear productos y asignarles ventas aleatorias
        for categoria, productos in categorias.items():
            categoria_obj = Category.objects.create(name=categoria)
            for producto in productos:
                unidad = next(
                    (u for u, ps in unidades.items() if producto in ps), "Unidad"
                )
                unidad_obj, created = Unit.objects.get_or_create(name=unidad)

                # Precios estimados
                precio_compra = round(random.uniform(0.5, 20.0), 2)
                precio_venta = round(precio_compra * random.uniform(1.1, 2.0), 2)

                # Seleccionar proveedor al azar
                proveedor_obj = random.choice(proveedores_objs)

                producto_obj = Product.objects.create(
                    name=producto,
                    category=categoria_obj,
                    supplier=proveedor_obj,
                    unit=unidad_obj,
                    purchase_price=precio_compra,
                    sale_price=precio_venta,
                    current_stock=random.randint(50, 500),
                )

                # Crear ventas de ejemplo para cada producto
                for _ in range(
                    random.randint(10, 30)
                ):  # Generar entre 10 y 30 ventas para cada producto
                    Sale.objects.create(
                        product=producto_obj,
                        quantity=random.randint(1, 20),
                        date=timezone.now()
                        - timezone.timedelta(
                            days=random.randint(1, 730)
                        ),  # Fechas en los últimos 2 años
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Se han creado 50 productos con ventas en diferentes fechas."
            )
        )
