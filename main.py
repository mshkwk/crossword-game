from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.session import run_js, eval_js 
import random
import time
import threading

# ================= БАНК ВОПРОСОВ =================
BANK = {
    "Компьютер и его устройство": {
        "Базовый": [
            ("ПРОЦЕССОР", "Главное устройство обработки данных в компьютере?"),
            ("КЛАВИАТУРА", "Устройство для ввода текста?"),
            ("ПРИНТЕР", "Устройство для вывода информации на бумагу?"),
            ("МОНИТОР", "Устройство для отображения информации?"),
            ("МЫШЬ", "Устройство управления курсором?"),
        ],
        "Средний": [
            ("ОПЕРАТИВНАЯ", "Память, в которой данные хранятся только во время работы компьютера?"),
            ("НАКОПИТЕЛЬ", "Как называется память для долговременного хранения данных?"),
            ("СМАРТФОН", "Карманный компьютер с сенсорным экраном?"),
            ("СУПЕРКОМПЬЮТЕРЫ", "Самые мощные компьютеры в мире?"),
            ("ЧАСТОТА", "Характеристика процессора, измеряемая в гигагерцах?"),
        ],
        "Повышенный": [
            ("ПАРАЛЛЕЛИЗМ", "Одновременное выполнение нескольких вычислительных процессов?"),
            ("ЧЕТВЕРТОЕ", "Поколение компьютеров, основанное на микропроцессорах?"),
            ("СКАНЕР", "Устройство ввода отпечатка пальца?"),
            ("БИОМЕТРИЯ", "Система распознавания личности по физическим признакам?"),
            ("РАЗРЯДНОСТЬ", "Количество битов, обрабатываемых процессором за один раз?"),
        ]
    },
    "Программы и данные": {
        "Базовый": [
            ("ФАЙЛ", "Именованная область хранения данных?"),
            ("ПАПКА", "Место хранения файлов?"),
            ("СИСТЕМА", "Набор программ, управляющих компьютером?"),
            ("МЕНЕДЖЕР", "Программа для поиска файлов?"),
            ("ВИРУС", "Вредоносная программа?"),
        ],
        "Средний": [
            ("ПУТЬ", "Полное название папок, ведущих к файлу?"),
            ("АРХИВАЦИЯ", "Процесс уменьшения размера файла?"),
            ("АНТИВИРУС", "Программа для борьбы с вирусами?"),
            ("ПРИКЛАДНОЕ", "Программное обеспечение для решения пользовательских задач?"),
            ("СИСТЕМНОМУ", "Операционная система относится к какому виду ПО?"),
        ],
        "Повышенный": [
            ("ФАЙЛОВАЯСИСТЕМА", "Совокупность правил организации хранения файлов?"),
            ("СВОБОДНОЕ", "Бесплатное программное обеспечение с открытым кодом?"),
            ("ТРАНСЛЯТОР", "Программа для создания других программ?"),
            ("АРХИВ", "Файл, содержащий несколько файлов в сжатом виде?"),
            ("ОХРАНОЙ", "Защита программ законом называется правовой ...?"),
        ]
    },
    "Компьютерные сети": {
        "Базовый": [
            ("ИНТЕРНЕТ", "Всемирная компьютерная сеть?"),
            ("БРАУЗЕР", "Программа для просмотра веб-страниц?"),
            ("САЙТ", "Набор веб-страниц?"),
            ("ПИСЬМО", "Электронное сообщение?"),
            ("ВЕБСТРАНИЦА", "Документ в интернете?"),
        ],
        "Средний": [
            ("ПОИСКОВИК", "Сервис для поиска информации в сети?"),
            ("ЭТИКЕТ", "Правила поведения в сети?"),
            ("ИЗОБРАЖЕНИЕ", "Визуальное представление какого-либо объекта?"),
            ("ВИДЕОСВЯЗЬ", "Средство общения через Интернет с видео?"),
            ("ДОСТОВЕРНОСТЬ", "Проверка информации на истинность?"),
        ],
        "Повышенный": [
            ("URL", "Уникальный адрес веб-ресурса?"),
            ("СЕТЬ", "Совокупность компьютеров, соединённых для обмена данными?"),
            ("БЕЗОПАСНОСТЬ", "Система мер по защите цифровых данных?"),
            ("ЧАТ", "Обмен сообщениями в режиме реального времени?"),
            ("КОММУНИКАЦИЯ", "Процесс передачи информации между устройствами?"),
        ]
    },
    "Информация и процессы": {
        "Базовый": [
            ("ИНФОРМАЦИЯ", "Сведения об объектах и явлениях окружающего мира?"),
            ("ПРИЕМ", "Процесс получения информации?"),
            ("ХРАНЕНИЕ", "Процесс сохранения информации?"),
            ("ПЕРЕДАЧА", "Процесс отправки информации?"),
            ("ОБРАБОТКА", "Процесс изменения информации?"),
        ],
        "Средний": [
            ("ДИСКРЕТНОСТЬ", "Представление непрерывной информации отдельными значениями?"),
            ("ПРОЦЕСС", "Последовательность действий над данными?"),
            ("ДАННЫЕ", "Информация, представленная для обработки компьютером?"),
            ("ДОСТОВЕРНОСТЬ", "Характеристика информации, отражающая её истинность?"),
            ("АКТУАЛЬНОСТЬ", "Свойство информации быть полезной в данный момент?"),
        ],
        "Повышенный": [
            ("ПРЕОБРАЗОВАНИЕ", "Информационный процесс, связанный с изменением содержания данных?"),
            ("ОПИСАНИЕ", "Представление объекта с помощью набора данных?"),
            ("АВТОМАТИЗИРОВАННАЯ", "Система, способная автоматически обрабатывать данные?"),
            ("ИНФОРМАТИВНОСТЬ", "Количество сведений, содержащихся в сообщении?"),
            ("КОММУНИКАЦИЯ", "Процесс обмена информацией между источником и получателем?"),
        ]
    },
    "Представление информации": {
        "Базовый": [
            ("БИТ", "Минимальная единица информации?"),
            ("БАЙТ", "8 бит это?"),
            ("АЛФАВИТ", "Набор символов языка?"),
            ("ДВОИЧНЫЙ", "Символы 0 и 1 образуют ... алфавит?"),
            ("КОДИРОВАНИЕ", "Процесс перевода информации в код?"),
        ],
        "Средний": [
            ("МОЩНОСТЬ", "Количество символов в алфавите?"),
            ("ASCII", "Таблица кодирования символов?"),
            ("UNICODE", "Современный стандарт кодирования символов?"),
            ("ДЕКОДИРОВАНИЕ", "Обратный процесс кодированию?"),
            ("КИЛОБАЙТ", "Единица объёма информации, равная 1024 байтам?"),
        ],
        "Повышенный": [
            ("RGB", "Цветовая модель компьютера?"),
            ("ПИКСЕЛЬ", "Минимальный элемент растрового изображения?"),
            ("РАСТРОВОЕ", "Представление изображения с помощью точек?"),
            ("ВЕКТОРНОЕ", "Представление изображения с помощью геометрических объектов?"),
            ("ГЛУБИНА", "Количество бит, используемых для хранения цвета?"),
        ]
    },
    "Текстовые документы": {
        "Базовый": [
            ("РЕДАКТОР", "Программа для работы с текстом?"),
            ("АБЗАЦ", "Отступ первой строки?"),
            ("ШРИФТ", "Стиль написания символов?"),
            ("СПИСОК", "Нумерованный перечень элементов?"),
            ("ТАБЛИЦА", "Табличная форма представления данных?"),
        ],
        "Средний": [
            ("КОЛОНТИТУЛ", "Текст, размещённый сверху или снизу страницы?"),
            ("ПРАВОПИСАНИЕ", "Проверка ошибок в тексте?"),
            ("ПЕРЕВОД", "Процесс передачи смысла текста с одного языка на другой?"),
            ("OCR", "Распознавание текста по изображению?"),
            ("ФОРМАТИРОВАНИЕ", "Выравнивание текста по краям страницы?"),
        ],
        "Повышенный": [
            ("СТИЛЬ", "Единый набор параметров оформления документа?"),
            ("ГИПЕРССЫЛКА", "Ссылка на другой документ или объект?"),
            ("НОМЕРАЦИЯ", "Автоматическое создание списка страниц?"),
            ("ОБТЕКАНИЕ", "Расположение текста вокруг рисунка?"),
            ("ДИКТОВКА", "Голосовой ввод текста?"),
        ]
    },
    "Компьютерная графика": {
        "Базовый": [
            ("РЕДАКТОР", "Программа для создания изображений?"),
            ("РАСТР", "Изображение из пикселей?"),
            ("ПРИМИТИВ", "Геометрическая фигура для построения рисунка?"),
            ("МАСШТАБИРОВАНИЕ", "Изменение размеров изображения?"),
            ("ОБЛАСТЬ", "Выделенная часть изображения?"),
        ],
        "Средний": [
            ("КОРРЕКЦИЯ", "Изменение яркости изображения?"),
            ("ВРАЩЕНИЕ", "Поворот изображения вокруг оси?"),
            ("ДУБЛИРОВАНИЕ", "Копирование части рисунка?"),
            ("ЗАЛИВКА", "Закрашивание области цветом?"),
            ("ВЕКТОР", "Изображение из геометрических объектов?"),
        ],
        "Повышенный": [
            ("КОНТРАСТНОСТЬ", "Улучшение различий между светлыми и тёмными участками изображения?"),
            ("ОБРЕЗКА", "Удаление части изображения?"),
            ("ОТРАЖЕНИЕ", "Зеркальное отображение рисунка?"),
            ("ЦВЕТОКОРРЕКЦИЯ", "Изменение цветового баланса изображения?"),
            ("МАСШТАБИРУЕМОСТЬ", "Основное преимущество векторной графики?"),
        ]
    },
    "Мультимедийные презентации": {
        "Базовый": [
            ("СЛАЙД", "Отдельная страница презентации?"),
            ("ПРЕЗЕНТАЦИЯ", "Последовательность показа слайдов?"),
            ("АНИМАЦИЯ", "Движение объектов на слайде?"),
            ("РИСУНОК", "Изображение, добавленное на слайд?"),
            ("АУДИО", "Звуковое сопровождение презентации?"),
        ],
        "Средний": [
            ("ПЕРЕХОД", "Смена между слайдами?"),
            ("ШАБЛОН", "Готовый образец оформления?"),
            ("ГИПЕРССЫЛКА", "Щелчок по объекту для перехода на другой слайд?"),
            ("ВИДЕОРОЛИК", "Фрагмент для просмотра, встроенный в презентацию?"),
            ("ДИЗАЙН", "Совокупность элементов оформления?"),
        ],
        "Повышенный": [
            ("АВТОПОКАЗ", "Автоматический показ слайдов по времени?"),
            ("ВИДЕОКЛИП", "Мультимедийный объект, объединяющий звук и изображение?"),
            ("ГИПЕРСВЯЗЬ", "Способ организации нелинейной навигации в презентации?"),
            ("ЭФФЕКТ", "Средство привлечения внимания к объекту на слайде?"),
            ("МУЛЬТИМЕДИА", "Представление информации с использованием нескольких видов данных?"),
        ]
    }
}

game_state = {
    "grid": {},
    "placed_words": [],
    "time_left": 0,
    "total_time": 0,
    "used_checks": 0,
    "remaining_checks": 3,
    "timer_running": False,
    "theme": "",
    "level": ""
}

class Crossword:
    def __init__(self):
        self.grid = {}

    def _is_black(self, r, c):
        return (r, c) not in self.grid

    def can_place(self, word, start_r, start_c, dr, dc):
        L = len(word)
        if not self._is_black(start_r - dr, start_c - dc):
            return False
        if not self._is_black(start_r + dr * L, start_c + dc * L):
            return False

        overlap_count = 0
        for i, ch in enumerate(word):
            r = start_r + dr * i
            c = start_c + dc * i
            if (r, c) in self.grid:
                if self.grid[(r, c)] != ch:
                    return False
                overlap_count += 1
            else:
                for dr2, dc2 in ((1,0), (-1,0), (0,1), (0,-1)):
                    nr, nc = r + dr2, c + dc2
                    if (nr, nc) in self.grid:
                        if not any(start_r + dr * j == nr and start_c + dc * j == nc for j in range(L)):
                            return False
        if overlap_count > 1:
            return False
        return True

    def add_word(self, word, start_r, start_c, dr, dc):
        L = len(word)
        for i, ch in enumerate(word):
            r = start_r + dr * i
            c = start_c + dc * i
            self.grid[(r, c)] = ch

    def get_bounding_box(self):
        if not self.grid:
            return 0, 0
        max_r = max(r for r, _ in self.grid)
        max_c = max(c for _, c in self.grid)
        return max_r, max_c

def place_crossword(words):
    cw = Crossword()
    placed = []
    items = list(enumerate(words))
    random.shuffle(items)

    for idx, (word, q) in items:
        num = idx + 1
        possible = []
        for (r, c), letter in cw.grid.items():
            for i, ch in enumerate(word):
                if ch == letter:
                    if cw.can_place(word, r, c - i, 0, 1):
                        possible.append((r, c - i, 0, 1, "across"))
                    if cw.can_place(word, r - i, c, 1, 0):
                        possible.append((r - i, c, 1, 0, "down"))
        if possible:
            sr, sc, dr, dc, dir_label = random.choice(possible)
            cw.add_word(word, sr, sc, dr, dc)
            placed.append({
                "num": num, "word": word, "q": q,
                "start_r": sr, "start_c": sc,
                "direction": dir_label
            })
        else:
            max_r, max_c = cw.get_bounding_box()
            if not cw.grid:
                new_r, new_c = 0, 0
            else:
                new_r = max_r + 2
                new_c = 0
            if cw.can_place(word, new_r, new_c, 0, 1):
                cw.add_word(word, new_r, new_c, 0, 1)
                placed.append({
                    "num": num, "word": word, "q": q,
                    "start_r": new_r, "start_c": new_c,
                    "direction": "across"
                })
            elif cw.can_place(word, new_r, new_c, 1, 0):
                cw.add_word(word, new_r, new_c, 1, 0)
                placed.append({
                    "num": num, "word": word, "q": q,
                    "start_r": new_r, "start_c": new_c,
                    "direction": "down"
                })
            else:
                if cw.can_place(word, new_r, new_c + 2, 0, 1):
                    cw.add_word(word, new_r, new_c + 2, 0, 1)
                    placed.append({
                        "num": num, "word": word, "q": q,
                        "start_r": new_r, "start_c": new_c + 2,
                        "direction": "across"
                    })
                elif cw.can_place(word, new_r, new_c + 2, 1, 0):
                    cw.add_word(word, new_r, new_c + 2, 1, 0)
                    placed.append({
                        "num": num, "word": word, "q": q,
                        "start_r": new_r, "start_c": new_c + 2,
                        "direction": "down"
                    })
                else:
                    cw.add_word(word, 0, 0, 0, 1)
                    placed.append({
                        "num": num, "word": word, "q": q,
                        "start_r": 0, "start_c": 0,
                        "direction": "across"
                    })

    if cw.grid:
        min_r = min(r for r, _ in cw.grid)
        min_c = min(c for _, c in cw.grid)
        shifted_grid = {}
        for (r, c), ch in cw.grid.items():
            shifted_grid[(r - min_r, c - min_c)] = ch
        for info in placed:
            info["start_r"] -= min_r
            info["start_c"] -= min_c
        return shifted_grid, placed
    return {}, placed

def generate_words(theme, level):
    words = BANK[theme][level]
    random.shuffle(words)
    return words[:5]

def create_crossword_html(grid, placed_words):
    if not grid:
        return "<p>Не удалось создать кроссворд</p>"
    max_r = max(r for r, _ in grid)
    max_c = max(c for _, c in grid)

    start_cells = {}
    for pw in placed_words:
        key = (pw['start_r'], pw['start_c'])
        if key not in start_cells:
            start_cells[key] = []
        start_cells[key].append(pw['num'])

    html = '<table style="border-collapse: collapse; margin: 0 auto;">'
    for r in range(max_r + 1):
        html += '<tr>'
        for c in range(max_c + 1):
            if (r, c) in grid:
                cell_id = f"cell_{r}_{c}"
                nums = start_cells.get((r, c), [])
                num_text = ','.join(map(str, nums)) if nums else ""

                next_across = f"cell_{r}_{c+1}" if (r, c+1) in grid else ""
                next_down = f"cell_{r+1}_{c}" if (r+1, c) in grid else ""
                prev_across = f"cell_{r}_{c-1}" if (r, c-1) in grid else ""
                prev_down = f"cell_{r-1}_{c}" if (r-1, c) in grid else ""

                html += f'''
                <td style="position: relative; padding: 0; border: 2px solid #B22222; width: 45px; height: 45px; text-align: center; background: #FFF8F0;">
                    {f'<span style="position: absolute; top: 1px; left: 3px; font-size: 8px; color: #B22222; font-weight: bold;">{num_text}</span>' if num_text else ''}
                    <input type="text" id="{cell_id}" 
                           maxlength="1" 
                           data-next-across="{next_across}"
                           data-next-down="{next_down}"
                           data-prev-across="{prev_across}"
                           data-prev-down="{prev_down}"
                           style="width: 38px; height: 38px; border: none; text-align: center; font-size: 18px; font-weight: bold; text-transform: uppercase; background: transparent; outline: none;"
                           oninput="this.value = this.value.toUpperCase()">
                </td>'''
            else:
                html += '<td style="width: 45px; height: 45px; background: #D3D3D3;"></td>'
        html += '</tr>'
    html += '</table>'
    return html

def create_questions_html(placed_words):
    html = '<div style="text-align: left; padding: 10px;">'
    html += '<h3 style="color: #B22222;">Вопросы:</h3>'
    for pw in sorted(placed_words, key=lambda x: x['num']):
        html += f'<p><b>{pw["num"]}.</b> {pw["q"]}</p>'
    html += '</div>'
    return html

def check_answers():
    run_js("""
    var cells = document.querySelectorAll('input[type="text"]');
    cells.forEach(function(cell) {
        var id = cell.id;
        var userAnswer = cell.value.toUpperCase();
        var correctAnswer = window.crosswordAnswers[id] || '';
        if (correctAnswer && userAnswer === correctAnswer) {
            cell.style.backgroundColor = '#2E8B57';
            cell.style.color = 'white';
            cell.disabled = true;
        } else if (correctAnswer) {
            cell.value = '';
            cell.style.backgroundColor = '#FFE8E8';
        }
    });
    """)

def calculate_score(correct_words):
    base_scores = {5: 100, 4: 70, 3: 40, 2: 20, 1: 10, 0: 0}
    base = base_scores.get(correct_words, 0)
    level_multipliers = {"Базовый": 1.0, "Средний": 1.5, "Повышенный": 2.0}
    multiplier = level_multipliers.get(game_state["level"], 1.0)
    time_percent = (game_state["time_left"] / game_state["total_time"] * 100) if game_state["total_time"] > 0 else 0
    if time_percent > 75:
        time_bonus = 30
    elif time_percent > 50:
        time_bonus = 20
    elif time_percent > 25:
        time_bonus = 10
    elif time_percent > 0:
        time_bonus = 5
    else:
        time_bonus = 0
    unused_checks = 3 - game_state["used_checks"]
    accuracy_bonus = unused_checks * 15
    penalty = 0
    if game_state["time_left"] == 0:
        penalty -= 20
    if game_state["remaining_checks"] == 0:
        penalty -= 10
    score = (base * multiplier) + time_bonus + accuracy_bonus + penalty
    return max(0, int(score))

def get_rank(score):
    if score >= 250:
        return "Гранд-магистр информатики"
    elif score >= 200:
        return "Магистр"
    elif score >= 150:
        return "Эксперт"
    elif score >= 100:
        return "Специалист"
    elif score >= 50:
        return "Практик"
    else:
        return "Новичок"

def get_grade(percent):
    if percent >= 90:
        return "5 (отлично)"
    elif percent >= 70:
        return "4 (хорошо)"
    elif percent >= 40:
        return "3 (удовлетворительно)"
    else:
        return "2 (неудовлетворительно)"

def get_achievements(correct_words):
    achievements = []
    time_percent = (game_state["time_left"] / game_state["total_time"] * 100) if game_state["total_time"] > 0 else 0
    if time_percent > 75:
        achievements.append("Спринтер (более 75% времени)")
    if game_state["used_checks"] == 0:
        achievements.append("Идеальная точность (0 проверок)")
    if game_state["level"] == "Повышенный" and correct_words == 5:
        achievements.append("На высшем уровне (повышенный + 5/5)")
    if game_state["used_checks"] <= 1:
        achievements.append("Внимательный (не более 1 проверки)")
    if game_state["time_left"] <= 30 and game_state["time_left"] > 0:
        achievements.append("В последний момент (осталось <= 30 сек)")
    if game_state["remaining_checks"] == 0:
        achievements.append("Настойчивый (все проверки)")
    if game_state["used_checks"] == 0 and correct_words == 5:
        achievements.append("Абсолютное знание (0 проверок + 5/5)")
    return achievements

def finish_game():
    game_state["timer_running"] = False
    run_js("clearInterval(window.timerInterval);")
    time.sleep(0.2)
    user_answers_js = """
    (function() {
        var cells = document.querySelectorAll('input[type="text"]');
        var answers = {};
        cells.forEach(function(cell) {
            answers[cell.id] = cell.value.toUpperCase();
        });
        return answers;
    })()
    """
    user_grid = eval_js(user_answers_js)
    correct_grid = game_state["grid"]
    correct_words = 0
    total_words = len(game_state["placed_words"])
    for pw in game_state["placed_words"]:
        word = pw["word"]
        start_r, start_c = pw["start_r"], pw["start_c"]
        direction = pw["direction"]
        all_correct = True
        for i, ch in enumerate(word):
            if direction == "down":
                r, c = start_r + i, start_c
            else:
                r, c = start_r, start_c + i
            cell_id = f"cell_{r}_{c}"
            user_letter = user_grid.get(cell_id, "")
            correct_letter = correct_grid.get((r, c), "")
            if user_letter != correct_letter:
                all_correct = False
                break
        if all_correct:
            correct_words += 1
    score = calculate_score(correct_words)
    rank = get_rank(score)
    percent = (correct_words / total_words * 100) if total_words > 0 else 0
    grade = get_grade(percent)
    achievements = get_achievements(correct_words)
    time_min = game_state["time_left"] // 60
    time_sec = game_state["time_left"] % 60
    unused = 3 - game_state["used_checks"]
    achievements_html = ""
    if achievements:
        achievements_html = "<h3>Достижения:</h3><ul>"
        for ach in achievements:
            achievements_html += f"<li>{ach}</li>"
        achievements_html += "</ul>"
    clear()
    put_html(f"""
    <div style="text-align: center; padding: 40px; background: #E8E0D5; min-height: 100vh;">
        <div style="background: #F5F0E8; max-width: 600px; margin: 0 auto; padding: 30px; 
                    border: 2px solid #B22222; border-radius: 20px;">
            <h1 style="color: #B22222; font-family: Georgia;">РЕЗУЛЬТАТЫ ИГРЫ</h1>
            <hr style="border-color: #B22222;">
            <p style="font-size: 18px;"><b>Правильных слов:</b> {correct_words}/{total_words}</p>
            <p style="font-size: 18px; color: {"#2E8B57" if percent >= 90 else "#4A90D9" if percent >= 70 else "#DAA520" if percent >= 40 else "#B22222"};"><b>Оценка:</b> {grade}</p>
            <p><b>Осталось времени:</b> {time_min}:{time_sec:02d}</p>
            <p><b>Использовано проверок:</b> {game_state["used_checks"]}/3</p>
            <p style="color: #2E8B57;"><b>Неиспользовано проверок:</b> {unused} (+{unused * 15} баллов)</p>
            <p><b>Уровень сложности:</b> {game_state["level"]}</p>
            <hr style="border-color: #D0C8B8;">
            <h2 style="color: #B22222; font-size: 36px;">ОЧКИ: {score}</h2>
            <h3 style="font-size: 20px;">Звание: {rank}</h3>
            {achievements_html}
        </div>
    </div>
    """)
    put_buttons([
        dict(label="ИГРАТЬ СНОВА", value="again", color="danger"),
        dict(label="ВЫЙТИ", value="exit", color="secondary"),
    ], onclick=lambda action: main_menu() if action == "again" else run_js("window.close()"))

def show_rules():
    rules_html = """
    <div style="max-width: 700px; padding: 10px;">
        <h2 style="color: #B22222; text-align: center; font-family: Georgia;">ПРАВИЛА ИГРЫ</h2>
        <hr style="border-color: #B22222;">
        <h3>Основные правила</h3>
        <ol>
            <li>Выберите тему и уровень сложности</li>
            <li>Введите ответы в клетки кроссворда</li>
            <li>Используйте проверку для подсветки правильных букв</li>
            <li>Завершите игру до истечения времени</li>
        </ol>
        <h3>Время на игру</h3>
        <ul>
            <li><b>Базовый:</b> 5 минут</li>
            <li><b>Средний:</b> 7 минут</li>
            <li><b>Повышенный:</b> 10 минут</li>
        </ul>
        <h3>Проверки</h3>
        <p>Доступно 3 проверки. Каждая неиспользованная проверка даёт <b>+15 очков</b>.</p>
        <h3>Система оценки</h3>
        <p><b>Очки = Базовые очки × Множитель сложности + Бонус времени + Бонус проверок + Штрафы</b></p>
        <h4>Базовые очки:</h4>
        <ul>
            <li>5/5 слов — 100 очков</li>
            <li>4/5 слов — 70 очков</li>
            <li>3/5 слов — 40 очков</li>
            <li>2/5 слов — 20 очков</li>
            <li>1/5 слов — 10 очков</li>
        </ul>
        <h4>Множитель сложности:</h4>
        <ul>
            <li>Базовый — ×1.0</li>
            <li>Средний — ×1.5</li>
            <li>Повышенный — ×2.0</li>
        </ul>
        <h4>Бонус времени:</h4>
        <ul>
            <li>Более 75% времени — +30</li>
            <li>50–75% времени — +20</li>
            <li>25–50% времени — +10</li>
            <li>Менее 25% — +5</li>
        </ul>
        <h4>Звания:</h4>
        <ul>
            <li>250+ — Гранд-магистр</li>
            <li>200–249 — Магистр</li>
            <li>150–199 — Эксперт</li>
            <li>100–149 — Специалист</li>
            <li>50–99 — Практик</li>
            <li>0–49 — Новичок</li>
        </ul>
    </div>
    """
    popup(
        content=[
            put_html(rules_html),
            put_button("ЗАКРЫТЬ", onclick=lambda: close_popup(), color="danger")
        ],
        title="Правила игры"
    )

def handle_action(action):
    if action == "check":
        if game_state["remaining_checks"] > 0:
            game_state["used_checks"] += 1
            game_state["remaining_checks"] -= 1
            check_answers()
            run_js(f'document.getElementById("checks_left").innerHTML = "{game_state["remaining_checks"]}";')
            toast("Проверка выполнена! Правильные буквы подсвечены зелёным.")
        else:
            toast("Проверки закончились!", color="error")
    elif action == "finish":
        finish_game()
    elif action == "rules":
        show_rules()

def start_game():
    clear()
    run_js("document.body.style.backgroundColor = '#E8E0D5';")
    theme = game_state["theme"]
    level = game_state["level"]
    words = generate_words(theme, level)
    grid, placed = place_crossword(words)
    game_state["grid"] = grid
    game_state["placed_words"] = placed

    if level == "Базовый":
        total_seconds = 5 * 60
    elif level == "Средний":
        total_seconds = 7 * 60
    else:
        total_seconds = 10 * 60
    game_state["time_left"] = total_seconds
    game_state["total_time"] = total_seconds
    game_state["timer_running"] = True

    crossword_html = create_crossword_html(grid, placed)
    questions_html = create_questions_html(placed)

    put_html(f"""
    <div style="display: flex; background: #E8E0D5; min-height: 100vh; padding: 20px;">
        <div style="flex: 2; text-align: center;">
            <h2 style="color: #B22222; font-family: Georgia;">КРОССВОРД</h2>
            <p>Тема: {theme} | Уровень: {level}</p>
            <div id="timer" style="font-size: 24px; color: #B22222; font-weight: bold; margin: 10px 0;">--:--</div>
            {crossword_html}
        </div>
        <div style="flex: 1; margin-left: 20px; background: #F5F0E8; padding: 15px; border-radius: 10px; border: 1px solid #D0C8B8;">
            {questions_html}
            <div style="margin-top: 20px; text-align: center;">
                <p style="font-size: 16px;">Проверок осталось: <b id="checks_left" style="color: #B22222;">{game_state["remaining_checks"]}</b></p>
            </div>
        </div>
    </div>
    """)

    answers_js = "{"
    for (r, c), letter in grid.items():
        answers_js += f'"cell_{r}_{c}": "{letter}", '
    answers_js += "}"
    run_js(f"window.crosswordAnswers = {answers_js};")

    run_js(f"""
    window.timeLeft = {total_seconds};
    var timerElement = document.getElementById('timer');
    function updateTimer() {{
        var mins = Math.floor(window.timeLeft / 60);
        var secs = window.timeLeft % 60;
        timerElement.innerHTML = ('0' + mins).slice(-2) + ':' + ('0' + secs).slice(-2);
        if (window.timeLeft <= 0) {{
            clearInterval(window.timerInterval);
        }} else {{
            window.timeLeft--;
        }}
    }}
    updateTimer();
    window.timerInterval = setInterval(updateTimer, 1000);
    """)

    run_js("""
    function goNext(cell) {
        var nextAcross = cell.getAttribute('data-next-across');
        var nextDown = cell.getAttribute('data-next-down');
        var nextId = nextAcross || nextDown;
        if (nextId) {
            var nextCell = document.getElementById(nextId);
            if (nextCell && !nextCell.disabled) {
                nextCell.focus();
            }
        }
    }
    function goPrev(cell) {
        var prevAcross = cell.getAttribute('data-prev-across');
        var prevDown = cell.getAttribute('data-prev-down');
        var prevId = prevAcross || prevDown;
        if (prevId) {
            var prevCell = document.getElementById(prevId);
            if (prevCell) {
                prevCell.focus();
            }
        }
    }
    var cells = document.querySelectorAll('input[type="text"]');
    cells.forEach(function(cell) {
        cell.addEventListener('input', function(e) {
            if (cell.value.length === 1) {
                goNext(cell);
            }
        });
        cell.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' && cell.value === '') {
                e.preventDefault();
                goPrev(cell);
            }
        });
    });
    """)

    put_buttons([
        dict(label="ПРОВЕРИТЬ", value="check", color="danger"),
        dict(label="ЗАВЕРШИТЬ", value="finish", color="secondary"),
        dict(label="ПРАВИЛА", value="rules", color="warning"),
    ], onclick=handle_action)

def main_menu():
    clear()
    run_js("document.body.style.backgroundColor = '#E8E0D5';")

    # Убираем белые обёртки (с задержкой)
    run_js("""
        setTimeout(function() {
            var containers = document.querySelectorAll('#pywebio-scope-ROOT .card, #pywebio-scope-ROOT .card-body, #pywebio-scope-ROOT .pywebio, #pywebio-scope-ROOT .container-fluid');
            containers.forEach(function(el) {
                el.style.background = 'transparent';
                el.style.boxShadow = 'none';
                el.style.border = 'none';
            });
            var form = document.querySelector('#pywebio-scope-ROOT form');
            if (form) {
                form.style.background = 'transparent';
                form.style.boxShadow = 'none';
                form.style.border = 'none';
                form.style.padding = '0';
                form.style.maxWidth = '500px';
                form.style.margin = '0 auto';
            }
        }, 100);
    """)

    put_html("""
    <div style="text-align: center; padding: 50px 20px 30px; background: transparent;">
        <h1 style="color: #B22222; font-size: 48px; font-family: Georgia; margin-bottom: 10px;">КРОССВОРД</h1>
        <p style="color: #5A4A3A; font-size: 20px; font-family: Georgia; margin: 0;">по информатике</p>
        <hr style="border-color: #B22222; width: 30%; margin: 20px auto;">
        <p style="color: #3D2E1E; font-size: 18px; margin: 10px 0;">Начни игру прямо сейчас!</p>
        <p style="color: #5A4A3A; font-size: 16px; margin-bottom: 20px;">Проверь свои знания по усвоенным темам</p>
    </div>
    """)

    put_html("""
    <div style="max-width: 500px; margin: 0 auto; padding: 0 20px;">
        <div style="margin-bottom: 15px;">
            <label style="color: #5A4A3A; font-weight: bold; font-family: Georgia; font-size: 18px; display: block; margin-bottom: 5px;">Выберите тему:</label>
            <select id="theme_select" style="width: 100%; padding: 12px 15px; font-size: 18px; font-family: Georgia; border: 2px solid #B22222; border-radius: 6px; background: transparent; color: #3D2E1E; outline: none; -webkit-appearance: none; -moz-appearance: none; appearance: none; background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 8"><path fill="%23B22222" d="M6 8L0 0h12z"/></svg>'); background-repeat: no-repeat; background-position: right 15px center; background-size: 12px; cursor: pointer;">
                <option>Компьютер и его устройство</option>
                <option>Программы и данные</option>
                <option>Компьютерные сети</option>
                <option>Информация и процессы</option>
                <option>Представление информации</option>
                <option>Текстовые документы</option>
                <option>Компьютерная графика</option>
                <option>Мультимедийные презентации</option>
            </select>
        </div>
        <div style="margin-bottom: 20px;">
            <label style="color: #5A4A3A; font-weight: bold; font-family: Georgia; font-size: 18px; display: block; margin-bottom: 5px;">Выберите уровень:</label>
            <select id="level_select" style="width: 100%; padding: 12px 15px; font-size: 18px; font-family: Georgia; border: 2px solid #B22222; border-radius: 6px; background: transparent; color: #3D2E1E; outline: none; -webkit-appearance: none; -moz-appearance: none; appearance: none; background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 8"><path fill="%23B22222" d="M6 8L0 0h12z"/></svg>'); background-repeat: no-repeat; background-position: right 15px center; background-size: 12px; cursor: pointer;">
                <option>Базовый</option>
                <option>Средний</option>
                <option>Повышенный</option>
            </select>
        </div>
        <div id="start_button_container" style="text-align: center;"></div>
    </div>
    """)

    # Функция-обработчик нажатия
    def on_start_click():
        theme = eval_js('document.getElementById("theme_select").value')
        level = eval_js('document.getElementById("level_select").value')
        game_state['theme'] = theme
        game_state['level'] = level
        start_game()

    # Вставляем кнопку PyWebIO в контейнер
    put_button("НАЧАТЬ ИГРУ", onclick=on_start_click, color='danger')

    # Применяем стили к этой кнопке, чтобы она выглядела как ваша кастомная
    run_js("""
        setTimeout(function() {
            var btn = document.querySelector('#start_button_container button');
            if (btn) {
                btn.style.width = '100%';
                btn.style.padding = '14px';
                btn.style.fontSize = '22px';
                btn.style.fontWeight = 'bold';
                btn.style.fontFamily = 'Georgia';
                btn.style.backgroundColor = '#B22222';
                btn.style.color = 'white';
                btn.style.border = 'none';
                btn.style.borderRadius = '8px';
                btn.style.cursor = 'pointer';
                btn.style.transition = 'background-color 0.3s';
                btn.id = 'start_btn';
            }
        }, 200);
    """)

def main():
    main_menu()

if __name__ == '__main__':
    start_server(main, port=8080, host='0.0.0.0', debug=False)
