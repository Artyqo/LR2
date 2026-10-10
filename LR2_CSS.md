# ЛР2 (CSS) — где что реализовано

Вариант 4 «Турагентство» (сайт «Глобус Тревел», проект `travel-agency/`).
Сторонние CSS-библиотеки не подключены (Bootstrap и т.п. нет), все inline-стили ЛР1 вынесены во внешние файлы:

| Файл | Назначение |
|---|---|
| `static/agency/css/style.css` | общие стили: переменные, шрифты, фон, ссылки, навигация, кнопки, формы, таблицы, списки, цитаты, прелоадер, медиа-запросы |
| `static/agency/css/pages.css` | стили отдельных страниц (главная, каталог, «О компании», новости, FAQ, контакты, политика, вакансии, отзывы, промокоды, прайс-лист…) |
| `static/agency/css/animation.css` | анимация главной страницы (подключается только на главной) |
| `static/agency/img/cert-border.svg` | графический файл рамки сертификата (`border-image`) |
| `static/agency/img/bg-pattern.svg`, `logo-mark.svg`, `check.svg` | фон сайта, знак логотипа / водяной знак, маркер списка |

## Селекторы
| Требование | Пример |
|---|---|
| элементов | `body`, `h1`, `blockquote`, `kbd`, `pre` (style.css, разд. 1, 11) |
| атрибутов: начинается с | `a[href^="mailto:"]`, `a[href^="tel:"]`, `.main a[href^="http"]` |
| атрибутов: заканчивается на | `a[href$=".pdf"]` (справка → «Памятка туриста») |
| атрибут с определённым значением | `[aria-current="page"]` (текущий пункт меню), `input[type="checkbox"]`, `a[target="_blank"]`, `.review__rating[data-rating="4"]` |
| классов | `.btn`, `.card`, `.tour-card` … |
| объединение (AND) | `.btn.btn--small`, `input[type="checkbox"]:checked`, `.form-control:out-of-range` |
| потомков / дочерних | `.site-nav .site-nav__link`, `.site-nav__list > li`, `section > h2`; соседний `li + li::before`, `tbody + tbody` |

## Псевдоклассы
| Требование | Где |
|---|---|
| ссылки `:link :visited :hover :active`, фокус `:focus :focus-visible` | style.css, разд. 2; поля форм `.form-control:focus` |
| первый / последний / n-й в списке | `.timeline__item:first-child / :last-child / :nth-child(even)` («О компании»), `.list-steps`, `.partner:nth-child(5n+2)` |
| первый / последний / n-й в таблице | `.table tbody tr:nth-child(even)`, `.table--ranking tr:first-child / :nth-child(2) / :last-child` (статистика) |
| доступные / обязательные / заблокированные | `.form-control:enabled`, `:required` (жёлтая полоса), `:disabled` (штриховка) — «Заявка на подбор» (поле «Валюта бюджета»), «Отзывы» (поле «Автор»), корзина (кнопки ±) |
| вне диапазона | `.form-control:out-of-range` + подсказка `.range-hint` — «Количество взрослых» > 10, время звонка, макс. цена в каталоге |
| включённые флажки и переключатели | `input[type="checkbox"]:checked`, `input[type="radio"]:checked`, `.choice input:checked + span` |
| кавычки по языку цитаты | `q:lang(ru/en/de/fr) { quotes: … }` — «Справка» → «Цитаты и отзывы» |
| дополнительно | `:target` (политика), `:user-invalid`, `:placeholder-shown`, `:empty`, `:where()` |

## Псевдоэлементы
| Требование | Где |
|---|---|
| первая буква / строка абзаца | буквица `.article__body p:first-child::first-letter` (полная новость); `::first-line` капителью — «О компании» → «Кто мы», стихотворение в «Справке» |
| контент в начале и конце фрагмента | `::before` ✉/☎/📄 у ссылок, `(PDF)` и `↗` через `::after`, значки сезонов у климата, 🥇🥈🥉 в рейтинге, линии у заголовков главной |
| маркеры — символы Юникода | `.list-planes { list-style-type: "✈ " }`, `.list-unicode li::before { content: "✔" }` (политика) |
| выделение текста | `::selection` (своё у сертификата) |

## Шрифты, текст, фон, курсор
* Основной шрифт — **Nunito** из Google Fonts; альтернативные — `"Segoe UI", Tahoma, Arial`; семейство — `sans-serif` (`--font-main`). Плюс Montserrat (заголовки), Comfortaa (название компании), PT Serif (сертификат, статьи), PT Mono (реквизиты).
* Текст (`.prose`, pages.css): поля/отступы, `text-indent` (красная строка), `line-height`, `word-spacing`, `letter-spacing`, `hyphens`, `overflow-wrap`, `text-align: justify`; `text-transform: uppercase` у заголовков разделов; капитель `font-variant: small-caps` (реквизиты, первая строка), `all-small-caps` у `abbr`. Перенос/разрыв — блок `.break-demo--css` в «Справке».
* Фон сайта — `body`: SVG-узор + градиент, `background-attachment: fixed`.
* Курсор: `pointer` у кнопок, `not-allowed` у заблокированных, `alias` у «Очистить», `copy` у промокода, `help` у элементов с `title`, `grab` у draggable, `ew-resize` у ползунка.

## Медиа-запросы
По ширине: `min-width: 1400px`, `max-width: 1100 / 992 / 768 / 600px` (на ≤768px меню сворачивается в кнопку «Меню» без JS — `:checked ~`).
По высоте: `max-height: 520px` (навигация не закрепляется, анимация ниже), `min-height: 1000px`, `min-height: 900px` (анимация выше).
Плюс `prefers-reduced-motion` и `print`.

## Страницы
| Страница | Что сделано |
|---|---|
| Каталог (`/tours/`, главная) | **CSS Grid**: `.catalog` — `repeat(auto-fill, minmax(250px, 1fr))`, карточка — `grid-template-areas`; на главной сетка 3×3, первая горящая путёвка — блок 2×2 |
| Главная — партнёры | круглые блоки `.partner__link`: `border-radius: 50%`, ширина 150px, у каждого свой цвет, тип (`solid/dashed/dotted/double/ridge`) и толщина рамки, `box-shadow` |
| Название компании | `.brand__name`: шрифт Comfortaa, `font-kerning: normal`, `font-feature-settings: "kern"`, `letter-spacing` |
| Главная — последняя статья | `position: relative` у карточки; `absolute` — картинка, стикер с датой, лента «Новое» (`rotate(45deg)`), растянутая ссылка `::after`; `z-index` |
| Навигация | `.site-nav { position: sticky; top: 0 }` — фиксируется при прокрутке |
| О компании — логотип | `transform: rotate() rotateY() scale()`, при наведении поворот на 360° |
| О компании — сертификат | `border-image` из `cert-border.svg` с префиксами `-webkit-/-moz-/-o-`; градиенты; фоновое изображение-водяной знак (`::before`, `z-index: -1`); печать поверх текста (`z-index: 2`); шрифт PT Serif, выравнивание по центру/справа |
| О компании — прочее | история — лента-таймлайн, реквизиты — моноширинный PT Mono + капитель, видео в «рамке» с тенью, `aspect-ratio` |
| Новости | `white-space: nowrap; overflow: hidden; text-overflow: ellipsis` для краткого содержания; полная статья — `columns: 2 260px`, `column-rule` |
| Словарь / FAQ | `details/summary` со своим маркером «+», нумерацией `counter()`, датой и анимацией раскрытия |
| Контакты | **Flexbox** внутри карточки сотрудника: фото / сведения / контакты (`flex`, `flex-wrap`, `align-items`) |
| Политика конфиденциальности | «бланк» с красной линией поля, номера разделов CSS-счётчиком, липкое оглавление, подсветка `:target` |
| Вакансии | **float/clear**: блоки `float: left` в два столбца, `:nth-child(odd) { clear: left }`, номер `float: left`, зарплата `float: right`, `clearfix` и `clear: both` у подвала |
| Отзывы | форма: системные шрифты по типу компонента — `font: caption` (кнопки), `menu` (список), `message-box` (поле, textarea), `small-caption` (подписи), `status-bar` (строка состояния) + псевдоклассы |
| Промокоды | списки: действующие — «билеты» с надрезами, архив — `list-style-type: upper-roman; list-style-position: inside`, условия — `list-style-image: url(check.svg)` |
| Прайс-лист (таблицы) | `border-collapse: collapse`; пустые ячейки (`td:empty`, колонка «Ближайший вылет») со штриховкой; `caption-side: top`; `text-align` + `vertical-align`; таблица по центру (`margin: auto`); строки (`nth-child`, `:hover`), столбцы (`<col>`), группы стран (`tbody + tbody`) |

## Анимация и прелоадер (вариант 4)
* **Главная** (`includes/hero_animation.html` + `animation.css`): блок 100% × 340px, цикл 18 с.
  0–6 с — небо с облаками: человек пролетает на самолёте с баннером «ГЛОБУС ТРЕВЕЛ»;
  6–12 с — море с волнами и чайками: человек машет с палубы корабля «ГЛОБУС ТРЕВЕЛ»;
  12–18 с — закат, пляж: человек едет на кабриолете по дороге среди качающихся пальм.
  Сцены используют одни `@keyframes` со сдвигом через отрицательный `animation-delay`.
* **Прелоадер** «вращение и изменение размера» (`.preloader__ring`, `@keyframes preloader-spin-scale`: `rotate()` + `scale()`), без JS, размещён внизу каждой страницы.
