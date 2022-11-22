#!/usr/bin/env python3

import sys
import typing
import doctest
import time
from test import *

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS

def update_formula(formula, var, value):
    """
    Updates the CNF formula based on the given variable and boolean value.
    rtype:List[List[Tuple]]
    
    >>> CNF2 = [[('a', True), ('b', True)],[('c', True), ('d', True)],[('e', True),('a', False)]]
    >>> update_formula(CNF2, 'a', False)
    [[('b', True)], [('c', True), ('d', True)]]
    """
    new_formula = []
    for statement in formula: # [('a', True), ('b', False), ('c', True)]
        statement_to_append = []
        satisfied = False
        for term in statement: # term is tuple (immutable) so no aliasing
            if term[0] != var:
                statement_to_append.append(term)
            else:
                if term[1] == value:
                    satisfied = True
                    break
        if not satisfied:
            if statement_to_append == []:
                return [[]]
            new_formula.append(statement_to_append)
    return new_formula

# def clear_unit_clauses(formula):
#     """
#     Returns formula after propogating unit clauses.
#     >>> CNF3 = [[("d", True)],
#         [("a", False), ("d", True)],
#         [("a", True), ("b", False),['c', True]],
#         [("b", True), ("c", True)],
#         [ ("c", False)],
#         [("a", True), ("b", False), ("c", False)]]
#     >>> clear_unit_clauses(CNF3)
#     [
#         [("a", True), ("b", False)],
#         [("b", True)] ]
#     """
#     # go through until you find unit clause. Once found create a new formula with htat unit clause updated.
#     # Go through this new formula to determine if there are any unit clauses in it.
#     # repeat until there are no unit clauses.
#     # unit_clause_bools = {}
#     # new_formula = formula
#     # agenda = [new_formula]
#     # while agenda:
#     #     # print(agenda)
#     #     new_formula = agenda.pop()
#     #     for clause in new_formula:
#     #         if len(clause) == 1:
#     #             agenda.append(update_formula(new_formula, clause[0][0], clause[0][1]))
#     #             unit_clause_bools[clause[0][0]] = clause[0][1]
#     #             # print(agenda)
#     #             break
#     # return new_formula, unit_clause_bools
            
    
    
#     # agenda = [[clause for clause in formula]]
#     # new_formula = agenda.pop()
#     # while agenda:
#     #     for clause in new_formula:
#     #         if len(clause) == 1:
#     #             new_formula = update_formula(new_formula, clause[0], clause[1])
#     #             break
#     pass
    
def find_unit_clause(formula):
    """
    Finds and returns the first unit clause in the fomula.
    """
    for c in range(len(formula)):
        if len(formula[c]) == 1:
            return c
    return None # not necessary in python, but is more clear to reader 

def SAT_solve(formula):
    """
    Recursively solve the satisfiability assignment.
    """
    # base case: nothing left in the formula
    # if formula == None:
    #     return None
    if not formula:
        return {}
    if [] in formula:
        return None    
    
    # if unit clause, set curr var to that, otherwise, set it to the previous
    clause_idx = find_unit_clause(formula)
    if clause_idx:
        curr_var = formula[clause_idx][0][0]
    else:
        curr_var = formula[0][0][0]
    
    # true case
    formula_true = update_formula(formula, curr_var, True)
    # check that setting the value to True doesn't cause a contridiction, 
    # if it does, don't recurse (discard that path)
    # if [] not in formula_true:
    if formula_true != [[]]:
        result = SAT_solve(formula_true)
        if result != None:
            result[curr_var] = True
            return result
    
    # false case
    formula_false = update_formula(formula, curr_var, False)
    # check that setting the value to False doesn't cause a contridiction, 
    # if it does, don't recurse (discard that path)
    # if [] not in formula_false:
    if formula_false != [[]]:
        result = SAT_solve(formula_false)
        if result != None:
            result[curr_var] = False
            return result
    
    return None

def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.
    DON'T USE FOR RECURSION, CREATE AT LEAST 2 OTHER HELPER FUNCTIONS

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    return SAT_solve(formula)
    # formula without the unit clauses
    # # print(f'Formula: {formula}')
    # start = time.time()
    # not_optim = SAT_solve(formula)
    # print(f'not optim: {not_optim}')
    # print(f'Non Optim Time: {time.time() - start}')
    
    # start2 = time.time()
    # optimized_formula, unit_clause_bools = clear_unit_clauses(formula)
    # # print(f'Optimized: {optimized_formula}')
    # sat_solved = SAT_solve(optimized_formula)
    # if sat_solved is not None:
    #     for k,v in unit_clause_bools.items():
    #         sat_solved[k] = v
    # print(f'Optim: {sat_solved}')
    # print(f'Optim Time: {time.time() - start2}')
    # print(sat_solved)

# def pairwise_cnf(n):
#     """
#     Create CNF that captures pairwise dependence between values at each coordinate.
#     """
    
def pairs_subgrid(n):
    """
    Gets the pairs in a square.
    rtype:List[Tuples]
    
    >>> pairs_subgrid(4)
    """
    # start at the edge of the box as an upper bound
    # subtract off the upperbound when obtaining pairs
    # num = 0
    # while 
    #     if num % n == 0:
    #         return
    #     pass
    # print('PAIRS SUBGRID')
    square_cnf = []
    root_n = int(n**0.5)
    r_max = root_n
    c_max = root_n
    # added = set()
    pair_sets = []
    while r_max < n + root_n:
        while c_max < n + root_n:
            for num in range(1,n+1):
                for r in range(r_max-root_n, r_max):
                    for c in range(c_max-root_n, c_max):
                        for r2 in range(r_max-root_n, r_max):
                            for c2 in range(c_max-root_n, c_max):
                                if r != r2 or c != c2:
                                    square_cnf.append([((r,c,num), False), ((r2,c2,num), False)])
            c_max += root_n
        r_max += root_n
        
    return square_cnf
    
    
    # while r_max < n + root_n:
    #     pairs = get_pairs(r_max, r_max - root_n)
    #     pairs2 = []
    #     # if pairs2 is not []:
    #     #     del pairs2
    #     #     pairs2 = []
    #     # print(f'rmax {r_max}')
    #     for r in range(r_max - root_n, r_max):
    #         # to_add = []
    #         for c in range(r_max-root_n, r_max):
    #             # print((r,c))
    #             # to_append = []
    #             for num in range(1,n+1):
    #                 # added.add((r,c))
    #                 pairs2.extend([((r,c,num),False)])
    #             # to_add.append(to_append)
                        
    #         # pairs2.append(to_add)
    #     # pairs2 = [item for sublist in pairs2 for item in sublist]
            
    #     # print(pairs2)
    #     pair_sets.append(pairs2)
    #     # print(pair_sets)
    #     # pairs2.clear()
    #     r_max += root_n
    # for pair_set in pair_sets:
    #     # print(pair_set)
    #     for pair in pair_set:
    #         for pair2 in pair_set:
    #             if pair != pair2:
    #                 square_cnf.append([pair, pair2])
    # print(square_cnf)                
    

    
                    
            
                        
        #                 # square_cnf.append([((r,c,num), False)])
                    
        #             for pair in pairs:
        #                 square_cnf.append([((,pair[0],num), False), ((k, pair[1],num), False)])
                
        #         for p1 in pairs:
        #             for p2 in pairs:
        #                 if p1 != p2:
        #                     square_cnf.append([(p1+(num,), False), (p2+(num,), False)])
                        
            
        #     # for p_idx in range(len(pairs)-1):
        #     #     square_cnf.append([((pairs[p_idx][0],pairs[p_idx][1],num), False), ((pairs[p_idx+1][0], pairs[p_idx+1][1],num), False)])
        # r_max += root_n  
    # print(square_cnf) 
    # return square_cnf
        
        
    #     c_max = root_n
    #     while c_max < n + root_n:
    #         for num in range(1,n+1):
    #             get_pairs(r_max, r_max - root_n)
    #             square_cnf.append()
    #         c_max += root_n
        
    #     r_max += root_n
    
def get_pairs_square(n, start=0):
    """
    Get all the pairs/possibilities in a square.
    """
    pairs = []
    for i in range(start, n):
        for j in range(start, n):
            pairs.append((i,j))
    return pairs
    
def get_pairs(n, start=0):
    """
    Gets the pairs of a given number and all subsequent numbers.
    rtype:List[Tuples]
    """
    pairs = []
    for num in range(start, n):
        next = 1
        # if not square or n % num + next != 0: # 0,1, 0,1
        while num + next <= n:
            pairs.append((num, num+next))
            # pairs.append([((r,c,num), False), ((r,c,num + next), False)])
            next += 1
            
    return pairs
    
def once_in_row_cnf(board, n):
    """
    Returns the CNF formula of each pair in a row having a given value at most once and of each pair in a column.
    """
    coord = (len(board), len(board[0]))
    cnf_row = []
    cnf_col = []
    # for r in range(coord[0]):
    #     for c in range(coord[1]):
    #         for num in range(n):
    #             cnf_row.append
                
    pairs = get_pairs(n)
    
    for num in range(1,n+1):
        for k in range(coord[0]-1): # because the board is guaranteed square
            for pair in pairs:
                cnf_row.append([((k,pair[0],num), False), ((k, pair[1],num), False)])
                cnf_col.append([((pair[0],k,num), False), ((pair[1], k,num), False)])
                
    # print(cnf_row)
    # print()
    # print(cnf_col)
                
        # for c in range(coord[1]-1):
        #     for pair in pairs:
        #         cnf_col.append([((pair[0],c,num), False), ((pair[1], c,num), False)])
        
        # for r in range(coord[0]-1):
        #     for c in range(coord[1]-1):
        #         cnf_row.append([((r,c,num), False), ((r,c+1,num), False)])
        #         cnf_col.append([((r,c,num), False), ((r+1,c,num), False)])
        
                # next = 1
                # while r + next < coord[1]:
                #     cnf_row.append([((r,c,num), False), ((r,c,num), False)])
                #     next += 1

    cnf_row.extend(cnf_col)
    return cnf_row

def val_exists_cnf(board, n):
    """
    Creates a CNF clauses that check that at least one value exists at a coordinate.
    rtype:List[List[Tuple[Tuple, Bool]]]
    """
    coord = (len(board), len(board[0])) # n x n
    cnf_coords = []
    cnf_pairwise = []
    # cnf_subgrid = []
    for r in range(coord[0]):
        for c in range(coord[1]):
            # makes sure the values already present in the starting board are accounted for.
            if board[r][c] != 0:
                cnf_coords.append([((r,c,board[r][c]), True)])
            # append the condition that there must be at least one value for a coordinate
            cnf_coords.append([((r,c,num), True) for num in range(1,n+1)])
            # makes sure more than one value is not in the same cell
            # this can possibly be made into a helper function if trouble with style checker
            for num in range(1,n):
                next = 1
                while next + num <= n:
                    cnf_pairwise.append([((r,c,num), False), ((r,c,num + next), False)])
                    next += 1
    
    # print(cnf_pairwise)
    cnf_coords.extend(cnf_pairwise)     
    return cnf_coords

def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    
    Example:
    [
        [()]
        ]
    """
    # check there's at least something at each index
    # make sure for each pair of numbers, there's not two nums at the same idx
    # sudoku board = sudoku_board.Transpose
    n = len(sudoku_board)
    # m = len(sudoku_board[0])
    # cnf = []
    # for r in range(n):
    #     for c in range(m):
    #         for i in range(n):
    sudoku_cnf = val_exists_cnf(sudoku_board,n)
    sudoku_cnf.extend(pairs_subgrid(n))
    sudoku_cnf.extend(once_in_row_cnf(sudoku_board, n))
    return sudoku_cnf
            
    


def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolveable board, return None
    instead.
    """
    new_board = [[[] for j in range(n)] for i in range(n)]
    if assignments == None:
        return None
    for k,v in assignments.items():
        if v:
            new_board[k[0]][k[1]] = k[2]
    print(new_board)
    return new_board
            

def _open_case(casename):
    with open(os.path.join(TEST_DIRECTORY, casename + ".json")) as f:
        cnf = json.load(f)
        res = [
            [(variable, polarity) for variable, polarity in clause] for clause in cnf
        ]
        rev = [
            [(variable, polarity) for variable, polarity in clause[::-1]]
            for clause in cnf
        ]
        rev_f = sorted(rev)
        s_f = res[::-1]
        s_f_2 = sorted(res, key=len)
        return res, rev, rev_f, s_f, s_f_2

# def test_it(casename, testfunc):
#     for cnf in _open_case(casename):
#         testfunc(cnf)


if __name__ == "__main__":
    CNF1 = [[('a', True), ('b', False), ('c', True)], [('a', False)]]
    CNF2 = [[('a', True), ('b', True)],[('c', True), ('d', True)],[('e', True),('a', False)]]
    CNF3 = [[("d", True)],
        [("a", False), ("d", True)],
        [("a", True), ("b", False), ("c", True)],
        [("b", True), ("c", True)],
        [ ("c", False)],
        [("a", True), ("b", False), ("c", False)],]
    # CNF3 = 
    # print(clear_unit_clauses(CNF3))
    # print(satisfying_assignment(CNF2))
    # print(find_unit_clauses([[('b', True)], [('c', True), ('d', True)]]))
    # print(update_formula(CNF2, 'a', False))
    # print(CNF2)
    # print(val_exists_cnf(4,4,4))
    # sudoku_test = [[0,0,0,0], 
    #                [1,4,0,0], 
    #                [0,0,1,3],
    #                [0,0,0,0]]
    # suodku_cnf = sudoku_board_to_sat_formula(sudoku_test)
    # # print(suodku_cnf)
    # assignments = SAT_solve(suodku_cnf)
    # print(SAT_solve(suodku_cnf))
    # print(assignments_to_sudoku_board(assignments, 4))
    # print(test_it('F', satisfying_assignment))
    import doctest

    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags, verbose=True)
