#include <iostream>

int main() {
    int h1, h2, min1, min2, total_minutes;
    std::cout << "Введите время начала работы (часы, минуты): ";
    std::cin >> h1 >> min1;
    std::cout << "Введите время конца работы (часы, минуты): ";
    std::cin >> h2 >> min2;
    int minutes_start = h1 * 60 + min1;
    int minutes_end = h2 * 60 + min2;
    total_minutes = minutes_end - minutes_start;
    if (total_minutes < 0) {
        total_minutes += 24 * 60;
    }
    int hours = total_minutes / 60;
    int minutes = total_minutes % 60;
    std::cout << "Студент решал задачи на протяжении " << hours << "ч. " << minutes << "мин.";
}