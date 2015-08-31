# -*- coding: utf-8 -*-
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings

import mptt

from autoslug.settings import slugify as default_slugify
from autoslug import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey

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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogue:category', args=[self.slug])



@python_2_unicode_compatible
class Product(models.Model):
    """
    Описание модели  Product
    """
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name=u'entries')
    user_name = models.ForeignKey(User, related_name='+', to_field=u'username')
    title = models.CharField(_('Product title'), max_length=255, blank=True)
    slug = AutoSlugField(populate_from='title', slugify=custom_slugify, unique=False)
    price = models.IntegerField(_('Price'), blank=True)
    description = models.TextField(_('Description'), blank=True)
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


