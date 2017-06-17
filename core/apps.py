from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class CoreConfig(DjangoSuitConfig):
    name = 'core'

    menu = (
        ParentItem('Content', children=[
            #ChildItem(model='demo.country'),
            #ChildItem(model='demo.continent'),
            #ChildItem(model='demo.showcase'),
            ChildItem('Custom view', url='warehouse_summary'),
        ], icon='fa fa-leaf'),
       
        ParentItem('Right Side Menu', children=[
            ChildItem('Password change', url='admin:password_change'),
        ], align_right=True, icon='fa fa-cog'),
    )

    def ready(self):
        super(CoreConfig, self).ready()
