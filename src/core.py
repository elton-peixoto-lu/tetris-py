import pygame
import random
import copy

# Inicialização do Pygame
pygame.init()

# Definição de cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Configurações do jogo
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
FPS = 30

# Define as peças do Tetris
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [1]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]]
]

SHAPES_COLORS = [CYAN, RED, MAGENTA, YELLOW, GREEN, BLUE, ORANGE]

# Adiciona a definição da cor branca (para a pontuação)
WHITE = (255, 255, 255)

# Adiciona a definição da fonte para a pontuação
SCORE_FONT = pygame.font.Font(None, 36)

# Variável global para a pontuação
score = 0

# Função para criar uma grade vazia
def create_grid():
    return [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]

# Função para desenhar a grade
def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value:
                pygame.draw.rect(screen, SHAPES_COLORS[value - 1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

# Função principal do jogo
def main():
    global score

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    grid = create_grid()
    current_piece, current_piece_color = get_random_piece()
    fall_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if is_valid_move(current_piece, grid, offset=(-1, 0)):
                        current_piece[1] -= 1
                elif event.key == pygame.K_RIGHT:
                    if is_valid_move(current_piece, grid, offset=(1, 0)):
                        current_piece[1] += 1
                elif event.key == pygame.K_DOWN:
                    if is_valid_move(current_piece, grid, offset=(0, 1)):
                        current_piece[2] += 1
                elif event.key == pygame.K_UP:  # Rotação no sentido horário
                    rotate_piece(current_piece, grid, clockwise=True)
                elif event.key == pygame.K_SPACE:  # Rotação no sentido anti-horário
                    rotate_piece(current_piece, grid, clockwise=False)

        screen.fill(BLACK)

        # Lógica de movimento da peça
        current_time = pygame.time.get_ticks()
        if current_time - fall_time > 1000:
            if is_valid_move(current_piece, grid, offset=(0, 1)):
                current_piece[2] += 1
            else:
                merge_piece(current_piece, grid, current_piece_color)
                clear_lines(grid)  # Verifica e remove linhas completas
                current_piece, current_piece_color = get_random_piece()
                if not is_valid_move(current_piece, grid):
                    # Se não for possível gerar uma nova peça, o jogo termina
                    pygame.quit()
                    quit()
            fall_time = current_time

        # Desenha a grade, a peça atual e a pontuação
        draw_grid(screen, grid)
        draw_piece(screen, current_piece, current_piece_color)
        draw_score(screen)

        pygame.display.flip()
        clock.tick(FPS)

# Função para verificar se um movimento é válido
def is_valid_move(piece, grid, offset=(0, 0)):
    for y, row in enumerate(piece[0]):
        for x, value in enumerate(row):
            if value:
                new_x = piece[1] + x + offset[0]
                new_y = piece[2] + y + offset[1]
                if (
                        new_x < 0
                        or new_x >= len(grid[0])
                        or new_y >= len(grid)
                        or (new_y >= 0 and grid[new_y][new_x])
                ):
                    return False
    return True

# Função para rotacionar a peça
def rotate_piece(piece, grid, clockwise=True):
    rotated_piece = copy.deepcopy(piece[0])

    if clockwise:
        rotated_piece.reverse()
        rotated_piece = [list(row) for row in zip(*rotated_piece)]
    else:
        rotated_piece = [list(row) for row in zip(*rotated_piece[::-1])]

    if is_valid_move([rotated_piece, piece[1], piece[2]], grid):
        piece[0] = rotated_piece

# Função para mesclar uma peça no tabuleiro
def merge_piece(piece, grid, color):
    for y, row in enumerate(piece[0]):
        for x, value in enumerate(row):
            if value:
                grid[piece[2] + y][piece[1] + x] = SHAPES_COLORS.index(color) + 1

# Função para obter uma peça aleatória
def get_random_piece():
    shape = random.choice(SHAPES)
    color = random.choice(SHAPES_COLORS)
    return [shape, 0, 0], color

# Função para verificar e remover linhas completas
def clear_lines(grid):
    global score
    lines_to_clear = [index for index, row in enumerate(grid) if all(row)]

    for line in lines_to_clear:
        del grid[line]
        grid.insert(0, [0] * (WIDTH // BLOCK_SIZE))
        score += 10  # Incrementa a pontuação por linha completa

# Função para desenhar a peça atual
def draw_piece(screen, piece, color):
    for y, row in enumerate(piece[0]):
        for x, value in enumerate(row):
            if value:
                pygame.draw.rect(
                    screen,
                    color,
                    (
                        (piece[1] + x) * BLOCK_SIZE,
                        (piece[2] + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    ),
                    0,
                )

# Função para desenhar a pontuação
def draw_score(screen):
    score_text = SCORE_FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

if __name__ == "__main__":
    main()