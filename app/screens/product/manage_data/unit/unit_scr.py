from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen

from app.components.components import db


class UnitScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.incoming_unit_id = None
        self.bind(on_pre_enter=self.display_unit_products)

    def display_unit_products(self, *args):
        rv_data = []
        for entry in db.get_unit_products(self.incoming_unit_id):
            item_data = {
                'prod_id': entry[0],
                'headline': entry[1],
                'itm_icon': 'dots-vertical',
                'img_path': entry[4],
            }

            rv_data.append(item_data)
        self.ids.rv_unit_products.data = rv_data
