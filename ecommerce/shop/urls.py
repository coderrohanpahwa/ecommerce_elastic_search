from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name="index"),
    path('add_product/',views.seller_index,name="seller_index"),
    path('product_info/<category>/<int:id>/',views.product_info,name="product_info"),
    path("search_results/",views.search_result,name="search_result"),
    path('cart/',views.add_to_cart,name="add_to_cart"),
    path("register_as/",views.register_as,name="register_as"),
    path("registration_step2/",views.registration_step2,name="registration_step2"),
    path("complete_your_payment/",views.complete_your_payment,name="complete_your_payment"),
    path("show_orders/",views.show_order,name="show_order"),
    path('update_product/',views.update_product,name="update_product"),
    path("seller_income/",views.seller_income,name="seller_income"),
    path("handle_filtering/",views.handle_filtering,name="handle_filtering")
]