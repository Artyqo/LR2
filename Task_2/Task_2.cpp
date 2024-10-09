#include <iostream>
#include <gtest/gtest.h>

int main() {
    double x,y,z;
    std::cout << "Введите значение первой стороны: ";
    std::cin >> x;
    std::cout << "Введите значение второй стороны: ";
    std::cin >> y;
    std::cout << "Введите значение второй стороны: ";
    std::cin >> z;
    if (x+y>z & x+z>y & y+z>x) {
        std::cout << "Такой треугольник существует!";
    } else {std::cout << "Такого треугольника не существует.";}
    return 0;
}