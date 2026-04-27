from random import randint, choices
from prettytable import PrettyTable
# source = ''.join([chr(_) for _ in range(33, 127)])
source = ''.join([chr(_) for _ in range(65, 77)])
str1 = ''.join(choices(source, k=randint(15, 20)))
str2 = ''.join(choices(source, k=randint(15, 20)))


print(f's1: {str1}\ns2:{str2}')

dp = [[''] * len(str1) for _ in range(len(str2))]

for i1, c1 in enumerate(str1):
    for i2, c2 in enumerate(str2):
        dp[i2][i1] = dp[i2-1][i1-1] if i1 and i2 else ''
        if c1 == c2:
            dp[i2][i1] += c2
        else:
            els = [dp[i2][i1-1] if i1 else '', dp[i2-1][i1] if i2 else '']
            els = sorted(els, key = lambda el: len(el))
            dp[i2][i1] = els[-1]


t = PrettyTable()
t.field_names = ['*'] + [f'{i}-{c}' for i, c in enumerate(str1)]
for c, r in enumerate(dp):
    t.add_row([str2[c]] + [f'{_}-{len(_)}' if _ else '-' for _ in r])
print(t)

row = sorted(dp[-1], key= lambda el: len(el))
row = {_ for _ in row if len(_) == len(row[-1])}
print('Наибольшая общая последовательность(и):', ', '.join(row))


