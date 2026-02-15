
from dsa.depth_first_algorithm.helpers import get_path,offset,is_legal_pos,read_maze

from dsa.queue.queue_py import Queue

def bfs(maze, start, end):
    queue = Queue()
    queue.enqueue(start)
    predecessors = {start: None}
    while not queue.is_empty():
        node = queue.dequeue()

        if node == end:
            return get_path(predecessors,start,end)
        for direction in ["up","right","down","left"]:
            row_offset,col_offset = offset[direction]
            neighbors = (node[0]+row_offset, node[1]+col_offset)
            if is_legal_pos(maze, neighbors) and neighbors not in predecessors:
                queue.enqueue(neighbors)
                predecessors[neighbors] = node
    return  None


if __name__ == '__main__':
    # Test 1
    maze = [[0] * 3 for row in range(3)]
    start_pos = (0, 0)
    goal_pos = (2, 2)
    result = bfs(maze, start_pos, goal_pos)
    print(result)
#    assert result == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    print("------------------------")
    # Test 2
    maze = read_maze("dsa/mazes/mini_maze_dfs.txt")

    start_pos = (0, 0)
    goal_pos = (2, 2)
    result = bfs(maze, start_pos, goal_pos)
    print(result)
    assert result == [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]

    # Test 3
    maze = read_maze("dsa/mazes/mini_maze_dfs.txt")
    start_pos = (0, 0)
    goal_pos = (3, 3)
    result = bfs(maze, start_pos, goal_pos)
    assert result is None
