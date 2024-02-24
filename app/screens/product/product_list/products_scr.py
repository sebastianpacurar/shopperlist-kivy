from kivymd.uix.screen import MDScreen

from app.components.components import db, DropdownHandler


class ProdsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drop = DropdownHandler()
        self.bind(on_pre_enter=self.display_products)
        self.bind(on_pre_leave=self.clean_up)

    def display_products(self, *args):
        rv_data = []
        for entry in db.get_all_products():
            item_data = {
                'prod_id': entry[0],
                'text': entry[1],
                'secondary_text': entry[2],
                'itm_icon': 'dots-vertical',
                'img_path': entry[3],
                'icon_func': lambda x: self.drop.toggle(x)
            }

            rv_data.append(item_data)
        self.ids.rv_prod_list.data = rv_data

    def display_search_results(self, widget):
        rv_data = []
        for entry in db.filter_product_names(widget.text):
            item_data = {
                'prod_id': entry[0],
                'text': entry[1],
                'secondary_text': entry[2],
                'itm_icon': 'dots-vertical',
                'img_path': entry[3],
                'icon_func': lambda x: self.drop.toggle(x)
            }

            rv_data.append(item_data)
        self.ids.rv_prod_list.data = rv_data

    def clean_up(self, *args):
        self.ids.text_field.text = ''
