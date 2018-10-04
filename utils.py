from os import listdir, unlink
from os.path import join, dirname, abspath, exists
import os


def get_images(folder):
    return [join(folder, file) for file in listdir(folder)]


def delete_images(folder):
    [unlink(dirname(abspath(file)) + '/' + join(folder, file)) for file in listdir(folder)]
    return 'delete-images-success'


def count_folders(folder):
    if os.path.exists(folder):
        return len(listdir(folder))
    else:
        return 0


def create_folder(folder):
    if not os.path.exists(folder):
        os.system('mkdir ' + folder)
        return 'folder-create-success'
    else:
        return 'folder-exists'


def move_images(origen, destination):
    if not os.path.exists(destination):
        create_folder(destination)
    os.system('cp ' + origen + '* ' + destination)
    return 'images-move-success'


def move_image(url_image, folder_destination):
    if not os.path.exists(folder_destination):
        create_folder(folder_destination)
    os.system('cp ' + url_image + ' ' + folder_destination)
    return 'image-move-success'


def delete_images_folder(folder):
    os.system('rm -rf ' + folder + '*')


if __name__ == "__main__":
    print('main')
