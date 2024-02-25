from kivymd.uix.screen import MDScreen

from app.components.components import db
from app.utils import constants as const


class AddDataScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.category_btn = None
        self.unit_btn = None
        self.bind(on_kv_post=self.set_definitions)

    def set_definitions(self, *args):
        self.sm = self.ids.data_manager
        self.sm.get_screen(const.PROD_CATEGORY_SCR).display_all_categories()
        self.category_btn = self.ids.category_btn
        self.unit_btn = self.ids.unit_btn
        self.category_btn.disabled = True
        self.unit_btn.disabled = False
        self.category_btn.bold = False
        self.unit_btn.bold = True

    def switch_scr(self, *args):
        if args[0].text == 'Categories':
            self.sm.transition.direction = 'right'
            self.sm.current = const.PROD_CATEGORY_SCR
            self.sm.get_screen(const.PROD_CATEGORY_SCR).display_all_categories()
            self.category_btn.disabled = True
            self.unit_btn.disabled = False
            self.category_btn.bold = False
            self.unit_btn.bold = True
        else:
            self.sm.transition.direction = 'left'
            self.sm.current = const.PROD_UNIT_SCR
            self.sm.get_screen(const.PROD_UNIT_SCR).display_all_units()
            self.category_btn.disabled = False
            self.unit_btn.disabled = True
            self.category_btn.bold = True
            self.unit_btn.bold = False


class CategoryScr(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_all_categories(self, *args):
        rv_data = []
        for entry in db.get_product_categories():
            rv_data.append({'text': entry[1]})

        self.ids.rv_category.data = rv_data


class UnitScr(MDScreen):
    def __init(self, **kwargs):
        super().__init__(**kwargs)

    def display_all_units(self, *args):
        rv_data = []
        for entry in db.get_product_units():
            rv_data.append({'text': entry[1]})

        self.ids.rv_unit.data = rv_data
