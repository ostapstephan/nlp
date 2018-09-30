import os
dictionary= {}
with open('Frequency_Dictionary.txt', 'r', encoding='iso-8859-1') as f:
    for line in f:
        word = line.split()[0]
        dictionary[word] = int(line.split()[1])


n = sum(dictionary.values())

print(n)
print(len(dictionary))

