from itertools import product
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Max

class Colors(models.Model):
  color_name = models.CharField(max_length=50,default=None)

  def __str__(self):
    return self.color_name

# Create your models here.
class Customer(models.Model):

  COUNTRY_PHONE_CODES = (
      ('+1', 'USA'),
      ('+81', 'Japan'),
      ('+91', 'India'),
      ('+49', 'Germany'),
      ('+44', 'UK'),
      ('+33', 'France'),
      ('+39', 'Italy'),
      ('+55', 'Brazil'),
      ('+86', 'China'),
      ('+7', 'Russia')
  )

  STATE_CHOICES = (('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Delhi', 'Delhi'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Puducherry', 'Puducherry'),)

  id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  customer_name = models.CharField(max_length=250)
  customer_phone = models.PositiveIntegerField()
  customer_address = models.CharField(max_length=250)
  customer_city = models.CharField(max_length=250)
  customer_state = models.CharField(choices=STATE_CHOICES,max_length=250)
  customer_country = models.CharField(choices=COUNTRY_PHONE_CODES,max_length=250)

  def __str__(self):
    return self.customer_name

class Product(models.Model):
  CATEGORY_CHOICES = (
    ('Mobiles','Mobiles'),
    ('Laptops','Laptops'),
    ('Headphones','Headphones'),
    ('Smartwatches','Smartwatches'),
  )

  id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  product_name = models.CharField(max_length=100)
  selling_price = models.FloatField()
  discounted_price = models.FloatField()
  description = models.TextField()  
  colors = models.ManyToManyField(Colors)
  brand = models.CharField(max_length=100)
  category = models.CharField(choices=CATEGORY_CHOICES,max_length=20)
  product_quantity = models.PositiveIntegerField()
  highlight_product_image = models.ImageField(upload_to='producting')
  front_product_image = models.ImageField(upload_to='product_images')
  back_product_image = models.ImageField(upload_to='product_images')
  rightside_product_image = models.ImageField(upload_to='product_images')
  leftside_product_image = models.ImageField(upload_to='product_images')
  manufactured_by = models.CharField(max_length=255,default='')
  auto_increment_id = models.PositiveBigIntegerField(editable=False, unique=False,default=1)
  def save(self, *args, **kwargs):
        if not self.auto_increment_id:
            max_id = Product.objects.aggregate(max_id=Max('auto_increment_id'))['max_id']
            self.auto_increment_id = (max_id or 0) + 1
        super().save(*args, **kwargs)

  def __str__(self):
    return self.product_name

  @property
  def total_discount(self):
    discount = (self.selling_price - self.discounted_price)/(self.selling_price) 
    return float(discount*100)

class Cart(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  color = models.ForeignKey(Colors,on_delete=models.CASCADE,default='')
  quantity = models.PositiveIntegerField(default=1)

  def __str__(self):
    return str(self.id)
  
  @property
  def total_amount(self):
    return self.product.discounted_price * self.quantity
  

class OrderPlaced(models.Model):

  ORDER_STATUS = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('Out For Delivery','Out For Delivery'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
  )

  user = models.ForeignKey(User,on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer,on_delete=models.CASCADE,default='')
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  ordered_date = models.DateTimeField(auto_now_add=True)
  order_status = models.CharField(choices=ORDER_STATUS,max_length=80,default='Pending')
  is_paid = models.BooleanField(default=False)
  razor_pay_order_id = models.CharField(max_length=200,default='',blank=True,null=True)
  razor_pay_payment_id = models.CharField(max_length=200,default='',blank=True,null=True)
  razor_pay_payment_signature = models.CharField(max_length=200,default='',blank=True,null=True)


  def __str__(self):
    return str(self.id)

  @property
  def each_product_total_cost(self):
    return self.product.discounted_price * self.quantity

class WishList(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  # customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
  # isWishlisted = models.BooleanField(default=False)
  added_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.id)

  @property
  def get_total_price(self):
    return self.product.discounted_price

class Review(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  order = models.ForeignKey(OrderPlaced,on_delete=models.CASCADE)
  ratings = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.id)
