from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from app.components.components import db
from db import operations as ops


class AddToListScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_id = None
        self.bind(on_enter=self.display_search_results)
        self.bind(on_pre_leave=self.clean_up)

    def display_search_results(self, *args):
        prefix_str = '' if not isinstance(args[0], MDTextField) else args[0].text
        rv_data = []

        for entry in db.filter_product_names_which_are_not_in_list(self.list_id, prefix_str):
            item_data = {
                'prod_id': entry[0],
                'headline': entry[1],
                'supporting': entry[2],
                'itm_icon': 'plus',
                'img_path': entry[4],
                'icon_func': lambda a, b=entry[0], c=entry[5], d=entry[3]: self.add_product_to_list(b, c, d)
            }

            rv_data.append(item_data)
        self.ids.rv_prod_list.data = rv_data

    def add_product_to_list(self, *args):
        ops.perform_add_prod_to_list(self.list_id, args[0], args[1], args[2]),
        self.display_search_results(self.ids.text_field)

    def clean_up(self, *args):
        self.ids.text_field.text = ''
