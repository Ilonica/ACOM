import cv2
import numpy as np
import time

def task2():
    # изображение cчитывается в любом возможном цветовом формате
    img1 = cv2.imread('seeu.jpg', cv2.IMREAD_ANYCOLOR)
    # окно изменяется на полноэкранный режим.
    cv2.namedWindow('Seeu kawai', cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Seeu kawai', img1)
    cv2.waitKey(0)

    # изображение всегда преобразовывается в 3-канальное цветное изображение BGR
    img2 = cv2.imread('art.png', cv2.IMREAD_COLOR)
    # пользователь не может изменить размер окна, размер ограничен отображаемым изображением
    cv2.namedWindow('Art Pafaits', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Art Pafaits', img2)
    cv2.waitKey(0)

    # изображение всегда преобразовывается в одноканальное изображение в оттенках серого
    img3 = cv2.imread('gaara.webp', cv2.IMREAD_GRAYSCALE)
    # изображение растягивается настолько, насколько это возможно
    cv2.namedWindow('The transformation of the city', cv2.WINDOW_FREERATIO)
    cv2.imshow('The transformation of the city', img3)
    cv2.waitKey(0)

def task3():
    # экземпляр класса с помощью конструктора, для чтения видео
    video = cv2.VideoCapture(r'C:\Users\User\Videos\Snowmiku.mp4', cv2.CAP_ANY)

    # цикл для обработки всех кадров
    while(True):
        # читаем видео разбивая его на картинки
        ret, frame = video.read()
        # изменено разрешение видео SD
        resized_frame = cv2.resize(frame, (854, 480))
        # конвертация из цветового пространства RGB в BGR
        bgr_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGBA)
        # проверка на конец изображений в видео
        if not(ret):
            break

        # отображаем видео покадрово в окнах с различными настройками
        cv2.imshow('Video', frame)
        cv2.imshow('Video SD', resized_frame)
        cv2.imshow('Video RGB in BGR', bgr_frame)

        # меняем кадр через 1 милисекунду, после нажатия exc(код 27) отображение кадров прекращается
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # освобождаем ресурсы, связанные с видеофайлом и записью
    video.release()
    # закрываем все открытые окна OpenCV
    cv2.destroyAllWindows()

# чтение
def task4():
    # экземпляр класса с помощью конструктора, для чтения видео
    video = cv2.VideoCapture('dance.mp4')
    # читаем видео разбивая его на картинки
    ret, frame = video.read()

    # ширина и высота кадров видео
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # устанавливаем кодек для сжатия видео в формате XVID
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    # cоздаем объект для записи видео в файл с параметрами (имя, кодек, fps, разрешение)
    video_writer = cv2.VideoWriter("output_t4.mp4", fourcc, 25, (w, h))

    # цикл для обработки всех кадров
    while (True):
        # читаем видео разбивая его на картинки
        ret, frame = video.read()
        # отображаем видео покадрово в окне
        cv2.imshow('video', frame)
        # записываем текущий кадр в выходной видеофайл
        video_writer.write(frame)

        # меняем кадр через 1 милисекунду, после нажатия 'q' отображение кадров прекращается
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # освобождаем ресурсы, связанные с видеофайлом и записью
    video.release()
    # закрываем все открытые окна OpenCV
    cv2.destroyAllWindows()

def task5():
    # считываем изображение
    frame = cv2.imread('seeu.jpg')
    # считываем изображение и переводим в формат HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # отображаем оба окна одновременно
    while (True):
        cv2.imshow('Seeu kawai', frame)
        cv2.imshow('Seeu kawai HSV', hsv)
        cv2.waitKey(0)

def task6():
    # инициализация объекта захвата видео
    img = cv2.VideoCapture(0)
    # устанавливаем ширину и высоту кадра с помощью флага
    img.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    img.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # вычисляем смещение для центрирования прямоугольников
    offset_width = (640 - 260) // 2
    offset_height = (480 - 280) // 2

    while True:
        ret, frame = img.read()

        # создаем пустую маску на весь фрейм для выделения области
        mask = np.zeros((480, 640, 3), dtype=np.uint8)

        # рисуем белый прямоугольник в маске, который совпадает со средним прямоугольником (левая верхняя точка и правая нижняя)
        mask = cv2.rectangle(mask, (offset_width, 120 + offset_height),
                             (260 + offset_width, 160 + offset_height),
                             (255, 255, 255), -1)

        # применяем размытие на весь фрейм с размером ядра 63
        blurred_frame = cv2.stackBlur(frame, (63, 63))

        # вставляем размытое изображение в исходное по маске, только там, где маска имеет значение 255
        # заменяем те пиксели в изображении frame, которые соответствуют белому прямоугольнику в маске, на соответствующие пиксели из размытых данных blurred_frame
        frame[mask == 255] = blurred_frame[mask == 255]

        # рисуем красные прямоугольники вокруг определенных областей
        cv2.rectangle(frame, (offset_width, 120 + offset_height),
                      (260 + offset_width, 160 + offset_height), (0, 0, 255), 2)
        cv2.rectangle(frame, (110 + offset_width, offset_height),
                      (150 + offset_width, 120 + offset_height), (0, 0, 255), 2)
        cv2.rectangle(frame, (110 + offset_width, 160 + offset_height),
                      (150 + offset_width, 280 + offset_height), (0, 0, 255), 2)

        cv2.imshow('frame', frame)

        # Прерываем цикл при нажатии esc
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Освобождаем ресурсы
    img.release()
    cv2.destroyAllWindows()

def task7():
    # инициализация объекта захвата видео
    video = cv2.VideoCapture(0)
    # читаем видео разбивая его на картинки
    ret, frame = video.read()

    # ширина и высота кадров видео
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # устанавливаем кодек для сжатия видео в формате XVID
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # cоздаем объект для записи видео в файл с параметрами (имя, кодек, fps, разрешение)
    video_writer = cv2.VideoWriter("output_t7.mp4", fourcc, 25, (w, h))

    # цикл для обработки всех кадров
    while (True):
        # читаем видео разбивая его на картинки
        ret, frame = video.read()
        # отображаем видео покадрово в окне
        cv2.imshow('video', frame)
        # записываем текущий кадр в выходной видеофайл
        video_writer.write(frame)

        # меняем кадр через 1 милисекунду, после нажатия esc отображение кадров прекращается
        if cv2.waitKey(1) & 0xFF == 27:
            break

    video.release()
    video_writer.release()
    cv2.destroyAllWindows()

    time.sleep(10)

    video_open = cv2.VideoCapture('output_t7.mp4', cv2.CAP_ANY)

    while (True):
        # читаем видео разбивая его на картинки
        ret, frame = video_open.read()
        # проверка на конец изображений в видео
        if not (ret):
            break

        # отображаем видео покадрово в окне
        cv2.imshow('Video', frame)

        # меняем кадр через 1 милисекунду, после нажатия exc(код 27) отображение кадров прекращается
        if cv2.waitKey(1) & 0xFF == 27:
            break

    video_open.release()
    cv2.destroyAllWindows()

def task8():
    # инициализация объекта захвата видео
    video = cv2.VideoCapture(0)

    # ширина и высота кадров видео
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # определяем координаты центра кадра
    center_x = w // 2
    center_y = h // 2

    # pассчитываем смещение для выравнивания прямоугольников по центру
    offw = (w - 260) // 2
    offh = (h - 280) // 2

    while True:
        # чтение кадра из видеопотока
        ret, frame = video.read()

        # получаем цвет пикселя в центре кадра
        center = frame[center_y][center_x]

        # Определяем цвет заливки для прямоугольников:
        # Если синий канал больше всех, цвет будет синим
        if (center[0] > center[1]) and (center[0] > center[2]):
            color = [255, 0, 0]
        # Если зеленый канал больше красного, цвет будет зеленым
        elif (center[1] > center[2]):
            color = [0, 255, 0]
        # Иначе цвет будет красным
        else:
            color = [0, 0, 255]

        # Рисуем три прямоугольника с выбранным цветом:
        # Верхний прямоугольник
        cv2.rectangle(frame, (0 + offw, 120 + offh), (260 + offw, 160 + offh), color, -1)
        cv2.rectangle(frame, (110 + offw, 0 + offh), (150 + offw, 120 + offh), color, -1)
        cv2.rectangle(frame, (110 + offw, 160 + offh), (150 + offw, 280 + offh), color, -1)

        cv2.imshow('frame', frame)
        # Если кадр не был успешно получен или нажата клавиша "Esc" (код 27), выходим из цикла
        if cv2.waitKey(1) & 0xFF == 27:
            break
    video.release()
    cv2.destroyAllWindows()

def task9():
    # Указываем IP-адрес и порт сервера, с которого будет идти видеопоток
    ip_address = '192.168.13.103'
    port = '8080'

    # Инициализируем захват видео с заданного URL-адреса
    video = cv2.VideoCapture(f"http://{ip_address}:{port}/video")
    while True:
        # Читаем кадр из видеопотока
        ret, frame = video.read()
        # Если кадр не был успешно получен или нажата клавиша "Esc" (код 27), выходим из цикла
        if not ret or cv2.waitKey(1) & 0xFF == 27:
            break
        cv2.imshow(f'Video stream from {ip_address}:{port}', frame)
    video.release()
    cv2.destroyAllWindows()

task9()
