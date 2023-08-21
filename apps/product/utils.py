import os
from datetime import datetime
from PIL import Image
now = datetime.now()


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def compress_img(image_name, new_size_ratio=1, quality=90, width=None, height=None, to_jpg=True):
    # load the image to memory
    img = Image.open(image_name)
    # get the original image size in bytes
    image_size = os.path.getsize(image_name)
    if new_size_ratio < 1.0:
        # if resizing ratio is below 1.0, then multiply width & height with this ratio to reduce image size
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.LANCZOS)
        # print new image shape
        print("[+] New Image shape:", img.size)
    elif width and height:
        # if width and height are set, resize with them instead
        img = img.resize((width, height), Image.LANCZOS)
        # print new image shape
        print("[+] New Image shape:", img.size)
    # split the filename and extension
    filename, ext = os.path.splitext(image_name)
    # make new filename appending _compressed to the original file name
    if to_jpg:
        # change the extension to JPEG
        new_filename = f"{filename}.jpg"
    else:
        # retain the same extension of the original image
        new_filename = f"{filename}_compressed{ext}"
    try:
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        # convert the image to RGB mode first
        img = img.convert("RGB")
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)


def path_and_rename(instance, filename):
    upload_to = 'product_images'
    # compress_img(filename)
    ext = filename.split('.')[-1]
    old_filename = filename.split('.')[0]
    # set filename as random string
    filename = f'{old_filename}_{now.strftime("%d-%m-%Y %H-%M")}.{ext}'
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def path_and_rename2(instance, filename):
    upload_to = 'category_images'

    ext = filename.split('.')[-1]
    old_filename = filename.split('.')[0]
    filename = f'{old_filename}_{now.strftime("%d-%m-%Y %H-%M")}.{ext}'
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def path_and_rename3(instance, filename):
    upload_to = 'subcategory_images'
    ext = filename.split('.')[-1]
    old_filename = filename.split('.')[0]

    # set filename as random string
    filename = f'{old_filename}_{now.strftime("%d-%m-%Y %H-%M")}.{ext}'
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def path_and_rename4(instance, filename):
    upload_to = 'second_subcategory_images'
    ext = filename.split('.')[-1]
    old_filename = filename.split('.')[0]

    # set filename as random string
    filename = f'{old_filename}_{now.strftime("%d-%m-%Y %H-%M")}.{ext}'
    # return the whole path to the file
    return os.path.join(upload_to, filename)