import random as rn

mineList = [[0] * 12 for i in range(12)]
buttonList = []


def mineCount():
    for i in range(1, 11):
        for j in range(1, 11):
            if mineList[i][j] == -1:
                continue
            else:
                if mineList[i - 1][j - 1] == -1:
                    mineList[i][j] += 1
                if mineList[i - 1][j] == -1:
                    mineList[i][j] += 1
                if mineList[i - 1][j + 1] == -1:
                    mineList[i][j] += 1
                if mineList[i][j - 1] == -1:
                    mineList[i][j] += 1
                if mineList[i][j + 1] == -1:
                    mineList[i][j] += 1
                if mineList[i + 1][j - 1] == -1:
                    mineList[i][j] += 1
                if mineList[i + 1][j] == -1:
                    mineList[i][j] += 1
                if mineList[i + 1][j + 1] == -1:
                    mineList[i][j] += 1


mine = []
for i in range(90):
    mine.append(0)
for i in range(10):
    mine.append(-1)

for i in range(1, 11):
    for j in range(1, 11):
        m = rn.choice(mine)
        mineList[i][j] = m
        mine.remove(m)

for i in mineList:
    print(i)

mineCount()

print("\n\n")
for i in mineList:
    print(i)
