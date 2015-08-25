# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import unittest
from django.test.client import Client

from src.apps.catalogue.models import Category

class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_add(self):
        Category.objects.create(name='test', is_active='True', description='test test test')

