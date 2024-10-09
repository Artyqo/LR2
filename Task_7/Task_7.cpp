#include <iostream>

int main() {
    double a, b, c;
    int N;
    std::cout << "Введите a: ";
    std::cin >> a;
    std::cout << "Введите b: ";
    std::cin >> b;
    std::cout << "Введите c: ";
    std::cin >> c;
    std::cout << "Введите значение N: ";
    std::cin >> N;
    switch(N) {
        case 2:
            std::cout << b * c - a * a;
            break;
        case 56:
            std::cout << b * c;
        break;
        case 7:
            std::cout << a * a + c;
        break;
        case 3:
            std::cout << a - b * c;
        break;
        default:
            std::cout << (a + b) * (a + b) * (a + b);
        break;
    }
    return 0;
}