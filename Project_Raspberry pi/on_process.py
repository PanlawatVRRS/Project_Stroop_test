import pygame
import sys
from pygame.locals import *
import random
import time
import os
import bluetooth

# Initialize Pygame
pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BORDER_MARGIN = 20\

# Get screen dimensions
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

word_list = ["ม่วง", "ขาว", "แดง", "น้ำเงิน","เขียว"]
color_list = [(153,0,153),(255,255,255),(255,0,0),(0,0,255),(0, 255, 0)]

def initialize_data():
    global word_display, color_display, word_code, color_code, combined_data
    word_display = []
    color_display = []
    word_code = []
    color_code = []
    combined_data = []

    for i in range(15):
        word_display.append(random.choice(word_list))
        while True:
            color = random.randint(0, len(word_list) - 1)
            if word_list[color] != word_display[i]:
                color_display.append(color_list[color])
                break

    for word in word_display:
        word_code.append(word_list.index(word))

    for color in color_display:
        color_code.append(color_list.index(color))

    combined_data = [(word_code[x], color_code[x]) for x in range(len(word_code))]

# Initialize data for the first time
initialize_data()

# Constants
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
WHITE = (255, 255, 255)
BLACK = (0,0,0)
ARCADE_RED = (200, 0, 0)
FONT_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 10
FONT_SIZE_2 = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 20
FONT_SIZE_3 = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 12

font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", FONT_SIZE)

# Placeholder functions for each option
def draw_menu(screen, title_text, title_rect, option_texts, option_rects, choice, device_connection_text,device_connection_rect,info_text_combined, info_rect):
    # Function to draw the menu on the screen
    screen.fill((0, 0, 0))
    screen.blit(info_text_combined, info_rect)
    screen.blit(title_text, title_rect)

    for i, (text, rect) in enumerate(zip(option_texts, option_rects)):
        if choice == i:  # Check if this option matches the current choice
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)  # Draw green rectangle for the current choice
        else:
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # Draw white rectangle for other options
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # Draw the red rectangle for device connection text
    pygame.draw.rect(screen, (255, 0, 0), device_connection_rect)  # Red rectangle
    screen.blit(device_connection_text, device_connection_text_rect)  # Text

    pygame.display.flip()

def play_game():
    print("Executing play_game function")
    font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", FONT_SIZE_2)
    large_font_size = FONT_SIZE_2 * 2  # Adjust this multiplier as needed for the desired text size
    large_font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", large_font_size)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    back_text = font.render("กลับ", True, (255, 255, 255))
    submit_text = font.render("ต่อไป", True, (255, 255, 255))
    center_text = large_font.render("กดต่อไปเพื่อเริ่มต้นทำแบบทดสอบ", True, (255, 255, 255))

    button_width = max(back_text.get_width(), submit_text.get_width()) + 40
    button_height = int(SCREEN_HEIGHT * 0.1)
    button_spacing = int(SCREEN_WIDTH * 0.05)

    back_rect = pygame.Rect(button_spacing, SCREEN_HEIGHT - button_height - button_spacing, button_width, button_height)
    submit_rect = pygame.Rect(SCREEN_WIDTH - button_spacing - button_width, SCREEN_HEIGHT - button_height - button_spacing, button_width, button_height)

    play_running = True
    while play_running:
        screen.fill(BLACK)
        
        # Draw "back" button
        pygame.draw.rect(screen, (255, 0, 0), back_rect)  # Red rectangle for "back" button
        screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))  # Center the text

        # Draw "submit" button
        pygame.draw.rect(screen, (0, 255, 0), submit_rect)  # Green rectangle for "next" button
        screen.blit(submit_text, (submit_rect.centerx - submit_text.get_width() // 2, submit_rect.centery - submit_text.get_height() // 2))  # Center the text

        # Draw the center text
        center_text_rect = center_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(center_text, center_text_rect.topleft)

        pygame.display.flip()

        print("wait for command")
        command = arduino_sock.recv(1024).decode("utf-8")
        command = command.strip()  # Remove leading/trailing whitespace
        if command == '0':
            # Go to the next page
            play_running = False
            break
        elif command == '1':
            # Move to the next image
            print("pass")
            game_start()
            play_running = False  # Exit the inner loop to update the tutorial page

def game_start():
    start_time = time.time()
    print("Game_start")
    score = 0
    current_index_to_change = 0
    word_color_flags = [False] * 15
    font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", FONT_SIZE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    pygame.display.flip()


    run = True
    while run:
        # วาด word list และกำหนดขนาดกรอบ
        for i in range(15):
            word = word_display[i]
            row = i // 5
            col = i % 5
            text_color = BLACK if word_color_flags[i] else color_display[i]
            text_surface = font.render(word, True, text_color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 5 * col + SCREEN_WIDTH // 10, SCREEN_HEIGHT // 3 * row + SCREEN_HEIGHT // 6))
            screen.blit(text_surface, text_rect)

            # สร้างกรอบสีดำสำหรับ word list ที่ถูกส่งแล้ว
            if word_color_flags[i]:
                pygame.draw.rect(screen, BLACK, text_rect.inflate(BORDER_MARGIN, BORDER_MARGIN), 0)

            border_color = WHITE if current_index_to_change == i else BLACK  # เลือกสีของกรอบตามเงื่อนไข
            pygame.draw.rect(screen, border_color, text_rect.inflate(BORDER_MARGIN, BORDER_MARGIN), 2)

        pygame.display.flip()

        if current_index_to_change == 15:
            run = False
            break

        shuffled_data = list(combined_data[current_index_to_change])
        random.shuffle(shuffled_data)
            
        # Convert the shuffled tuple to a string representation
        data_str = str(shuffled_data)
        arduino_sock.send(data_str)  # Send the string
        print("Send choice")
        # Wait for the Arduino's acknowledgment
        Answer = arduino_sock.recv(1024).decode("utf-8")

        Answer = int(Answer)
        if Answer == combined_data[current_index_to_change][1]:
            score += 1
            word_color_flags[current_index_to_change] = True
        else:
            screen.fill(BLACK)
            word_color_flags[current_index_to_change] = True
            for i in range(15):
                word = word_display[i]
                row = i // 5
                col = i % 5
                text_color = BLACK if word_color_flags[i] else color_display[i]
                text_surface = font.render(word, True, text_color)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 5 * col + SCREEN_WIDTH // 10, SCREEN_HEIGHT // 3 * row + SCREEN_HEIGHT // 6))
                screen.blit(text_surface, text_rect)

                # สร้างกรอบสีดำสำหรับ word list ที่ถูกส่งแล้ว
                if word_color_flags[i]:
                    pygame.draw.rect(screen, BLACK, text_rect.inflate(BORDER_MARGIN, BORDER_MARGIN), 0)

                border_color = WHITE if current_index_to_change == i else BLACK  # เลือกสีของกรอบตามเงื่อนไข
                pygame.draw.rect(screen, border_color, text_rect.inflate(BORDER_MARGIN, BORDER_MARGIN), 2)

        pygame.display.flip()  
        current_index_to_change += 1
            
    end_time = time.time()
    elapsed_time = end_time - start_time
    screen.fill(BLACK)

    # Render the elapsed_time in the middle of the screen
    font_big = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", FONT_SIZE_3)  # ปรับขนาด font
    elapsed_time_text = font_big.render(f"เวลาในการทำแบบทดสอบ: {elapsed_time:.2f} วินาที", True, WHITE)
    elapsed_time_rect = elapsed_time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))  # ปรับตำแหน่ง
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score_text = font_big.render(f"คะแนน: {score}/15", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, elapsed_time_rect.bottom + 20))  # ปรับตำแหน่ง

    font_next = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", int(SCREEN_HEIGHT * 0.06))
    back_text = font_next.render("กลับ", True, (255, 255, 255))
    submit_text = font_next.render("ต่อไป", True, (255, 255, 255))

    button_width = max(back_text.get_width(), submit_text.get_width()) + 40
    button_height = int(SCREEN_HEIGHT * 0.1)
    button_spacing = int(SCREEN_WIDTH * 0.05)

    submit_rect = pygame.Rect(SCREEN_WIDTH - button_spacing - button_width, SCREEN_HEIGHT - button_height - button_spacing, button_width, button_height)

    # Blit both the elapsed time and score texts on the screen
    screen.blit(elapsed_time_text, elapsed_time_rect)
    screen.blit(score_text, score_rect)

    # Draw "submit" button
    pygame.draw.rect(screen, (0, 255, 0), submit_rect)  # Green rectangle for "next" button
    screen.blit(submit_text, (submit_rect.centerx - submit_text.get_width() // 2, submit_rect.centery - submit_text.get_height() // 2))  # Center the text

    pygame.display.flip()
    print("wait for command")
    while True:
        command = arduino_sock.recv(1024).decode("utf-8")
        command = command.strip()  # Remove leading/trailing whitespace
        if command == '1':
            # Move to the next image
            break

    initialize_data()
    pygame.display.flip()

def show_tutorial():
    print("Executing show_tutorial function")
    font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", FONT_SIZE_2)
    # Load tutorial images
    tutorial_images = ["pic/tutorial_image1.png", "pic/tutorial_image2.png", "pic/tutorial_image3.png", "pic/tutorial_image4.png", "pic/tutorial_image5.png"]
    current_image_index = 0

    # Check if tutorial images exist
    for image_path in tutorial_images:
        if not os.path.exists(image_path):
            print(f"Error: Tutorial image '{image_path}' not found.")
            sys.exit()

    # Load font and create a surface for the "back" and "next" buttons
    font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", int(SCREEN_HEIGHT * 0.06))
    back_text = font.render("กลับ", True, (255, 255, 255))
    next_text = font.render("ต่อไป", True, (255, 255, 255))

    # Determine the size of the "back" and "next" buttons
    button_width = max(back_text.get_width(), next_text.get_width()) + 40
    button_height = int(SCREEN_HEIGHT * 0.1)
    button_spacing = int(SCREEN_WIDTH * 0.05)

    back_rect = pygame.Rect(button_spacing, SCREEN_HEIGHT - button_height - button_spacing, button_width, button_height)
    next_rect = pygame.Rect(SCREEN_WIDTH - button_spacing - button_width, SCREEN_HEIGHT - button_height - button_spacing, button_width, button_height)

    # Set up the Pygame screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Game loop for the tutorial page
    tutorial_running = True

    while tutorial_running:
        print("loop_ok")
        screen.fill((0, 0, 0))  # Fill the screen with black
        title_font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", FONT_SIZE_3)
        tutorial_title = title_font.render("แนะนำวิธีการทำแบบทดสอบ", True, (255, 255, 255))
        title_rect = tutorial_title.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.13)))
        screen.blit(tutorial_title, title_rect)

        # Display current tutorial image at a smaller size
        original_image = pygame.image.load(tutorial_images[current_image_index])
        scaled_width = int(original_image.get_width() * 0.5)  # Adjust the scale factor as needed
        scaled_height = int(original_image.get_height() * 0.5)  # Adjust the scale factor as needed
        scaled_image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        image_rect = scaled_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(scaled_image, image_rect)

        # Display "back" and "next" buttons
        pygame.draw.rect(screen, (255, 0, 0), back_rect)  # Red rectangle for "back" button
        screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))  # Center the text

        pygame.draw.rect(screen, (0, 255, 0), next_rect)  # Green rectangle for "next" button
        screen.blit(next_text, (next_rect.centerx - next_text.get_width() // 2, next_rect.centery - next_text.get_height() // 2))  # Center the text

        pygame.display.flip()

        command = arduino_sock.recv(1024).decode("utf-8")
        command = command.strip()  # Remove leading/trailing whitespace
        if command == '0':
            print("command_0")
            # Go to the next page
            tutorial_running = False
            return
        if command == '1':
            print("command_1")
            # Move to the next image
            current_image_index = (current_image_index + 1) % len(tutorial_images) 
        # Do not quit Pygame, just return from the function

def exit_game():
    print("Exiting the game")
    pygame.quit()
    sys.exit()

def connect_to_arduino(pi_address, port):
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((pi_address, port))
        print("Connected to Arduino")
        return sock
    except bluetooth.BluetoothError as e:
        print("Bluetooth connection error:", e)
        return None

def moveToPage(choice):
    if choice == 0:
        print("choice Play\n")
        play_game()
    elif choice == 1:
        print("choice Tutorial\n")
        show_tutorial() 
        draw_menu(screen, title_text, title_rect, option_texts, option_rects, choice, device_connection_text, device_connection_rect,info_text_combined, info_rect)
    elif choice == 2:   
        print("choice exit\n")
        exit_game() 
        
    
# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stroop Test Menu")

# Define fonts and text for the main menu


title_font_size = int(SCREEN_WIDTH * 0.125)
font_size = int(SCREEN_WIDTH * 0.035)  # Reduce the font size for the menu options
title_font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", title_font_size)
font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", font_size)
title_text = title_font.render("Stroop Test", True, (255, 255, 255))
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

# Define menu options
options = ["เริ่มต้นการทำแบบทดสอบ", "แนะนำการทำแบบทดสอบ", "ออกจากการทำแบบทดสอบ"]
option_texts = [font.render(option, True, (255, 255, 255)) for option in options]

# Determine the position and size of the red rectangle
device_connection_rect = pygame.Rect(SCREEN_WIDTH - 230, SCREEN_HEIGHT - 50, 200, 30)  # Adjust position and size as needed
# Render the "Device_connection" text
device_connection_font = pygame.font.Font(None, 24)  # Adjust font size as needed
device_connection_text = device_connection_font.render("Device Connection", True, (255, 255, 255))
# Calculate the position of the text to center it within the rectangle
device_connection_text_rect = device_connection_text.get_rect(center=device_connection_rect.center)

# Calculate layout parameters for the main menu
total_height = (title_rect.height + sum(text.get_height() for text in option_texts) + len(option_texts) * int(SCREEN_HEIGHT * 0.025))
start_y = (SCREEN_HEIGHT - total_height) // 2
title_rect.top = start_y - int(SCREEN_HEIGHT * 0.0333)
start_y += title_rect.height + int(SCREEN_HEIGHT * 0.025)
spacing = int(SCREEN_HEIGHT * 0.0167)

# Adjust start_y to move everything up
start_y -= 100  # Adjust this value to move the text further up or down

# Set a fixed width and height for all option rectangles in the main menu
rect_width = int(SCREEN_WIDTH * 0.5)  # Adjust the width
rect_height = int(SCREEN_HEIGHT * 0.1)  # Adjust the height

# Position the options and rectangles in the main menu
rects = [pygame.Rect((SCREEN_WIDTH - rect_width) // 2, start_y + i * (rect_height + int(SCREEN_HEIGHT * 0.025)), rect_width, rect_height) for i in range(len(option_texts))]
option_rects = rects  # Assign the same rectangles to option_rects

info_font_size = int(SCREEN_WIDTH * 0.03)
info_font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", info_font_size)

# Render the first part of the sentence before "กดปุ่มสีแดง"
info_text_part1 = info_font.render("แนะนำ : ", True, (255, 255, 255))

# Render "กดปุ่มสีแดง" in red
red_text = info_font.render("กดปุ่มสีแดงเพื่อเลือกหัวข้อ", True, (255, 0, 0))

# Render the second part of the sentence after "กดปุ่มสีแดง"
info_text_part2 = info_font.render(" กดปุ่มสีเขียวเพื่อเข้าสู่หัวข้อ", True, (0, 255, 0))

# Combine the rendered surfaces into a single surface
info_text_combined = pygame.Surface((info_text_part1.get_width() + red_text.get_width() + info_text_part2.get_width(), info_font.get_height()), pygame.SRCALPHA)
info_text_combined.blit(info_text_part1, (0, 0))
info_text_combined.blit(red_text, (info_text_part1.get_width(), 0))
info_text_combined.blit(info_text_part2, (info_text_part1.get_width() + red_text.get_width(), 0))

# Calculate the center position for the combined text
info_rect = info_text_combined.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - int(SCREEN_HEIGHT * 0.95)))

# Game loop for the main menu
running = True
selected_option = 0  # Start with the first option selected
state = 0 #check is first run or not
choice = 0

print("Waiting for connection ....")

pi_address = "00:21:09:00:27:B7"  # Replace with your Pi's Bluetooth address
port = 1  # Bluetooth port

while running:
    font = pygame.font.Font("/home/strooptest/Desktop/Test_Bluetooth/BoonTook-Regular.ttf", FONT_SIZE)
    if state == 1:
        while True:
            command = arduino_sock.recv(1024).decode("utf-8")
            command = command.strip()  # Remove leading/trailing whitespace
            if command == '0':
                choice += 1
                if choice >= 3:
                    choice = 0
                print("choice = :" + str(choice))
            elif command == '1':
                moveToPage(choice)
            draw_menu(screen, title_text, title_rect, option_texts, option_rects, choice, device_connection_text,device_connection_rect,info_text_combined, info_rect)

    draw_menu(screen, title_text, title_rect, option_texts, option_rects, choice, device_connection_text,device_connection_rect,info_text_combined, info_rect)
    if state == 0:
        arduino_sock = connect_to_arduino(pi_address, port)
        arduino_sock.send(b"Start\n")  # Make sure to include the newline character
        print("Data sent to Arduino")
        received_data = arduino_sock.recv(1024).decode("utf-8")
        print("Received data from Arduino:", received_data)
        state = 1   