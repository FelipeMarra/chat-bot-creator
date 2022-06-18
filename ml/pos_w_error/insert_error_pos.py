import random

ALPHA = 0.05
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_W_UPER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

TEST_FILE = "./data/test.words"
TEST_FILE_W_ERROR = f"./data/test.words.{ALPHA*100}_error"

def append_line(new_line):
    with open(TEST_FILE_W_ERROR, 'r') as file:
        content = file.readlines()
        content.append(new_line)

    with open(TEST_FILE_W_ERROR, 'w') as file:
        file = file.writelines(content)

def apply_random_chage(char):
    selected_char = char
    prob = random.randint(0, 100)

    if prob > (1-ALPHA) * 100:
        index = random.randint(0, 25)
        selected_char = ALPHABET[index]

    return selected_char

#pegando o dataset de teste
testing_file = open(TEST_FILE, 'r')
testing_file_lines = testing_file.readlines()

#Criando dataset com erros
arquivo = open(TEST_FILE_W_ERROR, 'w')
arquivo.close()

#Até chegar no final do arquivo faça:
for line in testing_file_lines:
    new_line = ""

    #Até chegar em um espaço faça:
    for char in line:
        #Se não for uma letra
        if not (char in ALPHABET_W_UPER):
            new_line = f"{new_line}{char}"
        else:
        #Para cada letra aplicar uma probabilidade de alpha % 
        #de mudar para uma letra aleatória
            new_char = apply_random_chage(char)
            new_line = f"{new_line}{new_char}"
    #Escrever nova linha novo arquivo de testes
    append_line(new_line)