# """
# Copyright (c) 2023 Bryan Tjandra
# """

import time
import psutil
from branch_bound import UKP
from dynamic_programming import unboundedKnapsackDP
from generate_data import load_data_from_txt
import os

n = [100, 1000, 10000]
for i in n:
    W, val, wt = load_data_from_txt(f"data_{i}.txt")
    items = list(zip(val, wt))

    start_time = time.time()
    ukp = UKP(W, items)
    solution, value = ukp.solve()
    end_time = time.time()
    elapsed_time = end_time - start_time
    memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # Memory usage in MB
    psutil.Process(os.getpid()).memory_info().rss
    print("With Branch and Bound:")
    print(f"W (knapsack capacity)   :", W)
    print(f"Best value              : {value}")
    print(f"Elapsed Time            : {elapsed_time * 1000} ms")
    print(f"Memory Usage            : {memory_usage} MB")
    print()

    start_time = time.time()
    # Menggunakan fungsi dominated items dari bantuan class UKP yang sudah di-define
    ukp = UKP(W, items)
    ukp.eliminate_dominated_items()
    items = ukp.items  # Kalau di-comment, maka tidak menggunakan fungsi eliminate dominated items
    result, item_config = unboundedKnapsackDP(W, [item[0] for item in items], [item[1] for item in items])
    end_time = time.time()
    elapsed_time = end_time - start_time
    memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # Memory usage in MB
    psutil.Process(os.getpid()).memory_info().rss

    print("With Dynamic Programming")
    print(f"W (knapsack capacity)   :", W)
    print(f"Best value              : {result}")
    print(f"Elapsed Time            : {elapsed_time * 1000} ms")
    print(f"Memory Usage            : {memory_usage} MB")
    print()