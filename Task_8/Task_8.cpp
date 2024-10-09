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
        }\
    }
    return low;
}

const double pi = 3.141592653589793;

double sin_taylor (double x) {
    double term = x;
    double sum = term;
    double x_squared = x * x;
    for (int n = 1; n < 20; ++n) {
        term *= -x_squared / ((2 * n) * (2 * n + 1));
        sum += term;
    }
    return sum;
}

double arcsin (double x) {
    double low, high;
    if (x == 1)
        return 1.570796326794897;
    if (x == -1)
        return -1.570796326794897;
    if (x == 0)
        return 0;
    low = -1.570796326794897;
    high = 1.570796326794897;
    while (high - low > 1e-13) {
        double mid = (high + low) / 2;
        double sin_mid = sin_taylor(mid);
        if (sin_mid <= x)
            low = mid;
        else
            high = mid;
    }
    return low;
}

double deg (double rad) {
    return (rad * 180) / pi;
}
int main(){
    double x1, x2, x3, y1, y2, y3;
    std::cout << "Введите координаты треугольника x1, y1, x2, y2, x3, y3: ";
    std::cin >> x1 >> y1 >> x2 >> y2 >> x3 >> y3;

    double a = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
    double b = sqrt((x3 - x2) * (x3 - x2) + (y3 - y2) * (y3 - y2));
    double c = sqrt((x3 - x1) * (x3 - x1) + (y3 - y1) * (y3 - y1));
    std::cout << "Длины сторон треугольника: " << a << ", " << b << ", " << c << "\n";

    double P = a + b + c;
    double p = P / 2;
    double s_g = sqrt(p * (p - a) * (p - b) * (p - c));
    double ha = s_g * 2 / a;
    double hb = s_g * 2 / b;
    double hc = s_g * 2 / c;
    std::cout << "Длины высот треугольника: " << ha << ", " << hb << ", " << hc << "\n";

    double ma = 0.5 * sqrt(2 * c * c + 2 * b * b - a * a);
    double mb = 0.5 * sqrt(2 * a * a + 2 * c * c - b * b);
    double mc = 0.5 * sqrt(2 * a * a + 2 * b * b - c * c);
    std::cout << "Длины медиан треугольника: " << ma << ", " << mb << ", " << mc << "\n";

    double ba = sqrt (c * b * (c + b + a) * (c + b - a)) / (b + c);
    double bb = sqrt (c * a * (c + a + b) * (c + a - b)) / (a + c);
    double bc = sqrt (a * b * (a + b + c) * (a + b - c)) / (b + a);
    std::cout << "Длины биссектрис треугольника: " << ba << ", " << bb << ", " << bc << "\n";

    double R = (a * b * c) / (4 * s_g);
    double r = s_g / p;
    std::cout << "Радиус описанной и вписанной окружности: " << R << ", " << r << "\n";
    double s_o = pi * R * R;
    double p_o = 2 * pi * R;
    double s_v = pi * r * r;
    double p_v = 2 * pi * r;
    std::cout << "Площадь и длина вписанной окружности: " << s_v << ", " << p_v << "\n";
    std::cout << "Площадь и длина описанной окружности: " << s_o << ", " << p_o << "\n";


    double s_h = a * ha / 2;
    double s_R = a * b * c / (4 * R);
    std::cout << "Площадь и периметр треугольника: " << s_h << ", " << P << "\n";

    double ra = arcsin(a / (2 * R));
    double rb = arcsin(b / (2 * R));
    double rc = arcsin(c / (2 * R));
    if (a >= b & a >= c)
        ra = pi - (rb + rc);
    else  if (b >= a & b >= c)
        rb = pi - (ra + rc);
    else if (c >= a & c >= b)
        rc = pi - (ra + rb);

    std::cout << "Углы в радианах: "<< ra << ", " << rb << ", "  << rc << "\n";
    std::cout << "Углы в градусах: " << deg(ra) << ", " << deg(rb) << ", "  << deg(rc) << "\n";

    return 0;
}