import random
import time
def read_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        buffer_size = int(lines[0])
        matrix_size = tuple(map(int, lines[1].split()))
        matrix = []
        for i in range(matrix_size[0]):
            matrix.append(lines[i+2].split())
        number_of_sequences = int(lines[2+matrix_size[0]])
        sequences = []
        rewards = []
        for i in range(3+matrix_size[0], len(lines), 2):
            sequences.append((lines[i].replace(" ", "")).rstrip())
            rewards.append(int(lines[i+1]))
    return buffer_size, matrix_size, matrix, number_of_sequences, sequences, rewards

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
    
    rewards = []
    sequences = []

    for i in range(sequence_number):
        length = random.randint(2, max_sequence_size)
        sequence = ''
        for j in range(length):
            sequence = sequence+random.choice(tokens)
        sequences.append(sequence)
        rewards.append(random.randint(0,100))

    return buffer_size, matrix_size, matrix, sequence_number, sequences, rewards

def generate_path(current_buffer, index, currentPath, currentCoor, seenPath, buffer_size, paths, matrix_size, matrix, coordinate):
    if(current_buffer == buffer_size) or (all_sequence(sequences, currentPath) == True):
        paths.append(currentPath)
        coordinate.append(currentCoor)
        return None
    if (current_buffer == 0):
        for j in range(matrix_size[1]):
            generate_path(1, j, matrix[0][j], currentCoor+([1,j+1]), [[j, 0]], buffer_size, paths, matrix_size, matrix, coordinate)
    elif(current_buffer % 2 == 1):
        for i in range(matrix_size[0]):
            seen = False
            for coordinates in seenPath:
                if coordinates[0] == index and coordinates[1] == i:
                    seen = True
                    break
            if (seen == True):
                continue
            seenPath.append([index, i])
            generate_path(current_buffer+1, i, currentPath+matrix[i][index], currentCoor+([index+1, i+1]), seenPath, buffer_size, paths, matrix_size, matrix, coordinate)
            seenPath.pop()
    else:
        for j in range(matrix_size[1]):
            seen = False
            for coordinates in seenPath:
                if coordinates[1] == index and coordinates[0] == j:
                    seen = True
                    break
            if (seen == True):
                continue
            seenPath.append([j, index])
            generate_path(current_buffer+1, j, currentPath+matrix[index][j], currentCoor+([j+1, index+1]), seenPath, buffer_size, paths, matrix_size, matrix, coordinate)
            seenPath.pop()
    return paths, coordinate

def all_sequence(sequences, path):
    foundAll = 0
    for sequence in sequences:
        if sequence in path:
            foundAll += 1
    if foundAll == len(sequences):
        return True
    else:
        return False

def find_sequence(sequences, paths):
    maxreward = []
    for path in paths:
        reward = 0
        for i in range(len(sequences)):
            occur = path.count(sequences[i])
            if occur >= 1:
                reward += rewards[i]
        maxreward.append(reward)
    return maxreward

def find_optimal(maxreward, paths):
    max_num = maxreward[0]
    max_index = -1
    for i, num in enumerate(maxreward):
        if num > max_num:
            max_num = num
            max_index = i
    if max_num == 0:
        paths[max_index] = ''
        coordinate[max_index] = ''
    return max_num, paths[max_index], coordinate[max_index]

def max_length_sequence(sequences):
    maxlen = -1
    for sequence in sequences:
        if(len(sequence) > maxlen):
            maxlen = len(sequence)
    return maxlen

def optimize(path, sequences, initreward, coor):
    if (len(path) >= max_length_sequence(sequences)+2):
        temp = path[:-2]
        tempcoor = coor[:-2]
        reward = 0
        for i in range(len(sequences)):
            occur = temp.count(sequences[i])
            if occur >= 1:
                reward += rewards[i]
        if reward == initreward:
            path = temp
            coor = tempcoor
        else:
            return path, coor
        while(reward == initreward):
            temp = path[:-2]
            reward = 0
            for i in range(len(sequences)):
                occur = temp.count(sequences[i])
                if occur >= 1:
                    reward += rewards[i]
            if reward == initreward:
                path = temp
                coor = tempcoor
            else:
                return path, coor
    else:
        return path, coor

def save_solution(file_name, max_reward, max_sequence, max_buffer, max_coordinates, execution_time):
    with open(file_name, 'w') as file:
        file.write(f'Max reward: {max_reward}\n')
        file.write(f'Max sequence: {max_sequence}\n')
        file.write(f'Max buffer: {max_buffer}\n')
        file.write(f'Max coordinates: {max_coordinates}\n')
        file.write(f'Execution time: {execution_time} ms\n')


start_time = time.time()
file_name = input('Enter the file name with the game matrix (or press enter to generate one): ')
if file_name:
    buffer_size, matrix_size, matrix, number_of_sequences, sequences, rewards = read_file(file_name)
else:
    buffer_size, matrix_size, matrix, number_of_sequences, sequences, rewards = generate()
    print(matrix)
    print(sequences)
paths, coordinate = generate_path(0, 0, [], [], [], buffer_size, [], matrix_size, matrix, [])
maxreward = find_sequence(sequences, paths)
max_num, path, coor = (find_optimal(maxreward, paths))
path, coor = optimize(path, sequences, max_num, coor)
print(path, coor)
end_time = time.time()
print(end_time-start_time, "s")