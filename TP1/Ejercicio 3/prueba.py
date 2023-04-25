import multiprocessing as mp
import time
import math

results_a = []
results_b = []
results_c = []

def make_calculation_one(numbers):
    for number in numbers:
        results_a.append(math.sqrt(number ** 3))

def make_calculation_two(numbers):
    for number in numbers:
        results_b.append(math.sqrt(number ** 3))

def make_calculation_three(numbers):
    for number in numbers:
        results_c.append(math.sqrt(number ** 3))

if __name__ == '__main__':

    number_list = list(range(10000000))

    p1 = mp.Process(target=make_calculation_one, args=(number_list,))
    p2 = mp.Process(target=make_calculation_one, args=(number_list,))
    p3 = mp.Process(target=make_calculation_one, args=(number_list,))

    star = time.time()
    p1.start()
    p2.start()
    p3.start()
    end = time.time()

    print("Time: ", end - star)

    star = time.time()
    make_calculation_one(number_list)
    make_calculation_one(number_list)
    make_calculation_one(number_list)
    end = time.time()

    print("Time: ", end - star)
