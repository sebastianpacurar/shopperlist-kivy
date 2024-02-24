from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen

from app.components.components import db


class AddDataScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category = 'category_scr'
        self.unit = 'unit_scr'
        self.bind(on_pre_enter=self.init_on_category)

    def init_on_category(self, *args):
        category_btn = self.ids.category_btn
        unit_btn = self.ids.unit_btn
        category_btn.disabled = True
        unit_btn.disabled = False
        category_btn.bold = False
        unit_btn.bold = True
        sm = self.ids.data_manager
        sm.current = self.category
        sm.get_screen(self.category).display_all_categories()

    def switch_scr(self, *args):
        category_btn = self.ids.category_btn
        unit_btn = self.ids.unit_btn
        sm = self.ids.data_manager

        if args[0].text == 'Categories':
            sm.transition.direction = 'right'
            sm.current = self.category
            sm.get_screen(self.category).display_all_categories()
            category_btn.disabled = True
            unit_btn.disabled = False
            category_btn.bold = False
            unit_btn.bold = True
        else:
            sm.transition.direction = 'left'
            sm.current = self.unit
            sm.get_screen(self.unit).display_all_units()
            category_btn.disabled = False
            unit_btn.disabled = True
            category_btn.bold = True
            unit_btn.bold = False


class CategoryScr(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_kv_post=self.display_all_categories)

    def display_all_categories(self, *args):
        rv_data = []
        for entry in db.get_product_categories():
            rv_data.append({'text': entry[1]})

        self.ids.rv_category.data = rv_data


class UnitScr(MDScreen):
    def __init(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_kv_post=self.display_all_units)

    def display_all_units(self, *args):
        rv_data = []
        for entry in db.get_product_units():
            rv_data.append({'text': entry[1]})

        self.ids.rv_unit.data = rv_data
