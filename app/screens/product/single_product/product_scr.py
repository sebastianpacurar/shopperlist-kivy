from kivy.properties import ObjectProperty, DictProperty, StringProperty
from kivymd.uix.screen import MDScreen

from app.components.components import db


class ProdScreen(MDScreen):
    top_bar = ObjectProperty()
    img_path = StringProperty()
    data = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prod_id = None
        self.bind(on_pre_enter=self.init_data)

    def init_data(self, *args):
        res = db.get_product(self.prod_id)
        self.data = {
            'id': res[0],
            'name': res[1],
            'category': res[2],
            'unit': res[3],
            'price': res[4]
        }
        self.img_path = res[5]
        self.top_bar.title = self.data['name']
        self.ids.prod_id.secondary_text = str(self.data['id'])
        self.ids.prod_name.secondary_text = self.data['name']
        self.ids.prod_category.secondary_text = self.data['category']
        self.ids.prod_unit.secondary_text = self.data['unit']
        self.ids.prod_price.secondary_text = str(self.data['price'])
