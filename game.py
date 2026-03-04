from grid import Grid
from blocks import *
import random
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

        pygame.mixer.music.load("sounds/music.ogg.ogg")
        pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:  # checking if there are no more blocks left in the list
            self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)  # removing the block from the list to avoid duplicates
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)  # moving back to the original position if the block is outside the grid

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)  # moving back to the original position if the block is outside the grid

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()  # locking the block in place if it cannot move down further

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][
                position.column] = self.current_block.id  # updating the grid with the id of the current block to indicate that the cell is occupied
        self.current_block = self.next_block  # setting the next block as the current block
        self.next_block = self.get_random_block()  # getting a new random block for the next block
        rows_cleared = self.grid.clear_full_rows()  # clearing any full rows after locking the block in place
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared,0)  # updating the score based on the number of rows cleared and move down points
        if self.block_fits() == False:  # checking if the new current block can fit in the grid after locking the previous block
            self.game_over = True  # setting the game over flag to true if the new block cannot fit, indicating that the game has ended

    def reset(self):
        self.grid.reset()  # resetting the grid to its initial state
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()  # getting a new random block for the current block
        self.next_block = self.get_random_block()  # getting a new random block for the next
        self.score = 0  # resetting the score to zero

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row,
                                  tile.column) == False:  # checking if any of the tiles of the current block are in occupied cells in the grid
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()  # rotating back to the original position if the block is outside the grid
        else:
            self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row,
                                   tile.column) == False:  # checking if any of the tiles of the current block are outside the grid
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11,
                                11)  # drawing the current block on the screen with an offset to position it correctly within the grid

        if self.next_block.id == 3:  # checking if the next block is an IBlock to adjust the offset for drawing it in the next block area
            self.next_block.draw(screen, 255,
                                 290)  # drawing the next block on the screen with an offset to position it in the next block area
        elif self.next_block.id == 4:  # checking if the next block is an OBlock to adjust the offset for drawing it in the next block area
            self.next_block.draw(screen, 255,
                                 280)  # drawing the next block on the screen with an offset to position it in the next block area
        else:
            self.next_block.draw(screen, 270,
                                 270)  # drawing the next block on the screen with an offset to position it in the next block area
