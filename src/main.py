import time
import itertools
import random

def read_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        buffer_size = int(lines[0])
        matrix_size = tuple(map(int, lines[1].split()))
        matrix = []
        for i in range(matrix_size[0]):
            matrix.append(lines[i+2].split())
        number_of_sequences = int(lines[2+matrix_size[1]])
        sequences = []
        rewards = []
        for i in range(3+matrix_size[1], len(lines), 2):
            sequences.append(lines[i].split())
            rewards.append(int(lines[i+1]))
    return matrix, sequences, rewards, buffer_size

def generate():
    unique_token_number = int(input("Masukkan jumlah token unik: "))
    tokens = list(map(str, input("Masukkan token unik: ").split()))
    buffer_size = int(input("Masukkan ukuran buffer: "))
    matrix_size = tuple(map(int, input("Masukkan ukuran matriks: ").split()))
    sequence_number = int(input("Masukkan banyak sekuens: "))
    max_sequence_size = int(input("Masukkan ukuran maksimum sekuens: "))

    matrix = [[None for j in range (matrix_size[1])] for i in range(matrix_size[0])]
    for i in range(matrix_size[0]):
        for j in range(matrix_size[1]):
            matrix[i][j] = random.choice(tokens)
    
    sequences = []
    rewards = []

    for i in range(sequence_number):
        length = random.randint(2, max_sequence_size)
        sequence = []
        for j in range(length):
            sequence.append(random.choice(tokens))
        sequences.append(sequence)
        rewards.append(random.randint(0,100))

    return matrix, sequences, rewards, buffer_size

def save_solution(file_name, max_reward, max_sequence, max_buffer, max_coordinates, execution_time):
    with open(file_name, 'w') as file:
        file.write(f'Max reward: {max_reward}\n')
        file.write(f'Max sequence: {max_sequence}\n')
        file.write(f'Max buffer: {max_buffer}\n')
        file.write(f'Max coordinates: {max_coordinates}\n')
        file.write(f'Execution time: {execution_time} ms\n')

def main():
    start_time = time.time()
    file_name = input('Enter the file name with the game matrix (or press enter to generate one): ')
    if file_name:
        matrix, sequences, rewards, buffer_size = read_file(file_name)
    else:
        matrix, sequences, rewards, buffer_size = generate()
    end_time = time.time()