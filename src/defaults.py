
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

DIO_IMAGE_FOLDER = 'images/products/%Y/%m/'
DIO_PROMOTION_FOLDER = 'images/promotions/'
DIO_DELETE_IMAGE_FILES = True

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 5,
    'MARGIN_PAGES_DISPLAYED': 3,
}