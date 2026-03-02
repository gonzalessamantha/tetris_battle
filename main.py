import pygame, sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)  # defining a font for the game title
score_surface = title_font.render("Score", True, Colors.white)  # rendering the score text surface with color
next_surface = title_font.render("Next", True, Colors.white)  # rendering the next block text surface with color
game_over_surface = title_font.render("GAME OVER", True, Colors.red)  # rendering the game over text surface with color

score_rect = pygame.Rect(320, 55, 170, 60)  # defining a rectangle for the score surface to position it on the screen
next_rect = pygame.Rect(320, 215, 170,
                        180)  # defining a rectangle for the next block surface to position it on the screen

screen = pygame.display.set_mode((500, 620))  # game window using Cordinate Systems
pygame.display.set_caption("Tetris Battle")  # game title

clock = pygame.time.Clock()  # controlling frame rate

game = Game()

GAME_UPDDATE = pygame.USEREVENT + 1  # creating a custom event for updating the game state
pygame.time.set_timer(GAME_UPDDATE, 200)  # setting a timer to trigger the custom event every 200 milliseconds

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # breaking the loop when the user clicks the close button
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # checking for key press events
            if game.game_over == True:  # resetting the game if it is over and any key is pressed
                game.game_over = False
                game.reset()  # calling the reset method of the game object to restart the game
            if event.key == pygame.K_LEFT and game.game_over == False:  # move left
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:  # move right
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:  # move down faster
                game.move_down()
                game.update_score(0, 1)  # updating the score with move down points when the down key is pressed
            if event.key == pygame.K_UP and game.game_over == False:  # rotate the block
                game.rotate()
        if event.type == GAME_UPDDATE and game.game_over == False:  # checking for the custom game update event
            game.move_down()  # moving the current block down by one row after each update event

    # drawing
    score_value_surface = title_font.render(str(game.score), True,
                                            Colors.white)  # rendering the score value surface with the current score

    screen.fill(Colors.dark_blue)  # fill the screen with the defined dark blue color
    screen.blit(score_surface, (365, 20, 50, 50))  # blit the score surface onto the screen at position (365, 20)
    screen.blit(next_surface, (375, 180, 50, 50))  # blit the next block surface onto the screen at position (375, 180)

    if game.game_over == True:  # checking if the game is over to display the game over message
        screen.blit(game_over_surface,
                    (320, 450, 50, 50))  # blit the game over surface onto the screen at position (320, 450)

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0,
                     20)  # drawing a rectangle for the score background using the defined light blue color
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                  centery=score_rect.centery))  # blit the score value surface onto the screen at position (360, 80)
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0,
                     10)  # drawing a rectangle for the next block background using the defined light blue color
    game.draw(screen)  # calling the draw method of the game object to render the game elements on the screen

    pygame.display.update()
    clock.tick(60)  # tick the clock to maintain 60 frames per second
