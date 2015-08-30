# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import mptt.fields
import src.apps.catalogue.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('structure', models.CharField(default=b'standalone', max_length=10, verbose_name='Product structure', choices=[(b'standalone', 'Stand-alone product'), (b'parent', 'Parent product'), (b'child', 'Child product')])),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', unique=True, slugify=src.apps.catalogue.models.custom_slugify)),
                ('is_active', models.BooleanField(default=None, verbose_name='Is active')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name='Parent', blank=True, to='catalogue.Category', null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Product title', blank=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', editable=False, slugify=src.apps.catalogue.models.custom_slugify)),
                ('price', models.IntegerField(verbose_name='Price', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated', db_index=True)),
                ('is_discountable', models.BooleanField(default=True, verbose_name='Is discountable?')),
            ],
            options={
                'ordering': ['-date_created'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(verbose_name='Category', to='catalogue.Category')),
                ('product', models.ForeignKey(verbose_name='Product', to='catalogue.Product')),
            ],
            options={
                'ordering': ['product', 'category'],
                'verbose_name': 'Product category',
                'verbose_name_plural': 'Product categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.ImageField(upload_to=b'images/products/%Y/%m/', max_length=255, verbose_name=b'Original')),
                ('caption', models.CharField(max_length=200, verbose_name='Caption', blank=True)),
                ('display_order', models.PositiveIntegerField(default=0, verbose_name='Display order')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('product', models.ForeignKey(related_name=b'images', verbose_name='Product', to='catalogue.Product')),
            ],
            options={
                'ordering': ['display_order'],
                'verbose_name': 'Product image',
                'verbose_name_plural': 'Product images',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='productimage',
            unique_together=set([('product', 'display_order')]),
        ),
        migrations.AlterUniqueTogether(
            name='productcategory',
            unique_together=set([('product', 'category')]),
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='catalogue.Category', verbose_name='Categories', through='catalogue.ProductCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(related_name='entries', verbose_name='Category', to='catalogue.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='user_name',
            field=models.ForeignKey(related_name=b'+', to=settings.AUTH_USER_MODEL, to_field='username'),
            preserve_default=True,
        ),
    ]
