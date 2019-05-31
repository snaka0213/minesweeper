import sys
from myClass import Object, Status, BoardData, check_win

#objects
WALL, NONE = Object.wall, Object.none
MINE, PANEL, CHECK = Object.mine, Object.panel, Object.check

#for console
obj_list = ['　', '１', '２', '３',
'４', '５', '６', '７', '８', '＊', '・', '＃']
def show_board(status, board):
    height = status.height
    width = status.width

    for i in range(height):
        line = ''
        for j in range(width):
            line += obj_list[board[i+1][j+1]]
        print(line)

#set_status
def set_status(status, level):
    if level == 1:
        return Status(10, 9, 9, -1, False)
    elif level == 2:
        return Status(40, 16, 16, -1, False)
    elif level == 3:
        return Status(99, 16, 30, -1, False)
    else:
        status.time = -1
        status.state = False
        return status

#global parameters
status = Status(mine = 10, width = 9, height = 9, time = -1, state = False)
level = int(input("level(1/2/3) >> "))
status = set_status(status, level)
board_data = BoardData(status)
board_data.initialize()

while not check_win(board_data):
    status = board_data.status
    open_board = board_data.open_board
    closed_board = board_data.closed_board

    show_board(status, open_board)
    select = input("open / check >> ")
    i = int(input("column >> "))
    j = int(input("row >> "))
    if select == "open":
        board_data.open_panel(i, j)
    elif select == "check":
        board_data.check_panel(i, j)
    if closed_board[i][j] == MINE:
        show_board(status, open_board)
        print("Game Over")
        sys.exit()

print("Game Clear!")
sys.exit()
