from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Choices for states
STATE_CHOICES = [(state, state) for state in [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
    "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
    "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
    "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
    "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu",
    "Lakshadweep", "National Capital Territory of Delhi", "Puducherry"]]

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.PositiveIntegerField(validators=[MaxValueValidator(999999), MinValueValidator(100000)])
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.name} - {self.city}"


CATEGORY_CHOICES = [
    ("M", "Mobile"), ("L", "Laptop"), ("MT", "Men Top"),
    ("MB", "Men Bottom"), ("WT", "Women Top"), ("WB", "Women Bottom"),
    ("B", "Boys"), ("G", "Girls"), ("TW", "Top Wear"), ("BW", "Bottom Wear")
]

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField(validators=[MinValueValidator(0)])
    discounted_price = models.FloatField(validators=[MinValueValidator(0)])
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to="productimage")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} - {self.brand}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.product.title} in cart"

    @property
    def total_amount(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = [
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
]

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-ordered_date']

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @property
    def total_amount(self):
        return self.quantity * self.product.discounted_price

