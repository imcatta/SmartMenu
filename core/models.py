from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.utils.html import format_html

class Shelf(models.Model):
    id = models.CharField(max_length=5, primary_key=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Scaffale'
        verbose_name_plural = 'Scaffali'


class UoM(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    readable_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{ self.readable_name } ({ self.name })'

    class Meta:
        verbose_name = 'Unità di misura'
        verbose_name_plural = 'Unità di misura'


class Product(models.Model):
    PIATTO = 1
    PREPARATO = 2
    MATERIA_PRIMA = 3
    KIND_CHOICES = ((PIATTO, 'Piatto'), (PREPARATO, 'Preparato'), (MATERIA_PRIMA, 'Materia prima'),)

    name = models.CharField(max_length=200, null=False, blank=False)
    uom = models.ForeignKey(UoM, on_delete=models.PROTECT, null=False, blank=False)
    kind = models.SmallIntegerField(choices=KIND_CHOICES, null=False, blank=False)
    is_complete_meal = models.NullBooleanField()

    def in_warehouse(self):
        return Warehouse.objects.filter(product=self).aggregate(models.Sum('quantity'))['quantity__sum'] or 0

    def can_be_produced(self):
        import math
        result = math.inf

        for ingredient in self.recipe.ingredient_set.all():
            print(ingredient)
            print(ingredient.product.in_warehouse())
            print(ingredient.qty_needed)

            result = min(result, ingredient.product.in_warehouse() / ingredient.qty_needed)
        
        return result

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name = 'Prodotto'
        verbose_name_plural = 'Prodotti'


class Recipe(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    note = models.TextField(null=True, blank=True)
    time_needed = models.IntegerField(verbose_name='Tempo necessario (in minuti)', default=15, validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'Ricetta'
        verbose_name_plural = 'Ricette'

class Ingredient(models.Model):
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, null=False, blank=False, on_delete=models.CASCADE)
    qty_needed = models.DecimalField(decimal_places=5, max_digits=15, null=False, blank=False,
                                     validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredienti'
        unique_together = ('product', 'recipe',)



class Warehouse(models.Model):
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.PROTECT)
    quantity = models.DecimalField(decimal_places=5, max_digits=15, null=False, blank=False,
                                   validators=[MinValueValidator(0)])
    shelf = models.ForeignKey(Shelf, null=False, blank=False, on_delete=models.PROTECT)
    date = models.DateTimeField(null=False, blank=False, default=now)

    def human_readable_quantity(self):
        return f'{ self.quantity } { self.product.uom.name }'

    class Meta:
        verbose_name = 'Magazzino'
        verbose_name_plural = 'Magazzino'


class Menu(models.Model):
    date = models.DateField(null=False, blank=False, verbose_name='Data')
    note = models.TextField(null=True, blank=True)
    courses = models.ManyToManyField(Product, verbose_name='Piatti')


    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu'

