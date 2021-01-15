consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'z']


def split_text(text):
    text = text.rstrip()
    text = text.replace(',', '')
    words_list = text.split(' ')
    syllables = []
    for word in words_list:
        syllables += split_word(word)
    return syllables


def split_word(word):
    word_length = len(word)
    if is_exception(word, word_length):
        return [word]
    syllable = ''
    syllables = []
    contains_vowel = False
    for letter_pos in range(word_length):
        letter = word[letter_pos]
        if letter in consonants:
            syllable += letter
            if next_position_within_range(word_length, letter_pos) and \
                    neighbouring_consonants(word, letter_pos):
                if contains_vowel:
                    syllables.append(syllable)
                    contains_vowel = False
                    syllable = ''
        elif contains_vowel:
            syllables.append(syllable)
            syllable = letter
        elif not contains_vowel:
            syllable += letter
            contains_vowel = True
        if not next_position_within_range(word_length, letter_pos):
            if not contains_vowel:
                add_to_last(syllables, syllable)
            else:
                syllables.append(syllable)
    return syllables


def add_to_last(syllables, syllable):
    if len(syllables) == 0:
        syllables.append(syllable)
    else:
        syllables[-1] += syllable


def neighbouring_consonants(word, position):
    return word[position + 1] in consonants


def next_position_within_range(word_length, position):
    return position < word_length - 1


def is_exception(word, word_length):
    return is_three_letter_word(word_length) or is_four_letter_word_ending_with_e(word, word_length)


def is_three_letter_word(word_length):
    return word_length <= 3


def is_four_letter_word_ending_with_e(word, word_length):
    return word_length == 4 and word[-1] == 'e'
