import sys

# This script implements the tic-tac-toe game of a person and a program

# The program follows the optimal strategy described in https://ru.wikipedia.org/wiki/

# If the strategy offers several options, a random choice is made

# ------------------------------------------------------------------------


def clear_field():          # clear playing field
    f = [[" " for i in range(3)] for i in range(3)]
    return f

# input-output -----------------------------------------------------------


def draw_field(f):           # draw playing field
    print("   1  2  3")
    for i in range(3):
        s = str(i+1)
        for j in range(3): s = s+"  "+ f[i][j]
        print(s)

def say_good_by(): print("До свидания!")


def get_line(s):             # get line, if it is "end" terminate process
    str = input(s)
    if str == "end":
        say_good_by()
        sys.exit(0)
    return str


def get_num(s):             # get number, it should be between 1 and 3
     while True :
        str = get_line(s)
        try:
            numb = int(str)
            if numb in range(1,4):
                return numb
            else : print("это плохой номер, попробуй еще раз")
        except: print("это не номер, попробуй еще раз")

#  globals ----------------------------------------------------------------


cross  = 'x'        # signs
nought = '0'

game = 0            # game state
win  = 1
loss = 2
draw = 3
over = 4

numb = 0            # move number

last = (0, 0)       # last move of crosses
init = (0, 0)       # init move of crosses

side = [(0,1), (1,2), (2,1), (1,0)]
oppside = [(2,1), (1,0), (0,1), (1,2)]

corner = [(0, 0), (0, 2), (2, 0), (2, 2)]       # corner
oppcorner = [(2, 2), (2, 0), (0, 2), (0, 0)]    # opposite corner

# possible lines ---------------------------------------------------------


def get_column(f, col):                         # column
    return [ f[row][col] for row in range(3)]


def get_diagonal_1(f):                          # diagonal 1
    return [ f[ i][i ] for i in range(3) ]


def get_diagonal_2(f):                          # diagonal 2
    return [ f[i][2 - i] for i in range(3) ]


# take cell cell = (row, col) in playing field f, sign - current sign ------------
def take_cell(f, cell, sign):
    global last
    row = cell[0]
    col = cell[1]
    f[row][col] = sign
    last = cell

# check move result ------------------------------------------------------


def move_result(f, sign):                       # move result,  f - playing field,  sing - opponent sign
    win_line = []
    for i in range(3): win_line.append(sign)

    for row in range(3):                                # check rows
        if f[row] == win_line : return win

    for col in range(3):                                # check columns
        if get_column(f, col) == win_line: return win

    if get_diagonal_1(f) == win_line : return win       # check diagonal 1

    if get_diagonal_2(f) == win_line : return win       # check diagonal 2

    for row in range(3):                                # do we have a free cell?
        for col in range(3):
            if f[row][col] == ' ': return game

    return draw

# opponent move ----------------------------------------------------------


def make_move(f, sign):      # get the cell number and check if it is free
    while True:
        row = get_num("cтрока  : ")     # get row
        col = get_num("столбец : ")     # get column
        row -= 1
        col -= 1
        if f[row][col] == ' ':
            take_cell(f, (row, col), sign)
            return
        print("клетка уже занята, попробуй еще!")


def say_draw(): print("Ну, ничья...")


def opp_move(f, sign):            # opponent move,  f - playing field, sing - opponent sign
    print("Твой ход")
    make_move(f, sign)
    draw_field(f)                       # draw field after move
    result = move_result(f, sign)       # check result
    if result == win:
        print("Ты выиграл, поздравляю!")
        return win
    if result == draw:
        say_draw()
        return draw
    return game

# ------------------------------------------------------------------------


def inverse(sign):                          # my opponent sign
    if sign == cross : return nought
    if sign == nought: return cross
    return None

#  make decision ---------------------------------------------------------


def free_cell(f, cell):     # cell is free
    row = cell[0]
    col = cell[1]
    if f[row][col] == ' ': return True
    else: return False


def crossed(f, cell):       # cross in the cell
    row = cell[0]
    col = cell[1]
    if f[row][col] == 'x': return True
    else: return False


def check_cell(f, p, cell): # if the cell in playing field f is free add it to the list of possibilities p
    row = cell[0]
    col = cell[1]
    if f[row][col] == ' ':p.append((row, col))


def choose_one(f, p, sign): # choose a possibility, f - playing field, p - list of possibilities, sign - current sign
    global last
    take_cell(f, p[0], sign)
    return


def take_free_cell(f, sign):   # take a free cell, f - playing field. sign - current sign
    p = []
    for row in range(3):
        for col in range(3):
            check_cell(f, p, (row, col))
    choose_one(f, p, sign)

# cross decision ----------------------------------------------------------


def cross_decision(f):    # cross decision

    global init
    global last
    global numb

    if numb == 0:
        take_cell(f, (1, 1), cross)
        init = (1,1)
        return

    p = []  # the list of possibilities

    # the nought move is made in the side
    if last == [0,1]:
        check_cell(f, p, (2, 0))
        check_cell(f, p, (2, 2))
    if last == [1,0]:
        check_cell(f, p, (0, 2))
        check_cell(f, p, (2, 2))
    if last == [1, 2]:
        check_cell(f, p, (0, 0))
        check_cell(f, p, (2, 0))
    if last == [2,1]:
        check_cell(f, p, (0, 0))
        check_cell(f, p, (0, 2))

    # the nought move is made in the corner, try to go to the opposite corner
    if last in corner:
        for i in range(4):
            if last == corner[i]:
                check_cell(f, p, oppcorner[i])

    if len(p) != 0 :            # if I have I some possibilities choose one of them
        choose_one(f, p, cross)
        return

    take_free_cell(f, cross)    # look for a free cell

# nought decision ---------------------------------------------------------


def nought_decision(f):

    p = []      # the list of possibilities

    # the first move of the crosses is made in the center, check corners
    if init == (1,1):
        for i in range(4):
            check_cell(f, p, corner[i])

    # the first move of the crosses is made in the corner
    if init in corner:
        if numb == 0:                       # first move?
            take_cell(f, (1, 1), nought)    # go to the center
            return
        if numb == 1:                       # second move?
            for i in range(4):              # take the opposite corner
                if init == corner[i]:
                    if free_cell(f, oppcorner[i]):
                        take_cell(f,oppcorner[i], nought)
                        return
            p = side    # if it is not free choose a side cell

    # the first move of the crosses is made in the side
    if init in side:
        if numb == 0:                       # first move?
            take_cell(f, (1,1), nought)     # go to the center
            return

        if numb == 1:                       # second move

            for i in range(4):              # is the move of the crosses made in the corner?
                if last == corner[i]:
                    take_cell(f, oppcorner[i], nought)
                    return

            if init in side:                                # the move of the crosses made in the side check corners
                if crossed(f,(0,1)) and crossed(f,(1,0)):   # corner 0,0
                    take_cell(f,(0,0), nought)
                    return
                if crossed(f,(1,2)) and crossed(f,(0,1)):   # corner 0,2
                    take_cell(f,(0,2), nought)
                    return
                if crossed(f,(2,1)) and crossed(f,(1,2)):   # corner 2,2
                    take_cell(f,(2,2), nought)
                    return
                if crossed(f,(1,0)) and crossed(f,(2,1)):   # corner 0,2
                    take_cell(f,(0,2), nought)
                    return

                for i in range(4):                  # is the move of the crosses made in the side?
                    if init == side[i]:             # is it the opposite side?
                        if last == oppside[i]:
                            for j in range(4):
                                check_cell(f, p, corner[j])

    if len(p) != 0:                 # if I have some possibilities choose one of them
        print(p)
        choose_one(f, p, nought)
        return

    take_free_cell(f, nought)       # if no take a free cell

# ------------------------------------------------------------------------


def make_decision(f, sign):                  # make decision

    opps = inverse(sign)                    # opponent sign

#   check main things which are the same for crosses and noughts

    chance = []                             # chance
    threat = []                             # threat
    for i in range(3):
        line = [ sign for j in range(3) ]
        line [i] = ' '
        chance.append(line)                 # chance
        line = [ opps for j in range(3) ]
        line [ i ] = ' '
        threat.append(line)                 # threat

    for row in range(3):                    # check rows
        line = f[row]
        for col in range(3):
            if line == chance[col]:
                take_cell(f, (row, col), sign)
                return
            if line == threat[col]:
                take_cell(f, (row, col), sign)
                return

    for col in range(3):                    # check columns
        line = get_column(f,col)
        for row in range(3):
            if line == chance[row]:
                take_cell(f, (row, col), sign)
                return
            if line == threat[row]:
                take_cell(f,(row, col), sign)
                return

    line = get_diagonal_1(f)                # check diagonal 1
    for i in range(3):
        if line == chance[i]:
            take_cell(f, (i, i), sign)
            return
        if line == threat[i]:
            take_cell(f, (i, i), sign)
            return

    line = get_diagonal_2(f)                # check diagonal 2
    for i in range(3):
        if line == chance[i]:
            take_cell(f,(i, 2-i),sign)
            return
        if line == threat[i]:
            take_cell(f,(i, 2-i),sign)
            return

    if sign == cross : cross_decision(f)      # cross decision
    if sign == nought: nought_decision(f)     # nought decision

    return

# my move ----------------------------------------------------------------


def my_move(f, sign):                   # my move, f - playing field, sing - my sign
    make_decision(f, sign)              # make decision
    print("Мой ход такой")
    draw_field(f)                       # draw field
    result = move_result(f, sign)       # check result
    if result == win:                   # is it win?
        print("Ура! Я выиграл!")
        return win
    if result == draw:                  # is it draw?
        say_draw()
        return draw
    return game


def choose_sign():                              # let the opponent to choose sign
    print("Ты какими будешь играть?")
    while True:
        sign = get_line("Скажи x или 0 : ")
        if sign == cross : return sign
        if sign == nought: return sign
        print("Ой, я такими н умею! Давай еще раз!")

# next game  -----------------------------------------------------------


def next_game():
    global numb
    opp_sign = choose_sign()                    # let the opponent to choose sign
    my_sign = inverse(opp_sign)                 # my sign is inverse
    field = clear_field()                       # clear field
    state = game                                # start the game
    numb = 0                                    # first move
    if opp_sign == cross :                      # the first move
        state = opp_move(field, opp_sign)       # is the move of the crosses
    while state == game:
        state = my_move(field, my_sign)         # my move
        if state != game: return state          # check state
        state = opp_move(field, opp_sign)       # opponent move
        if state != game: return state          # check state
        numb += 1                               # next move

# the whole session -----------------------------------------------------


def say_end(): print("Если надоест, скажи вошебное слово end, и игра закончится")


print("Привет, я умею играть в крестики-нолики!")
say_end()
while True:
    s = next_game()
    print("Давай еще сыграем!")
    answer = get_line("Скажи вошебное слово yes : ")
    if answer != "yes":
        say_good_by()
        exit(0)







