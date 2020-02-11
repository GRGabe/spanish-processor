import syllables as s

def conjugate_haber(tense,person,number):
    if tense == 1:
        if person == 1:
            return (number == 1 ? 'he' : 'hemos')
        elif person == 2 and number != 1:
            return 'habéis'
        else:
            return conjugate('har',tense,person,number)
    if tense == 2:
        return conjugate('habir',tense,person,number)
    elif tense == 3 or tense == 7:
        return conjugate('hubir',tense,person,number)
    return "haber !!!!" 

def conjugate(verb,tense,person,number):
    t = verb[-2]
    type = "aei".index(t)

    stem = verb[:-2]

    if tense > 7:
        return conjugate_haber(tense-7, person, number) + ' ' + stem + 'aii'[type] + 'do'

    std_ending = ''
    if person == 1 and number != 1:
        std_ending = 'mos'
    if person == 2:
        if number == 1:
            std_ending = 's'
        else:
            std_ending = 'is'
    if person == 3 and number != 1:
        std_ending = 'n'

    if tense == 2:
        if type == 0:
            if number == 2 and  person == 1:
                return stem + 'ábamos' 
            return stem + 'aba' + std_ending
        else:
            return stem + 'ía' + std_ending

    if tense == 5:
        return verb + 'ía' + std_ending

    if tense == 7:
        if type == 0:
            if number == 2 and person == 1:
                return stem + 'áramos / ' + stem + 'ásemos'
            return verb + 'ra' + std_ending + ' / ' + stem + 'ase' + std_ending
        else:
            if number == 2 and person ==1:
                return stem + 'iéramos / ' + stem + 'iésemos'
            return stem + 'iera' + std_ending + ' / ' + stem + 'iese' + std_ending
    return 'not yet included'

if __name__ == "__main__":
    while True:
        verb = input("Enter a Spanish infinitive verb (enter 'q' to quit): ")
        if verb == 'q':
            break
        tense = int(input("Enter tense number: "))
        person = int(input("Enter person (1 for first, etc.): "))
        number = int(input("Enter number (1 for singular, 2 for plural): "))
        print(conjugate(verb,tense,person,number))


"""
    if person == 1:
        if number == 1:
            std_ending = 'o'
        else:
            std_ending = t + 'mos'
    elif person == 2:
        if number == 1:
            if type == 0:
                std_ending = 'as'
            else:
                std_ending = 'es'
        else:
            if type == 0:
                std_ending = 'áis'
            elif type == 1:
                std_ending = 'éis'
            else:
                std_ending = 'ís'
    elif person == 3:
        if number == 1:
            if type == 0:
                std_ending = 'a'
            else:
                std_ending = 'e'
        else:
            if type == 0:
                std_ending = 'an'
            else:
                std_ending = 'en'
"""

