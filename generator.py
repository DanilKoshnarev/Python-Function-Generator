import os
import importlib.util

def generate_function(name, params, body, filename="generated_code.py"):
    """
    Генерирует Python-функцию и сохраняет её в файл.
    
    :param name: Имя функции.
    :param params: Лист параметров.
    :param body: Тело функции в виде строки.
    :param filename: Имя шары, в которую сейвим код.
    """
    param_str = ", ".join(params)
    function_code = f"def {name}({param_str}):\n" + "\n".join(f"    {line}" for line in body.splitlines())
    
    
    with open(filename, "w") as file:
        file.write(function_code)
        file.write("\n")  
    
    print(f"Функция '{name}' успешно сохранена в файл:'{filename}'.")

def load_and_execute_function(filename, function_name, *args, **kwargs):
    """
    Вытаскивает функцию из файла и выполняет её.
    
    :param filename: Имя файла с функцией.
    :param function_name: Имя функции для кола.
    :param args: Позешен аргументы функции.
    :param kwargs: Именованные аргументы функции.
    :return: Результат функции.
    """
    # Проверяем ,есть ли файлик
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл '{filename}' не найден.")
    
    # Динамически загружаем модуль
    spec = importlib.util.spec_from_file_location("generated_module", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Получаем функцию
    if not hasattr(module, function_name):
        raise AttributeError(f"Функция '{function_name}' не найдена в файле '{filename}'.")
    
    func = getattr(module, function_name)
    return func(*args, **kwargs)

# Пример использования
if __name__ == "__main__":
    # Шаг 1: Генерация функции
    function_name = "add_numbers"
    params = ["a", "b"]
    body = """
result = a + b
return result
"""
    filename = "generated_code.py"
    generate_function(function_name, params, body, filename)

    # Шаг 2: Загрузка и выполнение функции
    try:
        result = load_and_execute_function(filename, function_name, 10, 20)
        print(f"Результат выполнения функции '{function_name}': {result}")
    except (FileNotFoundError, AttributeError) as e:
        print(f"Ошибка: {e}")