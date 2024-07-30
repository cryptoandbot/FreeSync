import numpy as np
import sympy as sym
import copy as cpy

def stakeCalc(arbOpp, stake):
    stakePerGame = []
    for game in arbOpp:
        if len(game) == 2:
            matrix = np.empty((2, 0))
            n = 1
            for outcome in game.keys():
                for book in game[outcome]:
                    odd = game[outcome][book]
                    odds = np.matrix([[n * odd], [1]])
                    matrix = np.concatenate((matrix, odds), axis=1)
                    n = -1

            matrix = np.concatenate((matrix, [[0], [stake]]), axis=1)
            matrix = sym.Matrix(matrix).rref()[0]
            matrix = np.array(matrix).astype(np.float64)
            copy = cpy.deepcopy(game)
            n = 0
            for outcome in game.keys():
                for book in game[outcome]:
                    copy[outcome][book] = matrix.item(n,2)
                    n += 1
            stakePerGame.append(copy)

        elif len(game) == 3:
            oddsList = []
            for outcome in game.keys():
                for book in game[outcome]:
                    oddsList.append(game[outcome][book])
            matrix = np.matrix([[oddsList[0], -oddsList[1], 0, 0],
                                [0, -oddsList[1], oddsList[2], 0],
                                [1, 1, 1, stake]])
            matrix = sym.Matrix(matrix).rref()[0]
            matrix = np.array(matrix).astype(np.float64)
            copy = cpy.deepcopy(game)
            n = 0
            for outcome in game.keys():
                for book in game[outcome]:
                    copy[outcome][book] = matrix.item(n, 3)
                    n += 1
            stakePerGame.append(copy)

    return stakePerGame

def payoutPerStake(arbOpp, stakePerGame):
    payoutList = []
    for game in range(len(stakePerGame)):
        for outcome in stakePerGame[game].keys():
            for book in stakePerGame[game][outcome]:
                stake = stakePerGame[game][outcome][book]
                payout = arbOpp[game][outcome][book] * stake
                copy = stakePerGame[game]
                copy[outcome][book] = payout
        payoutList.append(copy)
    return payoutList
