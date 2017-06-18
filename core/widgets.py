from django import forms
from core.models import Product

class TableCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'core/forms/widgets/table_checkbox_select.html'

    def get_context(self, name, value, attrs):
        context = super(TableCheckboxSelectMultiple, self).get_context(name, value, attrs)
        for item in context['widget']['optgroups']:
            id = item[1][0]['value']
            product = Product.objects.get(id=id)
            if product.kind == Product.PIATTO:
                item[1][0]['product'] = product

            
        return context

