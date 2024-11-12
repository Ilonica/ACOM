import cv2
import numpy as np

def task1():
    # инициализация объекта захвата видео
    video = cv2.VideoCapture(0)
    # устанавливаем ширину и высоту кадра с помощью флага
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = video.read()

        # переводим кадры в формат HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('HSV', hsv)

        # прерываем цикл при нажатии esc
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # освобождаем ресурсы
    video.release()
    cv2.destroyAllWindows()

def task2():
    # инициализация объекта захвата видео
    video = cv2.VideoCapture(0)
    # устанавливаем ширину и высоту кадра с помощью флага
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = video.read()

        # нижняя и верхняя граница оттенка, смещение на 10 градусов
        h_min = 128 - (255 / 360 * 10)
        h_max = 128 + (255 / 360 * 10)
        # нижняя граница насыщенности, 65% от 255
        s_min = 255 // 100 * 65
        s_max = 255
        # нижняя граница яркости, 65% от 255
        v_min = 255 // 100 * 65
        v_max = 255

        # нижний и верхний пороги для цветовой фильтрации (левая и правая граница пропускаемого цвета)
        min_p = (h_min, s_min, v_min)
        max_p = (h_max, s_max, v_max)

        # переводим кадры в формат HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # сдвигаем оттенок на 128 и берем остаток от деления на 255 для сохранения диапазона
        hsv[:, :, 0] = (hsv[:, :, 0] + 128) % 255

        # создаем маску, выделяя области изображения, которые попадают в заданный диапазон HSV
        video_mask = cv2.inRange(hsv, min_p, max_p)
        # применяем маску
        video_m = cv2.bitwise_and(frame, frame, mask=video_mask)

        cv2.imshow('Treshold', video_m)

        # прерываем цикл при нажатии esc
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # освобождаем ресурсы
    video.release()
    cv2.destroyAllWindows()



def task3():
    # инициализация объекта захвата видео
    video = cv2.VideoCapture(0)
    # устанавливаем ширину и высоту кадра с помощью флага
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = video.read()

        # нижняя и верхняя граница оттенка, смещение на 10 градусов
        h_min = 128 - (255 / 360 * 10)
        h_max = 128 + (255 / 360 * 10)
        # нижняя граница насыщенности, 65% от 255
        s_min = 255 // 100 * 65
        s_max = 255
        # нижняя граница яркости, 65% от 255
        v_min = 255 // 100 * 65
        v_max = 255

        # нижний и верхний пороги для цветовой фильтрации (левая и правая граница пропускаемого цвета)
        min_p = (h_min, s_min, v_min)
        max_p = (h_max, s_max, v_max)

        # переводим кадры в формат HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # сдвигаем оттенок на 128 и берем остаток от деления на 255 для сохранения диапазона
        hsv[:, :, 0] = (hsv[:, :, 0] + 128) % 255

        # создаем маску, выделяя области изображения, которые попадают в заданный диапазон HSV
        video_mask = cv2.inRange(hsv, min_p, max_p)

        # создаем ядро для морфологических операций, с матрицей размера 5x5
        kernel = np.ones((5, 5), np.uint8)

        # операция "открытие", cначала выполняется эрозия, затем дилатация (даляет мелкие шумы на маске (белые точки))
        open_video = cv2.morphologyEx(video_mask, cv2.MORPH_OPEN, kernel)
        # операция "закрытие", заполняет разрывы внутри объектов на маске (черные точки внутри белых областей)
        close_video = cv2.morphologyEx(video_mask, cv2.MORPH_CLOSE, kernel)

        cv2.imshow('Open', open_video)
        cv2.imshow('Close', close_video)

        # прерываем цикл при нажатии esc
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # освобождаем ресурсы
    video.release()
    cv2.destroyAllWindows()

def task5():
    # инициализация объекта захвата видео
    video = cv2.VideoCapture(0)
    # устанавливаем ширину и высоту кадра с помощью флага
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    lastX = -1
    lastY = -1


    while True:
        ret, frame = video.read()
        h, w, c = frame.shape
        # инициализация пустого изображения для отслеживания пути (следа)
        path = np.zeros((h, w, 3), np.uint8)

        # нижняя и верхняя граница оттенка, смещение на 10 градусов
        h_min = 128 - (255 / 360 * 10)
        h_max = 128 + (255 / 360 * 10)
        # нижняя граница насыщенности, 65% от 255
        s_min = 255 // 100 * 65
        s_max = 255
        # нижняя граница яркости, 65% от 255
        v_min = 255 // 100 * 65
        v_max = 255

        # нижний и верхний пороги для цветовой фильтрации (левая и правая граница пропускаемого цвета)
        min_p = (h_min, s_min, v_min)
        max_p = (h_max, s_max, v_max)

        # переводим кадры в формат HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
        # сдвигаем оттенок на 128 и берем остаток от деления на 255 для сохранения диапазона
        hsv[:, :, 0] = (hsv[:, :, 0] + 128) % 255

        # создаем маску, выделяя области изображения, которые попадают в заданный диапазон HSV
        video_mask = cv2.inRange(hsv, min_p, max_p)

        # создаем ядро для морфологических операций, с матрицей размера 5x5
        kernel = np.ones((5, 5), np.uint8)

        # операция "открытие", cначала выполняется эрозия, затем дилатация (даляет мелкие шумы на маске (белые точки))
        open_video = cv2.morphologyEx(video_mask, cv2.MORPH_OPEN, kernel)
        # операция "закрытие", заполняет разрывы внутри объектов на маске (черные точки внутри белых областей)
        close_video = cv2.morphologyEx(open_video, cv2.MORPH_CLOSE, kernel)

        # применяем маску
        video_m = cv2.bitwise_and(frame, frame, mask=close_video)

        # вычисление моментов изображения для нахождения центра массы
        moments = cv2.moments(close_video, True)
        # зерновые моменты - суммы значений пикселей в различных степенях
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']
        # если площадь объекта больше порога (1000 пикселей), вычисляем его центр
        if dArea > 1000:
            # X-координата центра объекта
            posX = int(dM10 / dArea)
            # Y-координата центра объекта
            posY = int(dM01 / dArea)
            # отображение центра объекта на кадре
            cv2.circle(frame, (posX, posY), 10, (0, 0, 255), -1)

            # построение прямоугольника вокруг найденного объекта
            x, y, w, h = cv2.boundingRect(close_video)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # рисуем линию, которая соединяет текущую позицию с предыдущей, чтобы отобразить след
            if lastX >= 0 and lastY >= 0:
                cv2.line(path, (lastX, lastY), (posX, posY), (0, 0, 255), 2)

            # обновляем последнюю позицию X и Y
            lastX = posX
            lastY = posY
        else:
            # если объект не найден, сбрасываем позици
            lastX = -1
            lastY = -1

        # добавляем след на кадр
        frame = cv2.add(frame, path)

        cv2.imshow('Result', frame)
        cv2.imshow('Threshold', video_m)

        # прерываем цикл при нажатии esc
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # освобождаем ресурсы
    video.release()
    cv2.destroyAllWindows()

task5()
