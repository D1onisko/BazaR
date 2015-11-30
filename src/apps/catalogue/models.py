# -*- coding: utf-8 -*-
import os
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect

from autoslug.settings import slugify as default_slugify
from autoslug import AutoSlugField
from PIL import Image
from sorl.thumbnail import ImageField
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
import mptt


def _add_mini(s):
    parts = s.split(".")
    parts.insert(-1, "mini")
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)


def _del_mini(p):
    mini_path = _add_mini(p)
    if os.path.exists(mini_path):
        os.remove(mini_path)


def custom_slugify(value):
    # для перевода в кирилицу нужно установить pytils==0.3
    return default_slugify(value).replace('-', '_')


@python_2_unicode_compatible
class Category(MPTTModel):
    """
    Описание модели категория товара
    """

    STANDALONE, PARENT, CHILD = 'standalone', 'parent', 'child'
    STRUCTURE_CHOICES = (
        (STANDALONE, _('Stand-alone product')),
        (PARENT, _('Parent product')),
        (CHILD, _('Child product'))
    )
    structure = models.CharField(_('Product structure'), max_length=10, choices=STRUCTURE_CHOICES, default=STANDALONE)
    parent = TreeForeignKey(u'self', verbose_name=_(u'Parent'), blank=True, null=True, related_name=u'children')
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    description = models.TextField(_('Description'), blank=True)
    slug = AutoSlugField(populate_from='name', slugify=custom_slugify, unique=True)
    is_active = models.BooleanField(verbose_name=_('Is active'), default=None)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    class MPTTMeta:
        order_insertion_by = ['name']
        level_attr = 'level'

    objects = TreeManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogue:category', args=[self.slug])

mptt.register(Category)

@python_2_unicode_compatible
class Product(models.Model):
    """
    Описание модели  Product
    """
    category = TreeForeignKey(Category, verbose_name=_('Category'),related_name=u'entries',)
    user_name = models.ForeignKey(User, related_name='+', to_field=u'username')
    title = models.CharField(_('Product title'), max_length=255)
    slug = AutoSlugField(populate_from='title', slugify=custom_slugify, unique=False)
    price = models.IntegerField(verbose_name=_('Price'), max_length=10)
    valuta = models.CharField(_('Currency'), max_length=10)
    address = models.CharField(verbose_name=_('Address'), max_length=100)
    phone = models.IntegerField(verbose_name=_('Phone'), null=True)
    description = models.TextField(_('Description'), max_length=255)
    image = models.ImageField(verbose_name=_('Image'), upload_to=u'itempics', blank=True, null=True, default= u'images/test.jpg')
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)
    is_discountable = models.BooleanField(_("Is discountable?"), default=True, )

    class Meta:
        ordering = ['-date_created']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        if self.title:
            return self.title

    def get_absolute_url(self):
        return reverse('catalogue:product_detail', args=[str(self.pk)])


    objects = models.Manager()

    def _get_mini_path(self):
        return _add_mini(self.image.path)



    mini_path = property(_get_mini_path)

    def get_mini_html(self):
        html = '<a class="image-picker" href="%s"><img src="%s" alt="%s"/></a>'
        return html % (self.image.url, _add_mini(self.image.url), self.description)

    mini_html = property(get_mini_html)
    get_mini_html.short_description = 'Миниатюра'
    get_mini_html.allow_tags = True

    def save(self, force_insert=False, force_update=False, using=None):
        try:
            obj = Product.objects.get(id=self.id)
            if obj.image.path != self.image.path:
                _del_mini(obj.image.path)
                obj.image.delete()
        except:
            pass
        super(Product, self).save()
        img = Image.open(self.image.path)
        img.thumbnail(
            (128, 128),
            Image.ANTIALIAS
        )
        img.save(self.mini_path, 'JPEG')

    def delete(self, using=None):
        # переопределение метода delete. Удаляет объявление без удаления default-картинки
        def default_image(self):
            return _add_mini(self.image['images/test.jpg'])

        try:
            obj = Product.objects.get(id=self.id)
            if obj.image.path == default_image:
                _del_mini(obj.image.path)
                obj.image.delete()
        except (Product.DoesNotExist, ValueError):
            pass
        super(Product, self).delete()

