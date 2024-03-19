import pygame
import pickle
from copy import deepcopy as copy
from dictionary import get_dictionary, process_word
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Text Editor")

# Colors
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)

# Vars
font = pygame.font.Font(None, 36)

def calculate_predictive(actual_char, letter):
    ptext = ''
    if letter not in actual_char.maps:
        return (actual_char,'',False)
    next_char = actual_char.maps[letter][1]
    iter_char = copy(next_char)
    while iter_char and iter_char.maps:
        next_letter = iter_char.next_favorite
        if next_letter == '': break
        ptext += next_letter
        iter_char = iter_char.maps[next_letter][1]

    return (next_char,ptext,True)

# Main loop
def main():
    text = ''
    clock = pygame.time.Clock()
    dictionary = get_dictionary()
    
    actual_char = dictionary
    running = True
    ptext = ''
    word = ''
    print("Dictionary was loaded")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    text += '\n'
                elif event.key == pygame.K_BACKSPACE:
                    continue
                    #actual_char,ptext = (dictionary, '')
                    #text = text[:-1]
                else:
                    cont = True
                    if event.unicode == ' ':
                        dictionary = process_word(dictionary, word.lower())
                        word = ''
                        actual_char,ptext = (dictionary, '')
                    else:
                        actual_char,ptext,cont = calculate_predictive(actual_char, event.unicode.lower())
                    if cont:
                        word+=event.unicode
                        text += event.unicode

        # Clear the screen
        screen.fill(BLACK)

        # Render the text
        rendered_text = font.render(text, True, WHITE)
        rendered_ptext = font.render(ptext, True, GREY)
        text_width, text_height = rendered_text.get_size()
        
        screen.blit(rendered_text, (10, 10))
        screen.blit(rendered_ptext, (10+text_width, 10))

        # Update the display
        pygame.display.flip()
        clock.tick(30)

    with open("dictionary.pkl", 'wb') as file:
        pickle.dump(dictionary, file)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()