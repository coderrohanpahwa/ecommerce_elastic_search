from django.db import models
from django.core.validators import MaxValueValidator
# Create your models here.
from django.contrib.auth.models import User
class State(models.Model):
    state=models.CharField(max_length=100)
    def __str__(self):
        return self.state
class Country(models.Model):
    country=models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="Countries"
    def __str__(self):
        return self.country
class City(models.Model):
    pincode=models.IntegerField()
    city=models.CharField(max_length=100)
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    country=models.ForeignKey(Country,on_delete=models.CASCADE)
    def __str__(self):
        return self.city
    class Meta:
        verbose_name_plural="cities"
class Location(models.Model):
    address=models.CharField(max_length=100)
    city=models.ForeignKey(City,on_delete=models.CASCADE)
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    country=models.ForeignKey(Country,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural="Location"
    def __str__(self):
        return self.city.city +" || "+ self.state.state+" || " +self.country.country
class Category(models.Model):
    category=models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.category

class Subcategory(models.Model):
    subcategory=models.CharField(max_length=100,blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        verbose_name_plural="Subcategories"
    def __str__(self):
        return f'{self.category} || {self.subcategory}'
class SubcategoryLevel2(models.Model):
    subcategory=models.ForeignKey(Subcategory,on_delete=models.CASCADE,blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    subcategoryLevel2=models.CharField(max_length=100)
    def __str__(self):
        return f' {self.subcategory} || {self.subcategoryLevel2}'

class Seller(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.IntegerField(blank=True,null=True)
    location=models.ForeignKey(Location,on_delete=models.CASCADE)
    product_category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    email=models.EmailField(blank=True,null=True)
    def __str__(self):
        return f'{self.name} || {self.product_category}'
class Buyer(models.Model):
    name=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.IntegerField()
    location=models.ForeignKey(Location,on_delete=models.CASCADE)
    email=models.EmailField(blank=True,null=True)
    def __str__(self):
        return f'{self.id} || {self.name}'
class Company(models.Model):
    company=models.CharField(max_length=100)
    quality_type=models.CharField(choices=(("Premium","Premium"),("High","High"),("Low","Low"),("Bad","Bad")),max_length=20)
    def __str__(self):
        return self.company
class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    subcategory=models.ForeignKey(Subcategory,on_delete=models.CASCADE,null=True,blank=True)
    subcategory_level2=models.ForeignKey(SubcategoryLevel2,on_delete=models.CASCADE,blank=True,null=True)
    price=models.PositiveIntegerField()
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE)
    discount=models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    description=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return f'{self.name} || {self.category}'
class Rating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MaxValueValidator(5)])
class Availability(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    stock=models.PositiveIntegerField()
    class Meta:
        verbose_name_plural="availibility"
    def __str__(self):
        return f'{self.product} || {self.stock}'
class AddToCart(models.Model):
    name=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE,null=True,blank=True)
    buyer=models.ForeignKey(Buyer,on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.PositiveIntegerField()
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.name} || {self.quantity}'
    class Meta:
        verbose_name_plural="Add To Cart"
class Shipment(models.Model):
    name_of_company=models.CharField(
        max_length=50,
        choices=[("Ecart","Ecart"),("Delhivery","Delhivery"),("India Post","India Post")]
    )
    payment=models.PositiveIntegerField()
class Orders(models.Model):
    buyer=models.ForeignKey(Buyer,on_delete=models.CASCADE,blank=True,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    payment_method=models.CharField(max_length=50)
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE,null=True,blank=True)
    shipment=models.ForeignKey(Shipment,on_delete=models.CASCADE,blank=True,null=True)
    delivered=models.CharField(max_length=10,choices=(("Yes","yes"),("No","no")),null=True,blank=True)
    # def __str__(self):
    #     return f'{self.product.name} || {self.buyer.name} || Delivered : {self.delivered}'
    class Meta:
        verbose_name_plural="Orders"

class SellerIncome(models.Model):
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE,blank=True,null=True)
    number_of_products_sold=models.IntegerField(null=True)
    turnover_gained=models.IntegerField(blank=True)
