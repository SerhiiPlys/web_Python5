"""Скрипт написан под мои личные предпочтения с учетом требований ДЗ
   Версия с потоками
   К сожалению у программы жесткая структура - одно должно выполняться за
   другим. то есть пока я  не получу пути ко всем файлам, то бесполезно
   распаковывать архивы итд...поэтому потоковость здесь псевдопараллельная
   механизм Локера я импортровал(просто показать что понимаю что это такое),
   но не использовал - мне достаточно после
   запуска потока использовать join дождаться окончания и запустить следующий
   Далее
   здесь у меня нет независымых последовательных вычислений, чтобы максимально
   использовать потоковость (превратить их в параллельные).
   а здесь в основном обращения к API ОС, поэтому
   бедноватое использование потоковости
   Далее
   К тому же потому что потоки используют общие ресурсы то пришлось пару
   переменных сделать глобальными, чего всегда по возможности нужно
   избегать

   Далее комментарии на англ и в соответствии с PEP8
"""

import os      # work with file system
import sys     # for command line
import shutil  # for func copy
import re      # string func
import time
from threading import Thread, RLock

path_test = "C:\\Users\\Ultra\\Desktop\\garbage"
log_list = []
path = ''
ls_files = []

TRANS = {}


def make_trans_dict():
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j",
                   "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "",
                   "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
    global TRANS
    CYR = []
    for i in CYRILLIC_SYMBOLS:
        CYR.append(i)
    for i, j in zip(CYR, TRANSLATION):
        TRANS[ord(i)] = j
        TRANS[ord(i.upper())] = j.upper()


def check_name(name_a):
    name_a_a = name_a.translate(TRANS)
    return re.sub(r'[^a-zA-Z0-9.]', '_', name_a_a)


def check_empty_dir(path_a):
    """Check, if folder is empty then  True
       if folder not empty ot not is then False
    """
    if os.path.exists(path_a):
        sz = os.path.getsize(path_a)
        if sz == 0:
            return True
        else:
            return False
    else:
        return False


def del_empty_dir(path_b):
    """Delete empty dir
       Check before that size of folder is 0
    """
    ls_1 = os.listdir(path_b)
    # check for chaild empty folder
    if bool(ls_1) is True:
        path_b_a = os.path.join(path_b, ls_1[0])
        del_empty_dir(path_b_a)
        ls_1.pop(0)
        if bool(ls_1) is True:
            del_empty_dir(path_b)
        else:
            os.rmdir(path_b)
            return
    else:
        # delete folder - root
        os.rmdir(path_b)


def main():
    """Enrtypoint - check path from commandline
        or prompt via input
    """
    global path
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        if os.path.exists(path):
            print(path)
            print("Папка существует, продолжаем")
        else:
            # dont exist path, prompt via input
            print("Ошибка в комстроке пути к папке либо папки не существует")
            path = input("Введите путь к папке:\nИспользуйте двойной Бэкслеш \\\\ \
как разделитель\n")
            print(path)
            log_list.append(f"Папка для расхламления {path}\n")
    else:
        # path is empty, prompt via input
        print("Путь в комстроке пуст")
        path = input("Введите путь к папке:\nИспользуйте двойной Бэкслеш \\\\ \
как разделитель\n")
        print(path)
        log_list.append(f"Папка для расхламления {path}\n")

    # make dict for transliteration
    make_trans_dict()


def thread_create_folders(locker):
    '''Making target folders
    '''

    global path
    if not os.path.isdir(path):
        print("Ошибка в пути к папке")
        os._exit(-1)
    else:
        if not os.path.exists(path+'\\images'):
            os.mkdir(path+'\\images')
        if not os.path.exists(path+'\\documents'):
            os.mkdir(path+'\\documents')
        if not os.path.exists(path+'/audio'):
            os.mkdir(path+'/audio')
        if not os.path.exists(path+'/video'):
            os.mkdir(path+'/video')
        if not os.path.exists(path+'/archives'):
            os.mkdir(path+'/archives')
        if not os.path.exists(path+'/others'):
            os.mkdir(path+'/others')


def thread_parsing_path(locker):
    """Get all pathes to all files in target path
    """
    global path       # target path
    global ls_files   # list of path+file
    print("Список существующих файлов в выбранной папке:")
    log_list.append("Список существующих файлов в выбранной папке:\n")
    for root, dirs, files in os.walk(path):
        for f in files:
            full_adr = os.path.join(root, f)
            print(full_adr)
            log_list.append(full_adr+'\n')
            ls_files.append(full_adr)
    print(' ')


def thread_copy_to_dest(locker):
    """Copy all files to target folders of extenstion
    """
    global ls_files
    for full_adr_s in ls_files:
        try:
            if (("images" in full_adr_s) or ("documents" in full_adr_s) or
                    ("video" in full_adr_s) or ("audio" in full_adr_s) or
                    ("archives" in full_adr_s) or ("other" in full_adr_s)):
                # dont touch files existing in target folders
                continue
            elif ((".xlsx" in full_adr_s) or (".txt" in full_adr_s) or
                  (".doc" in full_adr_s) or (".docx" in full_adr_s) or
                  (".pdf" in full_adr_s) or (".pptx" in full_adr_s)):
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\documents', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} \
в \n{full_adr_d}\n")
            elif ((".jpeg" in full_adr_s) or (".bmp" in full_adr_s) or
                  (".jpg" in full_adr_s) or (".png" in full_adr_s)):
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\images', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} \
в \n{full_adr_d}\n")
            elif ((".avi" in full_adr_s) or (".mpeg" in full_adr_s) or
                  (".mp4" in full_adr_s) or (".mov" in full_adr_s)):
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\video', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} \
в \n{full_adr_d}\n")
            elif ((".mp3" in full_adr_s) or (".ogg" in full_adr_s) or
                  (".wav" in full_adr_s) or (".amr" in full_adr_s)):
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\audio', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} \
в \n{full_adr_d}\n")
            elif ((".zip" in full_adr_s) or (".rar" in full_adr_s) or
                  (".tar" in full_adr_s) or (".gz" in full_adr_s)):
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\archives', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} \
в \n{full_adr_d}\n")
            else:
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\others', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} \
в \n{full_adr_d}\n")
        except:
            print("Ошибка в путях либо копировании файлов")
            log_list.append("Ошибка в путях либо копировании файлов\n")
            os._exit(-2)


def thread_delete_empty(locker):
    """Delete empty folders and subfolders
    """
    global path
    print("Список удаляемых пустых папок:")
    log_list.append("Список удаляемых пустых папок:\n")
    ls_dirs_1 = os.listdir(path)
    for d in ls_dirs_1:
        full_adr = os.path.join(path, d)
        if check_empty_dir(full_adr):
            try:
                if (("images" in full_adr) or ("documents" in full_adr) or
                        ("video" in full_adr) or ("audio" in full_adr) or
                        ("archives" in full_adr) or ("other" in full_adr)):
                    # dont touch empty folders in target folders
                    continue
                else:
                    print(f"Удаление пустой папки\n{full_adr}")
                    log_list.append(f"Удаление пустой папки\n{full_adr}\n")
                    # delelte empty folder and subfolders - recursion
                    del_empty_dir(full_adr)
            except:
                print("Ошибка в удалении пустых папок")
    print(' ')


def thread_unpack_archives(locker):
    """Unpack archives existing in tagret folder
    """
    global path
    print("Перемещение и распаковка архивов:")
    log_list.append("Перемещение и распаковка архивов:\n")
    ls_archives = os.listdir(path+'/archives')
    for arc in ls_archives:
        if (".zip" in arc) or (".rar" in arc) or (".tar" in arc):
            arc_n = arc[0:len(arc) - 4]
            if not os.path.exists(os.path.join(path+'/archives', arc_n)):
                os.mkdir(os.path.join(path+'/archives', arc_n))
            try:
                shutil.unpack_archive(arc, os.path.join(path+'/archives',
                                                        arc_n))
                os.remove(os.path.join(path+'/archives', arc))
                print(f"Архив {arc} распакован в папку {arc}")
                log_list.append(f"Архив {arc} распакован в папку {arc}\n")
            except:
                print(f"{arc} архив неопознан или поврежден")
                log_list.append(f"{arc} архив неопознан или поврежден\n")
        elif (".gz" in arc):
            arc_n = arc[0:len(arc) - 3]
            if not os.path.exists(os.path.join(path+'/archives', arc_n)):
                os.mkdir(os.path.join(path+'/archives', arc_n))
            try:
                shutil.unpack_archive(arc, os.path.join(path+'/archives',
                                                        arc_n))
                os.remove(os.path.join(path+'/archives', arc))
                print(f"Архив {arc} распакован в папку {arc}")
                log_list.append(f"Архив {arc} распакован в папку {arc}\n")
            except:
                print(f"{arc} архив неопознан или поврежден")
                log_list.append(f"{arc} архив неопознан или поврежден\n")


def thread_logging(locker):
    """Create logfile
    """
    global path
    local_time = time.asctime()
    print(f"Создан логфайл {local_time}.txt")
    with open(path+"\\log.txt", 'x') as file_log:
        file_log.write((f"Файл логирования сортировки папки {path}\
                       \nсоздан {local_time} \n"))
        s_log = ''
        for item in log_list:
            s_log += item
        file_log.write(s_log)


if __name__ == "__main__":
    main()

lock_1 = RLock()
thread_1 = Thread(target=thread_create_folders, args=(lock_1,))
thread_2 = Thread(target=thread_parsing_path, args=(lock_1,))
thread_3 = Thread(target=thread_copy_to_dest, args=(lock_1,))
thread_4 = Thread(target=thread_delete_empty, args=(lock_1,))
thread_5 = Thread(target=thread_unpack_archives, args=(lock_1,))
thread_6 = Thread(target=thread_logging, args=(lock_1,))
thread_1.start()
thread_1.join()
thread_2.start()
thread_2.join()
thread_3.start()
thread_3.join()
thread_4.start()
thread_4.join()
thread_5.start()
thread_5.join()
thread_6.start()
thread_6.join()
