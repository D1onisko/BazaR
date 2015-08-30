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

from src.apps.catalogue.manager import ProductManager, BrowsableProductManager
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
class ProductCategory(models.Model):
    """
    Промежуточная модель для Product
    """
    product = models.ForeignKey('Product', verbose_name=_("Product"))
    category = models.ForeignKey('Category', verbose_name=_("Category"))

    class Meta:
        ordering = ['product', 'category']
        unique_together = ('product', 'category')
        verbose_name = _('Product category')
        verbose_name_plural = _('Product categories')

    def __str__(self):
        return u"<productcategory for product '%s'>" % self.product


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
    categories = models.ManyToManyField('Category', through='ProductCategory', verbose_name=_("Categories"))
    is_discountable = models.BooleanField(_("Is discountable?"), default=True, )

    objects = ProductManager()
    browsable = BrowsableProductManager()

    class Meta:
        ordering = ['-date_created']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        if self.title:
            return self.title

    def get_absolute_url(self):
        return reverse('catalogue:detail',
                       kwargs={'product_slug': self.slug, 'pk': self.id})

        # Properties

    @property
    def is_standalone(self):
        return self.structure == self.STANDALONE

    @property
    def is_parent(self):
        return self.structure == self.PARENT

    @property
    def is_child(self):
        return self.structure == self.CHILD

    def get_title(self):
        """
        Return a product's title or it's parent's title if it has no title
        """
        title = self.title
        if not title and self.parent_id:
            title = self.parent.title
        return title

    get_title.short_description = pgettext_lazy(u"Product title", u"Title")

    def get_is_discountable(self):
        """
        At the moment, is_discountable can't be set individually for child
        products; they inherit it from their parent.
        """
        if self.is_child:
            return self.parent.is_discountable
        else:
            return self.is_discountable

    def get_categories(self):
        """
        Return a product's categories or parent's if there is a parent product.
        """
        if self.is_child:
            return self.parent.categories
        else:
            return self.categories

    get_categories.short_description = _("Categories")

    # Images

    def get_missing_image(self):
        """
        Returns a missing image object.
        """
        # This class should have a 'name' property so it mimics the Django file
        # field.
        return MissingProductImage()

    def primary_image(self):
        """
        Returns the primary image for a product. Usually used when one can
        only display one product image, e.g. in a list of products.
        """
        images = self.images.all()
        ordering = self.images.model.Meta.ordering
        if not ordering or ordering[0] != 'display_order':
            # Only apply order_by() if a custom model doesn't use default
            # ordering. Applying order_by() busts the prefetch cache of
            # the ProductManager
            images = images.order_by('display_order')
        try:
            return images[0]
        except IndexError:
            # We return a dict with fields that mirror the key properties of
            # the ProductImage class so this missing image can be used
            # interchangeably in templates.  Strategy pattern ftw!
            return {
                'original': self.get_missing_image(),
                'caption': '',
                'is_missing': True}


@python_2_unicode_compatible
class ProductImage(models.Model):
    """
    An image of a product
    """
    product = models.ForeignKey('Product', related_name='images', verbose_name=_("Product"))
    original = models.ImageField(("Original"), upload_to=settings.DIO_IMAGE_FOLDER, max_length=255)
    caption = models.CharField(_("Caption"), max_length=200, blank=True)
    display_order = models.PositiveIntegerField(_("Display order"), default=0,)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)

    class Meta:
        ordering = ["display_order"]
        unique_together = ("product", "display_order")
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')

    def __str__(self):
        return u"Image of '%s'" % self.product

    def is_primary(self):
        return self.display_order == 0

    def delete(self, *args, **kwargs):
        """
        Always keep the display_order as consecutive integers. This avoids
        issue #855.
        """
        super(ProductImage, self).delete(*args, **kwargs)
        for idx, image in enumerate(self.product.images.all()):
            image.display_order = idx
            image.save()
