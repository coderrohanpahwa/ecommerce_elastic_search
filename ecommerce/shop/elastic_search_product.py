from datetime import datetime
from elasticsearch_dsl import Document,Date,Nested,Boolean,analyzer,InnerDoc,Completion,Keyword,Text,connections,Long
class Category(InnerDoc):
    category=Text()
class Subcategory(InnerDoc):
    subcategory=Text()
    category=Nested(Category)
class SubcategoryLevel2(InnerDoc):
    subcategory=Nested(Subcategory)
    category=Nested(Category)
    subcategoryLevel2=Text()
class User(InnerDoc):
    username=Text()
    email=Text()
class State(InnerDoc):
    state=Text()
class Country(InnerDoc):
    country=Text()
class City(InnerDoc):
    city=Text()
    pincode=Long()
    state=Nested(State)
    country=Nested(Country)

class Location(InnerDoc):
    address=Text()
    city=Nested(City)
    state=Nested(State)
    country=Nested(Country)
class Seller(InnerDoc):
    name=Nested(User)
    phone=Long()
    Location=Nested()
class Company(InnerDoc):
    company=Text()
    quality_type=Text()
class Product(Document):
    name=Text(fields={"keyword":Keyword()})
    category=Nested(Category)
    subcategory=Nested(Subcategory)
    subcategoryLevel2=Nested(SubcategoryLevel2)
    price=Long()
    seller=Nested(Seller)
    discount=Long()
    description=Text()
    company=Nested(Company)
    class Index:
        name="ecommerce_products_using_python"
    def save(self,**kwargs):
        return super().save(**kwargs)

connections.create_connection()
if not Product._index.exists():
    Product.init()
