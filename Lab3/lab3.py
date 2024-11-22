import numpy as np
import cv2

def gauss(x, y, a, b, sigma):
    o = 2 * pow(sigma, 2)
    # функция Гаусса (плотность распределения) для двумерной случайной величины
    return 1/(o * np.pi) * np.e **(-1 * ((x-a)* (x-a) +(y-b)* (y-b))/o)

def kernel(ksize, sigma):
    kernel = np.zeros((ksize, ksize))
    # математическое ожидание двумерной случайной величины (координаты центрального элемента матрицы)
    a = b = ksize//2 + 1
    for i in range(ksize):
        for j in range(ksize):
            kernel[i, j] = gauss(i+1, j+1, a, b, sigma)

    return kernel

def task1_2():
    kernels = [(3, 5), (5, 5), (7, 5)]
    for ksize, sigma in kernels:
        kernel = kernel(ksize, sigma)
        print(f"Размер ядра: {ksize}, среднеквадратичное отклонение: {sigma}")
        print(kernel)

        # Нормируем ядро
        kernel /= np.sum(kernel)
        print("Матрица ядра после нормирования:")
        print(kernel)
        print(f"Сумма элементов нормированного ядра: {np.sum(kernel)}\n")


def gaussian_blur(img, ksize, sigma):

    # нормирование матрицы таким образом, чтобы сумма элементов равнялась 1
    kernel = kernel(ksize, sigma)
    kernel /= np.sum(kernel)

    # cоздание копии изображения для сохранения результата
    blurred = img.copy()
    # извлечение высоты и ширины изображения
    h, w = img.shape[:2]
    # половина размера ядра, используется для обработки краёв, чтобы не выйти за границы изображения
    half_kernel_size = int(ksize // 2)

    # примененяем свёртку Гаусса ко всем внутренним пикселям изображения
    # y, x — координаты текущего пикселя изображения
    for y in range(half_kernel_size, h - half_kernel_size):
        for x in range(half_kernel_size, w - half_kernel_size):
            val = 0
            # k, l индексы смещения в ядре свертки относительно центрального пикселя
            for k in range(-(ksize // 2), ksize // 2 + 1):
                for l in range(-(ksize // 2), ksize // 2 + 1):
                    # операция свертки - суммируется взвешенное влияние соседей, и это значение становится новым для пикселя (y, x)
                    val += img[y + k, x + l] * kernel[k + half_kernel_size, l + half_kernel_size]
            blurred[y, x] = val

    return blurred

task1_2()

img = cv2.imread('seeu.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow('Original', img)
cv2.imwrite(f'noblur.jpg', img)

# размерность матрицы свертки
ksize= 5
# среднеквадратичное отклонение
sigma = 9

img_blur_mine = gaussian_blur(img, ksize, sigma)
cv2.imshow(f'Blurred (kernel_size={ksize}, std_deviation={sigma})', img_blur_mine)
cv2.imwrite(f'blur_{ksize}_{sigma}.jpg', img_blur_mine)

# спользуем встроенную библиотеку для размытия
img_blur_lib = cv2.GaussianBlur(img, (11,11), 5)
cv2.imshow('Blurred by library', img_blur_lib)

cv2.imwrite(f'blur_lib_11_5.jpg', img_blur_lib)

cv2.waitKey(0)
cv2.destroyAllWindows()
