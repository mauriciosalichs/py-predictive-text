import pygame
import pickle
from copy import deepcopy as copy
from dictionary import *
import sys

# Initialize Pygame
pygame.init()
# Set up the display
WIDTH, HEIGHT = 1500, 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Text Editor")
font = pygame.font.Font(None, 36)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)

punctuations = get_punctuations()

# Main loop
def main():
    text = ''
    clock = pygame.time.Clock()
    dictionary = get_dictionary()
    predict_mode = True
    
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
                elif event.key == pygame.K_LSHIFT:
                    continue
                elif event.key == pygame.K_TAB and predict_mode:
                    text+=ptext+' '
                    word+=ptext
                    dictionary = process_word(dictionary, word.lower())
                    actual_char,ptext,word = (dictionary, '', '')
                elif event.key == pygame.K_BACKSPACE:
                    #if text[-1].isalpha(): actual_char,ptext,_ = calculate_predictive_word(dictionary, word[:-1])
                    ptext = ''
                    text = text[:-1]
                    predict_mode = False
                else:
                    cont = True
                    if event.unicode in punctuations:
                        if predict_mode:
                            dictionary = process_word(dictionary, word.lower())
                        actual_char,ptext,word = (dictionary, '', '')
                        predict_mode = True
                    elif predict_mode:
                        actual_char,ptext,cont = calculate_predictive_letter(actual_char, event.unicode.lower())
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

    pygame.quit()
    with open("dictionary.pkl", 'wb') as file:
        pickle.dump(dictionary, file)
    print("Saved dictionary")
    sys.exit()

if __name__ == "__main__":
    main()