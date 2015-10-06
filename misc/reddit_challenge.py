# Reddit coding challenge:
# Write a function that returns a word and whether or not the letters are in alphabetical order

letters = list('abcdefghijklmnopqrstuvwxyz')
numbers = range(0, len(letters))
letter_nums = dict(zip(letters, numbers))

def is_alphabetical(word):
    values = [letter_nums.get(val) for val in list(word)]
    test = sorted(values)==values
    return word, test

is_alphabetical('word')
is_alphabetical('almost')
is_alphabetical('boost')
is_alphabetical('moon')

