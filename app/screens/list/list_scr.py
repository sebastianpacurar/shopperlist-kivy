from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from app.components.components import db, BottomSheetQuantitySelector, \
    BottomSheetSelectionLineItem, RemoveProductFromListContent, BottomSheetItemDescription, \
    RvItemOneLine, RvItemTwoLine, RvItemThreeLine
from db import operations as ops
from app.utils import constants as const


class ListScreen(MDScreen):
    top_bar_height = NumericProperty()
    count_all = NumericProperty()
    count_checked = NumericProperty()
    count_unchecked = NumericProperty()
    category_filter_message = StringProperty('All Categories')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_id = None
        self.sm = None
        self.tabs = None
        self.price_box = None
        self.qty_box = None
        self.rv_all = None
        self.rv_in = None
        self.rv_out = None
        self.panel = None
        self.panel_chevron = None
        self.checkbox_setup = {'Price': False, 'Qty': False}
        self.prev_checkbox_active = None
        self.initial_setup = False
        self.filtered_category = 'All Categories'
        self.main_app = MDApp.get_running_app()
        self.bind(on_pre_enter=self.init_data)
        self.bind(on_pre_leave=self.clean_up)

    def clear_filters_txt(self, *args):
        self.ids.filter_category_txt.text = ''
        self.ids.filter_category_txt.filter_suffix = self.filtered_category

    def reset_filters(self, *args):
        if self.filtered_category != 'All Categories':
            self.clear_filters_txt()
            self.update_filtered_category('All Categories')
            self.refresh_data()

    def close_expandable(self):
        if self.panel.is_open:
            self.tap_expansion_chevron(self.panel, self.panel_chevron)

    def clean_up(self, *args):
        self.reset_filters()
        self.close_expandable()

    def update_filtered_category(self, value):
        self.filtered_category = value
        self.category_filter_message = value

    def switch_to_first_tab(self, dt):
        all_items_tab = self.tabs.get_tabs_list()[-1]
        self.tabs.switch_tab(instance=all_items_tab)

    def set_definitions(self, *args):
        self.sm = self.ids.list_view_manager
        self.tabs = self.ids.tabs
        self.price_box = self.ids.price_box
        self.qty_box = self.ids.qty_box
        self.rv_all = self.ids.all_prods_scr.ids.rv_all_prods_list
        self.rv_in = self.ids.in_prods_scr.ids.rv_in_prods_list
        self.rv_out = self.ids.out_prods_scr.ids.rv_out_prods_list
        self.panel = self.ids.panel
        self.panel_chevron = self.ids.chevron

    def init_data(self, *args):
        self.set_definitions()
        self.set_prod_count()
        self.sm.get_screen(self.sm.current).display_products(self.list_id, self.filtered_category)
        if not self.initial_setup:
            Clock.schedule_once(self.switch_to_first_tab, .001)
            self.initial_setup = True

    def set_prod_count(self):
        if self.filtered_category == 'All Categories':
            self.count_all = db.get_shop_list_all_count(self.list_id)
            self.count_checked = db.get_shop_list_checked_unchecked_count(self.list_id, 1)
            self.count_unchecked = db.get_shop_list_checked_unchecked_count(self.list_id, 0)
        else:
            self.count_all = db.get_filtered_list_by_category_count(self.list_id, self.filtered_category)
            self.count_checked = db.get_filtered_list_checked_unchecked_by_category_count(self.list_id, 1, self.filtered_category)
            self.count_unchecked = db.get_filtered_list_checked_unchecked_by_category_count(self.list_id, 0, self.filtered_category)

    def switch_scr(self, *args):
        tab_item = args[1]
        curr = const.ALL_PRODS_LIST_SCR
        val = tab_item.children[0].text.split(' ')[0]
        match val:
            case 'In':
                curr = const.IN_PRODS_LIST_SCR
            case 'Out':
                curr = const.OUT_PRODS_LIST_SCR
        if self.sm.current != curr:
            match curr:
                case const.ALL_PRODS_LIST_SCR:
                    self.sm.transition.direction = 'right'
                    self.sm.current = const.ALL_PRODS_LIST_SCR
                    self.sm.get_screen(const.ALL_PRODS_LIST_SCR).display_products(self.list_id, self.filtered_category)
                case const.IN_PRODS_LIST_SCR:
                    self.sm.transition.direction = 'right' if self.sm.current == const.OUT_PRODS_LIST_SCR else 'left'
                    self.sm.current = const.IN_PRODS_LIST_SCR
                    self.sm.get_screen(const.IN_PRODS_LIST_SCR).display_products(self.list_id, self.filtered_category)
                case const.OUT_PRODS_LIST_SCR:
                    self.sm.transition.direction = 'left'
                    self.sm.current = const.OUT_PRODS_LIST_SCR
                    self.sm.get_screen(const.OUT_PRODS_LIST_SCR).display_products(self.list_id, self.filtered_category)

    def refresh_data(self, *args):
        self.sm.get_screen(const.ALL_PRODS_LIST_SCR).display_products(self.list_id, self.filtered_category)
        self.sm.get_screen(const.IN_PRODS_LIST_SCR).display_products(self.list_id, self.filtered_category)
        self.sm.get_screen(const.OUT_PRODS_LIST_SCR).display_products(self.list_id, self.filtered_category)
        self.set_prod_count()

    def set_checkbox_setup(self, *args):
        self.checkbox_setup[args[0].text] = args[1].active
        self.set_list_layout()

    def set_list_layout(self):
        checkbox_price = self.checkbox_setup.get('Price', False)
        checkbox_qty = self.checkbox_setup.get('Qty', False)
        viewclass_map = {
            (True, True): RvItemThreeLine,
            (True, False): RvItemTwoLine,
            (False, True): RvItemTwoLine,
            (False, False): RvItemOneLine
        }
        if checkbox_price and not checkbox_qty:
            self.prev_checkbox_active = 'Price'
        elif not checkbox_price and checkbox_qty:
            self.prev_checkbox_active = 'Qty'

        viewclass = viewclass_map.get((checkbox_price, checkbox_qty), RvItemOneLine)
        self.rv_all.viewclass = viewclass
        self.rv_in.viewclass = viewclass
        self.rv_out.viewclass = viewclass

        self.refresh_data()

    def tap_expansion_chevron(self, panel, chevron):
        panel.open() if not panel.is_open else panel.close()
        panel.set_chevron_down(chevron) if not panel.is_open else panel.set_chevron_up(chevron)


class BaseListViewScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_scr = None
        self.main_app = MDApp.get_running_app()
        Clock.schedule_once(self.set_list_scr)

    def set_list_scr(self, *args):
        self.list_scr = self.main_app.sm.get_screen(const.LIST_SCR)

    def refresh_screens(self):
        self.main_app.sm.get_screen(const.LIST_SCR).refresh_data()

    def create_item_data(self, entry):
        supporting_txt, tertiary_txt = '', ''
        list_scr = self.main_app.sm.get_screen(const.LIST_SCR)
        price_active = list_scr.checkbox_setup.get('Price', False)
        qty_active = list_scr.checkbox_setup.get('Qty', False)

        price_val = f'{round(entry[4] * entry[7], 2)} $'
        qty_val = f'{entry[7]} {entry[3]}'

        if price_active and not qty_active:
            supporting_txt, tertiary_txt = price_val, ''
        elif qty_active and not price_active:
            supporting_txt, tertiary_txt = qty_val, ''
        elif list_scr.prev_checkbox_active == 'Price':
            supporting_txt, tertiary_txt = price_val, qty_val
        elif list_scr.prev_checkbox_active == 'Qty':
            supporting_txt, tertiary_txt = qty_val, price_val

        item_data = {
            'headline': entry[2],
            'supporting': supporting_txt,
            'tertiary': tertiary_txt,
            'itm_icon': 'checkbox-marked' if bool(entry[8]) else 'checkbox-blank-outline',
            'checkbox_func': lambda l_id=entry[0], p_id=entry[1], val=entry[8]: (ops.perform_list_item_toggle(l_id, p_id, not val), self.refresh_screens()),
            'sheet_func': lambda name=entry[2], l_id=entry[0], p_id=entry[1], unit=entry[3], price=entry[4], category=entry[5], img=entry[6], quant=entry[7]: (
                self.main_app.toggle_bottom(name, set_bottom_sheet_content(l_id, p_id, unit, price, category, img, quant))
            )
        }
        return item_data


class AllProdsScreen(BaseListViewScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_products(self, *args):
        rv_data = []
        if args[1] != 'All Categories':
            entries = db.get_shop_list_filtered(list_id=args[0], category_name=args[1])
        else:
            entries = db.get_shop_list(list_id=args[0])

        for entry in entries:
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)

        self.ids.rv_all_prods_list.data = rv_data


class InProdsScreen(BaseListViewScreen):
    def display_products(self, *args):
        rv_data = []
        if args[1] != 'All Categories':
            entries = db.get_shop_list_checked_unchecked_filtered(list_id=args[0], checked=1, category_name=args[1])
        else:
            entries = db.get_shop_list_checked_unchecked(list_id=args[0], checked=1)

        for entry in entries:
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)

        self.ids.rv_in_prods_list.data = rv_data


class OutProdsScreen(BaseListViewScreen):
    def display_products(self, *args):
        rv_data = []
        if args[1] != 'All Categories':
            entries = db.get_shop_list_checked_unchecked_filtered(list_id=args[0], checked=0, category_name=args[1])
        else:
            entries = db.get_shop_list_checked_unchecked(list_id=args[0], checked=0)

        for entry in entries:
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)

        self.ids.rv_out_prods_list.data = rv_data


def set_bottom_sheet_content(list_id, product_id, unit, price, category, img, quantity):
    main_app = MDApp.get_running_app()
    return [
        BottomSheetItemDescription(
            img_path=img,
            price=f'{round(price, 2)}$ / {unit}',
            category=category,
        ),
        BottomSheetQuantitySelector(
            quantity_val=quantity,
            initial_quantity=quantity,
            unit_price=price,
            price_val=price * quantity,
            apply_btn_disabled=True,
            decrease_btn_disabled=False if quantity > 1 else True,
            apply_quantity_func=lambda x, y=list_id, z=product_id: (
                ops.perform_quantity_update(x, y, z),
                main_app.sm.get_screen(const.LIST_SCR).refresh_data(),
                main_app.bottom.set_state('toggle')
            )
        ),
        BottomSheetSelectionLineItem(
            text='Remove from list',
            on_release=lambda _: (
                main_app.show_dialog(RemoveProductFromListContent(), list_id, product_id),
                main_app.bottom.set_state('toggle')
            ),
        ),
    ]
