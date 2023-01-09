import os
from shapes import GAP, Cell
import json
from random import randint, choice

class MapGenerator():
    def __init__(self, block_list_name, dir_path="assets/rooms") -> None:
        list_path = os.path.join(dir_path, block_list_name)
        if not os.path.exists(list_path):
            block_list = []
            block_id = 0
            for file_name in os.listdir(dir_path):
                with open(os.path.join(dir_path, file_name), "r") as file:
                    try:
                        block = json.loads(file.read())
                        if block["symmetric"]:
                            block["id"] = block_id
                            block_id = block_id + 1
                            block_list.append(block)
                        else:
                            temp_block_list = []
                            for _ in range(4):
                                block["id"] = block_id
                                block_id = block_id + 1
                                exists = False

                                for existing_block in temp_block_list:
                                    if existing_block["room"] == block["room"]:
                                        exists = True

                                if not exists:
                                    temp_block_list.append(block.copy())

                                block["room"] = rotate_2D_matrix_right(block["room"])
                                block["directions"] = rotate_1D_matrix_right(block["directions"])

                            for new_block in temp_block_list:
                                block_list.append(new_block)
                    except:
                        pass

            with open(list_path, "w+") as block_file:
                json.dump({"blocks": block_list}, block_file, indent=1)

        with open(list_path, "r") as block_list:
            self.block_dict = {}
            for block in json.load(block_list)["blocks"]:
                self.block_dict[block["id"]] = block

    def generate(self, screen_width, screen_hight):
        num_width = ((screen_width // (GAP*2)) // 5)
        num_hight = ((screen_hight // (GAP)) // 5)
        print(f"Map size {num_width}x{num_hight}")
        block_ids = []
        for block_id in self.block_dict.keys():
            block_ids.append(block_id)
        
        self.room_grid = [[block_ids.copy() for _ in range(num_width)] for _ in range(num_hight)]
        self.restriction_grid = [[[-1, -1, -1, -1] for _ in range(num_width)] for _ in range(num_hight)]
        for y, row in enumerate(self.restriction_grid):
            for x, cell in enumerate(row):
                changed = False
                if x == 0:
                    cell[3] = 1
                elif x == len(row) - 1:
                    cell[1] = 1
                
                if y == 0:
                    cell[0] = 1
                elif y == len(self.restriction_grid) - 1:
                    cell[2] = 1
        
        rand_top = randint(0, num_width-1)
        
        if rand_top == 0:
            rand_offset = randint(4,7)
        elif rand_top == num_width-1:
            rand_offset = randint(3,6)
        else:
            rand_offset = randint(3,7)

        self.restriction_grid[0][rand_top][0] = rand_offset
        self.alien_start = (rand_top * 5 + (rand_offset - 3), 0)

        rand_bot = randint(0, num_width-1)
        if rand_bot == 0:
            rand_offset = randint(3,6)
        elif rand_bot == num_width-1:
            rand_offset = randint(4,7)
        else:
            rand_offset = randint(3,7)

        self.restriction_grid[num_hight-1][rand_bot][2] = rand_offset
        self.human_start = (rand_bot * 5 + (7 - rand_offset), num_hight * 5 - 1)
        print(rand_offset)

        for y, row in enumerate(self.restriction_grid):
            for x, cell in enumerate(row):
                if cell != [-1, -1, -1, -1]:
                    self.reduce(x, y)
        print()
        while not self.is_finished():
            for y, row in enumerate(self.room_grid):
                for x, cell in enumerate(row):
                    if len(cell) == 1:
                        continue
                    elif not cell:
                        cell.append(0)
                    temp_id = choice(cell)
                    cell.clear()
                    cell.append(temp_id)
                    self.restriction_grid[y][x] = [res if res != -1 else old_res for res, old_res in zip(self.block_dict[temp_id]["restrictions"], self.restriction_grid[y][x])]
                    self.propagate(x, y)

        self.map = [[[[Cell(room_x + 5 * x, room_y + 5 * y, isWall = room_value) for room_x, room_value in enumerate(room_row)] for room_y, room_row in enumerate(self.block_dict[cell[0]]["room"])]for x, cell in enumerate(row)] for y, row in enumerate(self.room_grid)]
        
        # self.print_map()

    def reduce(self, x, y):
        to_remove = []
        for id in self.room_grid[y][x]:
            if not directions_match(self.block_dict[id]["directions"], self.restriction_grid[y][x]):
                to_remove.append(id)
        if to_remove == self.room_grid[y][x]:
            print()
        for id in to_remove:
             self.room_grid[y][x].remove(id)
    
    def propagate(self, x, y):
        if x - 1 >= 0:
            self.restriction_grid[y][x-1][1] = self.restriction_grid[y][x][3]
        if x + 1 < len(self.restriction_grid[y]):
            self.restriction_grid[y][x+1][3] = self.restriction_grid[y][x][1]

        if y - 1 >= 0:
            self.restriction_grid[y-1][x][2] = self.restriction_grid[y][x][0]
        if y + 1 < len(self.restriction_grid):
            self.restriction_grid[y+1][x][0] = self.restriction_grid[y][x][2]

    def is_finished(self):
        for row in self.room_grid:
            for cell in row:
                if len(cell) > 1:
                    return False
        print("Map finished")
        return True

    def print_map(self):
        for row in self.room_grid:
            for cell in row:
                if isinstance(cell, int):
                    print(cell, end=" ")
                    continue
                if len(cell) > 1:
                    print("?", end=" ")
                elif len(cell) == 0:
                    print("!", end=" ")
                else:
                    print(cell[0], end=" ")
            print()

def rotate_2D_matrix_right(matrix):
    return [[1 if matrix[4-x][y] else 0 for x in range(len(matrix[y]))] for y in range(len(matrix))]

def rotate_1D_matrix_right(matrix):
    return [matrix[x-1] for x in range(len(matrix))]

def directions_match(directions, target):
    for dir, tar in zip(directions, target):
        if tar == -1:
            continue
        elif dir != tar:
            return False
    return True

if __name__ == "__main__":
    matrix = [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1]
    ]
    print(matrix)
    print(rotate_2D_matrix_right(matrix))
    print()
    matrix = [1,2,3,0]
    print(matrix)
    print(rotate_1D_matrix_right(matrix))
    map_gen = MapGenerator("DefaultRooms.json")
    map_gen.generate(1536, 864)