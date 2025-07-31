import pygame
import os
from pygame import mixer
import random
from datetime import datetime
import calendar
import sys
import math
import tkinter as tk
from tkinter import filedialog

# Initialize Pygame and Mixer for MP3
pygame.init()
mixer.init()

# Set up display for Gameboy resolution, then scale it up
WIDTH, HEIGHT = 900, 700  # Scaled up by 4x
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gameboy Style - Multi App')
CELL_SIZE = 40
GRID_SIZE = 5  # Start with a 5x5 grid
MARGIN = 100  # Space for numbers outside the grid

# Gameboy-like colors (Green and Black palette)
DARK_GREEN = (0, 48, 0)
MEDIUM_GREEN = (32, 96, 32)
LIGHT_GREEN = (128, 192, 128)
VERY_LIGHT_GREEN = (200, 255, 200)
BUTTON_COLOR = (50, 150, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (211, 211, 211)

# Fonts
font = pygame.font.SysFont('Arial', 24)

# Function to draw text (simplified for pixelated look)
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))


#--------- Editor de Texto Simple----------   

# Function to draw the text content on the screen
def draw_text_app():
    screen.fill(WHITE)
    for i, line in enumerate(content):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (10, 10 + i * 30))
    pygame.display.update()

# Function to add text at the current cursor position
def add_text(char):
    line_idx, char_idx = cursor_position
    content[line_idx] = content[line_idx][:char_idx] + char + content[line_idx][char_idx:]
    cursor_position[1] += 1

# Function to save the content to a file
def save_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as f:
            f.write("\n".join(content))
    root.destroy()

# Function to open a file and load its content
def open_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as f:
            global content, cursor_position
            content = f.read().splitlines()
            cursor_position = [len(content) - 1, len(content[-1])] if content else [0, 0]
    root.destroy()


def simple_text_app():
    
# Text content and cursor position
    content = [""]
    cursor_position = [0, 0]  # [line_index, char_index]

# Main loop for the text editor
    running = True
    while running:
        draw_text_app()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                # Basic text input
                if event.unicode.isprintable():
                        add_text(event.unicode)
            
                # Special keys handling
                elif event.key == pygame.K_BACKSPACE:
                    line_idx, char_idx = cursor_position
                    if char_idx > 0:
                        content[line_idx] = content[line_idx][:char_idx - 1] + content[line_idx][char_idx:]
                        cursor_position[1] -= 1
                    elif line_idx > 0:
                        prev_line_length = len(content[line_idx - 1])
                        content[line_idx - 1] += content[line_idx]
                        del content[line_idx]
                        cursor_position = [line_idx - 1, prev_line_length]
            
                elif event.key == pygame.K_RETURN:
                    line_idx, char_idx = cursor_position
                    new_line = content[line_idx][char_idx:]
                    content[line_idx] = content[line_idx][:char_idx]
                    content.insert(line_idx + 1, new_line)
                    cursor_position = [line_idx + 1, 0]
            
                elif event.key == pygame.K_LEFT:
                    line_idx, char_idx = cursor_position
                    if char_idx > 0:
                        cursor_position[1] -= 1
                    elif line_idx > 0:
                        cursor_position = [line_idx - 1, len(content[line_idx - 1])]
            
                elif event.key == pygame.K_RIGHT:
                    line_idx, char_idx = cursor_position
                    if char_idx < len(content[line_idx]):
                        cursor_position[1] += 1
                    elif line_idx < len(content) - 1:
                        cursor_position = [line_idx + 1, 0]
            
                elif event.key == pygame.K_UP:
                    line_idx, char_idx = cursor_position
                    if line_idx > 0:
                        cursor_position = [line_idx - 1, min(char_idx, len(content[line_idx - 1]))]
            
                elif event.key == pygame.K_DOWN:
                    line_idx, char_idx = cursor_position
                    if line_idx < len(content) - 1:
                        cursor_position = [line_idx + 1, min(char_idx, len(content[line_idx + 1]))]

                # Save file with CTRL + S
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_file()

                # Open file with CTRL + O
                elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    open_file()

    # Quit Pygame when finished
    pygame.quit()
    
#--------- Reproductor de mp3----------   
# MP3 Player variables
playlist = []
current_track = None
paused = False
current_track_index = 0

# Function to add files to the playlist
def add_to_playlist():
    global playlist
    folder_path = input("Enter the folder path containing MP3s: ")
    try:
        for file in os.listdir(folder_path):
            if file.endswith('.mp3'):
                playlist.append(os.path.join(folder_path, file))
        print("Files added to the playlist.")
    except FileNotFoundError:
        print("Invalid folder path.")

# Function to play a track
def play_track():
    global current_track, paused
    if len(playlist) > 0:
        if current_track is None or not mixer.music.get_busy():
            mixer.music.load(playlist[current_track_index])
            mixer.music.play()
            current_track = playlist[current_track_index]
            paused = False

# Function to pause or resume the track
def pause_track():
    global paused
    if paused:
        mixer.music.unpause()
        paused = False
    else:
        mixer.music.pause()
        paused = True

# Function to stop playback
def stop_track():
    mixer.music.stop()

# Function to go to the next track
def next_track():
    global current_track_index
    if len(playlist) > 0:
        current_track_index = (current_track_index + 1) % len(playlist)
        play_track()

# Function to go to the previous track
def previous_track():
    global current_track_index
    if len(playlist) > 0:
        current_track_index = (current_track_index - 1) % len(playlist)
        play_track()

# Function to draw spectrum analyzer (simulated)
def draw_spectrum_analyzer(surface):
    spectrum_bars = 10  # Number of bars in the analyzer
    max_height = 50  # Max height for the spectrum bars
    for i in range(spectrum_bars):
        bar_height = random.randint(5, max_height)
        bar_width = 10
        bar_x = i * (bar_width + 5) + 30
        pygame.draw.rect(surface, LIGHT_GREEN, (bar_x, 10, bar_width, bar_height))

# Function to display a clock
def display_clock():
    running = True
    while running:
        screen.fill(DARK_GREEN)

        current_time = datetime.now().strftime("%H:%M:%S")
        draw_text(screen, 'Clock', font, VERY_LIGHT_GREEN, 60, 50)
        draw_text(screen, current_time, font, VERY_LIGHT_GREEN, 60, 70)

        # Scale and display the low-res surface
        scaled_surface = pygame.transform.scale(screen, (WIDTH, HEIGHT))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

todo_list = []  # Each item will be a tuple: (description, severity)

severity_colors = {
    "low": (173, 216, 230),  # Light Blue
    "medium": (255, 165, 0), # Orange
    "high": (255, 0, 0)      # Red
}

# Function to add items to the to-do list with severity
def add_todo_item(item, severity):
    if severity not in severity_colors:
        severity = "low"  # Default to 'low' if an invalid severity is given
    todo_list.append((item, severity))

# Function to display the to-do list with severity colors and auto-bullets
def display_todo_list():
    running = True
    menu_active = True  # Track if the menu is active
    selected_menu_option = 0
    new_item_input = ""
    severity_input = ""

    while running:
        screen.fill(DARK_GREEN)

        # Display the menu
        if menu_active:
            draw_text(screen, 'To-Do List Menu', font, VERY_LIGHT_GREEN, 50, 30)
            menu_options = ['1. Add To-Do Item', '2. Display To-Do List', '3. Quit']
            
            for i, option in enumerate(menu_options):
                color = LIGHT_GRAY if i == selected_menu_option else VERY_LIGHT_GREEN
                draw_text(screen, option, font, color, 50, 80 + i * 40)
        
        # Handle adding a new item
        if selected_menu_option == 0 and not menu_active:
            draw_text(screen, "Enter To-Do Item:", font, VERY_LIGHT_GREEN, 50, 80)
            draw_text(screen, new_item_input, font, VERY_LIGHT_GREEN, 250, 80)
            draw_text(screen, "Enter Severity (low, medium, high):", font, VERY_LIGHT_GREEN, 50, 120)
            draw_text(screen, severity_input, font, VERY_LIGHT_GREEN, 400, 120)

        # Display the to-do list
        if selected_menu_option == 1 and not menu_active:
            draw_text(screen, 'To-Do List', font, VERY_LIGHT_GREEN, 50, 30)
            for i, (item, severity) in enumerate(todo_list):
                bullet = "•" if severity == "low" else "◉" if severity == "medium" else "★"
                color = severity_colors[severity]
                draw_text(screen, f'{bullet} {item}', font, color, 20, 80 + i * 30)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not menu_active:
                        menu_active = True
                    else:
                        running = False

                # Navigate through the menu options
                if menu_active:
                    if event.key == pygame.K_DOWN:
                        selected_menu_option = (selected_menu_option + 1) % 3
                    elif event.key == pygame.K_UP:
                        selected_menu_option = (selected_menu_option - 1) % 3
                    elif event.key == pygame.K_RETURN:
                        menu_active = False
                        if selected_menu_option == 2:  # Quit
                            running = False

                # Handle new item input
                elif selected_menu_option == 0:
                    if event.key == pygame.K_BACKSPACE:
                        if severity_input:
                            severity_input = severity_input[:-1]
                        elif new_item_input:
                            new_item_input = new_item_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if new_item_input and severity_input:
                            add_todo_item(new_item_input, severity_input.lower())
                            new_item_input = ""
                            severity_input = ""
                            menu_active = True
                    else:
                        if severity_input == "":
                            new_item_input += event.unicode
                        else:
                            severity_input += event.unicode

                # Go back to menu from the list display
                elif selected_menu_option == 1:
                    menu_active = True

    pygame.quit()

# Function to display the MP3 player
def mp3_player():
    global paused
    running = True
    while running:
        screen.fill(DARK_GREEN)

        # Draw spectrum analyzer at the top
        draw_spectrum_analyzer(screen)

        # Draw playlist and controls on the low-res surface
        draw_text(screen, 'MP3 Player', font, VERY_LIGHT_GREEN, 20, 70)
        draw_text(screen, f'Track: {os.path.basename(current_track) if current_track else "None"}', font, VERY_LIGHT_GREEN, 20, 90)

        # Display playlist
        draw_text(screen, 'Playlist:', font, VERY_LIGHT_GREEN, 20, 110)
        for i, track in enumerate(playlist):
            draw_text(screen, f'{i+1}. {os.path.basename(track)}', font, VERY_LIGHT_GREEN, 20, 130 + i * 10)

        draw_text(screen, 'P: Play/Pause | N: Next | B: Previous | S: Stop | A: Add | ESC: Exit', font, MEDIUM_GREEN, 10, 200)

        # Scale the low-res surface to the higher resolution display
        scaled_surface = pygame.transform.scale(screen, (WIDTH, HEIGHT))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if mixer.music.get_busy():
                        pause_track()
                    else:
                        play_track()
                elif event.key == pygame.K_n:
                    next_track()
                elif event.key == pygame.K_b:
                    previous_track()
                elif event.key == pygame.K_s:
                    stop_track()
                elif event.key == pygame.K_a:
                    add_to_playlist()
                elif event.key == pygame.K_ESCAPE:
                    running = False


# Global variables for calculator
calc_input = ""   # Current input string for the calculator
calc_history = [] # List to store calculation history
memory_value = 0  # Memory storage value

# Function to evaluate the current calculator input

def evaluate_expression(expression):
    try:
        # Replace common functions with math module equivalents
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('arcsin', 'math.asin')
        expression = expression.replace('arccos', 'math.acos')
        expression = expression.replace('arctan', 'math.atan')
        expression = expression.replace('sinh', 'math.sinh')
        expression = expression.replace('cosh', 'math.cosh')
        expression = expression.replace('tanh', 'math.tanh')
        expression = expression.replace('log', 'math.log10')  # Base-10 log
        expression = expression.replace('ln', 'math.log')  # Natural log
        expression = expression.replace('e^', 'math.exp')  # Exponential function (e^x)

        # Evaluate the expression safely
        result = eval(expression)
        calc_history.append(f"{expression} = {result}")
        return result
    except Exception as e:
        return "Error"


# Function to draw the calculator on the screen
def draw_calculator():
    screen.fill(DARK_GREEN)  # Fill the main screen directly now

    # Draw the input box
    pygame.draw.rect(screen, VERY_LIGHT_GREEN, pygame.Rect(20, 50, 400, 50), 1)
    draw_text(screen, calc_input, font, VERY_LIGHT_GREEN, 30, 60)  # Adjust positions and sizes

    # Example button positions for new resolution
    buttons = [
        # Standard calculator buttons
        ('7', 20, 150), ('8', 100, 150), ('9', 180, 150), ('/', 260, 150),
        ('4', 20, 200), ('5', 100, 200), ('6', 180, 200), ('*', 260, 200),
        ('1', 20, 250), ('2', 100, 250), ('3', 180, 250), ('-', 260, 250),
        ('0', 20, 300), ('.', 100, 300), ('=', 180, 300), ('+', 260, 300),
        
        # Scientific operation buttons
        ('sin', 340, 150), ('cos', 340, 200), ('tan', 340, 250), ('sqrt', 340, 300),
        ('arcsin', 420, 150), ('arccos', 420, 200), ('arctan', 420, 250), ('e^x', 420, 300),
        ('log', 500, 150), ('ln', 500, 200), ('sinh', 500, 250), ('cosh', 500, 300),
        ('tanh', 580, 150), ('C', 580, 200), ('M+', 580, 250), ('M-', 580, 300),
        ('MR', 660, 150), ('MC', 660, 200)
    ]

    # Adjust button sizes and text placement for better fit
    for (text, x, y) in buttons:
        pygame.draw.rect(screen, VERY_LIGHT_GREEN, pygame.Rect(x, y, 70, 40), 1)
        draw_text(screen, text, font, VERY_LIGHT_GREEN, x + 10, y + 10)

    # History panel update
    draw_text(screen, "History:", font, VERY_LIGHT_GREEN, 500, 50)
    for i, entry in enumerate(calc_history[-5:]):  # Show last 5 entries
        draw_text(screen, entry, font, VERY_LIGHT_GREEN, 500, 80 + i * 30)

# Function to handle calculator input
def handle_calculator_input(event):
    global calc_input, memory_value
    
    # Numbers and basic operators
    if event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                     pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
        calc_input += event.unicode
    elif event.key in (pygame.K_PLUS, pygame.K_MINUS, pygame.K_ASTERISK, pygame.K_SLASH, pygame.K_PERIOD):
        calc_input += event.unicode

    # Evaluate expression
    elif event.key == pygame.K_RETURN:  # Enter key to evaluate the expression
        calc_input = str(evaluate_expression(calc_input))

    # Backspace and clear
    elif event.key == pygame.K_BACKSPACE:
        calc_input = calc_input[:-1]
    elif event.key == pygame.K_c:
        calc_input = ""

    # Scientific functions
    elif event.key == pygame.K_s:  # sin function
        calc_input += "sin("
    elif event.key == pygame.K_o:  # cos function
        calc_input += "cos("
    elif event.key == pygame.K_t:  # tan function
        calc_input += "tan("
    elif event.key == pygame.K_a:  # arcsin function
        calc_input += "arcsin("
    elif event.key == pygame.K_b:  # arccos function
        calc_input += "arccos("
    elif event.key == pygame.K_n:  # arctan function
        calc_input += "arctan("
    elif event.key == pygame.K_q:  # sqrt function
        calc_input += "sqrt("
    elif event.key == pygame.K_e:  # e^x function
        calc_input += "e^("
    elif event.key == pygame.K_l:  # log function
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # If Shift + L, use ln (natural log)
            calc_input += "ln("
        else:
            calc_input += "log("
    elif event.key == pygame.K_h:  # sinh, cosh, tanh functions
        calc_input += "sinh("
    elif event.key == pygame.K_j:
        calc_input += "cosh("
    elif event.key == pygame.K_k:
        calc_input += "tanh("

    # Memory functions
    elif event.key == pygame.K_m:  # Memory recall
        calc_input += str(memory_value)
    elif event.key == pygame.K_PLUS and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        try:
            memory_value += float(evaluate_expression(calc_input))
            calc_input = ""  # Clear input after storing in memory
        except:
            pass
    elif event.key == pygame.K_MINUS and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        try:
            memory_value -= float(evaluate_expression(calc_input))
            calc_input = ""  # Clear input after subtracting from memory
        except:
            pass
    elif event.key == pygame.K_r:  # Memory clear
        memory_value = 0

    # Update display after any key press to reflect the changes
    draw_calculator()

   
def calculator_app():
    global calc_input
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(DARK_GREEN)  # Fill the main screen with new resolution

        draw_calculator()  # Directly draw on the main screen now
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Properly close the program
                running = False
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Return to main menu on ESC key
                    running = False
                    return  # Exit calculator app loop and return to the main menu
                else:
                    handle_calculator_input(event)
            
        clock.tick(30)  # Set desired FPS for normal resolution

# Graphing parameters
graph_center = [400, 300]  # Center of the graph on the screen
scale = 50  # Number of pixels per unit on the graph

# Function to draw the graph grid and axes
def draw_grid(screen):
    screen.fill(LIGHT_GREEN)
    # Draw grid lines
    for x in range(0, 800, scale):
        pygame.draw.line(screen, BLACK, (x, 0), (x, 600), 1)
    for y in range(0, 600, scale):
        pygame.draw.line(screen, BLACK, (0, y), (800, y), 1)
    
    # Draw axes
    pygame.draw.line(screen, BLACK, (0, graph_center[1]), (800, graph_center[1]), 2)
    pygame.draw.line(screen, BLACK, (graph_center[0], 0), (graph_center[0], 600), 2)

# Function to plot a mathematical function on the graph
def plot_function(screen, func, color=VERY_LIGHT_GREEN):
    prev_x = None
    prev_y = None
    for x in range(0, 800):
        # Convert screen coordinates to graph coordinates
        graph_x = (x - graph_center[0]) / scale
        try:
            # Calculate the y value using the function
            graph_y = -func(graph_x) * scale + graph_center[1]
            
            # Convert back to screen coordinates
            y = int(graph_y)
            
            # Draw line segment from previous point to current point
            if prev_x is not None and prev_y is not None:
                pygame.draw.line(screen, color, (prev_x, prev_y), (x, y), 2)
                
            prev_x, prev_y = x, y
        except Exception as e:
            prev_x, prev_y = None, None

# Function to handle zoom and pan
def handle_zoom_pan(event):
    global graph_center, scale
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:  # Scroll up to zoom in
            scale += 5
        elif event.button == 5:  # Scroll down to zoom out
            scale = max(5, scale - 5)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            graph_center[0] += 20
        elif event.key == pygame.K_RIGHT:
            graph_center[0] -= 20
        elif event.key == pygame.K_UP:
            graph_center[1] += 20
        elif event.key == pygame.K_DOWN:
            graph_center[1] -= 20

# Graphing app main loop
def graphing_app():
    global graph_center, scale
    running = True
    functions = [
        lambda x: math.sin(x),  # y = sin(x)
        lambda x: x ** 2 / 10,  # y = x^2 / 10
    ]
    
    while running:
        draw_grid(screen)
        
        # Plot all functions
        colors = [VERY_LIGHT_GREEN, BUTTON_COLOR, LIGHT_GREEN]
        for i, func in enumerate(functions):
            plot_function(screen, func, colors[i % len(colors)])
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Return to main menu
                    running = False
                    return
            handle_zoom_pan(event)
        
        pygame.time.Clock().tick(30)  # Control frame rate

# To run the graphing app, you would call graphing_app()
# graphing_app()




# Global variables for calendar
current_year = datetime.now().year
current_month = datetime.now().month
selected_day = datetime.now().day

# Store events in a dictionary with dates as keys
events = {
    "2024-09-24": ["Doctor Appointment at 3 PM", "Team Meeting at 10 AM"]
}

# Function to draw the calendar on the screen
def draw_calendar(view='month'):
    screen.fill(DARK_GREEN)
    draw_text(screen, f"{calendar.month_name[current_month]} {current_year}", font, VERY_LIGHT_GREEN, 300, 20)

    if view == 'month':
        draw_month_view()
    elif view == 'week':
        draw_week_view()
    elif view == 'year':
        draw_year_view()

# Function to draw the month view
def draw_month_view():
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(day_names):
        draw_text(screen, day, font, VERY_LIGHT_GREEN, 100 + i * 80, 80)

    cal = calendar.Calendar()
    month_days = list(cal.itermonthdays(current_year, current_month))
    start_x, start_y = 100, 120
    day_x, day_y = start_x, start_y

    for index, day in enumerate(month_days):
        if day == 0:
            day_x += 80
            if (index + 1) % 7 == 0:
                day_x = start_x
                day_y += 60
            continue

        if day == selected_day:
            pygame.draw.rect(screen, VERY_LIGHT_GREEN, pygame.Rect(day_x - 10, day_y - 10, 60, 40), 0)

        draw_text(screen, str(day), font, VERY_LIGHT_GREEN, day_x, day_y)
        display_events_for_day(day_x, day_y, day)

        day_x += 80
        if (index + 1) % 7 == 0:
            day_x = start_x
            day_y += 60

    draw_navigation_buttons()

# Function to draw navigation buttons and handle input
def draw_navigation_buttons():
    draw_text(screen, "<", font, BUTTON_COLOR, 50, 20)  # Previous month
    draw_text(screen, ">", font, BUTTON_COLOR, 700, 20)  # Next month
    draw_text(screen, "Year -", font, BUTTON_COLOR, 50, 500)  # Previous year
    draw_text(screen, "Year +", font, BUTTON_COLOR, 650, 500)  # Next year
    draw_text(screen, "Week View", font, BUTTON_COLOR, 320, 500)  # Week view
    draw_text(screen, "Year View", font, BUTTON_COLOR, 450, 500)  # Year view

# Function to draw the week view
def draw_week_view():
    # Implementation to show the current week with events
    week_text = "Week View Not Implemented"
    draw_text(screen, week_text, font, VERY_LIGHT_GREEN, 200, 250)

# Function to draw the year view
def draw_year_view():
    # Implementation to show a yearly overview
    year_text = "Year View Not Implemented"
    draw_text(screen, year_text, font, VERY_LIGHT_GREEN, 200, 250)

def display_events_for_day(day_x, day_y, day):
    date_key = f"{current_year}-{str(current_month).zfill(2)}-{str(day).zfill(2)}"
    if date_key in events:
        for i, event in enumerate(events[date_key]):
            draw_text(screen, event, font, VERY_LIGHT_GREEN, day_x, day_y + 30 + (i * 20))

# Function to handle calendar input for navigation and events
def handle_calendar_input(event):
    global current_month, current_year, selected_day

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:  # Previous month
            current_month -= 1
            if current_month < 1:
                current_month = 12
                current_year -= 1
        elif event.key == pygame.K_RIGHT:  # Next month
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
        elif event.key == pygame.K_UP:  # Previous year
            current_year -= 1
        elif event.key == pygame.K_DOWN:  # Next year
            current_year += 1

    # Mouse click for selecting a specific day or button
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        # Check if clicked on a day cell
        if 100 <= mouse_x <= 660 and 120 <= mouse_y <= 480:
            col = (mouse_x - 100) // 80
            row = (mouse_y - 120) // 60
            day_index = row * 7 + col

            # Check if clicked on a valid day
            month_days = list(calendar.Calendar().itermonthdays(current_year, current_month))
            if 0 < month_days[day_index] <= 31:
                selected_day = month_days[day_index]
        
        # Check for button clicks
        if 50 <= mouse_x <= 90 and 20 <= mouse_y <= 60:
            current_month -= 1  # Previous month
            if current_month < 1:
                current_month = 12
                current_year -= 1
        elif 700 <= mouse_x <= 740 and 20 <= mouse_y <= 60:
            current_month += 1  # Next month
            if current_month > 12:
                current_month = 1
                current_year += 1
        elif 50 <= mouse_x <= 130 and 500 <= mouse_y <= 540:
            current_year -= 1  # Previous year
        elif 650 <= mouse_x <= 730 and 500 <= mouse_y <= 540:
            current_year += 1  # Next year
        elif 320 <= mouse_x <= 430 and 500 <= mouse_y <= 540:
            draw_calendar('week')  # Week view
        elif 450 <= mouse_x <= 560 and 500 <= mouse_y <= 540:
            draw_calendar('year')  # Year view

# Function to add an event to a specific date
def add_event_to_date(date, event):
    if date not in events:
        events[date] = []
    events[date].append(event)

# Application loop for calendar
def calendar_app():
    clock = pygame.time.Clock()
    running = True

    while running:
        draw_calendar()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            handle_calendar_input(event)

        clock.tick(30)  # Set desired FPS for smooth navigation

# Add some example events
add_event_to_date("2024-09-25", "Team Meeting at 10 AM")
add_event_to_date("2024-09-24", "Doctor Appointment at 3 PM")

               
# Snake Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction
speed = 15
food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
food_spawn = True
score = 0

# Function to run Snake Game
def snake_game():
    global snake_pos, snake_body, snake_direction, change_to, speed, food_pos, food_spawn, score
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # Check if direction is not opposite of the current direction
        if change_to == 'UP' and snake_direction != 'DOWN':
            snake_direction = 'UP'
        if change_to == 'DOWN' and snake_direction != 'UP':
            snake_direction = 'DOWN'
        if change_to == 'LEFT' and snake_direction != 'RIGHT':
            snake_direction = 'LEFT'
        if change_to == 'RIGHT' and snake_direction != 'LEFT':
            snake_direction = 'RIGHT'

        # Move the snake
        if snake_direction == 'UP':
            snake_pos[1] -= 10
        if snake_direction == 'DOWN':
            snake_pos[1] += 10
        if snake_direction == 'LEFT':
            snake_pos[0] -= 10
        if snake_direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]

        food_spawn = True
        screen.fill(DARK_GREEN)

        # Draw Snake and Food
        for pos in snake_body:
            pygame.draw.rect(screen, VERY_LIGHT_GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screen, LIGHT_GREEN, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH-10:
            running = False
        if snake_pos[1] < 0 or snake_pos[1] > HEIGHT-10:
            running = False
        for block in snake_body[1:]:
            if snake_pos == block:
                running = False
        
        draw_text(screen, f"{score}", font, VERY_LIGHT_GREEN, 300, 20)
        screen.blit(screen, (0, 0))
        pygame.display.update()
        clock.tick(speed)
        
        
# Define character matrices for different states
happy_character = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0]
]

sad_character = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0]
]

tired_character = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0]
]

# Function to draw the pixel character on the screen
def draw_character(surface, character_matrix, x, y, pixel_size=4):
    """ Draws a matrix-based character on the given surface.
    Args:
        surface: The pygame surface to draw on.
        character_matrix: 2D list representing the character.
        x, y: Position to start drawing the character.
        pixel_size: Size of each pixel in the character.
    """
    for row_index, row in enumerate(character_matrix):
        for col_index, pixel in enumerate(row):
            if pixel:  # Only draw filled pixels (value 1)
                pygame.draw.rect(
                    surface,
                    VERY_LIGHT_GREEN,  # Color for the character pixel
                    pygame.Rect(
                        x + col_index * pixel_size,
                        y + row_index * pixel_size,
                        pixel_size,
                        pixel_size
                    )
                )
        
# Define Tamagotchi variables
pet_hunger = 50  # Hunger level (0-100, 0 means starving)
pet_happiness = 50  # Happiness level (0-100)
pet_energy = 50  # Energy level (0-100)
pet_name = "Pet"  # Default pet name
action_timeout = 0  # A simple cooldown for actions

# Update the Tamagotchi mini-game function to use the pixel character
def tamagotchi_game():
    global pet_hunger, pet_happiness, pet_energy, action_timeout
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(DARK_GREEN)

        # Update pet stats over time
        if action_timeout == 0:
            pet_hunger = max(0, pet_hunger - 1)
            pet_energy = max(0, pet_energy - 1)
            pet_happiness = max(0, pet_happiness - 1)
            action_timeout = 60  # Reset action timeout (acts as cooldown)
        else:
            action_timeout -= 1

        # Choose the appropriate character matrix based on the pet's status
        if pet_hunger < 30 or pet_energy < 30:
            character = tired_character  # Tired or hungry pet
        elif pet_happiness < 30:
            character = sad_character  # Sad pet
        else:
            character = happy_character  # Happy pet

        # Draw pet status
        draw_text(screen, f'{pet_name}', font, VERY_LIGHT_GREEN, 50, 20)
        draw_text(screen, f'Hunger: {pet_hunger}', font, VERY_LIGHT_GREEN, 30, 40)
        draw_text(screen, f'Happiness: {pet_happiness}', font, VERY_LIGHT_GREEN, 30, 60)
        draw_text(screen, f'Energy: {pet_energy}', font, VERY_LIGHT_GREEN, 30, 80)

        # Check pet status and game over conditions
        if pet_hunger == 0 or pet_energy == 0:
            draw_text(screen, 'Your pet is too weak...', font, VERY_LIGHT_GREEN, 30, 100)
            draw_text(screen, 'Game Over!', font, VERY_LIGHT_GREEN, 50, 120)

        # Draw the character on the screen
        draw_character(screen, character, 80, 120, pixel_size=4)

        draw_text(screen, '1: Feed | 2: Play | 3: Sleep | ESC: Exit', font, MEDIUM_GREEN, 10, 140)

        # Scale and display the low-res surface
        scaled_surface = pygame.transform.scale(screen, (WIDTH, HEIGHT))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if pet_hunger < 100:
                        pet_hunger = min(100, pet_hunger + 20)
                        draw_text(screen, 'You fed your pet!', font, VERY_LIGHT_GREEN, 30, 160)
                elif event.key == pygame.K_2:
                    if pet_energy > 10:
                        pet_energy = max(0, pet_energy - 10)
                        pet_happiness = min(100, pet_happiness + 20)
                        draw_text(screen, 'You played with your pet!', font, VERY_LIGHT_GREEN, 30, 160)
                elif event.key == pygame.K_3:
                    if pet_energy < 100:
                        pet_energy = min(100, pet_energy + 30)
                        draw_text(screen, 'Your pet took a nap!', font, VERY_LIGHT_GREEN, 30, 160)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(10)  # Control the frame rate for the mini-game


# Placeholder solution (1 is filled, 0 is blank)
solution = [
    [1, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1]
]

# Declare user_grid as a global variable
user_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Clues for rows and columns
row_clues = [[1, 1], [2], [4], [1, 2], [1, 1]]
col_clues = [[2, 1], [1, 1], [1], [2, 2], [2]]


# Function to draw the grid and clues
def draw_grid():
    screen.fill(DARK_GREEN)  # Gameboy-like background color

    # Draw vertical lines
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(screen, VERY_LIGHT_GREEN, (MARGIN + x * CELL_SIZE, MARGIN),
                         (MARGIN + x * CELL_SIZE, MARGIN + GRID_SIZE * CELL_SIZE), 2)

    # Draw horizontal lines
    for y in range(GRID_SIZE + 1):
        pygame.draw.line(screen, VERY_LIGHT_GREEN, (MARGIN, MARGIN + y * CELL_SIZE),
                         (MARGIN + GRID_SIZE * CELL_SIZE, MARGIN + y * CELL_SIZE), 2)

    # Draw the cells
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if user_grid[y][x] == 1:  # Filled cell
                pygame.draw.rect(screen, BLACK, pygame.Rect(MARGIN + x * CELL_SIZE + 2,
                                                            MARGIN + y * CELL_SIZE + 2,
                                                            CELL_SIZE - 3, CELL_SIZE - 3))
            elif user_grid[y][x] == 0:  # Marked cell
                pygame.draw.rect(screen, MEDIUM_GREEN, pygame.Rect(MARGIN + x * CELL_SIZE + 2,
                                                                   MARGIN + y * CELL_SIZE + 2,
                                                                   CELL_SIZE - 3, CELL_SIZE - 3))

    # Draw the row clues
    for y in range(GRID_SIZE):
        clue_text = ' '.join(map(str, row_clues[y]))
        text_surface = font.render(clue_text, True, VERY_LIGHT_GREEN)
        screen.blit(text_surface, (MARGIN - 50, MARGIN + y * CELL_SIZE + 10))

    # Draw the column clues
    for x in range(GRID_SIZE):
        clue_text = ' '.join(map(str, col_clues[x]))
        text_surface = font.render(clue_text, True, VERY_LIGHT_GREEN)
        screen.blit(text_surface, (MARGIN + x * CELL_SIZE + 10, MARGIN - 40))


# Function to check if the user has completed the puzzle
def check_solution():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if user_grid[y][x] != solution[y][x]:  # Check if grid matches the solution
                return False
    return True


# Nonogram app function
def nonogram_app():
    global user_grid  # Declare user_grid as global

    running = True
    while running:
        screen.fill(DARK_GREEN)
        draw_grid()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = (mouse_x - MARGIN) // CELL_SIZE
                grid_y = (mouse_y - MARGIN) // CELL_SIZE

                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    if event.button == 1:  # Left click to fill
                        user_grid[grid_y][grid_x] = 1
                    elif event.button == 3:  # Right click to mark
                        user_grid[grid_y][grid_x] = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Clear the grid with 'C' key
                    user_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                elif event.key == pygame.K_q:  # Press 'Q' to quit
                    running = False

        # Check if the puzzle is complete
        if check_solution():
            text_surface = font.render("You Win!", True, VERY_LIGHT_GREEN)
            screen.blit(text_surface, (MARGIN + GRID_SIZE * CELL_SIZE + 50, MARGIN))

        # Update the screen
        pygame.display.flip()

# Main menu function
def main_menu():
    running = True
    while running:
        screen.fill(DARK_GREEN)

        draw_text(screen, 'Main Menu', font, VERY_LIGHT_GREEN, 60, 40)
        draw_text(screen, '1. MP3 Player App', font, VERY_LIGHT_GREEN, 50, 60)
        draw_text(screen, '2. Clock App', font, VERY_LIGHT_GREEN, 50, 80)
        draw_text(screen, '3. To-Do List App', font, VERY_LIGHT_GREEN, 50, 100)
        draw_text(screen, '4. Calculator App', font, VERY_LIGHT_GREEN, 50, 120)
        draw_text(screen, '5. Calendar App', font, VERY_LIGHT_GREEN, 50, 140)
        draw_text(screen, '6. Snake Game App', font, VERY_LIGHT_GREEN, 50,160)
        draw_text(screen, '7. Tamagotchi Game App', font, VERY_LIGHT_GREEN, 50,180)
        draw_text(screen, '8. Graphic App', font, VERY_LIGHT_GREEN, 50, 200)
        draw_text(screen, '9. Simple Text App', font, VERY_LIGHT_GREEN, 50, 220)
        draw_text(screen, 'N. Nonogram App', font, VERY_LIGHT_GREEN, 50, 240)
        draw_text(screen, 'Q. Quit', font, VERY_LIGHT_GREEN, 50, 260)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mp3_player()
                if event.key == pygame.K_2:
                    display_clock()
                if event.key == pygame.K_3:
                    display_todo_list()
                if event.key == pygame.K_4:
                    calculator_app()
                if event.key == pygame.K_5:
                    calendar_app()
                if event.key == pygame.K_6:
                    snake_game()
                if event.key == pygame.K_7:
                    tamagotchi_game()
                if event.key == pygame.K_8:
                    graphing_app()
                if event.key == pygame.K_9:
                    simple_text_app()
                if event.key == pygame.K_n:
                        nonogram_app()
                if event.key == pygame.K_q:
                    running = False
# Run the main menu
if __name__ == "__main__":
    main_menu()
