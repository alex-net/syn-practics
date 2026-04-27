from random import randint
from prettytable import PrettyTable
from math import factorial

n = randint(2, 20)
print(f'Число {n}')

dp = [[0 for __ in  range(n+1)] for _ in range(n+1)]
# количество разбиений  числа i1 (i) на слогаемые с максимальным слогаемым i2 (k)
for i1 in range(n+1): # i
    for i2 in range(n+1): # k
        if not i1: # начальное условие
            dp[i1][i2] = 1
        if i1 >= i2 and i2:
            dp[i1][i2] = dp[i1][i2 - 1] + dp[i1 - i2][i2]
        if i1 < i2:
            dp[i1][i2] = dp[i1][i1]


t = PrettyTable()
t.field_names = ['*'] + [i for i in range(n + 1)]
for i, r in enumerate(dp):
    t.add_row([i] + r)

print(t)
print(f'Количество разбиений числа {n} на слогаемые = {dp[n][n]}')
