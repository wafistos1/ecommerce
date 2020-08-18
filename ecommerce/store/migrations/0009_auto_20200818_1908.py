# Generated by Django 3.1 on 2020-08-18 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
        ('store', '0008_auto_20200818_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='register.customer'),
        ),
        migrations.AlterField(
            model_name='product',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorite', to='register.Customer'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='register.customer'),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]