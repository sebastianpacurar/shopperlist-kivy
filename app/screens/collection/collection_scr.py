from kivy.metrics import sp
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from app.components.components import db


class CollectionScreen(MDScreen):
    select_list = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all = 'all_collection_scr'
        self.mine = 'usr_collection_scr'

    def switch_scr(self, *args):
        sm = self.ids.collections_manager

        if args[0].text == 'My Lists':
            sm.transition.direction = 'right'
            sm.current = self.mine
            sm.get_screen(self.mine).display_user_collections()
        else:
            sm.transition.direction = 'left'
            sm.current = self.all
            sm.get_screen(self.all).display_all_collections()


class BaseCollectionScr(MDScreen):
    select_list = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_item_data(self, entry):
        list_id, user_id, name, stamp, creator = map(lambda x: str(x), entry)
        if not isinstance(stamp, str):
            stamp = entry[2].strftime("%Y-%m-%d %I:%M %p")

        return {
            'id': list_id,
            'text': name,
            'secondary_text': f'created by {creator}',
            'tertiary_text': stamp,
            'itm_icon': 'dots-vertical',
            'on_release': lambda x=list_id: self.select_list(x),
        }


class AllCollectionScr(BaseCollectionScr):
    def display_all_collections(self):
        rv_data = []
        for entry in db.get_all_shop_lists():
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)

        self.ids.rv_collection.data = rv_data


class UserCollectionScr(BaseCollectionScr):
    def display_user_collections(self):
        rv_data = []
        curr_user = db.get_active_user()[0]

        for entry in db.get_shop_lists_for_active_user(curr_user):
            item_data = self.create_item_data(entry)
            rv_data.append(item_data)

        self.ids.rv_usr_collection.data = rv_data
