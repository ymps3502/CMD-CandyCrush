import random
from colorama import init, Fore
import os
import platform
import time

colors = 5
board = [[0] * 9 for _ in range(9)]
count = 20
score = 0


def creatBoard():
    for i in range(0, 9):
        for j in range(0, 9):
            try:
                candidate = [x for x in range(1, colors + 1)]
                if(board[i][j - 2] == board[i][j - 1]):
                    try:
                        candidate.remove(board[i][j - 1])
                    except ValueError:
                        pass
                if(board[i - 2][j] == board[i - 1][j]):
                    try:
                        candidate.remove(board[i - 1][j])
                    except ValueError:
                        pass
            except IndexError:
                pass
            board[i][j] = random.choice(candidate)


def printBoard():
    if(platform.system() == 'Windows'):
        os.system('cls')
    else:
        os.system('clear')
    for i in range(9, 0, -1):
        print Fore.LIGHTBLACK_EX + "{0: <2}".format(i),
        for j in board[9 - i]:
            if(j == 1):
                print Fore.LIGHTBLUE_EX + "{0: <2}".format(j),
            if(j == 2):
                print Fore.LIGHTGREEN_EX + "{0: <2}".format(j),
            if(j == 3):
                print Fore.LIGHTYELLOW_EX + "{0: <2}".format(j),
            if(j == 4):
                print Fore.LIGHTWHITE_EX + "{0: <2}".format(j),
            if(j == 5):
                print Fore.LIGHTMAGENTA_EX + "{0: <2}".format(j),
            if(j == 6):
                print Fore.LIGHTRED_EX + "{0: <2}".format(j),
            if(j == 7):
                print Fore.BLUE + "{0: <2}".format(j),
            if(j == 8):
                print Fore.GREEN + "{0: <2}".format(j),
            if(j == 9):
                print Fore.YELLOW + "{0: <2}".format(j),
        print
    print(Fore.LIGHTBLACK_EX + ''.join(
        ['{:<3}'.format(x) for x in range(0, 10)]
    ))


def swap(x1, y1, x2, y2):
    temp = board[y1][x1]
    board[y1][x1] = board[y2][x2]
    board[y2][x2] = temp


def swapCheck():
    for i in range(0, 9):
        for j in range(0, 9):
            try:
                if(board[i][j] != board[i][j + 1]):
                    swap(j, i, j + 1, i)
                    if(has3match()):
                        swap(j, i, j + 1, i)
                        return True
                    else:
                        swap(j, i, j + 1, i)
                    swap(j, i, j, i + 1)
                    if(has3match()):
                        swap(j, i, j, i + 1)
                        return True
                    else:
                        swap(j, i, j, i + 1)
            except IndexError:
                pass
    return False


def has3match():
    for i in range(0, 9):
        for j in range(0, 9):
            try:
                if(board[i][j] == board[i + 1][j] == board[i + 2][j]):
                    return True
            except IndexError:
                pass
            try:
                if(board[i][j] == board[i][j + 1] == board[i][j + 2]):
                    return True
            except IndexError:
                pass
    return False


def eliminate3match():
    same_index_x = []
    same_index_y = []
    for i in range(0, 9):
        for j in range(0, 9):
            try:
                if(board[i][j] == board[i + 1][j] == board[i + 2][j]):
                    same_index_y.append(i)
                    same_index_x.append(j)
                    same_index_y.append(i + 1)
                    same_index_x.append(j)
                    same_index_y.append(i + 2)
                    same_index_x.append(j)
            except IndexError:
                pass
            try:
                if(board[i][j] == board[i][j + 1] == board[i][j + 2]):
                    same_index_y.append(i)
                    same_index_x.append(j)
                    same_index_y.append(i)
                    same_index_x.append(j + 1)
                    same_index_y.append(i)
                    same_index_x.append(j + 2)
            except IndexError:
                pass
    for i, j in zip(same_index_y, same_index_x):
        if(board[i][j] != 0):
            print("elemate ({0}, {1}) = {2}".format(
                j + 1, 9 - i, board[i][j]))
            board[i][j] = 0
            time.sleep(0.75)
            global score
            score = score + 1


def drop():
    for i in range(0, 9):
        array = [row[i] for row in board]
        array = [x for x in array if x != 0]
        while len(array) < 9:
            array.insert(0, random.randint(1, colors))
        for j in range(0, 9):
            board[j][i] = array[j]
    return


def swapable(x1, y1, x2, y2):
    swap(x1, y1, x2, y2)
    if(0 <= x1 == x2 < 9 and abs(y1 - y2) == 1 and has3match()):
        return True
    if(0 <= y1 == y2 < 9 and abs(x1 - x2) == 1 and has3match()):
        return True
    else:
        swap(x1, y1, x2, y2)
        print(
            Fore.YELLOW +
            "can not swap ({0}, {1}), ({2}, {3})"
            .format(x1 + 1, 9 - y1, x2 + 1, 9 - y2)
        )
        time.sleep(3)
        return False


def play_swap(x1, y1, x2, y2):
    if(swapable(x1, y1, x2, y2)):
        global count
        count = count - 1
        while has3match():
            eliminate3match()
            drop()
            printBoard()
    while not swapCheck():
        print("there's no place to move, reset the board")
        time.sleep(3)
        creatBoard()
    return


def printStatus():
    print("score: {0}\t moves: {1}".format(score, count))


def getInput():
    again = False
    while 1:
        msgstr = "Please input the coordinate((x1, y1), (x2, y2)): "
        inputstr = raw_input(msgstr)
        inputstr = inputstr.replace('(', '')
        inputstr = inputstr.replace(')', '')
        inputstr = inputstr.replace(',', '')
        inputstr = inputstr.replace(' ', '')
        coordinate = list(inputstr)
        try:
            coordinate = list(map(int, coordinate))
        except ValueError:
            print(Fore.RED + "Please input currect value!")
            continue
        for i in coordinate:
            if(i > 9 or i < 1):
                again = True
                break
        if(again or len(coordinate) != 4):
            print(Fore.RED + "Please input currect value!")
            again = False
            continue
        break
    return coordinate


def setColors():
    while True:
        msgstr = "Please input number of the color: (3~9)"
        try:
            inputnum = int(input(msgstr))
        except NameError:
            print(Fore.RED + "Please input currect value!")
            continue
        if(inputnum > 9 or inputnum < 3):
            print(Fore.RED + "Please input currect value!")
            continue
        else:
            global colors
            colors = inputnum
            break


if __name__ == "__main__":
    init(autoreset=True)
    setColors()
    while True:
        creatBoard()
        if swapCheck():
            break
    while count > 0:
        printBoard()
        printStatus()
        coordinate = getInput()
        play_swap(
            coordinate[0] - 1, 9 - coordinate[1],
            coordinate[2] - 1, 9 - coordinate[3])
    print("Game Over!")
    print("Your score is {0}".format(score))
