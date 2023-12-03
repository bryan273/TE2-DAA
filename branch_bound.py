# Branch & Bound Unbounded 0/1 Knapsack
"""
Copyright (c) 2023 Bryan Tjandra
"""

import math

class UKP:
    def __init__(self, W, items, debug=False):
        self.W = W
        self.items = items
        self.n = len(items)
        self.M = None
        self.best_solution = None
        self.best_value = None
        self.debug = debug

    def eliminate_dominated_items(self):
        """
        Eliminate dominated item to remove the excess calculation of items
        """
        N = list(range(self.n))
        j = 0
        while j < len(N) - 1:
            k = j + 1
            while k < len(N):
                wj, vj = self.items[N[j]][1], self.items[N[j]][0]
                wk, vk = self.items[N[k]][1], self.items[N[k]][0]
                if (wk // wj) * vj >= vk:
                    N.pop(k)
                elif (wj // wk) * vk >= vj:
                    N.pop(j)
                    k = len(N)
                else:
                    k += 1
            j += 1
        self.items = [self.items[i] for i in N]
        self.n = len(self.items)
        if self.debug:
          print(f"After elimination: {self.items}")

    def calculate_upper_bound(self, W_prime, V_N, i):
        """
        W_prime: The residual capacity of the knapsack at the current node.
        V_N: The total value of the items loaded up to the current node.
        i: The index of the current item being considered.
        """
        items = self.items
        n = self.n

        if i + 2 < n:
            v1, w1 = items[i]
            v2, w2 = items[i + 1]
            v3, w3 = items[i + 2]

            z_prime = V_N + (W_prime // w2) * v2
            W_double_prime = W_prime - (W_prime // w2) * w2
            U_prime = z_prime + (W_double_prime * v3 // w3)

            W_double_prime_adjusted = W_double_prime + math.ceil((1 / w1) * (w2 - W_double_prime)) * w1
            U_double_prime = z_prime + math.floor((W_double_prime_adjusted * v2 / w2) - math.ceil((1 / w1) * (w2 - W_double_prime)) * v1)

            U = max(U_prime, U_double_prime)
        else:
            U = V_N

        if self.debug:
          print(f"Upper Bound at i={i}, W'={W_prime}, V(N)={V_N}: U={U}")
        return U

    def step1_initialize(self):
        self.eliminate_dominated_items()
        self.items.sort(key=lambda x: x[0] / x[1], reverse=True)
        self.M = [[0 for _ in range(self.W + 1)] for _ in range(self.n)]
        self.best_solution = [0 for _ in range(self.n)]
        self.best_value = 0

        x = [0 for _ in range(self.n)]
        i = 0
        x[0] = self.W // self.items[0][1]
        V_N = self.items[0][0] * x[0]
        W_prime = self.W - self.items[0][1] * x[0]
        U = self.calculate_upper_bound(W_prime, V_N, i)
        self.best_value = V_N
        self.best_solution = x.copy()

        m = []
        for _ in range(self.n):
            min_w = float('inf')
            for j, (v, w) in enumerate(self.items):
                if j > _ and w < min_w:
                    min_w = w
            m.append(min_w)
        if self.debug:
          print(f"After sorting: {self.items}")
        if self.debug:
          print(f"Initialization: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, U={U}, m={m}")
        return x, i, V_N, W_prime, U, m

    def step2_develop(self, x, i, V_N, W_prime, U, m):
        while True:
            if W_prime < m[i]:
                if self.best_value < V_N:
                    self.best_value = V_N
                    self.best_solution = x.copy()
                    if self.best_value == U:
                        if self.debug:
                          print(f"Develop 1: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Finish")
                        return x, i, V_N, W_prime, "Finish"
                if self.debug:
                  print(f"Develop 2: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Backtrack")
                return x, i, V_N, W_prime, "Backtrack"
            else:
                min_j = min((j for j in range(i + 1, self.n) if self.items[j][1] <= W_prime), default=None)
                if (min_j is None) or (V_N + self.calculate_upper_bound(W_prime, V_N, min_j) <= self.best_value):
                    if self.debug:
                      print(f"Develop 3: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Backtrack")
                    return x, i, V_N, W_prime, "Backtrack"
                if self.M[i][W_prime] >= V_N:
                    if self.debug:
                      print(f"Develop 4: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Backtrack")
                    return x, i, V_N, W_prime, "Backtrack"
                x[min_j] = W_prime // self.items[min_j][1]
                V_N += self.items[min_j][0] * x[min_j]
                W_prime -= self.items[min_j][1] * x[min_j]
                self.M[i][W_prime] = V_N
                i = min_j
                if self.debug:
                  print(f"Develop 5: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Develop")

    def step3_backtrack(self, x, i, V_N, W_prime, m):
        while True:
            max_j = max((j for j in range(i + 1) if x[j] > 0), default=None)
            if max_j is None:
                if self.debug:
                  print(f"Backtrack 1: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Finish")
                return x, i, V_N, W_prime, "Finish"
            i = max_j
            x[i] -= 1
            V_N -= self.items[i][0]
            W_prime += self.items[i][1]
            if W_prime < m[i]:
                if self.debug:
                  print(f"Backtrack 2: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Backtrack")
                continue
            if V_N + math.floor(W_prime * self.items[i + 1][0] / self.items[i + 1][1]) <= self.best_value:
                V_N -= self.items[i][0] * x[i]
                W_prime += self.items[i][1] * x[i]
                x[i] = 0
                if self.debug:
                  print(f"Backtrack 3: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Backtrack")
                continue
            if W_prime >= m[i]:
                if self.debug:
                  print(f"Backtrack 4: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Develop")
                return x, i, V_N, W_prime, "Develop"
            if self.debug:
              print(f"Backtrack 5: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Backtrack")

    def step4_replace_item(self, x, i, V_N, W_prime, m):
        j = i
        h = j + 1
        while True:
            if self.best_value >= V_N + math.floor(W_prime * self.items[h][0] / self.items[h][1]):
                return x, i, V_N, W_prime, "Backtrack"
            if self.items[h][1] >= self.items[j][1]:
                if (self.items[h][1] == self.items[j][1]) or (self.items[h][1] > W_prime) or (self.best_value >= V_N + self.items[h][0]):
                    h += 1
                    if self.debug:
                      print(f"Replace Item 1: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Develop")
                    continue
                self.best_value = V_N + self.items[h][0]
                self.best_solution = x.copy()
                x[h] = 1
                if self.best_value == self.calculate_upper_bound(W_prime, V_N, h):
                    return x, i, V_N, W_prime, "Finish"
                j = h
                h += 1
                if self.debug:
                  print(f"Replace Item 2: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Develop")
                continue
            else:
                if W_prime - self.items[h][1] < m[h - 1]:
                    h += 1
                    if self.debug:
                      print(f"Replace Item 3: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Develop")
                    continue
                i = h
                x[i] = W_prime // self.items[i][1]
                V_N += self.items[i][0] * x[i]
                W_prime -= self.items[i][1] * x[i]
                if self.debug:
                  print(f"Replace Item 4: x={x}, i={i}, V(N)={V_N}, W'={W_prime}, x^={self.best_solution}, z^={self.best_value}, next_step=Develop")
                return x, i, V_N, W_prime, "Develop"

    def branch_and_bound(self):
        x, i, V_N, W_prime, U, m = self.step1_initialize()
        next_step = "Develop"
        while True:
            if next_step == "Develop":
                x, i, V_N, W_prime, next_step = self.step2_develop(x, i, V_N, W_prime, U, m)
            if next_step == "Backtrack":
                x, i, V_N, W_prime, next_step = self.step3_backtrack(x, i, V_N, W_prime, m)
            if next_step == "Finish":
                break
            if next_step == "Replace":
                x, i, V_N, W_prime, next_step = self.step4_replace_item(x, i, V_N, W_prime, m)
        if self.debug:
          print(f"Branch and Bound: Best solution={self.best_solution}, Best value={self.best_value}")
        return self.best_solution, self.best_value

    def solve(self):
        return self.branch_and_bound()
    

if __name__ == '__main__':
    W = 198
    val = [10, 30, 20, 15, 25, 35, 12, 28, 18]
    wt = [5, 10, 15, 8, 17, 23, 6, 12, 10]
    # wt = [5.1, 10.2, 15.7, 8.5, 17.9, 23.9, 6.7, 12.5, 10.5]

    items = list(zip(val, wt))
    ukp = UKP(W, items, debug=False)
    solution, value = ukp.solve()

    print(f"W (knapsack capacity)   :",W)
    print(f"Items <value, weight>   :",list(zip(val,wt)))
    print(f"Best value              : {solution}")
    print(f"Best item configuration : {value}")