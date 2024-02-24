from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from app.components.components import db


class CollectionScreen(MDScreen):
    select_list = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all = 'all_collection_scr'
        self.mine = 'usr_collection_scr'
        self.bind(on_pre_enter=self.init_on_my_lists)

    def init_on_my_lists(self, *args):
        my_lists_btn = self.ids.my_lists_btn
        all_lists_btn = self.ids.all_lists_btn
        my_lists_btn.disabled = True
        all_lists_btn.disabled = False
        my_lists_btn.bold = False
        all_lists_btn.bold = True
        sm = self.ids.collections_manager
        sm.current = self.mine
        sm.get_screen(self.mine).display_user_collections()

    def switch_scr(self, *args):
        my_lists_btn = self.ids.my_lists_btn
        all_lists_btn = self.ids.all_lists_btn
        sm = self.ids.collections_manager

        if args[0].text == 'My Lists':
            sm.transition.direction = 'right'
            sm.current = self.mine
            sm.get_screen(self.mine).display_user_collections()
            my_lists_btn.disabled = True
            all_lists_btn.disabled = False
            my_lists_btn.bold = False
            all_lists_btn.bold = True
        else:
            sm.transition.direction = 'left'
            sm.current = self.all
            sm.get_screen(self.all).display_all_collections()
            my_lists_btn.disabled = False
            all_lists_btn.disabled = True
            my_lists_btn.bold = True
            all_lists_btn.bold = False


class BaseCollectionScr(MDScreen):
    select_list = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_item_data(self, entry):
        entry = [str(x) for x in entry]
        stamp = entry[3]
        if not isinstance(stamp, str):
            stamp = entry[2].strftime("%Y-%m-%d %I:%M %p")
        if len(entry) == 5:
            item_data = {
                'id': entry[0],
                'text': entry[2],
                'secondary_text': f'created by {entry[4]}',
                'tertiary_text': stamp,
                'itm_icon': 'dots-vertical',
                'on_release': lambda x=entry[0]: self.select_list(x),
            }
        else:
            item_data = {
                'id': entry[0],
                'text': entry[2],
                'secondary_text': stamp,
                'itm_icon': 'dots-vertical',
                'on_release': lambda x=entry[0]: self.select_list(x),
            }
        return item_data


class AllCollectionScr(BaseCollectionScr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_kv_post=self.display_all_collections)

    def display_all_collections(self, *args):
        rv_data = []
        for entry in db.get_all_shop_lists():
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)

        self.ids.rv_collection.data = rv_data


class UserCollectionScr(BaseCollectionScr):
    def __init(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_kv_post=self.display_user_collections)

    def display_user_collections(self, *args):
        rv_data = []
        curr_user = db.get_active_user()[0]

        for entry in db.get_shop_lists_for_active_user(curr_user):
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)

        self.ids.rv_usr_collection.data = rv_data
