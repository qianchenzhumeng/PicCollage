# coding: utf-8
from PIL import Image, ImageDraw, UnidentifiedImageError
import os

margin = 118

def get_images(dir):
    images = []
    for root,dirs,files in os.walk(dir):
        for name in files:
            try:
                im = Image.open(os.path.join(root, name))
                images.append(im)
            except UnidentifiedImageError:
                pass
    return images

def get_canvas():
    #A4(300 ppi): 2480*3508
    img = Image.new("RGB", (2480, 3508), (255,255,255))
    return img

def get_canvas_horizontal():
    #A4(300 ppi): 3508*2480
    img = Image.new("RGB", (3508, 2480), (255,255,255))
    return img

def calculate_scale_rate(original, current):
    return current / original * 1.0

def scale_image(img, rate):
    w, h = img.size
    img.thumbnail((w*rate, h*rate))
    return img

def draw_img_on_canvas(img, canvas, origin):
    draw = ImageDraw.Draw(canvas)
    x_origin, y_origin = origin
    for x in range(img.width):
        for y in range(img.height):
            draw.point((x_origin+x, y_origin+y), fill = img.getpixel((x, y)))

def get_another_image_in_one_row(image, images, pixels):
    '''
    给定一张图片，寻找另一张能在同一行放下的图片。
    '''
    image_width = image.width
    for img in images:
        if img.width + image_width <= pixels:
            return img
    return None

def paste_up(canvas, top_margin, images):
    if len(images) is 0:
        return 0
    img_0_0 = images[0]
    img_0_1 = get_another_image_in_one_row(img_0_0, images[1:], canvas.width)

    if img_0_1 is not None:
        x_interval = (canvas.width - img_0_0.width - img_0_1.width)/3
        x_offset = x_interval * 2 + img_0_0.width
        draw_img_on_canvas(img_0_1, canvas, (x_offset,top_margin))
        images.remove(img_0_1)
    else:
        x_interval = (canvas.width - img_0_0.width)/2
    
    draw_img_on_canvas(img_0_0, canvas, (x_interval,top_margin))
    images.remove(img_0_0)
    
    return top_margin + img_0_0.height

if __name__ == "__main__":
    images_original = get_images("./horizontal")
    images_resized = []
    canvas_index = 0
    for img in images_original:
        rate = calculate_scale_rate(img.height, 877)
        img_new = scale_image(img, rate)
        images_resized.append(img_new)
    while(len(images_resized) is not 0):
        canvas_index += 1
        print("canvas_index: %d" % canvas_index)
        canvas = get_canvas()
        top_margin = paste_up(canvas, 118, images_resized) + margin
        top_margin = paste_up(canvas, top_margin, images_resized) + margin
        top_margin = paste_up(canvas, top_margin, images_resized) + margin
        canvas.save('canvas_{}.jpg'.format(canvas_index), 'jpeg')
        print(len(images_resized))

    #纵向
    images_original = get_images("./longitudinal")
    images_resized = []
    for img in images_original:
        rate = calculate_scale_rate(img.width, 877)
        img_new = scale_image(img, rate)
        img_rotated = img_new.transpose(Image.ROTATE_90)
        images_resized.append(img_rotated)
    while(len(images_resized) is not 0):
        canvas_index += 1
        print("canvas_index: %d" % canvas_index)
        canvas = get_canvas_horizontal()
        top_margin = paste_up(canvas, 118, images_resized) + margin
        top_margin = paste_up(canvas, top_margin, images_resized) + margin
        top_margin = paste_up(canvas, top_margin, images_resized) + margin
        canvas.save('canvas_{}.jpg'.format(canvas_index), 'jpeg')
        print(len(images_resized))