from kivy.properties import NumericProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from app.components.components import db, MySnackbar
from app.utils import constants as const


class AddDataScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_result = None
        self.sm = None
        self.text_field = None
        self.search_field = None
        self.add_btn = None
        self.bind(on_kv_post=self.set_definitions)

    def set_definitions(self, *args):
        self.text_field = self.ids.text_field
        self.search_field = self.ids.search_field
        self.add_btn = self.ids.add_btn
        self.sm = self.ids.data_manager
        self.sm.get_screen(const.PROD_CATEGORY_SCR).display_all_categories()
        self.sm.get_screen(const.PROD_UNIT_SCR).display_all_units()

    def reset_fields(self):
        self.text_field.text = ''
        self.search_field.text = ''

    def switch_scr(self, *args):
        if self.sm.current != args[0]:
            match args[0]:
                case const.PROD_CATEGORY_SCR:
                    self.sm.transition.direction = 'right'
                    self.sm.current = const.PROD_CATEGORY_SCR
                    self.sm.get_screen(const.PROD_CATEGORY_SCR).display_all_categories()
                    self.reset_fields()
                case const.PROD_UNIT_SCR:
                    self.sm.transition.direction = 'left'
                    self.sm.current = const.PROD_UNIT_SCR
                    self.sm.get_screen(const.PROD_UNIT_SCR).display_all_units()
                    self.reset_fields()

    def add_entity(self):
        msg = 'Cannot be empty'
        if len(self.text_field.text) > 0:
            match self.sm.current:
                case const.PROD_CATEGORY_SCR:
                    msg = f'Cannot add {self.text_field.text} Category'
                    self.db_result = db.add_category(self.text_field.text)
                    if self.db_result:
                        msg = f'{self.text_field.text} Category added'
                        self.sm.get_screen(const.PROD_CATEGORY_SCR).display_all_categories()
                        self.reset_fields()
                case const.PROD_UNIT_SCR:
                    msg = f'Cannot add {self.text_field.text} Unit'
                    self.db_result = db.add_unit(self.text_field.text)
                    if self.db_result:
                        msg = f'{self.text_field.text} unit added'
                        self.sm.get_screen(const.PROD_UNIT_SCR).display_all_units()
                        self.reset_fields()

        MySnackbar(msg, self.db_result)

    def filter_displayed_list(self, *args):
        match self.sm.current:
            case const.PROD_CATEGORY_SCR:
                self.sm.get_screen(const.PROD_CATEGORY_SCR).display_search_results(args[0])
            case const.PROD_UNIT_SCR:
                self.sm.get_screen(const.PROD_UNIT_SCR).display_search_results(args[0])


class CategoryScr(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_all_categories(self, *args):
        rv_data = []
        for entry in db.get_product_categories():
            rv_data.append({
                'itm_id': str(entry[0]),
                'text': entry[1],
                'itm_icon': 'dots-vertical',
                'sheet_func': lambda name=entry[1], cat_id=entry[0]: MDApp.get_running_app().toggle_bottom(name, cat_id),

            })
        self.ids.rv_category.data = rv_data

    def display_search_results(self, widget):
        rv_data = []
        for entry in db.filter_categories(widget.text):
            rv_data.append({
                'itm_id': str(entry[0]),
                'text': entry[1],
                'itm_icon': 'dots-vertical',
                'sheet_func': lambda name=entry[1], cat_id=entry[0]: MDApp.get_running_app().toggle_bottom(name, cat_id),
            })
        self.ids.rv_category.data = rv_data


class UnitScr(MDScreen):
    def __init(self, **kwargs):
        super().__init__(**kwargs)

    def display_all_units(self, *args):
        rv_data = []
        for entry in db.get_product_units():
            rv_data.append({
                'itm_id': str(entry[0]),
                'text': entry[1],
                'itm_icon': 'dots-vertical',
                'sheet_func': lambda name=entry[1], cat_id=entry[0]: MDApp.get_running_app().toggle_bottom(name, cat_id),
            })
        self.ids.rv_unit.data = rv_data

    def display_search_results(self, widget):
        rv_data = []
        for entry in db.filter_units(widget.text):
            rv_data.append({
                'itm_id': str(entry[0]),
                'text': entry[1],
                'itm_icon': 'dots-vertical',
                'sheet_func': lambda name=entry[1], unit_id=entry[0]: MDApp.get_running_app().toggle_bottom(name, unit_id),
            })
        self.ids.rv_unit.data = rv_data
