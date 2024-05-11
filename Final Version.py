from flask import Flask, render_template
import multiprocessing as mp
import os
import pygame
import random

app = Flask(__name__)

# Function to run the Pygame code
def run_pygame():
    # Constants
    WINDOW_WIDTH = 450
    WINDOW_HEIGHT = 450
    TILE_SIZE = 150
    ROWS = 3
    COLS = 3
    WHITE = (255, 255, 255)
    IMAGE_PATHS_FILE = 'last_image.txt'
    
    # Initialize pygame
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Image Puzzle")

    # Function to split image into tiles
    def split_image(image):
        tiles = []
        for y in range(0, ROWS):
            for x in range(0, COLS):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                tile = image.subsurface(rect)
                tiles.append(tile)
        return tiles

    # Function to shuffle tiles
    def shuffle_tiles(tiles):
        random.shuffle(tiles)

    # Function to draw tiles
    def draw_tiles(tiles):
        for i, tile in enumerate(tiles):
            row = i // COLS
            col = i % COLS
            window.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))

    # Function to get tile index
    def get_tile_index(pos):
        x, y = pos
        col = x // TILE_SIZE
        row = y // TILE_SIZE
        return row * COLS + col

    # Function to check if two tiles are adjacent
    def is_adjacent(tile1, tile2):
        return abs(tile1 - tile2) == 1 or abs(tile1 - tile2) == COLS

    # Function to swap tiles
    def swap_tiles(tiles, index1, index2):
        tiles[index1], tiles[index2] = tiles[index2], tiles[index1]

    # Function to select a random image path
    def select_random_image(image_paths):
        last_selected_image = None
        if os.path.exists(IMAGE_PATHS_FILE):
            with open(IMAGE_PATHS_FILE, 'r') as file:
                last_selected_image = file.read().strip()

        available_images = [image for image in image_paths if image != last_selected_image]
        selected_image_path = random.choice(available_images)

        with open(IMAGE_PATHS_FILE, 'w') as file:
            file.write(selected_image_path)

        return selected_image_path

    # Function to check if the current arrangement of tiles matches the original picture
    def check_solution(tiles, original_image):
        # Reconstruct the original image using the current arrangement of tiles
        reconstructed_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        for i, tile in enumerate(tiles):
            row = i // COLS
            col = i % COLS
            reconstructed_image.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))

        # Compare the reconstructed image with the original image
        original_image_str = pygame.image.tostring(original_image, 'RGB')
        reconstructed_image_str = pygame.image.tostring(reconstructed_image, 'RGB')
        difference = original_image_str != reconstructed_image_str
        return not difference

    # List of image paths
    image_paths = [
        r'C:\Users\user\Documents\Project\image1.jpg',
        r'C:\Users\user\Documents\Project\image2.jpg',
        r'C:\Users\user\Documents\Project\image3.jpg',
        r'C:\Users\user\Documents\Project\image4.jpg',
        r'C:\Users\user\Documents\Project\image5.jpg',
        r'C:\Users\user\Documents\Project\image6.webp'   
    ]

    # Select a random image path
    selected_image_path = select_random_image(image_paths)

    # Load selected image
    original_image = pygame.image.load(selected_image_path)
    original_image = pygame.transform.scale(original_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Split image into tiles
    tiles = split_image(original_image)
    shuffle_tiles(tiles)
    empty_tile_index = ROWS * COLS - 1  # Index of the empty tile
    dragging = False
    dragged_tile_index = -1

    # Event loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_tile_index = get_tile_index(mouse_pos)
                if clicked_tile_index != empty_tile_index:
                    dragging = True
                    dragged_tile_index = clicked_tile_index
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    target_tile_index = get_tile_index(mouse_pos)
                    if is_adjacent(dragged_tile_index, target_tile_index):
                        swap_tiles(tiles, dragged_tile_index, target_tile_index)
                        empty_tile_index = dragged_tile_index
                    dragging = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    # If the user presses "v", validate the solution
                    solution_correct = check_solution(tiles, original_image)
                    if solution_correct:
                        print("Access granted")
                    else:
                        print("Access denied")

        window.fill(WHITE)
        draw_tiles(tiles)
        pygame.display.update()

# Define Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_python_code', methods=['POST'])
def execute_python_code():
    # Create a process to run the Pygame code
    pygame_process = mp.Process(target=run_pygame)
    pygame_process.start()
    return "Game started!"

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True)
