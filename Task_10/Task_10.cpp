#include <iostream>

double sqrt (double x) {
    double low, high;
    if (x >= 1) {
        low = 1;
        high = x;
    }
    else {
        low = x;
        high = 1;
    }
    while (high - low > 1e-13) {
        double mid = (high + low) / 2;
        if (mid*mid >= x) {
            high = mid;
        }
        else {
            low = mid;
        }
    }
    return low;
}

int main() {
    double x1, y1, x2, y2, r, R;

    std::cout << "Введите координаты центра первого круга (x1, y1): ";
    std::cin >> x1 >> y1;
    std::cout << "Введите значение радиуса r первого круга: ";
    std::cin >> r;
    std::cout << "Введите координаты центра второго круга (x2, y2): ";
    std::cin >> x2 >> y2;
    std::cout << "Введите значение радиуса r первого круга: ";
    std::cin >> R;

    double L = sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2));
    std::cout << L;
    if (L <= R - r) {
        std::cout << "Да";
    } else if (L <= r - R) {
        std::cout << "Да, но справедливо обратное для двух фигур";
    } else if (L <= r + R) {
        std::cout << "Фигуры пересекаются";
    } else {
        std::cout << "Ни одно условие не выполнено";
    }

    return 0;
}