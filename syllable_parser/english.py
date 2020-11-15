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
    if word_length <= 3:
        return [word]
    syllable = ''
    syllables = []
    for letter_pos in range(word_length):
        letter = word[letter_pos]
        syllable += letter
        if letter in consonants:
            if next_position_within_range(word_length, letter_pos) and same_neighbouring_consonants(word, letter_pos):
                add_to_last(syllables, syllable)
                syllable = ''
        else:
            syllables.append(syllable)
            syllable = ''
        if not next_position_within_range(word_length, letter_pos):
            add_to_last(syllables, syllable)
    return syllables


def add_to_last(syllables, syllable):
    if len(syllables) == 0:
        syllables.append(syllable)
    else:
        syllables[-1] += syllable


def same_neighbouring_consonants(word, position):
    return word[position + 1] in consonants


def next_position_within_range(word_length, position):
    return position < word_length - 1
