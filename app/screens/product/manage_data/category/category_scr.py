from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen

from app.components.components import db


class CategoryScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.incoming_category_id = None
        self.bind(on_pre_enter=self.display_category_products)

    def display_category_products(self, *args):
        rv_data = []
        for entry in db.get_category_products(self.incoming_category_id):
            item_data = {
                'prod_id': entry[0],
                'headline': entry[1],
                'itm_icon': 'dots-vertical',
                'img_path': entry[4],
            }

            rv_data.append(item_data)
        self.ids.rv_category_products.data = rv_data
