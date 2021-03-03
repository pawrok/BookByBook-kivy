from PIL import Image

def crop_and_resize(img_path, book_id):
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
    cropped_img.save('book_covers/' + str(book_id) + '.jpg')


crop_and_resize("C:\\git repositories\\bookcase\\book_covers\\1920x1200.jpg", 5)