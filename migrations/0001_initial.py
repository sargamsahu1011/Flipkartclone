# Generated by Django 4.1.1 on 2022-09-11 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("locality", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=50)),
                ("zipcode", models.IntegerField()),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                            ("Maharashtra", "Maharashtra"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("selling_price", models.FloatField()),
                ("discounted_price", models.FloatField()),
                ("description", models.TextField()),
                ("brand", models.CharField(max_length=100)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("M", "Mobile"),
                            ("M", "Mobile"),
                            ("M", "Mobile"),
                            ("M", "Mobile"),
                        ],
                        max_length=2,
                    ),
                ),
                ("product_image", models.ImageField(upload_to="productimage")),
            ],
        ),
        migrations.CreateModel(
            name="OrderPlaced",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("ordered_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Accepted", "Accepted"),
                            ("Packed", "Packed"),
                            ("On The Way", "On The Way"),
                            ("Delivered", "Delivered"),
                            ("Cancel", "Cancel"),
                        ],
                        default="Pending",
                        max_length=50,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.customer"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.product"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.product"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
