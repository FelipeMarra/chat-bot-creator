import random

ALPHA = 0.05
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

#WSJ_24.pos é o dataset de treino
testing_file = open("WSJ_24.pos", 'r')
testing_file_lines = testing_file.readlines()

#Criando dataset com erros
arquivo = open('WSJ_24_w_error.pos', 'w')
arquivo.close()

#Até chegar no final do arquivo faça:
for line in testing_file_lines:
    new_line = ""
    reached_space = False

    #Até chegar em um espaço faça:
    for char in line:
        if char.isspace():
            reached_space = True
        #Se chegar no espaço ou não for uma letra
        if reached_space or not (char in ALPHABET_W_UPER):
            new_line = f"{new_line}{char}"
        else:
        #Para cada caractere aplicar uma probabilidade de alpha % 
        #de mudar para uma letra aleatória
            new_char = apply_random_chage(char)
            new_line = f"{new_line}{new_char}"
    #Escrever nova linha novo arquivo de testes
    append_line(new_line)