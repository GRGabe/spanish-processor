def is_vowel(ch):
    if ch in "aáeéiíoóuúüwy":
        return True
    return False

def is_strong(ch):
    if ch in "aáeéíoóú":
        return True
    return False

def is_weak(ch):
    if ch in "iuüwy":
        return True
    return False

def is_liquid(ch):
    if ch in "rl":
        return True
    return False

def is_pre_liquid(ch):
    if ch in "bcdfgkpt":
        return True
    return False

def is_accent(ch):
    if ch in "áéíóú":
        return True
    return False


def syllable_position(word):
    """
    This method finds the position of the first letter of the last syllable in the word.
    Position is counted backwards from the last letter, indexed starting at 0.
    This method assumes that the word given is a correctly spelled Spanish word in lowercase letters which is not a loanword. 
    In practice this will be used iteratively while removing the previous last syllable.

    For describing the phonotactics of Spanish we will use:
        lowercase letters to stand for exactly one letter
        uppercase letters to stand for one or more letters
        v,V to stand for vowels
        c,C to stand for consonants
        s   to stand for strong vowels (a, á, e, é, í, o, ó, ú)
        w   to stand for weak vowels (i, u, ü, w, y)
        f,F to stand for final consonants (in reality only d, n, s, r, 
        l   to stand for liquid consonants (l, r) 
        p   to stand for letters that can be before liquids in the same syllable (b, c, d, f, g, k, p, t)
        x   to stand for exactly one unknown letter
        X   to stand for any number of letters (including 0 letters) that are unknown
        '   to mark breaks in syllables
	From the point of view of pronunciation the following pairs of letters count as a single consonant: ('ch', 'll', 'qu', 'rr')

    Syllables in Spanish are of the form (C)V(C), or more specifically (C)V(F)
    The final, F, can be a single consonant or a consonant and an 's' (this rule is assumed to be followed and not checked)
    The inital consonant, C, can be a single consonant, c, or pl (a pre-liquid and a liquid) as listed above. 

    There are two types of vowels in Spanish: strong and weak. 
    The vowel, V, of a syllable can be of the form (w)s(w), or (w)w.
    If a weak vowel is directly between two strong vowels it is in the same syllable as the second strong vowel: sws => s'ws
    If there are three or more weak vowels in a row (such as in some onomatopoeias), they break in pairs from the end: wwwww => w'ww'ww.
    The form wsw is favored over ww, so wwsw => w'wsw and similarly wws => w'ws.
    In general maximal syllables are formed from the end with the exception of wsww => wsw'w. 
    """

    #The first step is to ignore any final consonants (denoted: F)
    final = 0
    while (final + 1 < len(word)) and not is_vowel(word[-1-final]):
        final +=1


    #If the whole word is F or vF, that is the syllable 
    if len(word) < final + 2:
        return final


    #Else XxvF. If XcvF, then the vowel is determined, determine the consonant
    elif not is_vowel(word[-2-final]):
        pos = final + 1


    #Else XvvF. If vvF, then 
    elif len(word) < final + 3:
        #If the word is vsF, then
        if is_strong(word[-1-final]):
            #If the word is ssF, then s'sF
            if is_strong(word[-2-final]):
                return final

            #Else the word is wsF, and that is the syllable
            else:
                return final + 1

        #Else the word is vwF, so either wwF or swF, which is the syllable
        else:
            return final + 1


    #Else, XxvvF. If XcvvF, then
    elif not is_vowel(word[-3-final]):
        #If XcvsF, then
        if is_strong(word[-1-final]):
            #If XcssF, then Xcs'sF
            if is_strong(word[-2-final]):
                return final

            #Else XcwsF, then the vowel is determined, determine the consonant
            else:
                pos = final + 2

        #Else XcvwF, which is either XcwwF or XcswF, then the vowel is determined, determine the consonant
        else:
            pos = final + 2


    #Else XvvvF. If XvvsF, then
    elif is_strong(word[-1-final]):
        #Else  XvwsF, then Xv'wsF
        if word[ -3-final : len(word)-final ] == "uie":
            if 3+final <= len(word):
                if word[-4-final] == "q":
                    return final + 3

        #Triple check!!!!!!!!!!
        #If XvssF, then Xvs'sF
            if is_strong(word[-2-final]):
                return final 

            ####
            else:
                return final + 1

        else:
            return final + 1


    #Else XvvwF. If XvswF, then
    elif is_strong(word[-2-final]):
        #If XsswF, then Xs'swF
        if is_strong(word[-3-final]):
            return final + 1

        #Else XwswF. If wswF, that is the syllable
        elif len(word) < final + 4:
            return final + 2

        #Else XxwswF. If XcwswF, then the vowel is determined, determine the consonant
        elif not is_vowel(word[-4-final]):
            pos = final + 3

        #Else XvwswF. If XswswF, then Xsw'swF ???????????????????????
        elif is_strong(word[-4-final]):
            return final + 1

        #Else XwwswF, so Xw'wswF
        else:
            return final + 2


    #Else XvwwF. If XswwF, then Xsw'wF.
    elif is_strong(word[-3-final]):
        return final


    #Else XwwwF, then Xw'wwF (The final vowel possibility!)
    else:
        return final + 1



    #Now determine the consonant
    #If there is only one letter, cVF, so that is the syllable
    if len(word) < pos + 2:
            return pos


    #Else XxcVF. If XplVF, then X'plVF.
    elif is_liquid(word[-1-pos]) and is_pre_liquid(word[-2-pos]):
            return pos + 1


    #Else if X"ch"VF, then X ' "ch"VF
    elif word[-2-pos:-pos] == 'ch':
            return pos + 1


    #Else if X"ll"VF, then X ' "ll"VF
    elif word[-2-pos:-pos] == 'll':
            return pos + 1


    #Else if X"rr"VF, then X ' "rr"VF
    elif word[-2-pos:-pos] == 'rr':
            return pos + 1


    #Else Xx'cVF
    return pos




def syllables(word):
    syllables = []

    while (word):
        i = syllable_position(word)
        syllables.insert(0, word[-1-i:])
        word = word[:-1-i]

    return syllables

def syllable_parts(syllable):
    initial = ''
    vowel = ''
    final = '' 
    ch = syllable[0]
    while ch and not is_vowel(ch):
        initial += ch
        syllable = syllable[1:]
        if syllable:
            ch = syllable[0]
        else:
            ch = ''
    while ch and is_vowel(ch):
        vowel += ch
        syllable = syllable[1:]
        if syllable:
            ch = syllable[0]
        else:
            ch = ''
    while ch and not is_vowel(ch):
        final += ch
        syllable = syllable[1:]
        if syllable:
            ch = syllable[0]
        else:
            ch = ''
    return (initial, vowel, final)

def find_stress(word):
    syls = syllables(word.lower())
    index = -1
    l = len(syls)
    for i in range(l):
        for ch in syls[i]:
            if is_accent(ch):
                index = i
    if index >= 0:
        return index
    final = syllable_parts(syls[-1])[2]
    if len(final) == 1 and final not in "ns":
        return l-1
    return l-2

def classify_stress_type(word):
    i = find_stress(word)
    l = len(syllables(word.lower()))
    if i == l-1:
        return "aguda"
    if i == l-2:
        return "llana"
    return "esdrújula"

def classify_stress_type_eng(word):
    i = find_stress(word)
    l = len(syllables(word.lower()))
    if i == l-1:
        return "oxytone"
    if i == l-2:
        return "paroxytone"
    return "proparoxytone"
    


if __name__ == "__main__":
    while True:
        word = input("Enter a Spanish word (enter 'q' to quit): ")
        if word == 'q':
            break
        syls = syllables(word.lower())
        i = find_stress(word)
        print("Stress on", syls[i], i)
        print(classify_stress_type(word))
        print(classify_stress_type_eng(word))
        print(syllables(syls))
        for syl in syls:
            print(syllable_parts(syl))

    