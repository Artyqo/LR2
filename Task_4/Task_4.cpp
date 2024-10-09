#include<iostream>

int main() {
    int x, y;
    double a, b, c, k;
    std::cout << "Введите значение x: ";
    std::cin >> x;
    std::cout << "Введите значение y: ";
    std::cin >> y;
    std::cout << "Введите значение a: ";
    std::cin >> a;
    std::cout << "Введите значение b: ";
    std::cin >> b;
    std::cout << "Введите значение c: ";
    std::cin >> c;
    std::cout << "Введите значегие k: ";
    std::cin >> k;
    if (x>y) {
        y = 0;
        std::cout << "x = " << x << "\n";
        std::cout << "y = " << y << "\n";
    } else if (x==y) {
        x = 0;
        y = 0;
        std::cout << "x = " << x << "\n";
        std::cout << "y = " << y << "\n";
    } else {
        x = 0;
        std::cout << "x = " << x << "\n";
        std::cout << "y = " << y << "\n";
    }
    if (a > b & a > c) {
        a -= k;
        std::cout << "a = " << a << "\n";
        std::cout << "b = " << b << "\n";
        std::cout << "c = " << c << "\n";
    } else if (b > a & b > c) {
        b -= k;
        std::cout << "a = " << a << "\n";
        std::cout << "b = " << b << "\n";
        std::cout << "c = " << c << "\n";
    } else {
        c -= k;
        std::cout << "a = " << a << "\n";
        std::cout << "b = " << b << "\n";
        std::cout << "c = " << c << "\n";
    }
    return 0;
}