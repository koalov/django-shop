from django.db import models
from django.urls import reverse
from colorfield.fields import ColorField


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(max_length=1000, blank=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Characteristics(models.Model):
    MAN = 'Man'
    WOMEN = 'Women'
    CHILD = 'Child'

    ch_sex = [
        (MAN, 'Мужской'),
        (WOMEN, 'Женский'),
        (CHILD, 'Ребёнок')
        ]

    COLOR_PALETTE = [
        ("#FFFFFF", "white",),
        ("#000000", "black",),
            ]

    color = models.CharField(max_length=150, db_index=True, verbose_name='Цвет')
    # slug = models.SlugField(max_length=100, db_index=True, verbose_name='URL')
    brand = models.CharField(max_length=150, db_index=True, verbose_name='Бренд')
    type = models.CharField(max_length=150, db_index=True, verbose_name='Тип')
    size = models.CharField(max_length=150, db_index=True, verbose_name='Размер')
    material = models.CharField(max_length=150, db_index=True, verbose_name='Материал')
    consist = models.TextField(max_length=1000, blank=True, verbose_name='Состав')
    country = models.CharField(max_length=150, db_index=True, verbose_name='Страна Производитель')
    sex = models.CharField(max_length=10, choices=ch_sex, verbose_name='Пол')
    # created = models.DateTimeField(auto_now_add=True)
    # uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Характеристики'
        verbose_name_plural = 'Характеристики'

    # def get_absolute_url(self):
    #     return reverse('product', kwargs={'product': self.pk})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, db_index=True)
    image = models.ImageField(upload_to=f"product/%Y", blank=True)
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(verbose_name='Количество', default=20)
    available = models.BooleanField(default=True)
    characteristics = models.ManyToManyField(Characteristics) #related_name='characteristics'
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'prod_slug': self.slug})

    def image_img(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return '(Нет изображения)'

    image_img.short_description = 'Картинка'
    image_img.allow_tags = True


