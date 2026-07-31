# this is used to go right and left and up and down
offset = {
    "right":(0,1),
    "left":(0,-1),
    "down":(1,0),
    "up":(-1,0),
}

def read_maze(file_name):
    try:
        with open(file_name) as fh:
            maze = [[char for char in line.strip("\n")] for line in fh]
            num_cols_top_row = len(maze[0])
            for row in maze:
                if len(row) != num_cols_top_row:
                    print(" maze is not rectangular")
                    raise SystemExit
            return maze
    except IOError:
        print(" Problem reading maze file")
        raise SystemExit

def is_legal_pos(maze,pos):
    i,j = pos
    num_rows = len(maze)
    num_cols = len(maze[0])
    return 0 <= i < num_rows and 0 <= j < num_cols and maze[i][j] != '*'


def get_path(predecessor,start,goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = predecessor[current]
    path.append(start)
    path.reverse()
    return path