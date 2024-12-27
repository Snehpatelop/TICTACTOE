import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700  # Increased height for score display
LINE_WIDTH = 14
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = BLACK
LINE_COLOR = (200, 200, 200)
FONT = pygame.font.SysFont('Arial', 30)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Scorecard
scorecard = {'X': 0, 'O': 0}

# Player names
player_names = {'X': 'Player 1', 'O': 'Player 2'}

# Draw lines
def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)

# Draw figures
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, RED, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Check win
def check_win(player):
    # Vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    # Horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    # Ascending diagonal win check
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    # Descending diagonal win check
    if board[2][0] == board[1][1] == board[0][2] == player:
        return True
    return False

# Restart game
def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

# Display scorecard
def display_scorecard():
    score_text = f"Score - {player_names['X']}: {scorecard['X']}  {player_names['O']}: {scorecard['O']}"
    score_surface = FONT.render(score_text, True, LINE_COLOR)
    screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, HEIGHT - 60))

# Display current turn
def display_turn(player):
    turn_text = f"{player_names[player]}'s Turn ({player})"
    turn_surface = FONT.render(turn_text, True, LINE_COLOR)
    screen.blit(turn_surface, (WIDTH // 2 - turn_surface.get_width() // 2, HEIGHT - 100))

# Display winner or tie
def display_winner(winner):
    screen.fill(BLACK)
    if winner:
        win_text = f"{player_names[winner]} ({winner}) Wins!"
    else:
        win_text = "It's a Tie!"
    win_surface = FONT.render(win_text, True, LINE_COLOR)
    screen.blit(win_surface, (WIDTH // 2 - win_surface.get_width() // 2, HEIGHT // 2 - win_surface.get_height() // 2))
    reset_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
    pygame.draw.rect(screen, LINE_COLOR, reset_button)
    reset_text = FONT.render("Reset", True, BLACK)
    screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 10))
    pygame.display.update()
    return reset_button

# Main loop
def main():
    global player_names
    player = 'X'
    game_over = False
    draw_lines()

    # Menu for entering player names
    input_active = True
    input_boxes = [pygame.Rect(200, 200, 200, 32), pygame.Rect(200, 300, 200, 32)]
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = [color_inactive, color_inactive]
    text = ['', '']
    active = [False, False]

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(2):
                    if input_boxes[i].collidepoint(event.pos):
                        active[i] = not active[i]
                    else:
                        active[i] = False
                    color[i] = color_active if active[i] else color_inactive
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if active[i]:
                        if event.key == pygame.K_RETURN:
                            player_names['X' if i == 0 else 'O'] = text[i]
                            text[i] = ''
                            if i == 1:
                                input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            text[i] = text[i][:-1]
                        else:
                            text[i] += event.unicode

        screen.fill(BG_COLOR)
        for i in range(2):
            txt_surface = FONT.render(text[i], True, color[i])
            width = max(200, txt_surface.get_width() + 10)
            input_boxes[i].w = width
            screen.blit(txt_surface, (input_boxes[i].x + 5, input_boxes[i].y + 5))
            pygame.draw.rect(screen, color[i], input_boxes[i], 2)

        prompt_surface1 = FONT.render("Enter Player 1 Name:", True, LINE_COLOR)
        prompt_surface2 = FONT.render("Enter Player 2 Name:", True, LINE_COLOR)
        screen.blit(prompt_surface1, (input_boxes[0].x, input_boxes[0].y - 40))
        screen.blit(prompt_surface2, (input_boxes[1].x, input_boxes[1].y - 40))

        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]  # x
                mouseY = event.pos[1]  # y

                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player
                    if check_win(player):
                        game_over = True
                        scorecard[player] += 1
                        reset_button = display_winner(player)
                    elif all(all(row) for row in board):
                        game_over = True
                        reset_button = display_winner(None)
                    player = 'O' if player == 'X' else 'X'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    game_over = False

            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    restart()
                    game_over = False

        if not game_over:
            screen.fill(BG_COLOR)
            draw_lines()
            draw_figures()
            display_scorecard()
            display_turn(player)
            pygame.display.update()

if __name__ == "__main__":
    main()

