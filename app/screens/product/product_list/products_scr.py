from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from app.components.components import db, DropdownMenu, BottomSheetItemDescription, BottomSheetQuantitySelector, BottomSheetSelectionLineItem, RemoveProductFromListContent


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
                # 'itm_icon': 'dots-vertical',
                'img_path': entry[3],
                'icon_func': lambda x: DropdownMenu().drop(x)
            }

            rv_data.append(item_data)
        self.ids.rv_prod_list.data = rv_data

    def clean_up(self, *args):
        self.ids.text_field.text = ''


# TODO: continue from here to switch to bottom sheet viewing
def set_bottom_sheet_content(list_id, product_id, unit, price, category, img, quantity):
    main_app = MDApp.get_running_app()
    return [
        BottomSheetItemDescription(
            img_path=img,
            price=f'{round(price, 2)}$ / {unit}',
            category=category,
        ),
        BottomSheetSelectionLineItem(
            text='Remove from list',
            on_release=lambda _: (
                main_app.show_dialog(RemoveProductFromListContent(), list_id, product_id),
                main_app.bottom.set_state('toggle')
            ),
        ),
    ]
