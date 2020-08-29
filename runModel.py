from collections import defaultdict
from itertools import permutations

# reference values to find cells adjacent to (i, j)
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

# helper function to run model for each time step until fire stops burning
def model_step(b_grid, f_grid, h_grid, i_threshold, w_direction, burn_seeds,\
               grid_dd):
     
    # check ignition for each cell in the grid
    for i, j in grid_dd:
        input_cell = (i, j)
        all_adjacents = [(i + adj_row, j + adj_col) for adj_row, adj_col\
             in adjacent_ref]
        if w_direction in wind_ref:
            for adj_row, adj_col in wind_ref[w_direction]:
                all_adjacents.append((i + adj_row, j + adj_col))
        adj_input_cells = [cells for cells in all_adjacents if cells in\
                           grid_dd]
        ignition_factor = 0
        for cell in adj_input_cells:
            if grid_dd[cell][0] is True:
                if grid_dd[input_cell][2] > grid_dd[cell][2]:
                    ignition_factor += 2
                if grid_dd[input_cell][2] == grid_dd[cell][2]:
                    ignition_factor += 1
                if grid_dd[input_cell][2] < grid_dd[cell][2]:
                    ignition_factor += 0.5
        
        # if the cell has been ignited, change its state and add to burn_seeds
        if grid_dd[input_cell][0] is False and grid_dd[input_cell][1] > 0:
            if ignition_factor >= i_threshold:
                b_grid[i][j] = True
                burn_seeds.append((i, j))
        
        # if the cell is already on fire, update fuel and burn values
        if grid_dd[i, j][0] is True:  
            f_grid[i][j] -= 1
            if f_grid[i][j] <= 0:
                b_grid[i][j] = False

    # input updated grid state to 'run_model' function which will check \ 
    # whether the fire is still burning
    return run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds)
       
def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):
    
    # generate burn_grid at time 't' to input to model run
    b_grid = [[False for cells in f_grid] for cells in f_grid]
    for row, col in burn_seeds:
        if f_grid[row][col] > 0:
            b_grid[row][col] = True
    
    # build dictionary of dimensions of the grid at time 't' to input \ 
    # to model run
    grid_size = len(f_grid)  
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
    
    # check whether any cells are burning
    burn_status = []
    for i, j in grid_dd:
        burn_status.append(grid_dd[i, j][0])
    if True in burn_status:
        burn_status = True
    else:
        burn_status = False

    # if the fire is still burning, run the model for t + 1, otherwise return \
    # grid state
    if burn_status is False:
        return f_grid, len(burn_seeds)
    else:
        return model_step(b_grid, f_grid, h_grid, i_threshold, w_direction,\
                          burn_seeds, grid_dd)

