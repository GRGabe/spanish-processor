"""
Vowels
a á e é i í o ó u ú ü w y

Strong vowels
a á e é í o ó ú

weak vowels
i u ü w y


p t c b k d g f  can be followed by l r 

ch
"""

"""
Go back to vowel
	If weak vowel, see if proceeder is strong vowel
		If strong, include go to 1 
		If consonant, include go to 3
		If weak, stop
	1: If strong vowel, see if proceeder is weak vowel
		If weak vowel, include go to 2
		If consonant, include go to 3
		If strong vowel, stop
	2: If proceeder is vowel, stop
		If proceeder is consontnat, include go to 3 
	3: If proceeder is consonant, include
		If consonant is liquid, continue
			If proceeder is is preliq include then stop
 			else stop
		If consonant is h, continue
			If proceeder is 'h' include then stop
			else stop
		If consonant is not, stop
"""

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


def syl_pos(word):
    """
    This method finds the position of the first letter of the last syllable in the word.
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
    else:
        return pos
    #Case escape error.
    return 10


def syllabize(word):
    syllables = []
    while (word):
        i = syl_pos(word)
        syllables.insert(0, word[-1-i:])
        word = word[:-1-i]
    return syllables

word = input("Enter a Spanish word: ")
while word != 'q':
    print(syllabize(word))
    word = input("Enter a Spanish word (enter 'q' to quit): ")

"""
print(syl_pos("a"),0)
print(syl_pos("s"),0)
print(syl_pos("sht"),2)
print(syl_pos("au"),2)
print(syl_pos("it"))
print(syl_pos("i"),0)
print(syl_pos("ai"),1)
print(syl_pos("ia"),1)
print(syl_pos("ii"),1)
print(syl_pos("aa"),0)
print(syl_pos("iii"),1)
print(syl_pos("iia"),1)
print(syl_pos("iai"),2)
print(syl_pos("iaa"),0)
print(syl_pos("aii"),0)
print(syl_pos("aia"),1)
print(syl_pos("aai"),1)
print(syl_pos("aaa"),0)
print(syl_pos("iiii"),1)
print(syl_pos("iiia"),1)
print(syl_pos("iiai"),2)
print(syl_pos("iiaa"),0)
print(syl_pos("iaii"),0)
print(syl_pos("iaia"),1)
print(syl_pos("iaai"),1)
print(syl_pos("iaaa"),0)
print(syl_pos("aiii"),1)
print(syl_pos("aiia"),1)
print(syl_pos("aiai"),1)
print(syl_pos("aiaa"),0)
print(syl_pos("aaii"),0)
print(syl_pos("aaia"),1)
print(syl_pos("aaai"),1)
print(syl_pos("aaaa"),0)
print(syl_pos("ra"),1)
print(syl_pos("rs"),1)
print(syl_pos("rsht"),3)
print(syl_pos("rau"),2)
print(syl_pos("rit"),2)
print(syl_pos("ri"),1)
print(syl_pos("rai"),2)
print(syl_pos("ria"),2)
print(syl_pos("rii"),2)
print(syl_pos("raa"),0)
print(syl_pos("enchilada"),1)
print(syl_pos("ciudad"),2)
print(syl_pos("creer"),1)
print(syl_pos("bichón"),3)
print(syl_pos("ria"),2)
print(syl_pos("rii"),2)
print(syl_pos("raa"),0)
"""




"""
word = "caotiadaot"
syllables = []
count = 0
while (word):
    while (count < len(word)-1) and not is_vowel(word[-1-count]):
        count += 1
    if count < len(word)-1:
        if is_weak_vowel(word[-1-count]):
            if not is_weak_vowel(word[-2-count]):
                count += 1
                if count < len(word)-1:
                    if is_strong_vowel(word[-1-count]):
                        count += 1
                        pass
                        #weak proceeded by strong
                    else:
                        pass
                        #consonant
        elif is_strong_vowel(word[-1-count]):  
            if not is_strong_vowel(word[-2-count]):
                count += 1
                if count < len(word)-1:
                    if is_weak_vowel(word[-1-count]):
                        pass
                        #strong proceeded by weak
                    else:
                        pass
                        #consonant
        else: 
            print('error')
    print(word[-1-count])
    syllables.insert(0,word[-1-count:])
    word = word[:-1-count]
    count = 0
print(syllables)
"""