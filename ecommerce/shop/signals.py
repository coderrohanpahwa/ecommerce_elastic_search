from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product as product_model
from .models import Category as category_model
from django.contrib.auth.models import User
from .elastic_search_product import Product
from .elastic_search_category import Category
@receiver(post_save,sender=product_model)
def create_product_in_elastic_search(sender,instance,created,**kwargs):
    print("Invoked in signals")
    print(sender,instance,created)
    if created:
        id=instance.id
        name=instance.name
        category=instance.category.category
        subcategory=instance.subcategory.subcategory
        # subcategoryLevel2=instance.subcategory_level2.subcategoryLevel2
        price=instance.price
        discount=instance.discount
        description=instance.description
        company_name=instance.company.company
        company_type=instance.company.quality_type
        seller_id=instance.seller.id
        seller_username=instance.seller.name.username
        seller_phone=instance.seller.phone
        seller_location=instance.seller.location.address
        seller_city=instance.seller.location.city.city
        seller_state=instance.seller.location.state.state
        seller_country=instance.seller.location.country.country
        seller_email=instance.seller.email
        # I have to do work on query of location object
        Product(_id=instance.id,name=name,category={'category':instance.category.category},subcategory={'category':{'category':category},'subcategory':subcategory},subcategoryLevel2={'category':{'category':category},'subcategory':{'subcategory':subcategory,category:{'category':category}}},price=price,seller={'name':{'username':seller_username,"email":seller_email,"id":seller_id},"phone":seller_phone},discount=discount,description=description,company={"company":company_name,"quality_type":company_type}).save(refresh=True)

@receiver(post_save,sender=category_model)
def create_categories_in_elastic_search(sender,instance,created,**kwargs):
    if created:
        Category(_id=instance.id,category=instance.category).save(refresh=True)
