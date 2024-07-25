import pygame
import sys
import os
import time
import serial

# Initialize Pygame
pygame.init()

# Audio Initialization
pygame.mixer.init()
audio_dir = 'audio'

# Screen settings
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Keyboard Input Display")


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font settings
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 36)

# Input text
input_text = ''
word_trigger = False
choose_side = True

# Configure Serial Connection
ser = serial.Serial('COM4', 115200)  # Adjust the COM port as necessary

def get_side():
    while ser.in_waiting == 0:
        pass
    command = ser.readline().decode('utf-8').strip()
    print('get side: ' + command)
    return command

def draw_buttons():
    # Draw button A
    pygame.draw.rect(screen, GRAY, (150, 300, 150, 50))
    text_surface_a = button_font.render("Craft", True, BLACK)
    screen.blit(text_surface_a, (160, 310))
    
    # Draw button B
    pygame.draw.rect(screen, GRAY, (350, 300, 150, 50))
    text_surface_b = button_font.render("Automation", True, BLACK)
    screen.blit(text_surface_b, (360, 310))

def response_func(history):
    global weight
    global level
    sum = 0
    
    # get current action
    offering = history[-1][0]
    print(offering)
    side = history[-1][1]
    print(side)
    # calculate extreme weighting
    previous_word = None
    for i in range(len(history)):
        sel = history[i][1]
        scale = 1
        if sel == previous_word: 
            scale = 2
        if sel == 'A':
            sum = sum + scale
        else:
            sum = sum - scale
        previous_word = sel
    weight = sum
    print(sum)

    # level evaluation
    if sum < -1:
        level = -1
    elif sum < 2:
        level = 0
    else:
        level = 1

    # decide the audio file
    audio_file = offering + '_' + str(side) + '_'+ str(level) + '.wav'
    print(audio_file)
    play_sound(audio_file)


def play_sound(audio_file):
    global audio_dir
    try:
        sound_file = os.path.join(audio_dir, audio_file)
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Could not load sound file: {e}")
    
    # Wait until the music is done playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Wait for 10 ms to reduce CPU usage

# Waiting for Game to start
command = get_side()

# Game Intro
play_sound('intro.mp3')

# Main Gamme Loop
history = []
# Trigger words
words = ["COIN", "TIME", "LOVE", "TASK"]
trigger_words = ["COIN", "TIME", "LOVE", "TASK"]
trigger_words_len = len(words)
weight = 0
level = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                input_text = input_text.upper()
                if input_text in trigger_words:
                    if input_text == "COIN":
                        word_trigger = True
                        choose_side = False
                    elif input_text == "TIME":
                        word_trigger = True
                        choose_side = False
                    elif input_text == "LOVE":
                        word_trigger = True
                        choose_side = False
                    elif input_text == "TASK":
                        word_trigger = True
                        choose_side = False
                    else:
                        pass
                    trigger_words.remove(input_text)
                else:
                    ## try again audio
                    input_text = ''
                    word_trigger = False
                    choose_side = True
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                running = False
            else:
                input_text += event.unicode

        ## COMMENT THIS BELOW IF REPLACE THE SIDE SELECTION WITH PYSICAL BUTTON
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if word_trigger and not choose_side:
        #         x, y = event.pos
        #         if 150 <= x <= 300 and 300 <= y <= 350:
        #             print("Left button clicked!")
        #             history.append((input_text, 'C'))
        #         elif 350 <= x <= 500 and 300 <= y <= 350:
        #             print("Right button clicked!")
        #             history.append((input_text, 'A'))
        #         else:
        #             break
        #         choose_side = True
        ######
    
    # Clear screen
    screen.fill(BLACK)
    
    # Render text
    text_surface = font.render(input_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(text_surface, text_rect)
    # Show buttons if 'coin' is entered
    if word_trigger:
        # play audio
        
        command = get_side()
        history.append((input_text, command))

        ##### commment out
        # draw_buttons()
        # if choose_side:
        ##### comment

        print(history)
        # call response function
        response_func(history)

        if(len(history)!=trigger_words_len):
            # reset the display and state variables
            word_trigger = False
            input_text = ''
        else:
            running = False # game over
    
    # Update display
    pygame.display.flip()

screen.fill(BLACK)
pygame.display.flip()

# Ending
if level == -1:
    # extreme C
    play_sound('ending_extremeC.wav')
elif level == 0:
    # moderate C
    play_sound('ending_moderate.wav')
else: 
    # extreme A
    play_sound('ending_extremeA.wav')
time.sleep(5)

# Quit Pygame
pygame.quit()
sys.exit()
