from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from app.components.components import db, DropdownMenu


class ProdsScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_enter=self.display_search_results)
        self.bind(on_pre_leave=self.clean_up)

    def display_search_results(self, *args):
        prefix_str = '' if not isinstance(args[0], MDTextField) else args[0].text
        rv_data = []
        for entry in db.filter_product_names(prefix_str):
            item_data = {
                'prod_id': entry[0],
                'headline': entry[1],
                'supporting': entry[2],
                'itm_icon': 'dots-vertical',
                'img_path': entry[3],
                'icon_func': lambda x: DropdownMenu().drop(x)
            }

            rv_data.append(item_data)
        self.ids.rv_prod_list.data = rv_data

    def clean_up(self, *args):
        self.ids.text_field.text = ''
