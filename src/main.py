import random
import time
import os

def read_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        buffer_size = int(lines[0])
        matrix_size = tuple(map(int, lines[1].split()))
        matrix = []
        for i in range(matrix_size[1]):
            matrix.append(lines[i+2].split())
        number_of_sequences = int(lines[2+matrix_size[1]])
        sequences = []
        rewards = []
        for i in range(3+matrix_size[1], len(lines), 2):
            sequences.append((lines[i].replace(" ", "")).rstrip())
            rewards.append(int(lines[i+1]))
    return buffer_size, matrix_size, matrix, number_of_sequences, sequences, rewards

def generate():
    unique_token_number = int(input("Input number of unique token: "))
    tokens = list(map(str, input("Input unique token(s): ").split()))
    buffer_size = int(input("Input buffer size: "))
    matrix_size = tuple(map(int, input("Input matrix size (col row): ").split()))
    number_of_sequences = int(input("Input number of sequence: "))
    max_sequence_size = int(input("Input maximum size of sequence: "))

    matrix = [[None for j in range (matrix_size[0])] for i in range(matrix_size[1])]
    for i in range(matrix_size[1]):
        for j in range(matrix_size[0]):
            matrix[i][j] = random.choice(tokens)
    
    rewards = []
    sequences = []

    for i in range(number_of_sequences):
        length = random.randint(2, max_sequence_size)
        sequence = ''
        for j in range(length):
            sequence = sequence+random.choice(tokens)
        sequences.append(sequence)
        rewards.append(random.randint(0,100))

    return buffer_size, matrix_size, matrix, number_of_sequences, sequences, rewards

def generate_path(current_buffer, index, current_path, current_coor, passed, buffer_size, paths, matrix_size, matrix, coordinate):
    if(current_buffer == buffer_size) or (all_sequence(sequences, current_path) == True):
        paths.append(current_path)
        coordinate.append(current_coor)
        return None
    if (current_buffer == 0):
        for j in range(matrix_size[0]):
            generate_path(1, j, matrix[0][j], current_coor+([j+1, 1]), [[j, 0]], buffer_size, paths, matrix_size, matrix, coordinate)
    elif(current_buffer % 2 == 1):
        for i in range(matrix_size[1]):
            seen = False
            for coordinates in passed:
                if coordinates[0] == index and coordinates[1] == i:
                    seen = True
                    break
            if (seen == True):
                continue
            passed.append([index, i])
            generate_path(current_buffer+1, i, current_path+matrix[i][index], current_coor+([index+1, i+1]), passed, buffer_size, paths, matrix_size, matrix, coordinate)
            passed.pop()
    else:
        for j in range(matrix_size[0]):
            seen = False
            for coordinates in passed:
                if coordinates[1] == index and coordinates[0] == j:
                    seen = True
                    break
            if (seen == True):
                continue
            passed.append([j, index])
            generate_path(current_buffer+1, j, current_path+matrix[index][j], current_coor+([j+1, index+1]), passed, buffer_size, paths, matrix_size, matrix, coordinate)
            passed.pop()
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
    max_index = 0
    for i in range(len(maxreward)):
        if maxreward[i] > max_num:
            max_num = maxreward[i]
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

def save_solution(file_name, max_reward, max_sequence, max_coordinates, execution_time):
    with open(file_name, 'w') as file:
        if (max_num == 0):
            file.write("Tidak ada solusi."+'\n') 
            file.write(str(max_reward)+'\n')
            file.write("\n")
            file.write(execution_time+" ms")
        else:
            file.write(str(max_reward))
            file.write("\n")
            for i in range(len(max_sequence)):
                if i == len(max_sequence) - 1:
                    file.write(max_sequence[i])
                else:
                    if i % 2 == 1:
                        file.write(max_sequence[i]+' ')
                    else:
                        file.write(max_sequence[i])
            file.write("\n")
            for i in range(len(max_coordinates)):
                if i % 2 == 0:
                    file.write(str(max_coordinates[i])+', ')
                else:
                    file.write(str(max_coordinates[i]))
                    file.write("\n")
            file.write("\n")
            file.write(execution_time+" ms")

#main program
print("Cyberpunk 2077 Breach Protocol Solution")
print("=======================================")
print("1. Input Text File")
print("2. Generate Matrix and Sequence")
print("3. Exit")
print("=======================================")
choice = int(input("Choice: "))
print("=======================================")
stop_program = False
while(1 <= choice <= 3 and stop_program == False):
    if (1 <= choice <= 2):
        if (choice == 1):
            file_name = input("Enter the file name with the game matrix: ")
            relative_path = "test/"+file_name
            while not os.path.isfile(relative_path):
                file_name = input("File not found, reenter your file name: ")
                relative_path = "test/"+file_name
            buffer_size, matrix_size, matrix, number_of_sequences, sequences, rewards = read_file(relative_path)
        else:
            buffer_size, matrix_size, matrix, number_of_sequences, sequences, rewards = generate()
            print("=======================================")
            for i in range(matrix_size[1]):
                for j in range(matrix_size[0]):
                    if (j == matrix_size[0]-1):
                        print(matrix[i][j], end='\n')
                    else:
                        print(matrix[i][j], end=' ')

            for j in range(len(sequences)):
                sequence = sequences[j]
                for i in range(len(sequence)):
                    if i == len(sequence) - 1:
                        print(sequence[i])
                        print(str(rewards[j])+"\n")
                    else:
                        if i % 2 == 1:
                            print(sequence[i], end=' ')
                        else:
                            print(sequence[i], end='')   

        start_time = time.time()
        paths, coordinate = generate_path(0, 0, [], [], [], buffer_size, [], matrix_size, matrix, [])
        max_reward = find_sequence(sequences, paths)
        max_num, path, coor = (find_optimal(max_reward, paths))
        path, coor = optimize(path, sequences, max_num, coor)
        print("=======================================")
        if (max_num == 0):
            print("Tidak ada solusi.")
        print(max_num)
        for i in range(len(path)):
            if i == len(path) - 1:
                print(path[i])
            else:
                if i % 2 == 1:
                    print(path[i]+' ', end='')
                else:
                    print(path[i], end='')
        for i in range(len(coor)):
            if i % 2 == 0:
                print(str(coor[i])+', ', end='')
            else:
                print(str(coor[i]), end='\n')
        end_time = time.time()
        print("\n")
        print((end_time-start_time)*1000, "ms\n")
        save_file = input("Do you want to save this solution? (y/n): ")
        if(save_file == 'y'):
            file_name_save = input("Input file name: ")
            relative_path_save = "test/"+file_name_save
            while os.path.isfile(relative_path_save):
                file_name_save = input("File name is taken, reenter your file name: ")
                relative_path_save = "test/"+file_name_save
            save_solution(relative_path_save, max_num, path, coor, str((end_time-start_time)*1000))
            print("Your file has been saved!")
        print("Cyberpunk 2077 Breach Protocol Solution")
        print("=======================================")
        print("1. Input Text File")
        print("2. Generate Matrix and Sequence")
        print("3. Exit")
        print("=======================================")
        choice = int(input("Choice: "))
        print("=======================================")
    else:
        print("=======================================")
        print("             Thank You!                ")
        print("=======================================")
        print("         Shazya Audrea Taufik          ")
        print("               13522063                ")
        print("=======================================")
        stop_program = True