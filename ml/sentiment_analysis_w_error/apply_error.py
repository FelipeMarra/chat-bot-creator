import random

ALPHA = 1
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_W_UPER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def append_line(new_line):
    with open('WSJ_24_w_error.pos', 'r') as file:
        content = file.readlines()
        content.append(new_line)

    with open(f'WSJ_24_{ALPHA*100}_error.pos', 'w') as file:
        file = file.writelines(content)

def apply_random_chage(char):
    selected_char = char
    prob = random.randint(0, 100)

    if prob > (1-ALPHA) * 100:
        index = random.randint(0, 25)
        selected_char = ALPHABET[index]

    return selected_char

def apply_error(line:str):
        new_line = ""

        for char in line:
            #Se nao for letra nao faça nada
            if not (char in ALPHABET_W_UPER):
                new_line = f"{new_line}{char}"
            else:
            #Para cada caractere aplicar uma probabilidade de alpha % 
            #de mudar para uma letra aleatória
                new_char = apply_random_chage(char)
                new_line = f"{new_line}{new_char}"
        return new_line