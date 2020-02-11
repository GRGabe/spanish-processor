def conj(word):
    if word[-2:] == 'ar':
        print('This is an -ar verb')
        print(word)
        root = word[:-2]
        print(' ',root+'o',root+'amos')
        print(' ',root+'as',root+'áis')
        print(' ',root+'a',root+'an')
    elif word[-2:] == 'er':
        print('This is an -er verb')
        print(word)
        root = word[:-2]
        print(' ',root+'o',root+'emos')
        print(' ',root+'es',root+'éis')
        print(' ',root+'e',root+'en')
    elif word[-2:] == 'ir':
        print('This is an -ir verb')
        print(word)
        root = word[:-2]
        print(' ',root+'o',root+'imos')
        print(' ',root+'es',root+'ís')
        print(' ',root+'e',root+'en')
    else:
        print('This is not an infinitive verb.')

def is_vowel(ch):
    if ch in 'aeiou':
        return true
    return false

def syl(word):
    syl = []
    s = '' 
    while (word):
        s = word[-1]
        while (s):
       


verb = input("Enter a verb in the infinitive. ")
while (verb != 'q'):
    conj(verb)
    verb = input("Enter an infinitive verb. Enter 'q' to quit. ")