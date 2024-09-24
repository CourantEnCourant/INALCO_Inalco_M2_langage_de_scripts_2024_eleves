
def longest_substring(input_str: str) -> int:
    longest_count = 0
    count = 0
    letters = "abcdefghijklmnopqresuvwxyz "
    letter_used = {letter: False for letter in letters}
    current_substring_

    for letter in input_str:
        if not letter_used[letter]:
            letter_used[letter] = True
            count += 1
            if count > longest_count:
                longest_count = count
        else:
            letter_used = {letter: False for letter in letters}
            letter_used[letter] = True
            count = 1

    return longest_count



print(longest_substring("dvdf"))

