import random
"""
Copyright (c) 2023 Bryan Tjandra
"""

def generate_data(n):
    W = 10 * n + random.randint(1, n)
    val = [random.randint(1, 10 * n) * 3 for _ in range(n)]
    wt = [random.randint(1, 2 * n) * 2 for _ in range(n)]
    return W, val, wt

def save_data_to_txt(filename, W, val, wt):
    with open(filename, 'w') as file:
        file.write(f'W: {W}\n')
        file.write('val: ' + ', '.join(map(str, val)) + '\n')
        file.write('wt: ' + ', '.join(map(str, wt)) + '\n')

def load_data_from_txt(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        W = int(lines[0].split(': ')[1])
        val = list(map(int, lines[1].split(': ')[1].split(', ')))
        wt = list(map(int, lines[2].split(': ')[1].split(', ')))
        return W, val, wt

if __name__ == '__main__':
    n = [100, 1000, 10000]
    
    for i in n:
        W, val, wt = generate_data(i)
        save_data_to_txt(f'data_{i}.txt', W, val, wt)
        loaded_W, loaded_val, loaded_wt = load_data_from_txt(f'data_{i}.txt')

        print("Generated data:", W, val, wt)
        print("Loaded data:", loaded_W, loaded_val, loaded_wt)