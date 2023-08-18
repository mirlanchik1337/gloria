import os
from datetime import datetime

now = datetime.now()


def path_and_rename(instance, filename):
    now = datetime.now()
    upload_to = 'product_images'
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