from tkinter import *
import random as rn

w = Tk()
w.geometry("580x580")
w.title("지뢰찾기")

label = Label(w, text="Minesweeper Game", height=2, font=("Microsoft Sans Serif", 12))
label.pack()

mineList = []
buttonList = []
gameOver = 0
mode = 0  # 0은 파기 1은 지뢰 표시하기
find = 40
gameStarted = 0


def modeChange():
    global mode
    if mode == 0:
        mode = 1
        modeBt.config(bg="pink", text="FLAG")
    elif mode == 1:
        mode = 0
        modeBt.config(bg="yellow green", text="DIG")


modeBt = Button(
    w,
    text="DIG",
    width=6,
    height=1,
    bg="yellow green",
    font=("Microsoft Sans Serif", 15),
    command=modeChange,
)
modeBt.place(x=250, y=50)
findbt = Button(w, text=find, width=6, height=1, font=("Microsoft Sans Serif", 15))
findbt.place(x=50, y=50)


def main():
    global mode, gameStarted, gameOver, find, mineList, buttonList, timer

    mineList = [[0] * 16 for i in range(16)]
    buttonList = []
    gameOver = 0
    find = 40
    gameStarted = 0

    timer.timeSet()

    findbt["text"] = f"{find:03d}"
    timeBt["text"] = "000"
    resetbt["text"] = "Abandon"
    label["text"] = "Minesweeper Game"
    if mode == 1:
        modeChange()

    mine = []
    for i in range(216):
        mine.append(0)
    for i in range(40):
        mine.append(-1)

    for i in range(16):
        for j in range(16):
            m = rn.choice(mine)
            mineList[i][j] = m
            mine.remove(m)

    for i in range(16):
        rows = []
        for j in range(16):
            mine1 = Mine(i, j)
            mine1.b.place(x=30 * j + 50, y=25 * i + 100)
            rows.append(mine1)
        buttonList.append(rows)

    for i in range(16):
        for j in range(16):
            around(i, j)

    mineCount()

    w.mainloop()


def abandonGame():
    global timer, gameOver

    if gameOver == 0:
        resetbt["text"] = "New Game"
        gameOver = 1
        return

    resetbt["text"] = "Abandon"
    main()


timeBt = Button(w, text="000", width=6, height=1, font=("Microsoft Sans Serif", 15))
timeBt.place(x=450, y=50)

resetbt = Button(
    w, width=8, height=1, font=("Microsoft Sans Serif", 15), command=abandonGame
)
resetbt.place(x=426, y=510)


def findDown():
    global find
    find -= 1
    findbt["text"] = f"{find:03d}"


def findUp():
    global find
    find += 1
    findbt["text"] = f"{find:03d}"


class Timer:
    time = 0

    def timeSet(self, time=0):
        self.time = time

    def timeUp(self):
        global gameStarted, gameOver

        if self.time >= 999 or gameOver == 1:
            return
        else:
            gameStarted = 1
            timeBt["text"] = f"{self.time:03d}"
            self.time += 1
            w.after(1000, self.timeUp)


class Mine:
    def __init__(self, i, j):
        self.ii = i
        self.jj = j
        self.b = Button(
            text="",
            width=3,
            height=1,
            font=("Microsoft Sans Serif", 9),
            bg="gray",
            command=self.click,
        )
        self.lcnt = 0
        self.rcnt = 0
        self.lst = []

    def click(self):
        global gameStarted, gameOver, mode, label, mineList, buttonList, timer

        if gameOver == 0 and mode == 0 and self.rcnt == 0 and self.lcnt == 0:
            if mineList[self.ii][self.jj] == -1:
                over()
            else:
                if gameStarted == 0:
                    timer.timeUp()
                self.lcnt = 1
                dfs(self.ii, self.jj)
                winCheck()
                if gameOver == 1:
                    label["text"] = "You Won"
                    return
        elif gameOver == 0 and mode == 1 and self.lcnt == 0:
            if self.rcnt == 0:
                if gameStarted == 0:
                    timer.timeUp()
                self.b.config(bg="light blue", text="*")
                self.rcnt = 1
                findDown()
            elif self.rcnt == 1:
                self.b.config(bg="gray", text="")
                self.rcnt = 0
                findUp()
        elif gameOver == 0 and self.lcnt == 1:
            aroundShow(self.ii, self.jj)
            if gameOver == 1:
                return
            winCheck()
            if gameOver == 1:
                label["text"] = "You Won"
                return


def mineCount():
    for i in range(16):
        for j in range(16):
            if mineList[i][j] == -1:
                continue
            else:
                for t in buttonList[i][j].lst:
                    if mineList[t[0]][t[1]] == -1:
                        mineList[i][j] += 1


def around(x, y):
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i >= 0 and i <= 15 and j >= 0 and j <= 15:
                if not (i == x and j == y):
                    buttonList[x][y].lst.append([i, j])


def aroundShow(x, y):
    cnt = 0
    for t in buttonList[x][y].lst:
        if buttonList[t[0]][t[1]].rcnt == 1:
            cnt += 1

    if cnt == mineList[x][y]:
        for t in buttonList[x][y].lst:
            if buttonList[t[0]][t[1]].rcnt == 0:
                buttonList[t[0]][t[1]].lcnt = 1
                buttonList[t[0]][t[1]].b["bg"] = "white"
                if mineList[t[0]][t[1]] == 0:
                    dfs(t[0], t[1])
                elif mineList[t[0]][t[1]] == -1:
                    over()
                elif mineList[t[0]][t[1]] == 10:
                    continue
                else:
                    buttonList[t[0]][t[1]].b["text"] = mineList[t[0]][t[1]]


def dfs(x, y):
    buttonList[x][y].lcnt = 1

    if buttonList[x][y].rcnt == 0:
        buttonList[x][y].b["bg"] = "white"

        if mineList[x][y] == 0:
            buttonList[x][y].b["text"] = " "
            mineList[x][y] = 10
            for i in buttonList[x][y].lst:
                dfs(i[0], i[1])
        elif mineList[x][y] > 0 and mineList[x][y] < 10:
            buttonList[x][y].b["text"] = mineList[x][y]
        elif mineList[x][y] == 10:
            buttonList[x][y].b["text"] = " "


def winCheck():
    cnt = 0
    global gameOver, gameStarted

    for i in range(16):
        for j in range(16):
            if mineList[i][j] != -1:
                if buttonList[i][j].lcnt == 1:
                    cnt += 1

    if cnt == 216:
        resetbt["text"] = "New Game"
        gameOver = 1
        return


def over():
    global gameOver, timer
    gameOver = 1
    timer.timeSet()

    for k in range(16):
        for l in range(16):
            if mineList[k][l] == -1:
                buttonList[k][l].b.config(text="#", bg="red", fg="white")
    label["text"] = "Oops!"
    resetbt["text"] = "New Game"
    return


timer = Timer()

main()
