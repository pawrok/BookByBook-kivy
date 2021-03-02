from sqliteDB import SqliteDB
from plyer import filechooser
from shutil import copyfile
import re
import os.path

import kivy
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Canvas, ClearBuffers, ClearColor
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView 
from kivy.properties import ListProperty, StringProperty, ObjectProperty, \
        NumericProperty, BooleanProperty, AliasProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.config import Config
from kivy.graphics import *

Config.set('graphics', 'width', '325')
Config.set('graphics', 'height', '650')
dst_dir = os.getcwd() + "\\book_covers\\"
# kivy.require('1.9.0')

class RootRoot(BoxLayout):
    pass

class ShelfViewer(RecycleView): 
    def __init__(self, **kwargs): 
        super(ShelfViewer, self).__init__(**kwargs) 
        self.data = [{
            'shelf_title': 'title1'},
            {
            'shelf_title': 'title2'},
            {
            'shelf_title': 'title3'},
            {
            'shelf_title': 'title4'
            }]

class RootScreenManager(ScreenManager):
    pass

class MiddleScreenManager(ScreenManager):
    pass

class HomeScreen(Screen):
    pass


class HomeButton(Button):
    line_color = ListProperty([1, 1, 1, 1], rebind=True)

    def set_underline(self, rgb_color):
        self.line_color = rgb_color


class StatsScreen(Screen):
    pass

class AddScreen(Screen):
    input_title = StringProperty("Title")
    input_author = StringProperty("Author")
    input_category = StringProperty("Category")
    input_rating = NumericProperty(0)
    input_rented_person = StringProperty("Borrowed to...")
    input_date_completed = StringProperty("1.01.2021")
    input_pages = NumericProperty(0)
    book_id = NumericProperty(0)
    input_description = StringProperty("Description")
 
class WishScreen(Screen):
    pass

class SettingsScreen(Screen):
    def delete_DB(self):
        SqliteDB.delete_table()

class Books(Screen):
    pass

class Shelves(Screen):
    pass

class Tags(Screen):
    pass

class GridLayoutTest(GridLayout):
    pass

class BookItem(BoxLayout):
    title = StringProperty()
    cover = StringProperty()
    book_id = NumericProperty()
    
class FavButton(Button):
    is_fav = NumericProperty()
    is_fav = 0
    def set_favourite(self, fav_input):
        if fav_input == 0:
            self.is_fav = 1
            self.children[0].source = 'images/heart_red.png'
        elif fav_input == 1:
            self.is_fav = 0
            self.children[0].source = 'images/heart_black.png'
    
    def load_favourite(self, fav_input):
        if fav_input == 1:
            self.is_fav = 1
            self.children[0].source = 'images/heart_red.png'
        elif fav_input == 0:
            self.is_fav = 0
            self.children[0].source = 'images/heart_black.png'

class AddImageButton(Button):
    imageDest = StringProperty()
    imageDest = ''
    def add_book_image(self):
        try:
            path = filechooser.open_file(title="Pick a book cover ...", 
                             filters=[("*")])[0]
        except IndexError:
            return 0
        filenm = re.search('(\w)+.(\w)+$', path).group(0)
        # print(os.getcwd() + dst)
        self.imageDest = dst_dir + filenm
        copyfile(path, self.imageDest)
        self.children[0].source = self.imageDest
    
    def load_book_image(self, path):
        if path:
            self.imageDest = path
        else:
            self.imageDest = 'images/add_image.png'
        self.children[0].source = self.imageDest

class ReadButton(Button):
    isRead = NumericProperty()
    isRead = 0
    def set_read_status(self, read_input):
        if read_input == 0:
            self.isRead = 1
            self.children[0].source = 'images/checked.png'
        elif read_input == 1:
            self.isRead = 0
            self.children[0].source = 'images/blank.png'
    
    def load_read_status(self, read_input):
        if read_input == 1:
            self.isRead = 1
            self.children[0].source = 'images/checked.png'
        elif read_input == 0:
            self.isRead = 0
            self.children[0].source = 'images/blank.png'

class StarsButton(BoxLayout):
    rating = NumericProperty()

    def set_rating(self, value):
        if value == 1:
            self.ids['first_s'].children[0].source = 'images/star_full.png'
            self.ids['sec_s'].children[0].source = 'images/star_empty.png'
            self.ids['third_s'].children[0].source = 'images/star_empty.png'
            self.ids['fourth_s'].children[0].source = 'images/star_empty.png'
            self.rating = 1
        elif value == 2:
            self.ids['first_s'].children[0].source = 'images/star_full.png'
            self.ids['sec_s'].children[0].source = 'images/star_full.png'
            self.ids['third_s'].children[0].source = 'images/star_empty.png'
            self.ids['fourth_s'].children[0].source = 'images/star_empty.png'
            self.rating = 2
        elif value == 3:
            self.ids['first_s'].children[0].source = 'images/star_full.png'
            self.ids['sec_s'].children[0].source = 'images/star_full.png'
            self.ids['third_s'].children[0].source = 'images/star_full.png'
            self.ids['fourth_s'].children[0].source = 'images/star_empty.png'
            self.rating = 3
        elif value == 4:
            self.ids['first_s'].children[0].source = 'images/star_full.png'
            self.ids['sec_s'].children[0].source = 'images/star_full.png'
            self.ids['third_s'].children[0].source = 'images/star_full.png'
            self.ids['fourth_s'].children[0].source = 'images/star_full.png'
            self.rating = 4

class ShelfItem(BoxLayout):
    shelf_title = StringProperty()

class BookScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(BookScrollView, self).__init__(**kwargs)
        
        self.data = SqliteDB.get_books_fromDB()

        #TODO: height below is fixed, but should be dynamic
        layout = GridLayout(cols=3, spacing=15, size_hint_y=None, height=900, col_default_width = self.width / 3)
        for item in self.data:
            if not item['imageDest']:
                book_cover = 'images/book2.png'
            else:
                book_cover = item['imageDest']
            book = BookItem(book_id=item['ID'], title=item['title'], cover=book_cover)
            layout.add_widget(book)
        self.add_widget(layout)

    def search_title(self, title_str):
        books_to_del = []
        for book in self.children[0].children:
            if title_str not in book.title:
                books_to_del.append(book)

        for b in books_to_del:
            self.children[0].remove_widget(b)

class BookcaseApp(App):
    def build(self):
        self.title = 'BookByBook'
        # self.icon = ''
        SqliteDB()
        Builder.load_file('kv/root.kv')
        self.root = RootRoot()
        return self.root

    def add_book_to_db(
            self, input_title, input_author, input_category, input_rating, input_rented_person,
            input_date_completed, input_pages, isRead, imageDest, isFav, input_description):
        
        if input_rented_person:
            is_rent = True
        
        print("add")
        input_rating = int(input_rating)
        is_rent = int(is_rent)
        input_pages = int(input_pages)
        
        SqliteDB.add_book_toDB(
            input_title, input_author, input_category, input_rating,
            is_rent, input_rented_person, input_date_completed,
            input_pages, isRead, imageDest, isFav, input_description)
    
    def update_book_in_db(
            self, id, input_title, input_author, input_category, input_rating,
            input_rented_person, input_date_completed, input_pages, isRead,
            imageDest, isFav, input_description):
        
        if input_rented_person:
            is_rent = True

        print("update")
        
        input_rating = int(input_rating)
        is_rent = int(is_rent)
        input_pages = int(input_pages)
        
        SqliteDB.edit_book_inDB(
            id, input_title, input_author, input_category, input_rating,
            is_rent, input_rented_person, input_date_completed, input_pages,
            isRead, imageDest, isFav, input_description)
        
    def add_home_screen(self):
        index = 0
        for i in range(len(self.root.ids.rootmanager.screen_names)):
            if self.root.ids.rootmanager.screen_names[i].find('home') != -1:
                index = i
        
        self.root.ids['rootmanager'].remove_widget(self.root.ids.rootmanager.screens[index])
        self.root.ids['rootmanager'].add_widget(HomeScreen())

    def add_newbook_screen(self):
        index = 0
        for i in range(len(self.root.ids.rootmanager.screen_names)):
            if self.root.ids.rootmanager.screen_names[i].find('new') != -1:
                index = i
        
        self.root.ids['rootmanager'].remove_widget(self.root.ids.rootmanager.screens[index])
        self.root.ids['rootmanager'].add_widget(AddScreen())


    def open_edit_book(self, id):
        for i in range(len(self.root.ids.rootmanager.screen_names)):
            if self.root.ids.rootmanager.screen_names[i].find('new') != -1:
                index = i
        
        book_values = SqliteDB.get_single_book_fromDB(id)
        self.root.ids['rootmanager'].remove_widget(self.root.ids.rootmanager.screens[index])
        self.root.ids['rootmanager'].add_widget(AddScreen(
            input_title = book_values['title'],
            input_author = book_values['author'],
            input_category = book_values['category'],
            input_rating = book_values['rating'],
            input_rented_person = book_values['rentedPerson'],
            input_date_completed = book_values['dateCompleted'],
            input_pages = book_values['pageCount'],
            book_id = id,
            input_description = book_values['describtion'],

            ))

        self.root.ids['rootmanager'].current = 'new'
        self.root.ids['rootmanager'].screens[4].ids['stars_rating'].set_rating(book_values['rating'])
        self.root.ids['rootmanager'].screens[4].ids['fav_btn'].load_favourite(book_values['isFav'])
        self.root.ids['rootmanager'].screens[4].ids['read_btn'].load_read_status(book_values['isRead'])
        self.root.ids['rootmanager'].screens[4].ids['add_image_btn'].load_book_image(book_values['imageDest'])

if __name__ == '__main__':
    BookcaseApp().run()
