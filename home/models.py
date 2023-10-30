from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum
#Base Mdel
class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)

    class Metas:
        abstract=True

class PizzaCategory(BaseModel):
    category_name=models.CharField(max_length=100)

class Pizza(BaseModel):
    category = models.ForeignKey(PizzaCategory, on_delete=models.CASCADE, related_name='category')
    pizza_name=models.CharField(max_length=100)
    price=models.IntegerField(default=100)
    images=models.ImageField(upload_to='pizza')

class Cart(BaseModel):
    user=models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='carts')
    is_paid = models.BooleanField(default=False)
    @property
    def get_cart_total(self):
        total = CartItems.objects.filter(cart_user__user=self.user).aggregate(Sum('piza__price')).get('piza__price__sum')
        return total


class CartItems(BaseModel):
    cart_user=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    piza=models.ForeignKey(Pizza,on_delete=models.CASCADE,related_name='cart_items')

