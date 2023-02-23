import sys

'''This script outouts the lines of the first file, which should be changed with one of the actions: add(+) or remove(-) to get the second file from it'''

def diff(file1: str, file2: str) -> None:
    print(type(file1))
    f1_lines, f2_lines = read_files(file1, file2)
    levenshtein_matrix = levenshtein(f1_lines, f2_lines)
    opt_path = get_optimal_path(levenshtein_matrix, f1_lines, f2_lines)
    print_diff(opt_path)


def levenshtein(lines_of_file1: list, lines_of_file2: list) -> list:
    matrix = [[0] * (len(lines_of_file2) + 1) for _ in range(len(lines_of_file1) + 1)]
    for i in range(len(lines_of_file1) + 1):
        matrix[i][0] = i
    for j in range(len(lines_of_file2) + 1):
        matrix[0][j] = j
    for i in range(1, len(lines_of_file2) + 1):
        for j in range(1, len(lines_of_file2) + 1):
            if lines_of_file1[i - 1] == lines_of_file2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min(matrix[i - 1][j], matrix[i][j - 1], matrix[i - 1][j - 1]) + 1
    return matrix

def read_files(path_to_file1: str, path_to_file2: str) -> tuple():
    try:
        with open(path_to_file1) as f1, open(path_to_file2) as f2:
            f1_lines = f1.readlines()
            f2_lines = f2.readlines()
            return f1_lines, f2_lines
    except FileNotFoundError:
        print('File not found!')

def get_optimal_path(matrix: list, lines_of_file1: list, lines_of_file2: list) -> list:
    path = []
    i, j = len(lines_of_file1), len(lines_of_file2)
    while i > 0 or j > 0:
        if i > 0 and j > 0 and lines_of_file1[i - 1] == lines_of_file2[j - 1]:
            path.append((' ', lines_of_file1[i - 1]))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or matrix[i][j - 1] <= matrix[i - 1][j]):
            path.append(('+', lines_of_file2[j - 1]))
            j -= 1
        elif i > 0 and (j == 0 or matrix[i][j - 1] > matrix[i - 1][j]):
            path.append(('-', lines_of_file1[i - 1]))
            i -= 1
    return path

def print_diff(opt_path: list) -> None:
    opt_path.reverse()
    for operation, line in opt_path:
        if operation != ' ':
            print(operation, line.strip())

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Incorrect number of args!')
    else:
        diff(sys.argv[1], sys.argv[2])