// Слайдер баннеров на главной. Без JS показывается первый баннер.
// Слайды переключаются атрибутом hidden, внешний вид задан в pages.css.
document.addEventListener('DOMContentLoaded', function () {
    var box = document.querySelector('[data-banner]');
    if (!box) { return; }

    var slides = box.querySelectorAll('[data-banner-slide]');
    if (slides.length < 2) { return; }

    var current = 0;
    var timer = null;

    function show(index) {
        slides[current].hidden = true;
        current = (index + slides.length) % slides.length;
        slides[current].hidden = false;
    }

    function start() { timer = setInterval(function () { show(current + 1); }, 5000); }
    function stop() { clearInterval(timer); }

    box.querySelector('[data-banner-prev]').addEventListener('click', function () { show(current - 1); });
    box.querySelector('[data-banner-next]').addEventListener('click', function () { show(current + 1); });
    box.addEventListener('mouseenter', stop);
    box.addEventListener('mouseleave', start);

    start();
});
