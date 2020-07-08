import math
import copy

DIM = 9
DIM_SQRT = int(math.sqrt(DIM))
assert DIM_SQRT * DIM_SQRT == DIM
# DIMxDIM grid. 1...DIM in row, column, and \sqrt(DIM)x\sqrt(DIM) sub grid.  0 indicates empty


def get_candidates(grid, x, y):
    candidates = [True] * DIM # True means that index is a possibility
    # Remove all entries already in the same column
    for y_idx in range(0, DIM):
        if grid[x][y_idx] > 0:
            candidates[grid[x][y_idx] - 1] = False
            if x == 1 and y == 3:
                print("Removing", grid[x][y_idx])

    if x == 1 and y == 3:
        candidates_list = []
        for idx in range(0, len(candidates)):
            if candidates[idx] is True:
                candidates_list.append(idx + 1)
        print(candidates_list)
    # Remove all entries already in the same row
    for x_idx in range(0, DIM):
        if grid[x_idx][y] > 0:
            candidates[grid[x_idx][y] - 1] = False

    if x == 1 and y == 3:
        candidates_list = []
        for idx in range(0, len(candidates)):
            if candidates[idx] is True:
                candidates_list.append(idx + 1)
        print(candidates_list)

    # Remove all entries already in the same sub-grid
    x_start_sub_grid = (x // DIM_SQRT) * DIM_SQRT
    y_start_sub_grid = (y // DIM_SQRT) * DIM_SQRT
    for x_idx in range(x_start_sub_grid, x_start_sub_grid + DIM_SQRT):
        for y_idx in range(y_start_sub_grid, y_start_sub_grid + DIM_SQRT):
            if grid[x_idx][y_idx] > 0:
                candidates[grid[x_idx][y_idx] - 1] = False

    if x == 1 and y == 3:
        candidates_list = []
        for idx in range(0, len(candidates)):
            if candidates[idx] is True:
                candidates_list.append(idx + 1)
        print(candidates_list)


    candidates_list = []
    for idx in range(0, len(candidates)):
        if candidates[idx] is True:
            candidates_list.append(idx + 1)

    return candidates_list


grid = 1 # DIMxDIM array
# grid 0, 0 is bottom left

def get_best_cell(candidates):
    min_seen = DIM
    best = None
    for k,v in candidates.items():
        if len(v) < min_seen:
            min_seen = len(v)
            best = k
    return best


def fill_grid(grid):
    # Find and store candidates for each cell
    candidates = {} # (x, y) -> [candidates]
    for x in range(0, DIM):
        for y in range(0, DIM):
            if grid[x][y] == 0:
                c = get_candidates(grid, x, y)
                if len(c) == 0:  # no solution exists
                    print(x, y, "has no candidates")
                    return False
                candidates[(x, y)] = c

    explore_candidates(grid, candidates)
    print_grid(grid)
    return True


def update_candidates(candidates, best, c):
    # Remove c from candidates in the same x
    x, y = best
    for y_idx in range(0, DIM):
        if (x, y_idx) in candidates:
            l = candidates[x, y_idx]
            if c in l:
                l.remove(c)
            if len(l) == 0:
                return False

    # Remove c from candidates in the same y
    for x_idx in range(0, DIM):
        if (x_idx, y) in candidates:
            l = candidates[x_idx, y]
            if c in l:
                l.remove(c)
            if len(l) == 0:
                return False

    # Remove c from candidates in the same sub-grid
    x_start_sub_grid = (x // DIM_SQRT) * DIM_SQRT
    y_start_sub_grid = (y // DIM_SQRT) * DIM_SQRT
    for x_idx in range(x_start_sub_grid, x_start_sub_grid + DIM_SQRT):
        for y_idx in range(y_start_sub_grid, y_start_sub_grid + DIM_SQRT):
            if (x_idx, y_idx) in candidates:
                l = candidates[x_idx, y_idx]
                if c in l:
                    l.remove(c)
                if len(l) == 0:
                    return False
 
    return True

import os
import time
def explore_candidates(grid, candidates):
    # Get best cell to explore
    if len(candidates) == 0:
        return True
    best = get_best_cell(candidates)
    x, y = best
    #print("Best is", best, candidates[best])
    # Forward step
    for c in candidates[best]:
        #print("Trying", best, c)
        grid[x][y] = c
        os.system('clear')
        print_grid(grid)
        time.sleep(0.1)
        updated_candidates = copy.deepcopy(candidates)
        del updated_candidates[best]
        update_candidates(updated_candidates, best, c)
        if updated_candidates is None:
            # Backtrack
            #print("backtracking from", best, c)
            grid[x][y] = 0
            os.system('clear')
            print_grid(grid)
            time.sleep(0.1)
        else:
            success = explore_candidates(grid, updated_candidates)
            if success:
                return True
            else:
                # Backtrack
                print("backtracking from", best, c)
                grid[x][y] = 0
                os.system('clear')
                print_grid(grid)
                time.sleep(0.1)


def print_grid(grid):
    for x in range(DIM - 1, -1, -1):
        print(" | ".join([str(x) if x > 0 else ' ' for x in grid[x]]))
        print("___".join(["_"] * DIM))


def read_grid(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    grid = [[int(char) for char in line.strip()] for line in lines]
    grid.reverse()
    return grid

import sys
grid = read_grid(sys.argv[1])
import time
start = time.time()
fill_grid(grid)
end = time.time()
print("done in ", end - start)
        

