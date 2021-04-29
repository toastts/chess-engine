import random
import chess
import keras
from keras import models
import os
import tensorflow as ts
import numpy as np
import sys
from . import heuristics as hr
import concurrent.futures
import chess.polyglot
from multiprocessing import Process

class Player:
    depth=4
    loaded_model=None
    opening_book=None
    opening=None

    def __init__(self, board, color, time):
        dir_path=os.path.dirname(os.path.realpath(__file__))
        os.chdir(os.path.join(dir_path,".."))
        os.chdir("storage")
        self.loaded_model=models.load_model("chess_model.h5")
        os.chdir(os.path.join("..", os.path.join("code1", "books")))
    
    def matrix_rep(self,board):
        board_epd=board.epd()
        mat=[]
        pieces=board_epd.split(" ",1)[0]
        rows=pieces.split("/")
        for r in rows:
            sub_mat=[]
            for pic in r:
                if pic.isdigit():
                    for i in range(0, int(pic)):
                        sub_mat.append('.')
                else:
                    sub_mat.append(pic)
            mat.append(sub_mat)
        return mat
    
    def trans_code(self, matrix, pieces_dict):
        rows=[]
        for row in matrix:
            terms=[]
            for term in row:
                terms.append(pieces_dict[term])
            rows.append(terms)
        return rows
    
    one_hot_pieces_dict ={
        'p' : [1,0,0,0,0,0,0,0,0,0,0,0]
        'P' : [0,0,0,0,0,0,1,0,0,0,0,0]
        'n' : [0,1,0,0,0,0,0,0,0,0,0,0]
        'N' : [0,0,0,0,0,0,0,1,0,0,0,0]
        'b' : [0,0,1,0,0,0,0,0,0,0,0,0]
        'B' : [0,0,0,0,0,0,0,0,1,0,0,0]
        'r' : [0,0,0,1,0,0,0,0,0,0,0,0]
        'R' : [0,0,0,0,0,0,0,0,0,1,0,0]
        'q' : [0,0,0,0,1,0,0,0,0,0,0,0]
        'Q' : [0,0,0,0,0,0,0,0,0,0,1,0]
        'k' : [0,0,0,0,0,1,0,0,0,0,0,0]
        'K' : [0,0,0,0,0,0,0,0,0,0,0,1]
        '.' : [0,0,0,0,0,0,0,0,0,0,0,0]
    }

    def pre_eval(self, trans_mat_reshape):
        return self.loaded_model(trans_mat_reshape)

                