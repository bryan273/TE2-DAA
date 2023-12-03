# Dynamic Programming Unbounded 0/1 Knapsack
"""
Copyright (c) 2023 Bryan Tjandra
"""

def unboundedKnapsackDP(W, val, wt):
    n = len(val)
    dp = [0 for _ in range(W + 1)]
    itemCount = [[0 for _ in range(n)] for _ in range(W + 1)]

    for i in range(1, W + 1):
        for j in range(n):
            if wt[j] <= i and dp[i] < dp[i - wt[j]] + val[j]:
                dp[i] = dp[i - wt[j]] + val[j]
                itemCount[i] = itemCount[i - wt[j]].copy()
                itemCount[i][j] += 1

    return dp[W], itemCount[W]

if __name__ == '__main__':
    W = 198
    val = [10, 30, 20, 15, 25, 35, 12, 28, 18]
    wt = [5, 10, 15, 8, 17, 23, 6, 12, 10]

    max_value, item_config = unboundedKnapsackDP(W, val, wt)
    print(f"W (knapsack capacity)   :",W)
    print(f"Items <value, weight>   :",list(zip(val,wt)))
    print(f"Best value              : {max_value}")
    print(f"Best item configuration : {item_config}")