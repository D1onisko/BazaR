# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, BaseFormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from src.apps.catalogue.models import Product, Category
from src.apps.dashboard.forms import AddProductForm, UpdateProductForm


"""
Index page Dashboard
"""
class DashboardIndexView(TemplateView):
    template_name = 'apps/dashboard/profile.html'
    model = Product

    # Для вывода обьявлений определенного юзера
    def get(self, request, *args, **kwargs):
        kwargs['object_list'] = Product.objects.filter(user_name_id=request.user)
        return super(DashboardIndexView, self).get(request, *args, **kwargs)


"""
Create products in dashboard
"""
class ProductCreate(CreateView):
    template_name = 'apps/dashboard/add_product.html'
    model = Product
    form_class = AddProductForm

    def form_valid(self, form):
        form = AddProductForm(self.request.POST, self.request.FILES)
        add = form.save(commit=False)
        add.user_name_id = self.request.user
        add.save()
        return redirect('dashboard:dashboard_index')


"""
Update products in dashboard
"""
class ProductUpdate(UpdateView):
    template_name = 'apps/dashboard/update_product.html'
    model = Product
    form_class = UpdateProductForm



"""
Delete products in dashboard
"""
class ProductDelete(DeleteView):
    template_name = 'apps/dashboard/confirm_delete_product.html'
    model = Product
    success_url = reverse_lazy('dashboard:dashboard_index')

