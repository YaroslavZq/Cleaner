from pathlib import Path
import os
import shutil
import sys
from transliterate import translit
from string import punctuation

DIR_IGNOR_NAMES = ["archives", "video", "audio", "documents", "images", "other"]


def main():
    if len(sys.argv) < 2:
        print("Enter path to folder which should be cleaned")
        exit()
    path = sys.argv[1]
    if not (os.path.exists(path) and Path(path).is_dir()):
        print("Path incorrect")
        exit()

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
    try:
        dir_img = (os.path.join(path, "images"))
        os.mkdir(dir_img)
    except FileExistsError:
        print("images already created")
    try:
        dir_vid = (os.path.join(path, "video"))
        os.mkdir(dir_vid)
    except FileExistsError:
        print("video already created")
    try:
        dir_doc = (os.path.join(path, "documents"))
        os.mkdir(dir_doc)
    except FileExistsError:
        print("documents already created")
    try:
        dir_aud = (os.path.join(path, "audio"))
        os.mkdir(dir_aud)
    except FileExistsError:
        print("audio already created")
    try:
        dir_arc = (os.path.join(path, "archives"))
        os.mkdir(dir_arc)
    except FileExistsError:
        print("archives already created")
    try:
        dir_other = (os.path.join(path, "other"))
        os.mkdir(dir_other)
    except FileExistsError:
        print("other already created")

    # функція перебору файлів по папці
    def cleaner(path_holder):
        print(path_holder)
        for file in path_holder.iterdir():
            print(file)
            if file.is_dir() is True and file.name not in DIR_IGNOR_NAMES:
                cleaner(file)
            elif file.is_dir() is True and file.name in DIR_IGNOR_NAMES:
                continue
            new_file_name = Path(normalize(file))
            if new_file_name.is_file() is True and new_file_name.suffix in ['.jpeg', '.png', '.jpg', '.svg']:
                shutil.move(new_file_name, dir_img)
            elif new_file_name.is_file() is True and new_file_name.suffix in ['.avi', '.mp4', '.mov', '.mkv']:
                shutil.move(new_file_name, dir_vid)
            elif new_file_name.is_file() is True and new_file_name.suffix in ['.doc', '.docx', '.txt', '.pdf', '.xlsx',
                                                                              '.xls', '.pptx']:
                shutil.move(new_file_name, dir_doc)
            elif new_file_name.is_file() is True and new_file_name.suffix in ['.mp3', '.ogg', '.wav', '.amr']:
                shutil.move(new_file_name, dir_aud)
            elif new_file_name.is_file() is True and new_file_name.suffix in ['.zip', '.gz', '.tar']:
                archive = Path(shutil.move(new_file_name, dir_arc))
                new_folder = os.path.join(archive.parent, archive.name.split(".")[0])
                os.mkdir(new_folder)
                shutil.unpack_archive(archive, new_folder)
                os.remove(archive)
            elif new_file_name.is_file() is True:
                shutil.move(new_file_name, dir_other)
        # видалення порожніх та непотрібних папок
        for file in path_holder.iterdir():
            if file.is_dir() is True and file.name not in DIR_IGNOR_NAMES:
                os.rmdir(file)

    cleaner(Path(path))


if __name__ == "__main__":
    exit(main())
