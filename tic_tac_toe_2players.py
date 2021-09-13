import sys

# This is the simplest implementation of tic-tac-toe for a pair of players

# input-output ---------------------------------------------


def clear_field():          # clear playing field
    f = [[' ' for i in range(3)] for i in range(3)]
    return f


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

# globals -----------------------------------------------------


cross  = 'x'    # cross sign
nought = '0'    # nought sign

game = 0        # the game state
win  = 1
draw = 2

score_crosses = 0
score_noughts = 0

# lines to check ----------------------------------------------


def get_column(f, col):
    return [ f[row][col] for row in range(3)]


def get_diagonal_1(f):
    return [ f[i][i] for i in range(3) ]


def get_diagonal_2(f):
    return [ f[i][2 - i] for i in range(3) ]


def put_sign(f, sign):  # get the cell number and check if it is free
    while True:
        row = get_num("cтрока  : ")     # get row
        col = get_num("столбец : ")     # get column
        row -= 1
        col -= 1
        if f[row][col] == ' ':
            f[row][col] = sign
            return
        print("клетка уже занята, попробуй еще!")

# next move -------------------------------------------------


def next_move(f, sign):             # next move, f- playing field, sign - current sign

    if sign == cross : print("Ход крестиков")
    if sign == nought: print("Ход ноликов")

    put_sign(f, sign)   # get new position
    draw_field(f)        # draw playing field

    def check_line(line, s):                                            # check line for win
        if line == [ s for i in range(3) ]:return win
        return game

    for row in range(3):                                                # check rows
        if check_line(f[row], sign) == win: return win

    for col in range(3):                                                # check columns
        if check_line(get_column(f,col), sign) == win: return win

    if check_line(get_diagonal_1(f), sign) == win: return win           # check diagonal 1

    if check_line(get_diagonal_2(f), sign) == win: return win           # check diagonal 2

    for row in range(3):                                                # look for a free cell
        for col in range(3):
            if f[row][col] == ' ': return game

    return draw                                                         # no free cells

# next game -----------------------------------------------------


def next_game():

    global score_crosses
    global score_noughts

    def inverse(s):
        if s == cross: return nought
        if s == nought: return cross

    say_end()
    field = clear_field()
    draw_field(field)
    sign = cross
    state = game
    while state == game:
        state = next_move(field, sign)
        if state == win :
            if sign == cross :
                print("Выигрыш крестиков!")
                score_crosses += 1
                return
            if sign == nought:
                print("Выигрыш ноликов!")
                score_noughts += 1
                return
        if state == draw:
            print("Боевая ничья!")
            return
        sign = inverse(sign)

# the whole session -----------------------------------------------


def say_end():
    print("Если надоест, скажи вошебное слово end, и игра закончится")


print("Привет!")
while True:
    next_game()
    print(f"crosses : {score_crosses}")
    print(f"noughts : {score_noughts}")
    print("Будешь еще играть?")
    answer = get_line("Если да, скажи вошебное слово yes : ")
    if answer != "yes":
        say_good_by()
        exit(0)







