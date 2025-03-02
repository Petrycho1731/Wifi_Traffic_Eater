#https://github.com/Petrycho1731 

import os
import threading
import requests

try:
    from tkinter import Tk, Label, Button
    use_tkinter = True
except ImportError:
    use_tkinter = False

try:
    from customtkinter import CTk, CTkButton, CTkLabel, CTkFrame, set_appearance_mode
    use_customtkinter = os.name == 'nt'
except ImportError:
    use_customtkinter = False

URLS = [
    'https://speedtest.rastrnet.ru/1GB.zip',
    'https://speedtest.rastrnet.ru/500MB.zip',
    'https://speedtest.selectel.ru/10GB',
    'https://speedtest.selectel.ru/1GB',
]

eat = False
readed = 0


def check_internet():
    """Проверяет доступ в интернет"""
    try:
        requests.get('https://google.com', timeout=3)
        return True
    except requests.RequestException:
        return False


def download_thread(url):
    """Функция для скачивания файлов"""
    global eat, readed

    while eat:
        try:
            response = requests.get(url, stream=True, timeout=3)
            for chunk in response.iter_content(chunk_size=5_024_000):
                if not eat:
                    break
                readed += len(chunk)
                status_text = f'Хаваем: {round(readed / 1024 / 1024, 1)} МБ'
                print(status_text)

                if use_tkinter or use_customtkinter:
                    update_status(status_text)
        except requests.RequestException:
            pass


def start_download():
    """Запускает загрузку в отдельных потоках"""
    global eat, readed
    eat = True
    readed = 0

    print('Нажмите ENTER для остановки...')

    for url in URLS:
        threading.Thread(target=download_thread, args=(url,), daemon=True).start()

    if not (use_tkinter or use_customtkinter):
        input()
        stop_download()


def stop_download():
    """Останавливает загрузку"""
    global eat
    eat = False
    update_status('Загрузка остановлена')


def update_status(text):
    """Обновляет статус в GUI"""
    if use_tkinter:
        status_lbl.config(text=text)
    elif use_customtkinter:
        status_lbl.configure(text=text)


# Ждём инет перед запуском

print('Проверяем доступ в интернет...')
while not check_internet():
    pass

if not (use_tkinter or use_customtkinter):
    print('Не удалось загрузить GUI. Используем терминальную версию.')
    while True:
        command = input('Введите команду (traffic - Старт, exit - выход): ').strip().lower()
        if command == 'traffic':
            start_download()
        elif command == 'exit':
            os._exit(0)
        else:
            print('Неизвестная команда')

if use_tkinter:
    window = Tk()
    window.title('traffic_Eater | by Petrycho1731')
    window.geometry('300x125')
    window.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))

    status_lbl = Label(window, text='Статус: ожидание', font=('Arial Black', 13))
    status_lbl.pack()

    def toggle_download():
        global eat
        if eat:
            stop_download()
            start_btn.config(text='Старт')
        else:
            start_download()
            start_btn.config(text='Стоп')

    start_btn = Button(window, text='Старт', command=toggle_download)
    start_btn.pack()

    window.mainloop()

# GUI на сustomtkinter

if use_customtkinter:
    window = CTk()
    window.resizable(False, False)
    set_appearance_mode("dark")
    window.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
    window.title('TrafficDown')
    window.geometry('300x130')

    CTkFrame(window, width=280, height=105).place(x=10, y=10)

    status_lbl = CTkLabel(window, text='Статус: ожидание', font=('Arial Black', 13))
    status_lbl.place(relx=0.5, anchor='center', rely=0.25)

    def toggle_download():
        global eat
        if eat:
            stop_download()
            start_btn.configure(text='Старт')
        else:
            start_download()
            start_btn.configure(text='Стоп')

    start_btn = CTkButton(window, text='Старт', command=toggle_download)
    start_btn.place(x=85, y=70)

    window.mainloop()