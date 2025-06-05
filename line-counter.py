import re
import os

# Specify the list of file paths to check
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
    r'one_page2\src\App.vue',
    r'one_page2\src\main.js',
]

def is_code_line(line, ext):
    line = line.strip()
    if not line:
        return False  # empty line

    # Skip pure HTML-tag lines in .js/.vue (outside of <script> for .vue)
    if ext in {'.js', '.vue'}:
        if re.fullmatch(r'<[^>]+>', line):
            return False

    # Skip single-line comments
    if ext in {'.js', '.vue'} and line.startswith('//'):
        return False
    if ext == '.py' and line.startswith('#'):
        return False

    return True  # otherwise count as code line

def count_code_lines(file_path):
    count = 0
    ext = os.path.splitext(file_path)[1]
    inside_multiline_comment = False
    inside_script = False  # For .vue files: track if we're inside <script> tags

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stripped = line.strip()

                # Handle <script> tags for .vue files: only count lines within <script>...</script>
                if ext == '.vue':
                    # Enter <script> block
                    if re.match(r'<script\b', stripped):
                        inside_script = True
                        continue
                    # Exit </script> block
                    if re.match(r'</script>', stripped):
                        inside_script = False
                        continue
                    # Skip any lines outside <script>...</script>
                    if not inside_script:
                        continue

                # Handle multiline comments in .js/.vue (/* ... */)
                if ext in {'.js', '.vue'}:
                    if '/*' in stripped and '*/' not in stripped:
                        inside_multiline_comment = True
                    if inside_multiline_comment:
                        if '*/' in stripped:
                            inside_multiline_comment = False
                        continue
                    if stripped.startswith('/*') and stripped.endswith('*/'):
                        continue

                # Handle multiline comments in .py (''' or """)
                if ext == '.py':
                    # Detect start or end of a Python triple-quoted string
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
        print(f'{file_path} - file not found.')
        return None

    return count

if __name__ == '__main__':
    total_lines = 0
    for file in FILES_TO_CHECK:
        lines = count_code_lines(file)
        if lines is not None:
            total_lines += lines
            print(f'{file} - {lines} lines of code')
    print("\nTotal lines of code:", total_lines)
