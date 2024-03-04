from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen

from app.components.components import db


class ListScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_id = None
        self.bind(on_pre_enter=self.init_data)

    def init_data(self, *args):
        rv_data = []
        for entry in db.get_shop_list(self.list_id):
            item_data = {
                'headline': entry[1],
                'img_path': entry[4],
                '_no_ripple_effect': True,
            }
            rv_data.append(item_data)

        self.ids.rv_list_content.data = rv_data
