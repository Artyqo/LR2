#include <iostream>
#include "gtest/gtest.h"

int main() {
    double x, a, b, c;
    std::cout << "Введите значение x: ";
    std::cin >> x;
    c = x*x;
    a = x*(23*c+32);
    b = 69*c+8;
    std::cout << "Значение выражения 23х^3 + 69x^2 + 32x + 8 равно: " << a + b << "\n";
    std::cout << "Значение выражения -23х^3 + 69^2 - 32x + 8 равно: " << b - a << "\n";
    return 0;
}