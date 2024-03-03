from kivy.properties import ObjectProperty, DictProperty, StringProperty, NumericProperty
from kivymd.uix.screen import MDScreen

from app.components.components import db


class ProdScreen(MDScreen):
    top_bar = ObjectProperty()
    top_bar_height = NumericProperty()
    img_path = StringProperty()
    data = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.incoming_prod_id = None
        self.id_val = None
        self.prod_name = None
        self.prod_category = None
        self.prod_unit = None
        self.prod_price = None
        self.bind(on_kv_post=self.set_definitions)
        self.bind(on_pre_enter=self.init_data)

    def set_definitions(self, *args):
        self.id_val = self.ids.prod_id
        self.prod_name = self.ids.prod_name
        self.prod_category = self.ids.prod_category
        self.prod_unit = self.ids.prod_unit
        self.prod_price = self.ids.prod_price

    def init_data(self, *args):
        res = db.get_product(self.incoming_prod_id)
        self.data = {
            'id': res[0],
            'name': res[1],
            'category': res[2],
            'unit': res[3],
            'price': res[4]
        }
        self.img_path = res[5]
        self.top_bar.title = self.data['name']
        self.id_val.secondary_text = str(self.data['id'])
        self.prod_name.secondary_text = self.data['name']
        self.prod_category.secondary_text = self.data['category']
        self.prod_unit.secondary_text = self.data['unit']
        self.prod_price.secondary_text = str(self.data['price'])
