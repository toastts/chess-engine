import random
import chess


class Player:
    board = chess.Board

    def __init__(self, board, color, time):
        pass

    def move(self, board):
        print("\nLegal moves: " )
        for i in board.legal_moves:
            print(i.uci() + " ")
        while(True):
            uci = input(">")
            try:
                move = chess.Move.from_uci(uci)
                if move in board.legal_moves:
                    return move
                else:
                    print("what, you used to checkers or something?")
            except:
                print("not recognized as a move you dummy")

    def moverType(self):
        return True
