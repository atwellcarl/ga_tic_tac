'''
Top level functionality of tic tac toe program. Also contains
the AI to play an optimal game of tic tac toe.

Authors: Carl Atwell, Kaelan Engholdt
Date: 12/09/2019

'''

from random import randint
import tic_tac_toe
import copy
import warnings

# turn runtime warnings off
warnings.filterwarnings("ignore")

# GLOBALS
brd = []            # the board
who = ''            # indicates whether a human player or an AI will play against the GA
game_over = False   # indicates if the game has ended
win_count = 0       # counts the number of wins the GA achieves
loss_count = 0      # counts the number of losses the GA gets


def main():
    global brd, who, game_over, win_count, loss_count

    for i in range(3):
        brd.append([])
        for j in range(3):
            brd[i].append(0)
    temp = copy.deepcopy(brd)
    print('Welcome to GA Tic-Tac-Toe')
    print('Standard rules apply')
    print('Please stay and play a while :)\n')
    print('Board coordinates are as follows:')
    print('[00 01 02]')
    print('[10 11 12]')
    print('[20 21 22]\n')
    games_played = 0

    invalid = True
    while(invalid):
        games_played = raw_input("How many games of tic-tac-toe would you like to play? ")
        try:
            games_played = int(games_played)
            invalid = False
        except:
            pass

    invalid = True
    while (invalid):
        opponent = raw_input("Who will play the GA (human or ai)? ")
        if opponent == "human" or opponent == "ai":
            if opponent == "human":
                who = 'human'
                print("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
                print("The pathetic human vs. GA: Steve")
                print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
                print('\nPlayer 1 (human) will be 1.')
                print('Player 2 (GA) will be 2.')
            else:
                who = 'minimax'
                print("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
                print("AI: Minimax vs. GA: Steve")
                print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
                print('\nPlayer 1 (AI) will be 1.')
                print('Player 2 (GA) will be 2.')
            invalid = False

    tie_count = 0
    temp_brd = copy.deepcopy(brd)
    for i in range(games_played):
        game_over = False
        print("\nGame {} of {}".format(i + 1, games_played))
        print("_______________")
        starter, ender = first_move()
        # starter = '2'
        # ender = '1'
        print('The first move will be played by {}.'.format(starter))
        tie_count += play_game(starter, ender)
        brd = copy.deepcopy(temp_brd)
    print("\nGA Performance:")
    print("{} out of {} games won.".format(win_count, games_played))
    print("{} out of {} games tied.".format(tie_count, games_played))
    print("{} out of {} games lost.".format(loss_count, games_played))

def play_game(starter, ender):
    global game_over

    # temps ti switch
    temp = starter
    temp1 = ender
    won = 0

    while(not is_win() and possibleMove(brd) == True):
        if(temp == '2'):
            player = tic_tac_toe.ga_tic_tac()
            x, y = player.run_ga(brd, 0)
            print("The GA chose {} {} for its move.".format(x, y))
            make_play(temp, x, y)
        else:
            if who == 'human':
                invalid = True
                while(invalid):
                    coors = raw_input('What is your move? ')
                    invalid = not make_play(temp, int(coors[0]), int(coors[1]))
            elif who == 'minimax':
                x, y = best_move()
                print('The AI chose {} {} for its move.'.format(x, y))
                make_play(temp, x, y)
            else:
                raise
        print_board()
        if(possibleMove(brd) == False):
            won = 1
        # swap player turns
        temp2 = temp
        temp = temp1
        temp1 = temp2

    if not game_over and possibleMove(brd) == False:
        print('!!Tie Game!!')

    return won

def is_win():
    global game_over, win_count, loss_count

    # check rows (left to right)
    for i in brd:
        temp = ''
        for j in i:
            temp += str(j)
        if(temp == '111'):
            print ('!!1 Wins!!')
            loss_count += 1
            game_over = True
            return True
        elif(temp == '222'):
            print('!!2 Wins!!')
            win_count += 1
            game_over = True
            return True

    # check columns (up and down)
    for k in range(len(brd)):
        temp = ''
        for l in range(len(brd[k])):
            temp += str(brd[l][k])
        if(temp == '111'):
            print ('!!1 Wins!!')
            loss_count += 1
            game_over = True
            return True
        elif(temp == '222'):
            print('!!2 Wins!!')
            win_count += 1
            game_over = True
            return True

    # check diagonal (left to right)
    temp = ''
    for i in range(len(brd)):
        temp += str(brd[i][i])
    if(temp == '111'):
        print ('!!1 Wins!!')
        loss_count += 1
        game_over = True
        return True
    elif(temp == '222'):
        print('!!2 Wins!!')
        win_count += 1
        game_over = True
        return True

    # check diagonal (right to left)
    temp = ''
    for i in range(len(brd)):
        temp +=str(brd[(len(brd) - 1) - i][i])
    if(temp == '111'):
        print ('!!1 Wins!!')
        loss_count += 1
        game_over = True
        return True
    elif(temp == '222'):
        print('!!2 Wins!!')
        win_count += 1
        game_over = True
        return True

    return False

def first_move():
    num = randint(0, 1)
    if(num == 0):
        return '1', '2'
    elif(num == 1):
        return '2', '1'

def print_board():
    for i in range(len(brd)):
        print brd[i]

def make_play(mark, coor_x, coor_y):
    if is_valid(coor_x, coor_y):
        brd[coor_x][coor_y] = int(mark)
        return True
    else:
        return False

def is_valid(coor_x, coor_y):
    if (coor_x == 0 or coor_x == 1 or coor_x == 2) and \
       (coor_y == 0 or coor_y == 1 or coor_y == 2) and \
        brd[coor_x][coor_y] == 0:
        return True
    else:
        return False

# determines if there are possible moves on the board
def possibleMove(board):
    for i in board:
        for j in i:
            if( str(j) == '0'):
                return True
    return False

def eval_board(board):
    # check left to right
    for i in board:
        temp = ''
        for j in i:
            temp += str(j)
        if(temp == '111'):
            return 10
        elif(temp == '222'):
            return -10

    # check up and down
    for k in range(len(board)):
        temp = ''
        for l in range(len(board[k])):
            temp += str(board[l][k])
        if(temp == '111'):
            return 10
        elif(temp == '222'):
            return -10

    # check left to right diagonal
    temp = ''
    for i in range(len(board)):
        temp += str(board[i][i])
    if(temp == '111'):
        return 10
    elif(temp == '222'):
        return -10

    #check right to left diagonal
    temp = ''
    for i in range(len(board)):
        temp += str(board[(len(board) - 1) - i][i])
    if(temp == '111'):
        return 10
    elif(temp == '222'):
        return -10
    return 0


def minimax(board, depth, is_max):
    score = eval_board(board)
    # base cases
    # if AI has won
    if(score == 10):
        return score
    # if player has won
    if (score == -10):
        return score
    # if there are no moves left
    if(possibleMove(board) == False):
        return 0

    # recursive cases
    if(is_max == True):
        best = -1000

        for i in range(len(board)):
            for j in range(len(board)):
                if (board[i][j] == 0):
                    board[i][j] = 1
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = 0
        return best

    elif(is_max == False):
        best = 1000
        for i in range(len(board)):
            for j in range(len(board)):
                if(board[i][j] == 0):
                    board[i][j] = 2
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = 0
        return best

def best_move():
    board = brd
    best_move = -1000
    best_x = 8
    best_y = 8

    for i in range(len(brd)):
        for j in range(len(brd[i])):
            if(board[i][j] == 0):
                board[i][j] = 1
                move = minimax(board, 0, False)
                board[i][j] = 0

                if(move > best_move):
                    best_move = move
                    best_x = i
                    best_y = j

    return best_x, best_y

if __name__ == '__main__':
    main()
