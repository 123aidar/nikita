# -*- coding: utf-8 -*-
"""
Скрипт для проверки кодировки всех Python файлов в проекте
"""
import os
import sys

def check_file_encoding(filepath):
    """Проверяет, начинается ли файл с объявления кодировки UTF-8"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            second_line = f.readline().strip()
            
            # Проверяем первую или вторую строку
            if 'coding' in first_line or 'coding' in second_line:
                return True, "✓ Кодировка объявлена"
            else:
                return False, "✗ Нет объявления кодировки"
    except Exception as e:
        return False, f"✗ Ошибка: {e}"

def main():
    print("=" * 60)
    print("ПРОВЕРКА КОДИРОВКИ UTF-8 В PYTHON ФАЙЛАХ")
    print("=" * 60)
    print()
    
    # Директории для проверки
    apps = ['accounts', 'products', 'sales', 'inventory', 'reports', 'chat', 'grocery_store']
    
    files_to_check = []
    for app in apps:
        if os.path.exists(app):
            for root, dirs, files in os.walk(app):
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        files_to_check.append(filepath)
    
    # Проверяем каждый файл
    ok_count = 0
    error_count = 0
    
    for filepath in sorted(files_to_check):
        is_ok, message = check_file_encoding(filepath)
        status = "✓" if is_ok else "✗"
        print(f"{status} {filepath}")
        
        if is_ok:
            ok_count += 1
        else:
            error_count += 1
    
    print()
    print("=" * 60)
    print(f"Проверено файлов: {len(files_to_check)}")
    print(f"С кодировкой: {ok_count}")
    print(f"Без кодировки: {error_count}")
    print("=" * 60)
    
    if error_count > 0:
        print()
        print("ВНИМАНИЕ: Некоторые файлы не имеют объявления кодировки!")
        print("Добавьте в начало каждого файла:")
        print("# -*- coding: utf-8 -*-")
    else:
        print()
        print("✓ Все файлы имеют правильное объявление кодировки!")

if __name__ == '__main__':
    main()
