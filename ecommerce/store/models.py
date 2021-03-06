from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from register.models import Profil
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
# from djangoratings.fields import RatingField
import uuid
# Create your models here.


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Item(models.Model): 
    """[summary]

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    description = models.TextField(null=True, blank=True) 
    favorite = models.ManyToManyField(Profil, related_name='favorite', blank=True)
    is_favorite = models.BooleanField(default=False, null=True, blank=True)
    # rating = RatingField(range=5)


    def get_rate_item(self):
        rate = Rating.objects.filter(item=self).aggregate(Avg('stars'))
        rating = rate['stars__avg']
        if rating == None:
            rating = 0
        rating = int(rating)
        return rating

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store_detail", args=[str(self.id)])

    def get_add_to_cart_url(self):
        return reverse("add_to_cart", args=[str(self.id)])

    def get_list_cart(self):
        return reverse('list_cart', args=(str(self.id)))

    # def get_remove_from_cart_url(self):
    #     return reverse("core:remove-from-cart", args=[str(self.id)])

    # def get_favorite_url(self):  # new
    #     return reverse('favorite_annonce', args=[str(self.id)])
 
    # def get_update_url(self):  # new
    #     return reverse('annonce_update', args=[str(self.id)])
 
    # def get_delete_url(self):  # new
    #     return reverse('annonce_delete', args=[str(self.id)])


class OrderItem(models.Model):
    """[summary]

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    user = models.ForeignKey(Profil,  on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemOrders')
    quantity = models.IntegerField(default=0)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item(self):
        return OrderItem.objects.all().count()

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', args=(str(self.pk)))

    def get_total_orderitem(self):
        total = 0
        items = OrderItem.objects.filter(user=self.user)
        for item in items:
            total += item.get_total_item_price()
        return total


class Order(models.Model):
    """[summary]

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    user = models.ForeignKey(Profil, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    # ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('ShippingAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey('ShippingAddress', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    # coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def __str__(self):
        return str(self.id)


class ShippingAddress(models.Model):
    """[summary]

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, null=True, related_name='profil_address')
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=False)
    address1 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.address


class ImagesItem(models.Model):
    """[summary]

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    item_images = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='image')
    image = models.FileField(upload_to='image/', default='image_default.jpg', blank=True, null=True)
    
    class Meta:
        pass

    def __str__(self):
        return self.item_images.title


class Rating(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    item = models.ManyToManyField(Item, related_name='item')
    user = models.ManyToManyField(Profil, related_name='profile') 
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])