from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
seller,created=Group.objects.get_or_create(name="seller")
ct=ContentType.objects.get_for_model(User)
permission=Permission.objects.create(codename="seller",name="seller",content_type=ct)
seller.permissions.add(permission)
buyer,created=Group.objects.get_or_create(name="buyer")
permission=Permission.objects.create(codename="buyer",name="buyer",content_type=ct)
buyer.permissions.add(permission)