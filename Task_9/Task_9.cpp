#include <iostream>
#include <cmath>


int main() {
    double x, z, a, b, f, y;
    std::string X_Value, F_Value;
    int N;
    std::cout << "Введите значение z: ";
    std::cin >> z;
    std::cout << "Введите значение a: ";
    std::cin >> a;
    std::cout << "Введите значение b: ";
    std::cin >> b;
    std::cout << "Введите значение N (1, 2 or 3): ";
    std::cin >> N;
    if (z>=1) {
        x = z + log(z);
        X_Value = "z + log(z)";
    } else {
        x = pow(z, 3) + 0.2;
        X_Value = "z^3 + 0.2";
    }
    switch (N) {
        case 1:
            f = 2 * x;
            F_Value = "2x";
            break;
        case 2:
            f = pow(x, 3);
            F_Value = "x^3";
            break;
        case 3:
            f = x / 3;
            F_Value = "x/3";
            break;
    }
    y = 2 * a * pow(cos(pow(x, 2)), 3) + pow(sin(pow(x, 3)), 2) - b * f;
    std::cout << "Результат:" << y << "\n";
    std::cout << "Результат получился таким, т.к. при z = " << z << " переменной x было присвоено значение: " << X_Value << "." << "\n";
    std::cout << "Также на результат повлияло значение N, при котором функция f(x) приняла значение: " << F_Value << ".";
    return 0;
}