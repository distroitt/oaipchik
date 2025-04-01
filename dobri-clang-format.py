#!/usr/bin/env python3
import sys
import os
import re

def format_cpp_file(input_path, output_path=None):
    """
    Форматирует C++ файл, устанавливая:
      - 1 пустую строку между методами внутри класса,
      - 2 пустые строки между функциями вне класса.
    """
    if output_path is None:
        output_path = input_path

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Шаблоны для определения начала класса и окончания класса.
    class_start_pattern = re.compile(r'\s*class\s+\w+.*\{')
    class_end_pattern   = re.compile(r'^\s*};\s*$')
    # Пример шаблона для начала определения функции или метода:
    function_start_pattern = re.compile(r'^\s*(?:\w+\s+)*\w+\s*\([^)]*\)\s*(?:const\s*)?\s*{')


    result_lines = []
    in_class = False   # Флаг: находимся ли мы внутри класса
    prev_method = False  # Флаг: предыдущий блок внутри класса был методом
    i = 0
    rar = False
    class_fhod_pattern = re.compile(r'\w+::.+(){')

    while i < len(lines):
        line = lines[i]

        # Обнаруживаем начало объявления класса.
        if class_start_pattern.search(line):
            in_class = True
            prev_method = False  # при входе в класс сбрасываем флаг
            result_lines.append(line)
            i += 1
            continue

        # Обнаруживаем конец класса (например, строка вида "};").
        if in_class and class_end_pattern.match(line):
            in_class = False
            result_lines.append(line)
            prev_method = False
            i += 1
            continue
        
        if class_fhod_pattern.search(line) and not (re.match(r'^\s*if\s*\(', line) or re.match(r'^\s*switch\s*\(', line)):
            if rar:
                while result_lines and result_lines[-1].strip() == "":
                        result_lines.pop()
                result_lines.append("\n")
            else:
                rar = True
        # Если строка соответствует началу определения функции/метода.
        if function_start_pattern.match(line) and not class_fhod_pattern.search(line):
            if in_class:
                # Если предыдущий блок внутри класса был методом – вставляем ровно 1 пустую строку.
                if prev_method:
                    # Удаляем все завершающие пустые строки, если они есть.
                    while result_lines and result_lines[-1].strip() == "":
                        result_lines.pop()
                    result_lines.append("\n")
                # Добавляем строку с объявлением метода.
                result_lines.append(line)
                prev_method = True
            else:
                # Функция вне класса: перед объявлением вставляем 2 пустые строки.
                while result_lines and result_lines[-1].strip() == "":
                    result_lines.pop()
                if re.match(r'^\s*if\s*\(', line) or re.match(r'^\s*switch\s*\(', line):
                    # Просто переносим строку как есть
                    result_lines.append(line)
                else:
                    result_lines.append("\n")
                    result_lines.append("\n")
                    result_lines.append(line)

            # Обработка тела функции/метода: отслеживаем баланс фигурных скобок.
            function_depth = line.count("{") - line.count("}")
            i += 1
            while i < len(lines) and function_depth > 0:
                current_line = lines[i]
                result_lines.append(current_line)
                function_depth += current_line.count("{") - current_line.count("}")
                i += 1
            continue

        # Для остальных строк просто копируем содержимое.
        result_lines.append(line)
        # Если внутри класса и встретилась не пустая строка, которая не относится к методу,
        # сбрасываем флаг prev_method, чтобы пустая строка вставлялась только между подряд идущими методами.
        if in_class and line.strip() != "":
            prev_method = False
        i += 1

    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.writelines(result_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file

    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден")
        sys.exit(1)

    format_cpp_file(input_file, output_file)