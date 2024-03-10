from kivy.properties import ObjectProperty, DictProperty, StringProperty, NumericProperty
from kivymd.uix.screen import MDScreen

from app.components.components import db


class ProdScreen(MDScreen):
    top_bar = ObjectProperty()
    top_bar_height = NumericProperty()
    img_path = StringProperty()
    prod_id = StringProperty()
    prod_name = StringProperty()
    prod_category = StringProperty()
    prod_unit = StringProperty()
    prod_price = StringProperty()
    data = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.incoming_prod_id = None
        self.bind(on_pre_enter=self.init_data)

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
        self.prod_id = str(self.data['id'])
        self.prod_name = self.data['name']
        self.prod_category = self.data['category']
        self.prod_unit = self.data['unit']
        self.prod_price = str(self.data['price'])
