from sqliteDB import SqliteDB
from plyer import filechooser
from shutil import copyfile
from PIL import Image
from random import randint
import re
import os.path

import kivy
from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView 
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.config import Config
from kivy.graphics import *

Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '652')
dst_dir = os.getcwd() + "\\book_covers\\"


class RootWidget(BoxLayout):
    pass

class HomeScreen(Screen):
    pass

class ShelfViewer(RecycleView): 
    def __init__(self, **kwargs): 
        super(ShelfViewer, self).__init__(**kwargs) 
        self.data = [
            {'shelf_title': 'title1'},
            {'shelf_title': 'title2'},
            {'shelf_title': 'title3'},
            {'shelf_title': 'title4'}]


class HomeButton(Button):
    line_color = ListProperty([1, 1, 1, 1], rebind=True)

    def set_underline(self, rgb_color):
        self.line_color = rgb_color


class AddScreen(Screen):
    title = StringProperty("")
    author = StringProperty("")
    category = StringProperty("")
    rating = NumericProperty(0)
    rented_person = StringProperty("")
    date_completed = StringProperty("")
    pages = NumericProperty(0)
    book_id = NumericProperty(0)
    description = StringProperty("")
    shelves = StringProperty("")
    tags = StringProperty("")

    def save_book(self, values):
        if self.book_id > 0:
            SqliteDB.edit_book_in_db(self.book_id, *values)
        else:
            SqliteDB.add_book_to_db(*values)

class BookItem(BoxLayout):
    title = StringProperty()
    cover = StringProperty()
    book_id = NumericProperty()


class FavButton(Button):
    is_fav = NumericProperty(0)
    
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
    imageDest = StringProperty('')
    
    def add_book_image(self, book_id):
        try:
            path = filechooser.open_file(title="Pick a book cover ...", 
                                         filters=[("*")])[0]
        except IndexError:
            return 0
        
        # TODO: save img as temp.jpg, then after book's save change it to id.jpg
        if book_id == 0:
            book_id = randint(9999, 999999)

        self.crop_and_resize(path, book_id)
        
        self.imageDest = dst_dir + str(book_id) + '.jpg'
        self.children[0].source = self.imageDest
    
    def load_book_image(self, path):
        if path:
            self.imageDest = path
        else:
            self.imageDest = 'images/book2.png'
        
        self.children[0].source = self.imageDest
    
    def crop_and_resize(self, img_path, book_id):
        ratio = 475 / 300   # height / width
        size = (300, 475)

        original = Image.open(img_path)
        width, height = original.size   # Get dimensions 

        if width * ratio > height:
            new_width = height / ratio
            to_cut = width - new_width

            left = to_cut / 2
            top = 0
            right = width - (to_cut / 2)
            bottom = height

            cropped_img = original.crop((left, top, right, bottom))
        else:
            new_height = width * ratio
            to_cut = height - new_height

            left = 0
            top = to_cut / 2
            right = width
            bottom = height - (to_cut / 2)
            
            cropped_img = original.crop((left, top, right, bottom))

        cropped_img.thumbnail(size)

        cropped_img = cropped_img.convert('RGB')
        cropped_img.save(dst_dir + str(book_id) + '.jpg')


class ReadButton(Button):
    isRead = NumericProperty(0)

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


class BookGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(BookGridLayout, self).__init__(**kwargs)

        self.data = SqliteDB.get_db_values('booktable')

        for item in self.data:
            if not item['imageDest']:
                book_cover = 'images/book2.png'
            else:
                book_cover = item['imageDest']

            book = BookItem(book_id=item['book_id'], title=item['title'], cover=book_cover)
            self.add_widget(book)
            self.height += book.height / 3 + 10

    def search_title(self, title_str):
        books_to_del = []
        for book in self.children:
            if title_str not in book.title:
                books_to_del.append(book)

        for b in books_to_del:
            self.remove_widget(b)


class BookcaseApp(App):
    def build(self):
        self.title = 'BookByBook'
        # self.icon = ''

        SqliteDB()
        # Builder.load_file('kv/root.kv')

        self.root = RootWidget()
        return self.root
        
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


    def open_edit_book(self, book_id):
        for i in range(len(self.root.ids.rootmanager.screen_names)):
            if self.root.ids.rootmanager.screen_names[i].find('new') != -1:
                index = i
        
        book_values = SqliteDB.get_single_book_from_db(book_id)
        self.root.ids['rootmanager'].remove_widget(self.root.ids.rootmanager.screens[index])
        self.root.ids['rootmanager'].add_widget(AddScreen(
            title = book_values['title'],
            author = book_values['author'],
            category = book_values['category'],
            rating = book_values['rating'],
            rented_person = book_values['rentedPerson'],
            date_completed = book_values['dateCompleted'],
            pages = book_values['pageCount'],
            book_id = book_id,
            description = book_values['describtion']
            ))

        self.root.ids['rootmanager'].current = 'new'
        self.root.ids['rootmanager'].screens[4].ids['stars_rating'].set_rating(book_values['rating'])
        self.root.ids['rootmanager'].screens[4].ids['fav_btn'].load_favourite(book_values['isFav'])
        self.root.ids['rootmanager'].screens[4].ids['read_btn'].load_read_status(book_values['isRead'])
        self.root.ids['rootmanager'].screens[4].ids['add_image_btn'].load_book_image(book_values['imageDest'])


if __name__ == '__main__':
    BookcaseApp().run()
