from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
@receiver(post_save,sender=Product)

def create_product_in_elastic_search(sender,instance,created,**kwargs):
