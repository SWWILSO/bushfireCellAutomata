import csv
        
def parse_scenario(filename):
    
    # convert file to list that we can begin parsing
    csv_file = open(filename)
    reader = [tuple(line) for line in csv.reader(csv_file)]
    
    # build shell dictionary with correct data type for each key value, \
    # which will be incrementally populated later
    model_input = {'f_grid': [], 'h_grid': [], 'i_threshold': int(), \
                   'w_direction': '', 'burn_seeds': []}
    
    # if grid dimensions are acceptable, add them to dictionary using list index
    grid_size = int(reader[0][0])
    
    if grid_size > 0:
        f_list = reader[1: grid_size + 1]
        h_list = reader[grid_size + 1: grid_size * 2 + 1]

        for coords in f_list:
            model_input['f_grid'].append([int(points) for points in coords])
        for coords in h_list:
            model_input['h_grid'].append([int(points) for points in coords])
        
    #add ignition threshold to dictionary
        model_input['i_threshold'] = int(reader[grid_size * 2 + 1][0])
    
    # add wind direction, to be checked against accepted values later
        wind_check = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        model_input['w_direction'] = reader[grid_size * 2 + 2][0]
    
    # so long as the burn cells are within the grid dimensions, add them \
    # to the dictionary
        burn_list = reader[grid_size * 2 + 3:]
        for (point1, point2) in burn_list:
            if 0 <= int(point1) < grid_size and 0 <= int(point2) < grid_size:
                model_input['burn_seeds'].append(tuple([int(point1), \
                                                        int(point2)]))
  
    # complete final check of ignition and wind direction values
    # if OK, return the parsed model scenario
    if 0 < model_input['i_threshold'] < 8 and model_input['w_direction'] \
    in wind_check:
        return model_input
    
    # if any value checks fail, return None
    else:
        return None