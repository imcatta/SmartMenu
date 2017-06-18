from django.conf.urls import url

from . import views

urlpatterns = [
    # Django Suit custom admin view
    #url(r'^warehouse_summary/$', views.warehouse_summary_view, name='warehouse_summary'),
    url(r'^print-menu/(?P<menu_id>\d+)/$', views.get_menu_pdf, name='print_menu'),

]