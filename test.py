from PIL import Image

test_image = "test.png"
original = Image.open(test_image)
original.show()
ratio = 475 / 300   # height / width
width, height = original.size   # Get dimensions 

if width * ratio > height:
    new_width = height / ratio
    to_cut = width - new_width
    left = to_cut / 2
    top = 0
    right = width - (to_cut / 2)
    bottom = height
    cropped_example = original.crop((left, top, right, bottom))
else:
    new_height = width * ratio
    to_cut = height - new_height
    left = 0
    top = to_cut / 2
    right = width
    bottom = height - (to_cut / 2)
    cropped_example = original.crop((left, top, right, bottom))

size = (300, 475)

cropped_example.thumbnail(size)

cropped_example.show()

cropped_example = cropped_example.convert('RGB')
cropped_example.save('thumbnail.jpg')