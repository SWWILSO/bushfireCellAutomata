from collections import defaultdict
from itertools import permutations

# these values will be used later to find cells adjacent to (i, j)
adjacent_ref = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0),\
                  (1, -1), (0, -1)]

# if there is wind, these values will be used to find additional cells \
# adjacent to (i, j)
wind_ref = {'N': [(-2, -1), (-2, 0), (-2, 1)],\
            'NE': [(-2, 1), (-2, 2), (-1, 2)],\
            'E': [(-1, 2), (0, 2), (1, 2)],\
            'SE': [(1, 2), (2, 2), (2, 1)],\
            'S': [(2, 1), (2, 0), (2, -1)],\
            'SW': [(2, -1), (2, -2), (1, -2)],\
            'W': [(1, -2), (0, -2), (-1, -2)],\
            'NW': [(-1, -2), (-2, -2), (-2, -1)]}

def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    
    # first, i'll build the grid with respective dimensions \
    # (burn, fuel, height) added for each cell
    grid_size = len(f_grid)  
    input_cell = (i, j)
    separator = ''
    cells_list = [str(i) for i in range(grid_size)]
    cells_sequence = str((separator.join(cells_list)))
    
    grid_dd = defaultdict(list)
    for row, col in permutations(cells_sequence, 2):
        grid_dd[int(row), int(col)].append(b_grid[int(row)][int(col)])
        grid_dd[int(row), int(col)].append(f_grid[int(row)][int(col)])
        grid_dd[int(row), int(col)].append(h_grid[int(row)][int(col)])
    for row in range(len(cells_sequence)):
        grid_dd[int(row), int(row)].append(b_grid[int(row)][int(row)])
        grid_dd[int(row), int(row)].append(f_grid[int(row)][int(row)])
        grid_dd[int(row), int(row)].append(h_grid[int(row)][int(row)])

    # second, find all the cells adjacent to (i, j), irrespective of whether \
    # they're on the grid - for now
    all_adjacents = [(i + adj_row, j + adj_col) for adj_row, adj_col\
                 in adjacent_ref]
    
    # if there's wind, add these cells to possible adjacents
    if w_direction in wind_ref:
        for adj_row, adj_col in wind_ref[w_direction]:
            all_adjacents.append((i + adj_row, j + adj_col))

    # filter all adjacents which aren't on the grid
    adj_input_cells = [cells for cells in all_adjacents if cells in grid_dd]
    
    # check whether there are any burning cells adjacent to (i, j) \
    # if so, individually add their ignition factor taking height into account
    ignition_factor = 0
    for cell in adj_input_cells:
        if grid_dd[cell][0] is True:
            if grid_dd[input_cell][2] > grid_dd[cell][2]:
                ignition_factor += 2
            if grid_dd[input_cell][2] == grid_dd[cell][2]:
                ignition_factor += 1
            if grid_dd[input_cell][2] < grid_dd[cell][2]:
                ignition_factor += 0.5
    
    # check whether (i, j) is already burning and there's fuel
    if grid_dd[input_cell][0] is False and grid_dd[input_cell][1] > 0:
    
        # if so, do final check for whether ignition factor is high enough \
        # for (i, j) to start burning
        if ignition_factor >= i_threshold:
            return True
        else:
            return False
    else:
        return False