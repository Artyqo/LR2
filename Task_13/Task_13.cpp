#include <iostream>

void showValues(int step, int a, int b) {
    std::cout << "Шаг " << step << ": a = " << a << ", b = " << b << "\n";
}

int main() {
    int a, b;

    // Запрос чисел у пользователя
    std::cout << "Введите первое целое число (a): ";
    std::cin >> a;
    std::cout << "Введите второе целое число (b): ";
    std::cin >> b;

    // Изначальные значения
    showValues(0, a, b);

    // Шаг 1: Обмен значениями
    int step = 1;
    std::swap(a, b);
    showValues(step, a, b);

    // Шаг 2: Увеличение a на 1
    step++;
    a += 1;
    showValues(step, a, b);

    // Шаг 3: Удвоение b
    step++;
    b *= 2;
    showValues(step, a, b);

    return 0;
}