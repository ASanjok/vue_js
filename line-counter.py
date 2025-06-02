import re
import os

# Укажи здесь список путей к нужным файлам
FILES_TO_CHECK = [
    r'django\project\first_part\models.py',
    r'django\project\first_part\serializers.py',
    r'django\project\first_part\tasks.py',
    r'django\project\first_part\views.py',
    r'django\project\project\celery.py',
    r'django\project\project\urls.py',
    r'django\project\celery_message_consume.py',
    r'message_receiver\receiver.js',
    r'one_page2\src\router\index.js',
    r'one_page2\src\views\accountPage.vue',
    r'one_page2\src\views\loginFormPage.vue',
    r'one_page2\src\views\mapPage.vue',
    r'one_page2\src\views\registerFormPage.vue',
    r'one_page2\src\views\testMapPage.vue',
    r'one_page2\src\App.vue',
    r'one_page2\src\main.js',
]

def is_code_line(line, ext):
    line = line.strip()
    if not line:
        return False  # пустая строка

    # Пропустить чисто HTML-строки
    if ext in {'.js', '.vue'}:
        if re.fullmatch(r'<[^>]+>', line):  # строка — только один HTML-тег
            return False

    # Пропустить однострочные комментарии
    if ext in {'.js', '.vue'} and line.startswith('//'):
        return False
    if ext == '.py' and line.startswith('#'):
        return False

    return True  # строка считается кодом

def count_code_lines(file_path):
    count = 0
    ext = os.path.splitext(file_path)[1]
    inside_multiline_comment = False

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stripped = line.strip()

                # Многострочные комментарии (JS/Vue: /* */)
                if ext in {'.js', '.vue'}:
                    if '/*' in stripped and '*/' not in stripped:
                        inside_multiline_comment = True
                    if inside_multiline_comment:
                        if '*/' in stripped:
                            inside_multiline_comment = False
                        continue
                    if stripped.startswith('/*') and stripped.endswith('*/'):
                        continue

                # Многострочные комментарии (Python: ''' или """)
                if ext == '.py':
                    if re.match(r'^([ru]{0,2}["\']{3})', stripped):
                        if inside_multiline_comment:
                            inside_multiline_comment = False
                            continue
                        elif stripped.count('"""') == 1 or stripped.count("'''") == 1:
                            inside_multiline_comment = True
                            continue
                        elif stripped.count('"""') == 2 or stripped.count("'''") == 2:
                            continue
                    if inside_multiline_comment:
                        continue

                if is_code_line(line, ext):
                    count += 1

    except FileNotFoundError:
        print(f'{file_path} - файл не найден.')
        return None

    return count

if __name__ == '__main__':
    total_lines = 0
    for file in FILES_TO_CHECK:
        lines = count_code_lines(file)
        if lines is not None:
            total_lines += lines
            print(f'{file} - {lines} строк кода')
    print("\n\nИтого строк кода: ", total_lines)
