from django.contrib import admin
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import *
from core.widgets import TableCheckboxSelectMultiple
from django.utils.timezone import now

@admin.register(Shelf, UoM)
class GenericModelAdmin(admin.ModelAdmin):
    pass

class MenuAdminForm(forms.ModelForm):
    class Meta:
        model = Menu
        widgets = {
            'courses': TableCheckboxSelectMultiple(),
        }
        fields = ('date', 'courses', 'note',)

@admin.register(Menu)
class MenuModelAdmin(admin.ModelAdmin):
    form = MenuAdminForm


class ProductRecipeChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return str(obj)

class RecipeModelForm(forms.ModelForm):
    product = ProductRecipeChoiceField(queryset=Product.objects.filter(kind__in=(Product.PIATTO, Product.PREPARATO)))

    class Meta:
        model = Recipe
        fields = ('product', 'note', 'time_needed',)

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0

@admin.register(Recipe)
class RecipeModelAdmin(admin.ModelAdmin):
    form = RecipeModelForm
    inlines = [
        IngredientInline,
    ]


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(ProductModelAdmin, self).get_queryset(request)
        return qs.filter()

@admin.register(Warehouse)
class WarehouseModelAdmin(admin.ModelAdmin):
    fields = ('product', ('quantity', ), 'shelf', 'date',)
    list_display = ('product', 'human_readable_quantity', 'date', 'shelf',)

    def suit_row_attributes(self, obj, request):
        if obj.product.kind == Product.PIATTO and ((now() - obj.date).days >= 1):
            return {'class' :'table-danger'}

