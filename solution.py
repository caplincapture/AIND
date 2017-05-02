assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # print(value)
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    d1 = test_for_twin(values)
    # iterate through all the values grabbing each dictionary item's key
    # iterate through the keys 
    for key in d1:
        for arr in units[key]:
            for a in arr:
                if (values[key] == values[a] and key != a):
                    # iterate through update values              
                    for y in arr:
                        if(y != key and y != a):
                            values[y] = values[y].replace(values[a][0],'')
                            if(len(values[a]) > 1):
                                values[y] = values[y].replace(values[a][1],'')
 
    # Eliminate the naked twins as possibilities for their peers
    return values

# check each value in a list of columns 
# if there is a twin append it to a list and send it back

def test_for_twin(values):
    d  = []
    for key in values.keys():
        if len(values[key]) == 2:
            d.append(key)
    return d;
            
def cross(A, B):
    # "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# list of diagonal units
diag_1  = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']
diag_2 = ['A9','B8','C7','D6','E5','F4','G3','H2','I1']
# adding diagonals in peer/unit consideration
unitlist = row_units + column_units + square_units + [diag_1, diag_2] 
units = dict((s, [u for u in unitlist if s in u]) for s in boxes) 
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """  

    # dictionary of boxes
    d = {}
    for i in range(len(boxes)):
        d[boxes[i]] = '123456789' if  grid[i] == '.' else grid[i]
    return d
   

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # refer to lesson here
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    pass

def eliminate(values):
    for key,val in values.items():
        if len(val) == 1:
            for p in peers[key]:
                values[p] = values[p].replace(val,'')

    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # reduce puzzle from the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False 
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # retrieve unfilled squares w/ fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
        
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')