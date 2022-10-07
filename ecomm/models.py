from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Наименование Категории')
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='URL')
    description = models.TextField(max_length=1000, blank=True, verbose_name='Описание')
    available = models.BooleanField(default=True, verbose_name='Опубликован')
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name='children', null=True, blank=True,
                            verbose_name='Родительская Категория')

    class MPTTMeta:
        order_insertion_by = ['name']
        # level_attr = 'mptt_level'

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} | - {self.parent}' if self.parent else self.name

    def get_absolute_url(self):
        return reverse('ecomm:category', args=[self.slug])


class ProductType(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Product Name')
    available = models.BooleanField(default=True, verbose_name='Опубликован')

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
    name = models.CharField(max_length=150, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=150, db_index=True, unique=True, verbose_name='URL')
    image = models.ImageField(upload_to="product/%Y", blank=True, verbose_name="Фото")
    description = models.TextField(max_length=1000, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.IntegerField(verbose_name='Количество', default=20)
    available = models.BooleanField(default=True, verbose_name='Опубликован')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    uploaded = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
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
            return '(Нет изображения)'

    image_img.short_description = 'Картинка'
    image_img.allow_tags = True

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
