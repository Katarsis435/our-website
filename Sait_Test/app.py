from flask import Flask, render_template, jsonify, request
import random
import time
import threading

#ef476f

app = Flask(__name__)

# Глобальные переменные для управления визуализацией
visualizer_data = {
    'running': False,
    'current_algorithm': None,
    'bars': [random.randint(10, 280) for _ in range(50)],
    'sort_time': 0,
    'highlight_indices': [],
    'array_size': 50
}


@app.route('/') # Декоратор экземпляра приложения
def index():
    return render_template('index.html')


@app.route('/start-sorting/<algorithm>')
def start_sorting(algorithm):
    global visualizer_data

    if visualizer_data['running']:
        return "Визуализатор уже запущен!"

    # Получаем размер массива из параметров запроса
    size = request.args.get('size', default=50, type=int)
    size = max(10, min(100, size))  # Ограничение от 10 до 100

    # Инициализируем данные
    visualizer_data['bars'] = [random.randint(10, 280) for _ in range(size)]
    visualizer_data['current_algorithm'] = algorithm
    visualizer_data['sort_time'] = 0
    visualizer_data['highlight_indices'] = []
    visualizer_data['running'] = True
    visualizer_data['array_size'] = size

    # Запускаем сортировку в отдельном потоке
    thread = threading.Thread(target=run_sorting_algorithm, args=(algorithm,))
    thread.daemon = True
    thread.start()

    return f"Запуск {algorithm}..."


@app.route('/stop-sorting')
def stop_sorting():
    global visualizer_data
    visualizer_data['running'] = False
    return "Сортировка остановлена"


@app.route('/shuffle')
def shuffle_bars():
    global visualizer_data
    if not visualizer_data['running']:
        size = visualizer_data['array_size']
        visualizer_data['bars'] = [random.randint(10, 280) for _ in range(size)]
        visualizer_data['highlight_indices'] = []
    return "Массив перемешан"


@app.route('/change-size', methods=['POST'])
def change_size():
    global visualizer_data
    if not visualizer_data['running']:
        size = request.json.get('size', 50)
        size = max(10, min(100, size))  # Ограничение от 10 до 100
        visualizer_data['array_size'] = size
        visualizer_data['bars'] = [random.randint(10, 280) for _ in range(size)]
        visualizer_data['highlight_indices'] = []
        return f"Размер массива изменен на {size}"
    return "Невозможно изменить размер во время сортировки"


@app.route('/get-data')
def get_data():
    return jsonify(visualizer_data)


def run_sorting_algorithm(algorithm):
    global visualizer_data

    start_time = time.time()

    if algorithm == 'bubble':
        bubble_sort()
    elif algorithm == 'selection':
        selection_sort()
    elif algorithm == 'insertion':
        insertion_sort()
    elif algorithm == 'shell':
        shell_sort()
    elif algorithm == 'quick':
        quick_sort()
    elif algorithm == 'merge':
        merge_sort()
    elif algorithm == 'heap':
        heap_sort()
    elif algorithm == 'counting':
        counting_sort()

    visualizer_data['sort_time'] = time.time() - start_time #Записывает время выполнения сортировки
    visualizer_data['highlight_indices'] = [] #Очищает массив подсвечиваемых индексов
    visualizer_data['running'] = False #Устанавливает флаг выполнения в False


# СОРТИРОВКИ \/

#Пузырьковая сортировка
#Попарно сравнивает соседние элементы и меняет их местами, если они находятся в неправильном порядке. Процесс повторяется до тех пор, пока массив не будет отсортирован.
def bubble_sort():
    global visualizer_data
    bars = visualizer_data['bars']
    n = len(bars)
    for i in range(n):
        for j in range(0, n - i - 1):
            if not visualizer_data['running']:
                return
            if bars[j] > bars[j + 1]:
                bars[j], bars[j + 1] = bars[j + 1], bars[j]
                visualizer_data['highlight_indices'] = [j, j + 1]
            time.sleep(0.05)
# O(n²)


#Сортировка выбором
#Находит минимальный элемент в неотсортированной части массива и помещает его в начало. Процесс повторяется для оставшейся части массива.
def selection_sort():
    global visualizer_data
    bars = visualizer_data['bars']
    n = len(bars)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if not visualizer_data['running']:
                return
            if bars[j] < bars[min_idx]:
                min_idx = j
            visualizer_data['highlight_indices'] = [i, min_idx]
            time.sleep(0.05)
        bars[i], bars[min_idx] = bars[min_idx], bars[i]
        visualizer_data['highlight_indices'] = [i, min_idx]
        time.sleep(0.05)
# O(n²)


#Сортировка вставками
#Постепенно строит отсортированную последовательность, по одному элементу за раз, вставляя каждый новый элемент в правильную позицию в уже отсортированной части.
def insertion_sort():
    global visualizer_data
    bars = visualizer_data['bars']
    for i in range(1, len(bars)):
        key = bars[i]
        j = i - 1
        while j >= 0 and key < bars[j]:
            if not visualizer_data['running']:
                return
            bars[j + 1] = bars[j]
            j -= 1
            visualizer_data['highlight_indices'] = [i, j + 1]
            time.sleep(0.05)
        bars[j + 1] = key
        visualizer_data['highlight_indices'] = [i  , j + 1]
        time.sleep(0.05)


#Сортировка Шелла
#Улучшенная версия сортировки вставками. Сравнивает элементы, находящиеся на определенном расстоянии друг от друга, постепенно уменьшая это расстояние.
def shell_sort():
    global visualizer_data
    bars = visualizer_data['bars']
    n = len(bars)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = bars[i]
            j = i
            while j >= gap and bars[j - gap] > temp:
                if not visualizer_data['running']:
                    return
                bars[j] = bars[j - gap]
                j -= gap
                visualizer_data['highlight_indices'] = [i, j]
                time.sleep(0.05)
            bars[j] = temp
            visualizer_data['highlight_indices'] = [i, j]
            time.sleep(0.05)
        gap //= 2


# Быстрая сортировка.
# Выбирает опорный элемент и разделяет массив на две части: элементы меньше опорного и элементы больше опорного. Рекурсивно применяет этот процесс к обеим частям.
def quick_sort():
    global visualizer_data
    def _quick_sort(arr, low, high):
        if low < high and visualizer_data['running']:
            pi = partition(arr, low, high)
            _quick_sort(arr, low, pi - 1)
            _quick_sort(arr, pi + 1, high)
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if not visualizer_data['running']:
                return i + 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                visualizer_data['highlight_indices'] = [i, j]
                time.sleep(0.05)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        visualizer_data['highlight_indices'] = [i + 1, high]
        time.sleep(0.05)
        return i + 1
    _quick_sort(visualizer_data['bars'], 0, len(visualizer_data['bars']) - 1)


# Сортировка слиянием
# Рекурсивно разделяет массив на две половины до тех пор, пока не останутся отдельные элементы, затем объединяет их в отсортированном порядке.
def merge_sort():
    global visualizer_data
    def _merge_sort(arr, left, right):
        if left < right and visualizer_data['running']:
            mid = (left + right) // 2
            _merge_sort(arr, left, mid)
            _merge_sort(arr, mid + 1, right)
            merge(arr, left, mid, right)
    def merge(arr, left, mid, right):
        left_copy = arr[left:mid + 1]
        right_copy = arr[mid + 1:right + 1]
        l = r = 0
        k = left
        while l < len(left_copy) and r < len(right_copy) and visualizer_data['running']:
            if left_copy[l] <= right_copy[r]:
                arr[k] = left_copy[l]
                l += 1
            else:
                arr[k] = right_copy[r]
                r += 1
            k += 1
            visualizer_data['highlight_indices'] = [k]
            time.sleep(0.05)
        while l < len(left_copy) and visualizer_data['running']:
            arr[k] = left_copy[l]
            l += 1
            k += 1
            visualizer_data['highlight_indices'] = [k]
            time.sleep(0.05)
        while r < len(right_copy) and visualizer_data['running']:
            arr[k] = right_copy[r]
            r += 1
            k += 1
            visualizer_data['highlight_indices'] = [k]
            time.sleep(0.05)
    _merge_sort(visualizer_data['bars'], 0, len(visualizer_data['bars']) - 1)


# Пирамидальная сортировка
# Строит бинарную кучу из элементов массива, затем последовательно извлекает максимальный элемент и перестраивает кучу.
def heap_sort():
    global visualizer_data
    def heapify(arr, n, i):
        if not visualizer_data['running']:
            return
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[i] < arr[left]:
            largest = left
        if right < n and arr[largest] < arr[right]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            visualizer_data['highlight_indices'] = [i, largest]
            time.sleep(0.05)
            heapify(arr, n, largest)
    n = len(visualizer_data['bars'])
    for i in range(n // 2 - 1, -1, -1):
        if not visualizer_data['running']:
            return
        heapify(visualizer_data['bars'], n, i)
    for i in range(n - 1, 0, -1):
        if not visualizer_data['running']:
            return
        visualizer_data['bars'][i], visualizer_data['bars'][0] = visualizer_data['bars'][0], visualizer_data['bars'][i]
        visualizer_data['highlight_indices'] = [i, 0]
        time.sleep(0.05)
        heapify(visualizer_data['bars'], i, 0)


# Сортировка подсчетом
# Подсчитывает количество вхождений каждого элемента, затем восстанавливает отсортированный массив на основе этих подсчетов. Эффективна для целых чисел в небольшом диапазоне.
def counting_sort():
    global visualizer_data
    bars = visualizer_data['bars']
    max_val = max(bars)
    min_val = min(bars)
    count = [0] * (max_val - min_val + 1)
    for num in bars:
        if not visualizer_data['running']:
            return
        count[num - min_val] += 1
    idx = 0
    for i in range(len(count)):
        for j in range(count[i]):
            if not visualizer_data['running']:
                return
            bars[idx] = i + min_val
            idx += 1
            visualizer_data['highlight_indices'] = [idx - 1]
            time.sleep(0.05)


if __name__ == '__main__':
    app.run(debug=True)