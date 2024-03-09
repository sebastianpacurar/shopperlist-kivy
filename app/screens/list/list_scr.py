from kivy.properties import NumericProperty
from kivymd.app import MDApp

from kivymd.uix.screen import MDScreen

from app.components.components import db, BottomSheetQuantitySelector, \
    BottomSheetSelectionLineItem, RemoveProductFromListContent
from db import operations as ops


class ListScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_id = None
        self.main_app = MDApp.get_running_app()
        self.bind(on_pre_enter=self.init_data)

    def init_data(self, *args):
        rv_data = []
        for entry in db.get_shop_list(self.list_id):
            item_data = {
                'headline': entry[2],
                'supporting': f'{entry[7]} {entry[3]}',
                'tertiary': f'{round(entry[4] * entry[7], 2)} $',
                'img_path': entry[6],
                'checkbox_func': lambda item, item_checkbox: ops.perform_list_item_toggle(self.list_id, item, item_checkbox),
                'sheet_func': lambda name=entry[2], l_id=entry[0], p_id=entry[1], price=entry[4], quant=entry[7]: self.main_app.toggle_bottom(name, set_bottom_sheet_content(l_id, p_id, quant, price))
            }
            rv_data.append(item_data)

        self.ids.rv_list_content.data = rv_data


def set_bottom_sheet_content(list_id, product_id, quantity, price):
    main_app = MDApp.get_running_app()
    return [
        BottomSheetQuantitySelector(
            quantity_val=quantity,
            initial_quantity=quantity,
            unit_price=price,
            price_val=price * quantity,
            apply_btn_disabled=True,
            decrease_btn_disabled=False if quantity > 1 else True,
            apply_quantity_func=lambda x, y=list_id, z=product_id: (ops.perform_quantity_update(x, y, z), main_app.bottom.set_state('toggle'))
        ),
        BottomSheetSelectionLineItem(
            text='Remove from list',
            on_release=lambda _: (
                main_app.show_dialog(RemoveProductFromListContent(), list_id, product_id),
                main_app.bottom.set_state('toggle')),
        ),
    ]
