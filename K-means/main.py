import random
import math

# Функция для вычисления евклидова расстояния между двумя точками
def euclidean_distance(point1, point2):
    squared_sum = 0
    for i in range(len(point1)):
        squared_sum += (point1[i] - point2[i]) ** 2 #Для каждой координаты точек, вычисляет квадрат разности между координатами точек(kwadrat różnicy między współrzędnymi punktów)
    return math.sqrt(squared_sum)

# Функция для инициализации начальных центроидов
def initialize_centroids(data, k):
    # Выбираем случайным образом k точек из данных в качестве начальных центроидов
    centroids = random.sample(data, k)
    return centroids

# Функция для присвоения точек группам на основе ближайшего центроида
def assign_examples(data, centroids):
    groups = []
    for point in data:
        # Вычисляем расстояние от текущей точки до каждого центроида
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        # Присваиваем точку к группе с наименьшим расстоянием до центроида
        group = distances.index(min(distances))
        groups.append(group)
    return groups

# Функция для обновления положения центроидов
def update_centroids(data, groups, k):
    centroids = []
    for group in range(k):
        # Выбираем точки, принадлежащие текущей группе
        group_points = [data[i] for i in range(len(data)) if groups[i] == group]
        # Вычисляем новое положение центроида как среднее значение координат точек группы
        centroid = [sum(coord) / len(group_points) for coord in zip(*group_points)]
        centroids.append(centroid)
    return centroids

# Функция для вычисления суммы расстояний между точками и их центроидами
def calculate_sum_distances(data, groups, centroids):
    sum_distances = 0
    for i in range(len(data)):
        # Вычисляем расстояние между текущей точкой и ее центроидом
        sum_distances += euclidean_distance(data[i], centroids[groups[i]])
    return sum_distances

# Основная функция алгоритма k-средних
def k_means(data, k):
    # Инициализация начальных центроидов
    centroids = initialize_centroids(data, k)
    # Количество итераций
    num_iterations = 20
    for iteration in range(num_iterations):
        # Присвоение точек группам
        groups = assign_examples(data, centroids)
        # Обновление положения центроидов
        centroids = update_centroids(data, groups, k)
        # Вычисление суммы расстояний
        sum_distances = calculate_sum_distances(data, groups, centroids)
        # Вывод текущей суммы расстояний на итерации
        print(f"Iteration {iteration+1}: {sum_distances:.2f}")
    return groups

# Функция для отображения состава групп и классов
def display_group_compositions(groups, target):
    # Определение уникальных групп
    unique_groups = list(set(groups))
    # Подсчет количества точек в каждой группе
    group_compositions = {group: groups.count(group) for group in unique_groups}

    print()
    print("Group Compositions:")
    for group, count in group_compositions.items():
        print(f"Group {group + 1}: {count} examples")

    # Определение уникальных классов
    class_labels = list(set(target))
    # Подсчет количества точек для каждого класса
    class_compositions = {label: 0 for label in class_labels}

    for group, label in zip(groups, target):
        class_compositions[label] += 1

    print("\nClass Compositions:")
    for label, count in class_compositions.items():
        print(f"{label}: {count} examples")

# Создание пустого списка для хранения данных
data = []
# Создание пустого списка для хранения меток классов
target = []
# Чтение данных из файла "iris.data"
with open("iris.data", "r") as file:
    for line in file:
        if line.strip():
            # Разделение строки на значения
            row = line.strip().split(",")
            # Преобразование значений в числа и добавление их в список данных
            data.append([float(val) for val in row[:-1]])
            # Добавление последнего элемента строки (метки класса) в список меток классов
            target.append(row[-1])

# Ввод значения k от пользователя
k = int(input("Enter the value of k: "))

# Запуск алгоритма k-средних
groups = k_means(data, k)

# Отображение состава групп и классов
display_group_compositions(groups, target)
