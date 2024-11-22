#include <iostream>
#include <vector>
#include <cmath>
#include <opencv2/opencv.hpp>
#define M_PI 3.14159265358979323846

using namespace std;

// Функция Гаусса для двумерной случайной величины
double gauss(int x, int y, int a, int b, double sigma) {
    double o = 2 * pow(sigma, 2);
    return 1 / (o * M_PI) * exp(-1 * ((x - a) * (x - a) + (y - b) * (y - b)) / o);
}

// Генерация матрицы ядра Гаусса
vector<vector<double>> makeKernel(int ksize, double sigma) {
    vector<vector<double>> kernel(ksize, vector<double>(ksize));
    int a = ksize / 2 + 1; // Центральная координата матрицы ядра
    double sum = 0.0;

    // Заполнение ядра значениями Гаусса
    for (int i = 0; i < ksize; ++i) {
        for (int j = 0; j < ksize; ++j) {
            kernel[i][j] = gauss(i + 1, j + 1, a, a, sigma);
            sum += kernel[i][j];
        }
    }

    // Нормирование ядра (сумма элементов = 1)
    for (int i = 0; i < ksize; ++i) {
        for (int j = 0; j < ksize; ++j) {
            kernel[i][j] /= sum;
        }
    }

    return kernel;
}

// Применение размытия Гаусса к изображению через свертку
cv::Mat gaussianBlur(const cv::Mat& img, const vector<vector<double>>& kernel) {
    int kernelSize = static_cast<int>(kernel.size()); // Преобразование типа для совместимости
    int halfKernel = kernelSize / 2;

    cv::Mat blurred = img.clone();

    for (int y = halfKernel; y < img.rows - halfKernel; ++y) {
        for (int x = halfKernel; x < img.cols - halfKernel; ++x) {
            double val = 0.0;

            // Применяем ядро свертки
            for (int k = -halfKernel; k <= halfKernel; ++k) {
                for (int l = -halfKernel; l <= halfKernel; ++l) {
                    val += img.at<uchar>(y + k, x + l) * kernel[k + halfKernel][l + halfKernel];
                }
            }

            blurred.at<uchar>(y, x) = static_cast<uchar>(val);
        }
    }

    return blurred;
}

int main() {
    // Загружаем изображение
    cv::Mat img = cv::imread("C:/Users/User/source/repos/Lab3/seeu.jpg", cv::IMREAD_GRAYSCALE);

    if (img.empty()) {
        cerr << "Ошибка: Не удалось загрузить изображение!" << endl;
        return -1;
    }

    // Размер ядра и стандартное отклонение
    int ksize = 5;
    double sigma = 9.0;

    // Создаем ядро Гаусса
    vector<vector<double>> kernel = makeKernel(ksize, sigma);

    // Применяем размытие через свертку
    cv::Mat imgBlurred = gaussianBlur(img, kernel);

    // Сохраняем и показываем результаты
    cv::imshow("Original Image", img);
    cv::imshow("Blurred Image (Custom Gaussian)", imgBlurred);
    cv::imwrite("custom_gaussian_blur.jpg", imgBlurred);

    // Используем встроенную функцию OpenCV для сравнения
    cv::Mat imgBlurLib;
    cv::GaussianBlur(img, imgBlurLib, cv::Size(11, 11), 5.0);
    cv::imshow("Blurred Image (OpenCV)", imgBlurLib);
    cv::imwrite("opencv_gaussian_blur.jpg", imgBlurLib);

    cv::waitKey(0);
    return 0;
}
