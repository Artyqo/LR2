#include <iostream>

int main() {
    double b1, q, S;
    int n;
    std::cout << "Введите первый член геометрической прогрессии: ";
    std::cin >> b1;
    std::cout << "Введите ваш номер в журнале: ";
    std::cin >> n;
    q = 1./(n+1);
    S = b1/(1-q);
    std::cout << "Сумма всех членов убывающей геометрической прогрессии равна: " << S;
    return 0;
}