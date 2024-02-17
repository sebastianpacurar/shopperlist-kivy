from kivymd.uix.screen import MDScreen

from app.components.components import MySnackbar, db


class AddProdScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_result = None
        # self.bind(on_pre_leave=self.clean_up)

    def perform_product_add(self):
        name = self.ids.product_name_text.text
        price = self.ids.product_price_text.text
        category = self.ids.product_category_text.text
        unit = self.ids.product_unit_text.text
        self.db_result = db.add_product(name, price, category, unit)
        MySnackbar(self.db_result)

    def get_query_result(self):
        return self.db_result

    def clean_up(self, *args):
        self.ids.product_name_text.text = ''
        self.ids.product_price_text.text = ''
        self.ids.product_category_text.text = ''
        self.ids.product_unit_text.text = ''
