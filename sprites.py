import random
import math
import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col

class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)
    gameMap = set
    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass

class Zaki2(Agent):

    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def sortMaybeBaby(self, neighbors_sum, maybeBaby, row, col):
        maybeBaby.sort(
            key=lambda element: (
                element.cost(), neighbors_sum[element.position()],
                 math.sqrt((element.row - row) ** 2 + (element.col - col) ** 2)), reverse=True)

# class Aki(Agent):
#     def _init_(self, row, col, file_name):
#         super()._init_(row, col, file_name)
#
#     def get_agent_path(self, game_map, goal):
#
#         possible = []
#         path = [game_map[self.row][self.col]]
#         stack = []
#         paths = []
#
#         row = self.row
#         col = self.col
#         visited = [(row, col)]
#
#         flag = True
#
#         while flag:
#             if row == goal[0] and col == goal[1]:
#                 break
#
#             if row > 0:
#                 example = (row - 1, col)
#                 if example not in visited:
#                     possible.append(game_map[row - 1][col])
#             if col > 0:
#                 example = (row, col - 1)
#                 if example not in visited:
#                     possible.append(game_map[row][col - 1])
#             if row < (len(game_map) - 1):
#                 example = (row + 1, col)
#                 if example not in visited:
#                     possible.append(game_map[row + 1][col])
#             if col < (len(game_map[0]) - 1):
#                 example = (row, col + 1)
#                 if example not in visited:
#                     possible.append(game_map[row][col + 1])
#
#             if not possible:
#                 paths.append(((row, col), []))
#                 elem = stack.pop()
#                 row = elem.row
#                 col = elem.col
#
#                 visited.append((elem.row, elem.col))
#             else:
#                 possible.sort(
#                     key=lambda tile: (
#                         tile.cost(), -4 if tile.row < row else -3 if tile.col > col else -2 if tile.row > row else -1)
#                     , reverse=True)
#                 paths.append(((row, col), possible))
#                 for i in possible:
#                     visited.append(i.position())
#                 stack.extend(possible)
#                 elem = stack.pop()
#                 row = elem.row
#                 col = elem.col
#                 # visited.append((row, col))
#                 possible = []
#
#             if not stack:
#                 flag = False
#
#         paths = paths[-1::-1]
#         elem_r = goal[0]
#         elem_c = goal[1]
#         elem = game_map[goal[0]][goal[1]]
#
#         path_helper = []
#
#         for onepath in paths:
#             for onetile in onepath[1]:
#                 if (elem_r, elem_c) == onetile.position():
#                     elem_r, elem_c = onepath[0]
#                     path_helper.append(onetile)
#
#         path_helper.extend(path)
#         path_helper = path_helper[-1::-1]
#         path = path_helper
#
#         return path
#

class Aki(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def reversePath(self, pomPath):
        pom = pomPath[-1::-1]
        return pom

    def getFinalPath (self, allPaths, row2, col2, path):
        pomPath = []

        for singlePath in allPaths:
            for singleTile in singlePath[1]:
                isGoal = singleTile
                if isGoal.position() == (row2, col2):
                    row2, col2 = singlePath[0]
                    pomPath.append(singleTile)

        pomPath.extend(path)
        pomPath = self.reversePath(pomPath)
        return pomPath

    def sortMaybeBaby(self, maybeBaby, row, col):
        maybeBaby.sort(
            key=lambda element: (
                element.cost(), 0 if element.row < row else 1 if element.col > col else 2 if element.row > row else 3)
            , reverse=True)

    def get_agent_path(self, game_map, goal):
        row = self.row
        col = self.col
        maybeBaby = []
        allPaths = []
        path = [game_map[self.row][self.col]]
        stack = [game_map[self.row][self.col]]
        visited = [(row, col)]

        while len(stack) > 0:

            if len(stack) == 1 and stack[0].position() == (self.row, self.col):
                stack.pop()
            if (row, col) == (goal[0], goal[1]):
                break
            if row > 0:
                if (row - 1, col) not in visited:
                    maybeBaby.append(game_map[row - 1][col])
            if col > 0:
                if (row, col - 1) not in visited:
                    maybeBaby.append(game_map[row][col - 1])
            if row < (len(game_map) - 1):
                if (row + 1, col) not in visited:
                    maybeBaby.append(game_map[row + 1][col])
            if col < (len(game_map[0]) - 1):
                if (row, col + 1) not in visited:
                    maybeBaby.append(game_map[row][col + 1])

            if len(maybeBaby) < 1:
                allPaths.append(((row, col), []))
                elem = stack.pop()
                row = elem.row
                col = elem.col
                visited.append((row, col))
            else:
                self.sortMaybeBaby(maybeBaby, row, col)
                allPaths.append(((row, col), maybeBaby))
                for i in maybeBaby:
                    visited.append(i.position())
                stack.extend(maybeBaby)
                elem = stack.pop()
                row = elem.row
                col = elem.col
                maybeBaby = []

        allPaths = allPaths[-1::-1]
        row2 = goal[0]
        col2 = goal[1]

        return self.getFinalPath(allPaths, row2, col2, path)


class Zaki(Agent):

    def sortMaybeBaby(self, maybeBaby, row, col):
        maybeBaby.sort(key=lambda element: (element.cost(), math.sqrt((element.row - row)**2 + (element.col-col)**2)), reverse=True)


class Bole(Agent):

    def __init__(self, row, col, file_name): super().__init__(row, col, file_name)

    def sortQueue(self, queue, goal0, goal1):
        queue.sort(key=lambda lista: (sum(map(lambda element: element.cost(), lista)),
                                      math.sqrt((lista[-1].row - goal0) ** 2 + (lista[-1].col - goal1) ** 2)))

    def redosled(self, list1, list2, list3, list4):

        len1 = len(list1)
        len2 = len(list2)
        len3 = len(list3)
        len4 = len(list4)
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        minlen = 1000
        minsum = 1000000
        if len1 > 0:
            sum1 = 0
            for pom in list1:
                sum1 += pom.cost()
            if sum1 < minsum: minsum = sum1
            if sum1 == minsum:
                if len1 < minlen: minlen = len1
        if len2 > 0:
            sum2 = 0
            for pom in list2:
                sum2 += pom.cost()
            if sum2 < minsum: minsum = sum2
            if sum2 == minsum:
                if len2 < minlen: minlen = len2
        if len3 > 0:
            sum3 = 0
            for pom in list3:
                sum3 += pom.cost()
            if sum3 < minsum: minsum = sum3
            if sum3 == minsum:
                if len3 < minlen: minlen = len3
        if len4 > 0:
            sum4 = 0
            for pom in list4:
                sum4 += pom.cost()
            if sum4 < minsum: minsum = sum4
            if sum4 == minsum:
                if len4 < minlen: minlen = len4

        if minsum == sum1 and minlen == len1:
            return 1
        if minsum == sum2 and minlen == len2:
            return 2
        if minsum == sum3 and minlen == len3:
            return 3
        if minsum == sum4 and minlen == len4:
            return 4
        return 0


    def get_agent_path(self, game_map, goal):

        list1 = []
        list2 = []
        list3 = []
        list4 = []
        visited = [(self.row, self.col)]
        queue = [[game_map[self.row][self.col]]]
        while len(queue) > 0:

            path = queue.pop(0)
            (row, col) = path[-1].position()

            if (row, col) == (goal[0], goal[1]):
                return path

            if row > 0:
                if game_map[row-1][col] not in path and (row-1,col) not in visited:
                    list1 = path.copy()
                    list1.append(game_map[row - 1][col])
                    visited.append((row-1, col))
            if col > 0:
                if game_map[row][col - 1] not in path and (row, col-1) not in visited :
                    list2 = path.copy()
                    list2.append(game_map[row][col - 1])
                    visited.append((row, col-1))
            if row < (len(game_map) - 1):
                if game_map[row + 1][col] not in path and (row + 1, col) not in visited:
                    list3 = path.copy()
                    list3.append(game_map[row + 1][col])
                    visited.append((row + 1, col))
            if col < (len(game_map[0]) - 1):
                if game_map[row][col + 1] not in path and (row, col+1) not in visited:
                    list4 = path.copy()
                    list4.append(game_map[row][col + 1])
                    visited.append((row, col+1))

            for pom in range(4):
                k = self.redosled(list1, list2, list3, list4)

                if k == 0:
                    break

                if k == 1:
                    if len(list1) > 0:
                        l1 = list1.copy()
                        queue.append(l1)
                        self.sortQueue(queue, goal[0], goal[1])
                        list1.clear()

                if k == 2:
                    if len(list2) > 0:
                        l2 = list2.copy()
                        queue.append(l2)
                        self.sortQueue(queue, goal[0], goal[1])
                        list2.clear()

                if k == 3:
                    if len(list3) > 0:
                        l3 = list3.copy()
                        queue.append(l3)
                        self.sortQueue(queue, goal[0], goal[1])
                        list3.clear()

                if k == 4:
                    if len(list4) > 0:
                        l4 = list4.copy()
                        queue.append(l4)
                        self.sortQueue(queue, goal[0], goal[1])
                        list4.clear()


class Draza(Agent):

    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def sortQueue(self, queue):
        queue.sort(key=lambda lista: (sum(map(lambda element: element.cost(), lista)), len(lista), random.random()))

    def redosled(self, list1,list2,list3,list4):

        len1 = len(list1)
        len2 = len(list2)
        len3 = len(list3)
        len4 = len(list4)
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        minlen = 1000
        minsum = 1000000
        if len1 > 0:
            sum1 = 0
            for pom in list1:
                sum1 += pom.cost()
            if sum1 < minsum: minsum = sum1
            if sum1 == minsum:
                if len1 < minlen: minlen = len1
        if len2 > 0:
            sum2 = 0
            for pom in list2:
                sum2 += pom.cost()
            if sum2 < minsum: minsum = sum2
            if sum2 == minsum:
                if len2 < minlen: minlen = len2
        if len3 > 0:
            sum3 = 0
            for pom in list3:
                sum3 += pom.cost()
            if sum3 < minsum: minsum = sum3
            if sum3 == minsum:
                if len3 < minlen: minlen = len3
        if len4 > 0:
            sum4 = 0
            for pom in list4:
                sum4 += pom.cost()
            if sum4 < minsum: minsum = sum4
            if sum4 == minsum:
                if len4 < minlen: minlen = len4

        if minsum == sum1 and minlen == len1:
            return 1
        if minsum == sum2 and minlen == len2:
            return 2
        if minsum == sum3 and minlen == len3:
            return 3
        if minsum == sum4 and minlen == len4:
            return 4
        return 0

    def get_agent_path(self, game_map, goal):

        list1 = []
        list2 = []
        list3 = []
        list4 = []
        visited = [(self.row, self.col)]
        path = [game_map[self.row][self.col]]
        queue = [path]

        while len(queue) > 0:

            list = queue.pop(0)
            elem = list[-1]
            (row, col) = elem.position()

            if (row, col) == (goal[0], goal[1]):
                return list

            if row > 0:
                if game_map[row-1][col] not in list and (row-1,col) not in visited:
                    list1 = list.copy()
                    list1.append(game_map[row - 1][col])
                    visited.append((row-1, col))
            if col > 0:
                if game_map[row][col - 1] not in list and (row, col-1) not in visited :
                    list2 = list.copy()
                    list2.append(game_map[row][col - 1])
                    visited.append((row, col-1))
            if row < (len(game_map) - 1):
                if game_map[row + 1][col] not in list and (row + 1, col) not in visited:
                    list3 = list.copy()
                    list3.append(game_map[row + 1][col])
                    visited.append((row + 1, col))
            if col < (len(game_map[0]) - 1):
                if game_map[row][col + 1] not in list and (row, col+1) not in visited:
                    list4 = list.copy()
                    list4.append(game_map[row][col + 1])
                    visited.append((row, col+1))

            for pom in range(4):
                k = self.redosled(list1, list2, list3, list4)
                if k == 0:
                    break
                if k == 1 and len(list1) > 0:
                    l1 = list1.copy()
                    queue.append(l1)
                    self.sortQueue(queue)
                    list1.clear()

                if k == 2 and len(list2) > 0:
                    l2 = list2.copy()
                    queue.append(l2)
                    self.sortQueue(queue)
                    list2.clear()

                if k == 3 and len(list3) > 0:
                    l3 = list3.copy()
                    queue.append(l3)
                    self.sortQueue(queue)
                    list3.clear()

                if k == 4 and len(list4) > 0:
                    l4 = list4.copy()
                    queue.append(l4)
                    self.sortQueue(queue)
                    list4.clear()


class Jocke(Agent):

    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def reversePath(self, pomPath):
        pom = pomPath[-1::-1]
        return pom

    def getFinalPath (self, allPaths, row2, col2, path):
        pomPath = []

        for singlePath in allPaths:
            for singleTile in singlePath[1]:
                isGoal = singleTile
                if isGoal.position() == (row2, col2):
                    row2, col2 = singlePath[0]
                    pomPath.append(singleTile)

        pomPath.extend(path)
        pomPath = self.reversePath(pomPath)
        return pomPath

    def sortMaybeBaby2 (self, neighbors_sum, maybeBaby, row, col):

        maybeBaby.sort(
            key=lambda element: (
                neighbors_sum[element.position()],
                0 if element.row < row else 1 if element.col > col else 2 if element.row > row else 3))
    def sortMaybeBaby (self, neighbors_sum, maybeBaby, row, col):

        maybeBaby.sort(
            key=lambda element: (
                neighbors_sum[element.position()],
                0 if element.row < row else 1 if element.col > col else 2 if element.row > row else 3))

    def countSum (self, game_map, neighbors_sum, maybeBaby, row, col):

        for i in maybeBaby:
            sum = 0
            cnt = 0
            if i.col < (len(game_map[0]) - 1) and (row, col) is not (i.row, i.col + 1):
                sum = sum + game_map[i.row][i.col + 1].cost()
                cnt = cnt + 1
            if i.col > 0 and (row, col) is not (i.row, i.col - 1):
                sum = sum + game_map[i.row][i.col - 1].cost()
                cnt = cnt + 1
            if i.row > 0 and (row, col) is not (i.row - 1, i.col):
                sum = sum + game_map[i.row - 1][i.col].cost()
                cnt = cnt + 1
            if i.row < (len(game_map) - 1) and (row, col) is not (i.row + 1, i.col):
                sum = sum + game_map[i.row + 1][i.col].cost()
                cnt = cnt + 1

            if sum != 0:
                sum /= cnt

            neighbors_sum[i.position()] = sum

    def countWater (self, game_map, neighbors_sum, maybeBaby, row, col):

        for i in maybeBaby:
            cnt = 0
            if i.col < (len(game_map[0]) - 1) and (row, col) is not (i.row, i.col + 1):
                if game_map[i.row][i.col+1].kind() == 'w':
                    cnt = cnt + 1
            if i.col > 0 and (row, col) is not (i.row, i.col - 1):
                if game_map[i.row][i.col - 1].kind() == 'w':
                    cnt = cnt + 1
            if i.row > 0 and (row, col) is not (i.row - 1, i.col):
                if game_map[i.row-1][i.col].kind() == 'w':
                    cnt = cnt + 1
            if i.row < (len(game_map) - 1) and (row, col) is not (i.row + 1, i.col):
                if game_map[i.row+1][i.col].kind() == 'w':
                    cnt = cnt + 1
            if i.col < (len(game_map[0]) - 1) and i.row < (len(game_map) - 1) and (row, col) is not (i.row+1, i.col + 1):
                if game_map[i.row+1][i.col + 1].kind() == 'w':
                    cnt = cnt + 1
            if i.col > 0 and i.row > 0 and (row, col) is not (i.row - 1, i.col - 1):
                if game_map[i.row-1][i.col-1].kind() == 'w':
                    cnt = cnt + 1
            if i.row > 0 and i.col < (len(game_map[0]) - 1) and (row, col) is not (i.row - 1, i.col+1):
                if game_map[i.row-1][i.col + 1].kind() == 'w':
                    cnt = cnt + 1
            if i.col > 0 and i.row < (len(game_map) - 1) and (row, col) is not (i.row + 1, i.col - 1):
                if game_map[i.row+1][i.col - 1].kind() == 'w':
                    cnt = cnt + 1

            neighbors_sum[i.position()] = cnt

    def get_agent_path(self, game_map, goal):

        row = self.row
        col = self.col
        visited = []
        queue = [game_map[self.row][self.col]]
        path = queue.copy()
        visited.append((row, col))
        maybeBaby = []
        allPaths = []

        while len(queue) > 0:
            if len(queue) == 1 and queue[0].position() == (self.row, self.col):
                queue.pop()

            if (row, col) == (goal[0], goal[1]):
                break
            if row > 0:
                if (row - 1, col) not in visited:
                    maybeBaby.append(game_map[row - 1][col])
            if col > 0:
                if (row, col - 1) not in visited:
                    maybeBaby.append(game_map[row][col - 1])
            if row < (len(game_map) - 1):
                if (row + 1, col) not in visited:
                    maybeBaby.append(game_map[row + 1][col])
            if col < (len(game_map[0]) - 1):
                if (row, col + 1) not in visited:
                    maybeBaby.append(game_map[row][col + 1])

            if len(maybeBaby) < 1:
                allPaths.append(((row, col), []))
                (row, col) = queue.pop(0).position()
                visited.append((row, col))

            else:

                neighbors_sum = {}
                self.countSum(game_map, neighbors_sum, maybeBaby, row, col)

                # self.countWater(game_map, neighbors_sum, maybeBaby, row, col)
                self.sortMaybeBaby(neighbors_sum, maybeBaby, row, col)

                allPaths.append(((row, col), maybeBaby))
                print(allPaths)
                for i in maybeBaby:
                    visited.append(i.position())
                queue.extend(maybeBaby)
                (row,col) = queue.pop(0).position()
                maybeBaby = []

        allPaths = allPaths[-1::-1]
        row2 = goal[0]
        col2 = goal[1]

        return self.getFinalPath(allPaths, row2, col2, path)


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path


class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)



