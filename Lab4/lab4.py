import numpy as np
import cv2

# Функция для определения угла градиента на основе направления вектора (x, y).
def angle(x, y):
    tg = y / x  # Вычисление тангенса угла.
    v1 = 0.414  # Пороговые значения для тангенса (близко к углам 22.5° и 67.5°).
    v2 = 2.414
    # Определение угла в зависимости от диапазона тангенса.
    if (x > 0 and y < 0 and tg < -v2) or (x < 0 and y < 0 and tg > v2):
        return 0  # Горизонтальное направление (0°).
    elif x > 0 and y < 0 and tg < -v1:
        return 1  # Диагональное направление (45°).
    elif (x > 0 and y < 0 and tg > -v1) or (x > 0 and y > 0 and tg < v1):
        return 2  # Вертикальное направление (90°).
    elif x > 0 and y > 0 and tg < v2:
        return 3  # Диагональное направление (135°).
    elif (x > 0 and y > 0 and tg > v2) or (x < 0 and y > 0 and tg < -v2):
        return 4  # Горизонтальное направление (180°).
    elif x < 0 and y > 0 and tg < -v1:
        return 5  # Диагональное направление (225°).
    elif x < 0 and y < 0 and tg < v2:
        return 7  # Диагональное направление (315°).
    else:
        return 6  # Вертикальное направление (270°).

# Функция для выполнения свертки изображения с фильтром (ядром).
def convolution(img, ker):
    grad = np.zeros_like(img, np.int32)  # Пустое изображение для результата свертки.
    h, w = img.shape[:2]  # Размеры изображения.
    # Применение свертки, пробегая по каждому пикселю изображения.
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            val = 0  # Результат свертки для текущего пикселя.
            # Применение 3x3 фильтра.
            for k in range(3):
                for l in range(3):
                    val += img[x + k - 1, y + l - 1] * ker[k, l]
            grad[x, y] = val  # Запись результата свертки.
    return grad

# Вспомогательная функция для проверки, превышает ли значение в соседней точке порог.
def ok(neighbour, a, gr):
    return neighbour > 0 and a >= gr

# Основная функция обработки изображения.
def task4(filename):
    img = cv2.imread(filename)  # Чтение изображения.
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Преобразование в оттенки серого.
    cv2.imshow('Original', img)  # Отображение исходного изображения.
    img_blur = cv2.GaussianBlur(img, (5, 5), 0)  # Сглаживание изображения для удаления шума.
    cv2.imshow('Blur', img_blur)  # Отображение сглаженного изображения.

    # Определение ядер (фильтров) для вычисления градиентов.
    xkernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])  # Горизонтальный фильтр Собеля.
    ykernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])  # Вертикальный фильтр Собеля.

    gradX = convolution(img, xkernel)  # Вычисление горизонтального градиента.
    gradY = convolution(img, ykernel)  # Вычисление вертикального градиента.

    grad_len = np.sqrt(np.add(np.square(gradX), np.square(gradY)))  # Длина градиента.
    max_grad_len = grad_len.max()  # Максимальная длина градиента для нормализации.
    cv2.imshow('gradients', (grad_len / max_grad_len * 255).astype(np.uint8))  # Отображение градиентов.

    # Инициализация бинарного изображения для хранения контуров.
    edges = np.zeros_like(img)
    # Нахождение локальных максимумов градиента (непрерывных контуров).
    for x in range(1, edges.shape[0] - 1):
        for y in range(1, edges.shape[1] - 1):
            ang = angle(gradX[x, y], gradY[x, y])  # Угол градиента для текущего пикселя.
            # Определение соседей вдоль направления градиента.
            if ang == 0 or ang == 4:
                neighbor1 = [x - 1, y]
                neighbor2 = [x + 1, y]
            elif ang == 1 or ang == 5:
                neighbor1 = [x - 1, y + 1]
                neighbor2 = [x + 1, y - 1]
            elif ang == 2 or ang == 6:
                neighbor1 = [x, y + 1]
                neighbor2 = [x, y - 1]
            elif ang == 3 or ang == 7:
                neighbor1 = [x + 1, y + 1]
                neighbor2 = [x - 1, y - 1]
            # Проверка на локальный максимум.
            if grad_len[x, y] >= grad_len[neighbor1[0], neighbor1[1]] and grad_len[x, y] > grad_len[neighbor2[0], neighbor2[1]]:
                edges[x, y] = 255  # Обозначение контура.

    cv2.imshow('edges_before_double_filtering', edges)  # Отображение контуров до фильтрации.

    # Двойная пороговая фильтрация (Canny-like подход).
    low_level = max_grad_len // 25  # Низкий порог.
    high_level = max_grad_len // 5  # Высокий порог.
    edges2 = edges.copy()
    for x in range(1, edges2.shape[0] - 1):
        for y in range(1, edges2.shape[1] - 1):
            if edges2[x, y] > 0:
                if grad_len[x, y] < low_level:  # Удаление слабых контуров.
                    edges2[x, y] = 0
                elif grad_len[x, y] < high_level:  # Проверка соседей для слабых контуров.
                    if not any(
                        ok(edges2[x + dx, y + dy], grad_len[x + dx, y + dy], high_level)
                        for dx in [-1, 0, 1]
                        for dy in [-1, 0, 1]
                        if dx != 0 or dy != 0
                    ):
                        edges2[x, y] = 0

    cv2.imshow('edges_filter', edges2)  # Отображение фильтрованных контуров.
    edges_library = cv2.Canny(img, 200, 300)  # Контуры с использованием встроенной функции Canny.
    cv2.imshow('edges_library', edges_library)  # Отображение контуров Canny.
    cv2.waitKey(0)  # Ожидание закрытия окон.
    cv2.destroyAllWindows()  # Закрытие всех окон.

# Запуск основной функции с заданным изображением.
task4('./Images/bRelzN7xP7.jpg')
