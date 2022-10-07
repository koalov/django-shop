from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from ecomm.models import Product


class SearchProductView(ListView):
    template_name = 'search.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q', None)
        if query is not None:
            lookups = (Q(name__icontains=query) |
                       Q(description__icontains=query) |
                       Q(slug__icontains=query) |
                       Q(price__icontains=query))
            return Product.objects.filter(lookups).select_related('category')
        return Product.objects.none()