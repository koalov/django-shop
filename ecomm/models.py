from django.db import models
from django.db.models import Q
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class ProductQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(available=True)

    def featured(self):
        return self.filter(featured=True, available=True)

    def search(self, query):
        lookups = (Q(name__icontains=query) |
                   Q(description__icontains=query) |
                   Q(slug__icontains=query) |
                   Q(price__icontains=query) |
                   Q(tag__name__icontains=query))
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):

    def get_query_set(self):
        return ProductQuerySet(self.model, using=self._db)

    def active_all(self):
        return self.get_query_set().active()

    def featured(self):
        return self.get_query_set().featured()

    def get_by_id(self, pk):
        qs = self.get_queryset().filter(pk=pk)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_query_set().search(query)


class Category(MPTTModel):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Category name')
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='URL')
    description = models.TextField(max_length=1000, blank=True,
                                   verbose_name='Description')
    available = models.BooleanField(default=True, verbose_name='Published')
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name='children', null=True, blank=True,
                            verbose_name='Parent category')
    image = models.ImageField(upload_to="category/%Y", null=True, blank=True,
                              verbose_name="Photo")

    class MPTTMeta:
        order_insertion_by = ['name']
        # level_attr = 'mptt_level'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name} | - {self.parent}' if self.parent else self.name

    def get_absolute_url(self):
        return reverse('ecomm:category', args=[self.slug])


class ProductType(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Product Name')
    available = models.BooleanField(default=True, verbose_name='Published')

    class Meta:
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(max_length=150, db_index=True, verbose_name='Name')

    class Meta:
        verbose_name = 'Product Specification'
        verbose_name_plural = 'Product Specifications'

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    name = models.CharField(max_length=150, db_index=True, verbose_name='Name')
    slug = models.SlugField(max_length=150, db_index=True, unique=True, verbose_name='URL')
    image = models.ImageField(upload_to="product/%Y", blank=True, verbose_name="Photo")
    description = models.TextField(max_length=1000, blank=True,
                                   verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    quantity = models.IntegerField(verbose_name='Quantity', default=20)
    available = models.BooleanField(default=True, verbose_name='Published')
    featured = models.BooleanField(default=False, verbose_name='Featured')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Time created at')
    uploaded = models.DateTimeField(auto_now=True, verbose_name='Time updated at')
    objects = ProductManager()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ecomm:product_detail', args=[self.id, self.slug])

    def image_img(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return '(No image)'

    image_img.short_description = 'Image'
    image_img.allow_tags = True

    image_in_product = ImageSpecField(source='image',
                                      processors=[ResizeToFill(636, 636)],
                                      format='JPEG',
                                      options={'quality': 60})

    image_in_category = ImageSpecField(source='image',
                                       processors=[ResizeToFill(304, 456)],
                                       format='JPEG',
                                       options={'quality': 60})

    image_in_main = ImageSpecField(source='image',
                                   processors=[ResizeToFill(95, 150)],
                                   format='JPEG',
                                   options={'quality': 60})

    def get_short_description(self):
        if len(self.description) < 40:
            return self.description
        return self.description[:40]

    def get_short_name(self):
        if len(self.name) < 40:
            return self.name
        return self.name[:40]


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(max_length=255, verbose_name='Value')

    class Meta:
        verbose_name = 'Product Specification Value'
        verbose_name_plural = 'Product Specifications Values'

    def __str__(self):
        return self.value
