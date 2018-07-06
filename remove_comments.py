import os

def clean_python_file(filename):
    if os.path.exists(filename) == False:
        return -1

    file = open(filename, 'r')
    filelines = file.readlines()
    first_clean = []

    for line in filelines:
        j = 0
        while j < len(line) and (line[j] == '\t' or line[j] == ' '):
            j += 1
        if line[j] != '#':
            first_clean.append(line)
    file.close()

    file = open(filename, 'w')
    for line in first_clean:
        file.write(line)
    file.close()

    file = open(filename, 'r')
    content = file.read()

    i = 0
    result = []
    while i < len(content):
        if content[i:i+3] == "'''":
            i += 3
            while i < len(content) and content[i:i+3] != "'''":
                i += 1
            i += 3
            continue
        result.append(content[i])
        i += 1
    file.close()

    result = ''.join(result)
    file = open(filename, 'w')
    file.write(result)
    file.close()