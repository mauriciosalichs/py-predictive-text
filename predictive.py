import pygame
import pickle
from copy import deepcopy as copy
from dictionary import *
import sys

# Initialize Pygame
pygame.init()
# Set up the display
WIDTH, HEIGHT = 1300, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Editor by MS")
font = pygame.font.Font(None, 36)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)

punctuations = get_punctuations()

# Main loop
def main():
    screen.fill(WHITE)
    rendered_text = font.render("Cargando diccionario...", True, BLACK)
    screen.blit(rendered_text, (10, 10))
    pygame.display.flip()
    screen.fill(BLACK)
    
    text = ''
    texts = []
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
                    texts.append(text)
                    text = ''
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
                    predict_mode = False
                    if text:
                        text = text[:-1]
                    elif texts:
                        text = texts.pop()
                        text = text[:-1]
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
        i = 0
        for t in texts:
            rendered_text = font.render(t, True, WHITE)
            screen.blit(rendered_text, (10, i*30+10))
            i += 1
        rendered_text = font.render(text, True, WHITE)
        rendered_ptext = font.render(ptext, True, GREY)
        text_width, _ = rendered_text.get_size()
        pred_width, _ = rendered_ptext.get_size()
        
        if text_width+pred_width >= WIDTH - 20: # Text too wide
            last_word = text.split()[-1]  # Split the text into words
            texts.append(text[:-len(last_word)])
            text = last_word
            continue
        screen.blit(rendered_text, (10, i*30+10))
        screen.blit(rendered_ptext, (10+text_width, i*30+10))

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