from django.shortcuts import render,redirect
from .models import Product,Category,Availability,Seller,Company,Subcategory,SubcategoryLevel2,AddToCart,Buyer,User,Location,Orders,Shipment
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import ProductForm
from django.contrib import messages
# Create your views here.
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search,Q
from django.db.models import Sum
def check_if_buyer_or_seller(func):
    def inner(request):
        try :
            if Buyer.objects.filter(email=request.user.email) or Seller.objects.filter(email=request.user.email):
                print("Test passed")
            else :
                return HttpResponseRedirect(reverse("registration_step2"))
            if 'auth.seller' in request.user.get_all_permissions():
                return HttpResponseRedirect(reverse("seller_income"))
        except :
            pass
        return func(request)
    return inner
@check_if_buyer_or_seller
def index(request):
    category=Category.objects.all()
    print(category)
    empty_products = Availability.objects.filter(stock=0)
    for i in empty_products:
        print(i.product)
        print(i.product.category)
    dict={}
    for i in category:
        products=Product.objects.filter(category__category=i)
        for k in empty_products:
            if k.product.category==i:
                products =products.exclude(name=k.product.name)
        dict[f'{i}']=list(products)
    return render(request,'all_prod.html',{'category':category,"object_dict":dict,"empty_products":empty_products})
def seller_index(request):
    if request.method=="POST":
        # print(request.POST)
        if Product.objects.filter(name=request.POST['name_of_product'],seller=Seller.objects.get(email=request.user.email)):
            k=Availability.objects.get(product__name=Product.objects.filter(name=request.POST['name_of_product'])[0].name,seller=Seller.objects.get(email=request.user.email))
            k.stock+=1
            k.save()
        elif request.POST['name_of_product'] and request.POST['category'] and request.POST['price']:

            if Company.objects.filter(company=request.POST['company']):
                company=Company.objects.get(company=request.POST['company'])
            else :
                company=Company(company=request.POST['company'])
                company.save()
            if Category.objects.filter(category=request.POST['category']):
                category=Category.objects.get(category=request.POST['category'])
            else :
                category=Category(category=request.POST['category'])
                category.save()
            if Subcategory.objects.filter(subcategory=request.POST['subcategory'],category=category):
                subcategory=Subcategory.objects.get(subcategory=request.POST['subcategory'],category=category)
            else :
                subcategory=Subcategory(subcategory=request.POST['subcategory'],category=category)
                subcategory.save()
            if SubcategoryLevel2.objects.filter(subcategoryLevel2=request.POST['subcategory_level2']) and request.POST['subcategory_level2']:
                subcategory_level2=SubcategoryLevel2(subcategoryLevel2=request.POST['subcategory_level2'],subcategory=request.POST['subcategory_level2'],category=category)
            else:
                subcategory_level2=SubcategoryLevel2(subcategoryLevel2=request.POST['subcategory_level2'],category=category,subcategory=subcategory)
                subcategory_level2.save()
            # subcategory = request.POST['subcategory'], subcategory_level2 = request.POST['subcategory_level2']
            prod=Product(name=request.POST['name_of_product'],category=category,subcategory=subcategory,subcategory_level2=subcategory_level2,price=request.POST['price'],seller=Seller.objects.get(name=request.user),discount=request.POST['discount'],description=request.POST['description'],company=company)
            print(prod.id)
            prod.save()
            Availability(product=prod,stock=1,seller=Seller.objects.get(email=request.user.email)).save()
        return HttpResponseRedirect("/")
    fm=ProductForm()
    return render(request,'seller_index.html',{'form':fm})
def product_info(request,category,id,seller_id):
    # Here are the views for product info
    print(id,category,seller_id)
    product=Product.objects.get(id=id)
    print(product)
    seller=Seller.objects.get(id=seller_id)
    stock=Availability.objects.get(product=product,seller=seller).stock
    return render(request,'product_info.html',{'product':product,'stock':stock,'seller':seller})
def search_result(request):
    print(request.GET)
    all_prod={}
    product=""
    try:
        product=Product.objects.filter(name=request.GET['q'])
        c=product[0].category
    except:
        c=request.GET['q']
    print(c)
    category=Category.objects.get(category=c)
    all_prod=Product.objects.filter(category=category.id)
    if product and category:
        all_prod = Product.objects.filter(category=category.id)

        return render(request,'search_result.html',{'product':product[0],'all_prod':all_prod})
    return render(request,'search_result.html',{'all_prod':all_prod})
def add_to_cart(request):
    if request.method=="POST":
        prod=Product.objects.get(id=request.POST['product_id'])
        # messages.success(request,f'You have successfully add product {Product.objects.get(id=prod.id)}')
        k=Availability.objects.get(product=prod,seller__id=request.POST['seller_id'])
        print(k)
        print(k.stock-int(request.POST['quantity']))
        if k.stock-int(request.POST['quantity'])>=0:
            print("Invoked")
            k.stock-=int(request.POST['quantity'])
            k.save()
            try :
                prod_present=AddToCart.objects.get(name=prod,buyer=Buyer.objects.get(email=request.user.email))
                prod_present.quantity+=int(request.POST['quantity'])
                prod_present.save()
            except :
                prod_add=AddToCart(name=prod,seller=prod.seller,buyer=Buyer.objects.get(email=request.user.email),quantity=int(request.POST['quantity']))
                prod_add.save()
            print(request.user.email)
    all_prod=AddToCart.objects.filter(buyer=Buyer.objects.get(email=request.user.email).id)
    print(all_prod)
    return render(request,'add_to_cart.html',{'all_prod':all_prod})
def register_as(request):
    if request.method=="POST":
        print("Invoked")
        role=""
        print(request.POST.keys())
        if 'buyer' in request.POST.keys():
            if request.POST['buyer'] == "1":
                role="buyer"
        elif request.POST['seller'] == "1":
                role="seller"
        request.session['role']=role
        print(request.session['role'])
        return HttpResponseRedirect(reverse("registration_register"))
    return render(request,'register_as.html')
def registration_step2(request):
    if request.method=="POST":
        print("Invoked im POST method")
        print(request)
        if request.session['role']== "buyer":
            b = Buyer(name=request.user, email=request.user.email, phone=request.POST['phone'],
                      location=Location.objects.get(id=1)).save()
            return HttpResponseRedirect(reverse("index"))
        elif request.session['role'] == "seller":
            if Category.objects.filter(category=request.POST['product_category']):
                category=Category.objects.get(category=request.POST['product_category'])
            else :
                category=Category(category=request.POST['product_category'])
                category.save()

            Seller(name=request.user,email=request.user.email,location=Location.objects.get(id=1),product_category=category).save()
            return HttpResponseRedirect(reverse("seller_index"))
    if request.method=="GET":
        print("Invoked in get MEthod")
        if request.session.get("role",0)=="buyer":
            buyer = Group.objects.get(name="buyer")
            buyer.user_set.add(request.user)
            print("Invoked in buyer method")
        elif request.session.get("role",0)=="seller":
            print("Invoked for seller registration step2")
            seller = Group.objects.get(name="seller")
            seller.user_set.add(request.user)
    return render(request,'registration_step2.html')
def complete_your_payment(request):
    if request.method=="POST":
        prod_id=request.POST.get('product_id',0)
        if prod_id:
            prod=Product.objects.get(id=prod_id)
            k = Availability.objects.get(product=prod)
            k.stock -= 1
            k.save()
    for i,key in enumerate(request.POST):
        if key[:11]=="product_id_":
            prod=Product.objects.get(id=request.POST[key])
            print(prod)
            print(request.user.email)
            k=AddToCart.objects.get(name=prod.id,buyer__email=request.user.email,seller=prod.seller.id)
            k.delete()
            order=Orders(buyer=Buyer.objects.get(name=request.user),product=prod,payment_method="Paytm",shipment=Shipment.objects.get(id=1),seller=prod.seller)
            order.save()
            messages.success(request,f"You have successfully completed your payment for {prod.name}")
    return render(request,'purchase.html')
def show_order(request):
    order=Orders.objects.filter(buyer__id=Buyer.objects.get(email=request.user.email).id)
    pending_orders=order.filter(delivered="No")
    delivered_orders=order.filter(delivered="Yes")
    return render(request,'orders.html',{'pending_orders':pending_orders,'delivered_orders':delivered_orders})

# Kam Krna hai abhi ispe
def update_product(request):
    if request.method=="POST":
        print(request.POST)
        s=AddToCart.objects.get(name=Product.objects.get(id=request.POST['product_id']))
        seller=Seller.objects.get(id=request.POST['seller_id'])
        print(seller)
        k=Availability.objects.get(product=Product.objects.get(id=request.POST['product_id']),seller=seller)
        print(k.stock)
        if s.quantity>int(request.POST['quantity']):
            k.stock=k.stock-int(request.POST['quantity'])+s.quantity
            k.save()
        elif s.quantity<int(request.POST['quantity']):
            if k.stock-int(request.POST['quantity'])+s.quantity>0:
                k.stock=k.stock-int(request.POST['quantity'])+s.quantity
            k.save()
        print(s)
        s.quantity=request.POST['quantity']
        s.save()
    return HttpResponseRedirect(reverse("add_to_cart"))

def seller_income(request):
    delivered_orders=Orders.objects.filter(seller__email=request.user.email,delivered="Yes")
    undelivered_orders=Orders.objects.filter(seller__email=request.user.email).exclude(delivered="Yes")
    print(delivered_orders)
    print(undelivered_orders)
    earning=delivered_orders.aggregate(Sum('product__price'))['product__price__sum']
    print(earning)
    return render(request,'seller_income.html',{'delivered_orders':delivered_orders,'undelivered_orders':undelivered_orders,'earning':earning})
def handle_filtering(request):
    print(request.POST)
    clicked_items = []

    if request.method=="POST":
        for i in request.POST:
            if (i[:9]=="category_"):
                    clicked_items.append(i)
    print(clicked_items)
    client=Elasticsearch()
    # s=Search().using(client).index('ecommerce_products_using_python').query("nested",path="category",query=Q("match",category__category="Mobile")).query("range",discount={'lte':1}).query("range",discount={'gte':0}) #nested query with discount
    s=Search().using(client).index('ecommerce_products_using_python')
    for i,key in enumerate(request.POST):
        if i==0:
            continue
        if key[:9]=="category_":
            print(key[9:])
            s=s.query("nested",path="category",query=Q("match",category__category=f"{key[9:]}"))
    max_price=request.POST.get('max_price',"")
    min_price=request.POST.get('min_price',"")
    discount=request.POST.get("discount_range",0)
    if max_price and min_price:
        s=s.query("range",price={'lte':int(request.POST.get("max_price")) ,'gte':int(request.POST.get("min_price"))})
    if discount:
        s=s.query("range",discount={'lte':int(request.POST.get("discount_range"))})

    res=s.execute()
    category=Category.objects.all()
    prod_li=[]
    print(res)
    for i in range(len(res['hits']['hits'])):
        min_list=[]
        min_list.append(res['hits']['hits'][i]['_source']['name'])
        min_list.append(res['hits']['hits'][i]['_source']['price'])
        min_list.append(res['hits']['hits'][i]['_id'])
        min_list.append(res['hits']['hits'][i]['_source']['category']['category'])
        prod_li.append(min_list)
    print("--------->",clicked_items)
    print(discount)
    return render(request,'handle_filtering.html',{"category":category,"clicked_items":clicked_items,"all_prod":prod_li,'max_price':max_price,"min_price":min_price,'discount':discount})