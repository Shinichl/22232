import pygame
import os
import importlib.util
import sys
import cv2
from button import Button  

# Center the Pygame window
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Paths
simulation_file = "Menu/sims.py"
video_path = "INTERSECTION_bg.mp4"

# Use importlib to dynamically import the module
spec = importlib.util.spec_from_file_location("sims", simulation_file)
simulation_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(simulation_module)
Main = simulation_module.Main  # Access the Main class from the dynamically imported module

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# Initialize the video capture
cap = cv2.VideoCapture(video_path)

def get_font(size):
    return pygame.font.Font("Menu/assets/font.ttf", size)

def fade_fadein(image_path, fade_duration=3000):
    fadein_image = pygame.image.load(image_path).convert()
    fadein_image.set_alpha(0)  # Start with transparency

    fade_in_steps = 255  # Number of steps for fade-in effect
    fade_step = 255 / fade_duration  # Step size for each frame

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < fade_duration:
        alpha_value = int((pygame.time.get_ticks() - start_time) * fade_step)
        fadein_image.set_alpha(alpha_value)

        SCREEN.fill((0, 0, 0))  # Fill screen with black
        SCREEN.blit(fadein_image, (0, 0))  # Blit faded image onto screen
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Ensure image is fully visible at the end
    fadein_image.set_alpha(255)
    SCREEN.fill((0, 0, 0))  # Fill screen with black
    SCREEN.blit(fadein_image, (0, 0))  # Blit final image onto screen
    pygame.display.update()

def fade_out(image_path, fade_duration=3000):
    fadeout_image = pygame.image.load(image_path).convert()
    fadeout_image.set_alpha(255)  # Start with full opacity

    fade_out_steps = 255  # Number of steps for fade-out effect
    fade_step = 255 / fade_duration  # Step size for each frame

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < fade_duration:
        alpha_value = 255 - int((pygame.time.get_ticks() - start_time) * fade_step)
        fadeout_image.set_alpha(alpha_value)

        SCREEN.fill((0, 0, 0))  # Fill screen with black
        SCREEN.blit(fadeout_image, (0, 0))  # Blit faded image onto screen
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Ensure image is fully invisible at the end
    fadeout_image.set_alpha(0)
    SCREEN.fill((0, 0, 0))  # Fill screen with black
    SCREEN.blit(fadeout_image, (0, 0))  # Blit final image onto screen
    pygame.display.update()

def play():
    # Show fade fadein
    fade_fadein("images/fadein_image.png")

    main_simulation = Main()

    while True:
        main_simulation.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_simulation.quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        SCREEN.fill((0, 0, 0))  # Fill screen with black
        main_simulation.draw(SCREEN)

        pygame.display.update()

def credits():
    names = [
        "Lopez, John Red",
        "Adlao, Mark Clarence",
        "Paulite, James Mathieu",
        "Francisco, Alvinne",
        "De-Una, Andrie",
        "Ciriaco, Gian",
        "De Vera, Chrislyn",
        "Tabasa, Margarette",
        "Gaso, Jelly",
        "Sanchez, Jenica",
        "Ogabang, JB Rachine",
        "Sa"
    ]

    while True:
        credits_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill((255, 255, 255))  # Fill screen with white

        # Render video frame
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
            SCREEN.blit(frame, (0, 0))

        # Render names
        y_position = 200
        for name in names:
            name_text = get_font(40).render(name, True, (255, 255, 255))  # White color
            name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            SCREEN.blit(name_text, name_rect)
            y_position += 50   # Adjust spacing between names

        # Render "BACK" button
        credits_button = Button(image=pygame.image.load("Menu/assets/Back Rect.png"), pos=(800, 800), 
                                text_input="BACK", font=get_font(35), base_color="GREEN", hovering_color="BLACK")
        credits_button.changeColor(credits_mouse_pos)
        credits_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if credits_button.checkForInput(credits_mouse_pos):
                    main_Menu()

        pygame.display.update()

def main_Menu():
    while True:
        # Read the video frame
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
            SCREEN.blit(frame, (0, 0))

        Menu_mouse_pos = pygame.mouse.get_pos()

        # Render "TRAFFIC SIM" text
        Menu_text_shadow = get_font(70).render("TRAFFIC SIM", True, (0, 0, 0))
        Menu_text = get_font(70).render("TRAFFIC SIM", True, (255, 170, 0))
        Menu_shadow_rect = Menu_text_shadow.get_rect(center=(530 + 3, 100 + 3))
        Menu_rect = Menu_text.get_rect(center=(530, 100))
        SCREEN.blit(Menu_text_shadow, Menu_shadow_rect)
        SCREEN.blit(Menu_text, Menu_rect)

        # Render "START SIM" button
        play_button = Button(image=pygame.image.load("Menu/assets/Play Rect.png"), pos=(530, 350), 
                             text_input="START SIM", font=get_font(40), base_color="Green", hovering_color="White")
        play_button_shadow = get_font(40).render("START SIM", True, (0, 0, 0))
        play_button_rect = play_button_shadow.get_rect(center=(530 + 3, 350 + 3))
        SCREEN.blit(play_button_shadow, play_button_rect)

        # Render "CREDITS" button
        credits_button = Button(image=None, pos=(800, 800), 
                                text_input="CREDITS", font=get_font(40), base_color="Blue", hovering_color="White")
        credits_button_shadow = get_font(40).render("CREDITS", True, (0, 0, 0))
        credits_button_rect = credits_button_shadow.get_rect(center=(800 + 3, 800 + 3))
        SCREEN.blit(credits_button_shadow, credits_button_rect)

        # Render "QUIT" button
        quit_button = Button(image=pygame.image.load("Menu/assets/Quit Rect.png"), pos=(530, 470), 
                             text_input="QUIT", font=get_font(35), base_color="Red", hovering_color="White")

        for button in [play_button, credits_button, quit_button]:
            button.changeColor(Menu_mouse_pos)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(Menu_mouse_pos):
                    play()
                if credits_button.checkForInput(Menu_mouse_pos):
                    credits()
                if quit_button.checkForInput(Menu_mouse_pos):
                    fade_out("images/fadeout_image.png")
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Start the main Menu
main_Menu()
