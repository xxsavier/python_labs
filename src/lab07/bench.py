import random
import timeit
from src.lab04.io_txt_csv import write_csv
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast


def main():

    random.seed(42)

    def bench_sorts(n):
        """Бенчмарк сортировок

        Args:
            n(int): количество элементов в списке

        Returns:
            list: список с результатами
        """    
        data = [random.randint(-1_000_000, 1_000_000) for _ in range(n)]
        rows = []
        x = timeit.timeit(lambda:sorted(data), number=1)
        rows.append(("sort", n, "sorted", x))
        if n <= 10000:
            x = timeit.timeit(lambda:bubble_sort(data), number=1)
            rows.append(("sort", n, "bubble_sort", x))
            x = timeit.timeit(lambda:insertion_sort(data), number=1)
            rows.append(("sort", n, "insertion_sort", x))
            x = timeit.timeit(lambda:selection_sort(data), number=1)
            rows.append(("sort", n, "selection_sort", x))
        else:
            rows.append(("sort", n, "bubble_sort", '>60'))
            rows.append(("sort", n, "insertion_sort", '>60'))
            rows.append(("sort", n, "selection_sort", '>60'))
        return rows

    def bench_search():
        """Бенчмарк алгоритмов поиска

        Returns:
            list: список с результатами
        """    
        data_size = 100_000
        targets_quantity = 10_000
        data = [random.randint(-1_000_000, 1_000_000) for _ in range(data_size)]
        targets = [random.choice(data) for _ in range(targets_quantity)]
        rows = []
        type_time = 0
        for target in targets:
            x = timeit.timeit(lambda:linear_search(data, target), number=1)
            type_time += x
        rows.append(("search", data_size, "linear_search", type_time))
        type_time = 0
        x = timeit.timeit(lambda:sorted(data), number=1)
        sorted_data = sorted(data)
        rows.append(("sort", data_size, "sorted(for binary)", x))
        type_time = 0
        for target in targets:
            x = timeit.timeit(lambda:binary_search(sorted_data, target), number=1)
            type_time += x
        rows.append(("search", data_size, "binary_search", type_time))
        return rows

    def bench_two_sum(n):
        """Бенчмарк алгоритмов решения two_sum 

        Args:
            n(int): количество элементов в списке

        Returns:
            list: список с результатами
        """    
        data = [random.randint(-1_000_000, 1_000_000) for _ in range(n)]
        target = data[1] + data[42]
        rows = []
        x = timeit.timeit(lambda:two_sum_brute(data, target), number=1)
        rows.append(('two_sum', n, 'two_sum_brute', x))
        x = timeit.timeit(lambda:two_sum_fast(data, target), number=1)
        rows.append(('two_sum', n, 'two_sum_fast', x))
        return rows

    def get_rows():
        """Функция собирает все результаты в один список

        Returns:
            list: список со всеми результатами всех бенчмарков
        """    
        all_rows = []
        all_rows.extend(bench_sorts(1_000))
        all_rows.extend(bench_sorts(10_000))
        all_rows.extend(bench_sorts(100_000))
        all_rows.extend(bench_search())
        all_rows.extend(bench_two_sum(1_000))
        all_rows.extend(bench_two_sum(10_000))
        return all_rows

    csv_rows = get_rows()
    header = ("Task", "Length", "Method", "Time")
    write_csv(csv_rows, "data/lab07/bench.csv", header=header)

    max_len_t = max([len(str(x[3])) for x in csv_rows])
    print(f"| {'Task':<7} | {'Length':<6} | {'Method':<18} | {'Time'}" + (max_len_t-4)*' ' + ' |')
    print('—'*65)
    for t, l, m, ti in csv_rows:
        print(f"| {t:<7} | {l:<6} | {m:<18} | {ti}" + (max_len_t-len(str(ti)))*' ' + ' |')
        
if __name__ == "__main__":
    main()