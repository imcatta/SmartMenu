from django.db import transaction
from core.models import UoM, Shelf, Recipe, Product, Warehouse, Ingredient
from django.utils.timezone import now
from datetime import timedelta

with transaction.atomic():
    
    # User
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(username='admin', password='admin', email='')
    
    Warehouse.objects.all().delete()
    Recipe.objects.all().delete()
    Product.objects.all().delete()
    Shelf.objects.all().delete()
    UoM.objects.all().delete()
    Ingredient.objects.all().delete()

    # UoM
    uom_kg = UoM.objects.create(name='Kg', readable_name='Chilogrammo')
    uom_prz = UoM.objects.create(name='Prz', readable_name='Porzione')
    uom_l= UoM.objects.create(name='L', readable_name='Litro')
    uom_g = UoM.objects.create(name='g', readable_name='Grammo')

    # Shelf
    shelf_a1 = Shelf.objects.create(id='A1')
    shelf_a2 = Shelf.objects.create(id='A2')
    shelf_a3 = Shelf.objects.create(id='A3')
    shelf_b1 = Shelf.objects.create(id='B1')
    shelf_b2 = Shelf.objects.create(id='B2')
    shelf_c1 = Shelf.objects.create(id='C1')


    # Product
    p_riso = Product.objects.create(name='Riso', uom=uom_kg, kind=Product.MATERIA_PRIMA)
    p_pasta =Product.objects.create(name='Pasta', uom=uom_kg, kind=Product.MATERIA_PRIMA)
    p_salsa_pomodoro = Product.objects.create(name='Salsa di pomodoro', uom=uom_l, kind=Product.MATERIA_PRIMA)
    p_zafferano = Product.objects.create(name='Zafferano', uom=uom_g, kind=Product.MATERIA_PRIMA)
    p_sale = Product.objects.create(name='Sale', uom=uom_g, kind=Product.MATERIA_PRIMA)
    p_olio_oliva = Product.objects.create(name='Olio di oliva', uom=uom_l, kind=Product.MATERIA_PRIMA)
    p_farina = Product.objects.create(name='Farina 00', uom=uom_kg, kind=Product.MATERIA_PRIMA)
    p_impasto_pizza = Product.objects.create(name='Impasto pizza', uom=uom_kg, kind=Product.PREPARATO)
    p_pizza_margherita = Product.objects.create(name='Pizza margherita', uom=uom_prz, kind=Product.PIATTO, is_complete_meal=True)
    p_pizza_quattro_stagioni =Product.objects.create(name='Pizza quattro stagioni', uom=uom_prz, kind=Product.PIATTO, is_complete_meal=True)
    p_pizza_americana = Product.objects.create(name='Pizza americana', uom=uom_prz, kind=Product.PIATTO, is_complete_meal=True)
    p_mozzarella = Product.objects.create(name='Mozzarella', uom=uom_kg, kind=Product.MATERIA_PRIMA)
    p_patatine = Product.objects.create(name='Patatine', uom=uom_kg, kind=Product.MATERIA_PRIMA)
    p_basilico = Product.objects.create(name='Basilico', uom=uom_g, kind=Product.MATERIA_PRIMA)
    p_verdure = Product.objects.create(name='''Verdure sott'olio''', uom=uom_kg, kind=Product.MATERIA_PRIMA)
    p_pasta_pomodoro = Product.objects.create(name='Pasta al pomodoro', uom=uom_prz, kind=Product.PIATTO)
    p_riso_zafferano = Product.objects.create(name='Riso allo zafferano', uom=uom_prz, kind=Product.PIATTO)
    p_pasta_ragu = Product.objects.create(name='Pasta al ragù', uom=uom_prz, kind=Product.PIATTO)
    p_carne_trita = Product.objects.create(name='Carne trita', uom=uom_prz, kind=Product.MATERIA_PRIMA)
    p_ragu = Product.objects.create(name='Ragù', uom=uom_g, kind=Product.PREPARATO)
    p_lasagne = Product.objects.create(name='Lasagne', uom=uom_prz, kind=Product.PIATTO)
    p_pasta_ragu = Product.objects.create(name='Pasta al ragù', uom=uom_prz, kind=Product.PIATTO)
    p_besciamella = Product.objects.create(name='Besciamella', uom=uom_g, kind=Product.MATERIA_PRIMA)
    p_pasta_sfoglia = Product.objects.create(name='Pasta sfoglia', uom=uom_kg, kind=Product.MATERIA_PRIMA)


    # Warehouse
    from random import randint
    for p in Product.objects.filter(kind__in=(Product.MATERIA_PRIMA, Product.PREPARATO,)):
        Warehouse.objects.create(product=p, quantity=randint(0, 100), shelf=Shelf.objects.order_by('?').first())

    for p in Product.objects.filter(kind=Product.PIATTO):
        if randint(0, 1):
            date = now() if randint(0, 1) else now() - timedelta(days=2)
            shelf = Shelf.objects.order_by('?').first()
            Warehouse.objects.create(product=p, quantity=randint(0, 20), shelf=shelf, date=date)

    
    # Warehouse.objects.create(product=p_riso, quantity=20, shelf=shelf_a1)
    # Warehouse.objects.create(product=p_pasta, quantity=30, shelf=shelf_a1)
    # Warehouse.objects.create(product=p_salsa_pomodoro, quantity=15, shelf=shelf_b1)
    # Warehouse.objects.create(product=p_impasto_pizza, quantity=25, shelf=shelf_c1)
    # Warehouse.objects.create(product=p_sale, quantity=1500, shelf=shelf_b2)
    # Warehouse.objects.create(product=p_olio_oliva, quantity=30, shelf=shelf_b2)
    # Warehouse.objects.create(product=p_mozzarella, quantity=15, shelf=shelf_b2)
    # Warehouse.objects.create(product=p_basilico, quantity=15, shelf=shelf_b2)

    # Recipe

    r_pizza_margherita = Recipe.objects.create(product=p_pizza_margherita, time_needed=10)
    r_pizza_americana = Recipe.objects.create(product=p_pizza_americana, time_needed=12)
    r_pizza_quattro_stagioni = Recipe.objects.create(product=p_pizza_quattro_stagioni, time_needed=12)
    r_pasta_pomodoro = Recipe.objects.create(product=p_pasta_pomodoro, time_needed=10)
    r_riso_zafferano = Recipe.objects.create(product=p_riso_zafferano, time_needed=15)
    r_pasta_ragu =  Recipe.objects.create(product=p_pasta_ragu, time_needed=10)
    r_lasagne = Recipe.objects.create(product=p_lasagne, time_needed=60)

    # Ingredienti
    #Pizza margherita
    Ingredient.objects.create(recipe=r_pizza_margherita, product=p_impasto_pizza, qty_needed=0.2)
    Ingredient.objects.create(recipe=r_pizza_margherita, product=p_mozzarella, qty_needed=0.3)
    Ingredient.objects.create(recipe=r_pizza_margherita, product=p_sale, qty_needed=20)
    Ingredient.objects.create(recipe=r_pizza_margherita, product=p_basilico, qty_needed=4)
    #Pizza americana
    Ingredient.objects.create(recipe=r_pizza_americana, product=p_impasto_pizza, qty_needed=0.2)
    Ingredient.objects.create(recipe=r_pizza_americana, product=p_mozzarella, qty_needed=0.3)
    Ingredient.objects.create(recipe=r_pizza_americana, product=p_sale, qty_needed=20)
    Ingredient.objects.create(recipe=r_pizza_americana, product=p_patatine, qty_needed=0.20)
    #Pizza quattro stagiono
    Ingredient.objects.create(recipe=r_pizza_quattro_stagioni, product=p_impasto_pizza, qty_needed=0.2)
    Ingredient.objects.create(recipe=r_pizza_quattro_stagioni, product=p_mozzarella, qty_needed=0.3)
    Ingredient.objects.create(recipe=r_pizza_quattro_stagioni, product=p_sale, qty_needed=20)
    Ingredient.objects.create(recipe=r_pizza_quattro_stagioni, product=p_verdure, qty_needed=0.15)
    #Riso allo zafferano
    Ingredient.objects.create(recipe=r_riso_zafferano, product=p_riso, qty_needed=0.08)
    Ingredient.objects.create(recipe=r_pasta_pomodoro, product=p_zafferano, qty_needed=2)
    #Pasta al ragu
    Ingredient.objects.create(recipe=r_pasta_ragu, product=p_pasta, qty_needed=0.08)
    Ingredient.objects.create(recipe=r_pasta_ragu, product=p_ragu, qty_needed=30)
    #Pasta al pomodoro
    Ingredient.objects.create(recipe=r_pasta_pomodoro, product=p_pasta, qty_needed=0.08)
    Ingredient.objects.create(recipe=r_pasta_pomodoro, product=p_basilico, qty_needed=4)
    Ingredient.objects.create(recipe=r_pasta_pomodoro, product=p_salsa_pomodoro, qty_needed=0.01)
    #Lasagne
    Ingredient.objects.create(recipe=r_lasagne, product=p_pasta_sfoglia, qty_needed=0.08)
    Ingredient.objects.create(recipe=r_lasagne, product=p_ragu, qty_needed=0.3)
    Ingredient.objects.create(recipe=r_lasagne, product=p_besciamella, qty_needed=0.01)



    

