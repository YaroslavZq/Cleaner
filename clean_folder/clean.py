from pathlib import Path
import os
import shutil
import sys
from transliterate import translit
from string import punctuation

DIR_IGNOR_NAMES = ["archives", "video", "audio", "documents", "images", "other"]


# функція для зміни назви файлу
def normalize(dir_file):
    replacing_text = dir_file.name.split(".")[0]
    for symbol in punctuation + " ":
        replacing_text = replacing_text.replace(symbol, '_')
    try:
        new_file_name = translit(replacing_text, reversed=True) + dir_file.suffix.lower()
    except:
        new_file_name = replacing_text + dir_file.suffix.lower()
    new_file_name = os.path.join(dir_file.parent, new_file_name)
    os.rename(dir_file, new_file_name)
    return new_file_name


# створення папок для сортування
def create_directory(path, name):
    directory = os.path.join(path, name)
    try:
        os.mkdir(directory)
    except FileExistsError:
        print(f"{name} already created")
    return directory


# функція перебору файлів по папці
def cleaner(path_holder, path):
    print(path_holder)
    path_holder = Path(path_holder)
    for file in path_holder.iterdir():
        print(file)
        if file.is_dir() and file.name not in DIR_IGNOR_NAMES:
            cleaner(file, path)
        elif file.is_dir() and file.name in DIR_IGNOR_NAMES:
            continue
        new_file_name = Path(normalize(file))
        if new_file_name.is_file() and new_file_name.suffix in ['.jpeg', '.png', '.jpg', '.svg']:
            dir_img = create_directory(path, "images")
            shutil.move(new_file_name, dir_img)
        elif new_file_name.is_file() and new_file_name.suffix in ['.avi', '.mp4', '.mov', '.mkv']:
            dir_vid = create_directory(path, "video")
            shutil.move(new_file_name, dir_vid)
        elif new_file_name.is_file() and new_file_name.suffix in ['.doc', '.docx', '.txt', '.pdf', '.xlsx',
                                                                          '.xls', '.pptx']:
            dir_doc = create_directory(path, "documents")
            shutil.move(new_file_name, dir_doc)
        elif new_file_name.is_file() and new_file_name.suffix in ['.mp3', '.ogg', '.wav', '.amr']:
            dir_aud = create_directory(path, "audio")
            shutil.move(new_file_name, dir_aud)
        elif new_file_name.is_file() and new_file_name.suffix in ['.zip', '.gz', '.tar']:
            dir_arc = create_directory(path, "archives")
            archive = Path(shutil.move(new_file_name, dir_arc))
            new_folder = os.path.join(archive.parent, archive.name.split(".")[0])
            os.mkdir(new_folder)
            shutil.unpack_archive(archive, new_folder)
            os.remove(archive)
        elif new_file_name.is_file():
            dir_other = create_directory(path, "other")
            shutil.move(new_file_name, dir_other)
    # видалення порожніх та непотрібних папок
    for file in path_holder.iterdir():
        if file.is_dir() and file.name not in DIR_IGNOR_NAMES:
            os.rmdir(file)


def main():
    if len(sys.argv) < 2:
        print("Enter path to folder which should be cleaned")
        exit()
    path = sys.argv[1]
    if not (os.path.exists(path) and Path(path).is_dir()):
        print("Path incorrect")
        exit()
    cleaner(Path(path), path)


if __name__ == "__main__":
    exit(main())
