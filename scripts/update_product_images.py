import os
import sys
import django

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'street_access.settings')
django.setup()

from store.models import Product

updates = {
    1: {'name': 'Nike Jordan Retro 1', 'description': 'Iconic basketball sneakers', 'image_url': '/static/store/images/NikeJordanRetro1.jpg'},
    2: {'name': 'Nike Tech Tracksuit', 'description': 'Comfortable tech fabric tracksuit', 'image_url': '/static/store/images/NikeTechTracksuitCoolGray.jpg'},
    3: {'name': 'Supreme Hoodie', 'description': 'Limited edition street wear hoodie', 'image_url': '/static/store/images/SupremeHoodie.jpg'},
    4: {'name': 'Adidas Ultraboost', 'description': 'Running shoes with boost technology', 'image_url': '/static/store/images/AdidasUltraBoost.jpg'},
    5: {'name': 'Nike Jordan 1 Mid', 'description': 'Classic basketball shoes', 'image_url': '/static/store/images/Classicbasketballshoes.jpg'},
    6: {'name': 'Nike Tech Tracksuit', 'description': 'Reflective Nike Tech Tracksuit with sleek streetwear details', 'image_url': '/static/store/images/NikeTechTracksuitCoolGray.jpg'},
    7: {'name': 'Supreme Pullover', 'description': 'Limited edition streetwear pullover', 'image_url': '/static/store/images/Limitededitionstreetwearhoodie.jpg'},
    8: {'name': 'Adidas Superstar', 'description': 'Retro sneakers with timeless style', 'image_url': '/static/store/images/AdidasSuperstar.jpg'},
}

for pid, data in updates.items():
    try:
        product = Product.objects.get(id=pid)
        product.name = data['name']
        product.description = data['description']
        product.image_url = data['image_url']
        product.save()
        print(f'Updated product {pid}: {product.name}')
    except Product.DoesNotExist:
        print(f'Product id {pid} not found')
