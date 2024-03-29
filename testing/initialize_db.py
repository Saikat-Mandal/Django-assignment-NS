import os
import django
from django.conf import settings

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testing.settings')  # Adjust as per your project
django.setup()

from dashboard.models import Product
import random

def generate_products():
    products = [
        {"shape": "square", "size": "small"},
        {"shape": "circle", "size": "medium"},
        {"shape": "triangle", "size": "large"},
        {"shape": "rectangle", "size": "small"},
        {"shape": "hexagon", "size": "medium"},
        {"shape": "pentagon", "size": "large"}
    ]
    locations = ["pune", "mumbai" , "noida" , "kolkata"]

    total_products = 1000000
    batch_size = 1000  # Adjust batch size based on your system resources

    batches = total_products // batch_size

    for _ in range(batches):
        batch_products = []
        for _ in range(batch_size):
            product_info = random.choice(products)
            size = product_info["size"]
            shape = product_info["shape"]
            location = random.choice(locations)
            price = round(random.uniform(100, 500), 2)
            product = Product(shape=shape, size=size, location=location, price=price)
            batch_products.append(product)

        Product.objects.bulk_create(batch_products)

    # Create remaining products for the last batch
    remaining_products = total_products % batch_size
    if remaining_products:
        batch_products = []
        for _ in range(remaining_products):
            product_info = random.choice(products)
            size = product_info["size"]
            shape = product_info["shape"]
            location = random.choice(locations)
            price = round(random.uniform(100, 500), 2)
            product = Product(shape=shape, size=size, location=location, price=price)
            batch_products.append(product)

        Product.objects.bulk_create(batch_products)

if __name__ == "__main__":
    generate_products()
