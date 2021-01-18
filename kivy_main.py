from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, ObjectProperty, \
        NumericProperty, BooleanProperty, AliasProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

import kivy
kivy.require('1.8.0')

class BookItem(BoxLayout):
    book_title = StringProperty()

class BottomMenu(BoxLayout):
    book_title = StringProperty()

class ShelfItem(BoxLayout):
    shelf_title = StringProperty()

class RootWidget(BoxLayout):
    container = ObjectProperty(None)
    container2 = ObjectProperty(None)

class BookWidget(BoxLayout):
    data = ListProperty()
    def _get_data_for_widgets(self):
        return self.data
    data_for_widgets = AliasProperty(_get_data_for_widgets, bind=['data'])

class ShelfWidget(BoxLayout):
    data = ListProperty()
    def _get_data_for_widgets(self):
        return self.data
    data_for_widgets = AliasProperty(_get_data_for_widgets, bind=['data'])

class HomeScreen(Screen):
    homex = Builder.load_file('kv/root.kv')

class AddBookScreen(Screen):
    pass


class BookcaseApp(App):
    def build(self):
        self.book_store = BookWidget()
        self.load_books()
        self.shelf_store = ShelfWidget()
        self.load_shelves()
        self.root = Builder.load_file('kv/root.kv')
        self.createBottomMenu()


    def next_screen(self, screen):
        filename = screen + '.kv'
        Builder.unload_file('kv/' + filename)
        self.root.container.clear_widgets()
        screen = Builder.load_file('kv/' + filename)
        self.root.container.add_widget(screen)

    def MenuAddNote(self):
        self.root.clear_widgets()
        screen = Builder.load_file('kv/addBook.kv')
        self.root.add_widget(screen)

    def createBottomMenu(self):
        Builder.unload_file('kv/bottomMenu.kv')
        self.root.container2.clear_widgets()
        screen = Builder.load_file('kv/bottomMenu.kv')
        self.root.container2.add_widget(screen)

    def load_books(self):
        # if not exists(self.notes_fn):
        #     return
        # with open(self.notes_fn) as fd:
        data = [{
            'book_index': 5,
            'book_content': 'contentxxx',
            'book_title': 'title2'}]
        self.book_store.data = data

    def load_shelves(self):
        # if not exists(self.notes_fn):
        #     return
        # with open(self.notes_fn) as fd:
        data = [{
            'shelf_title': 'random shelf'}]
        self.shelf_store.data = data


if __name__ == '__main__':
    BookcaseApp().run() 