"""
JUSTIFY WORDS

Description:
-> Each line can contain no more than m characters (including space).
-> Each word should be present entirely on 1 line.
-> If multiple words are on a line, they should be seperated by a single space.

Constraints:
0 <= k <= 25
0 <= n <= 10
0 <= m <= 10
Words will be having only lowercase alphabets.

Time Limit:
1 sec

Input:
k -> number of words.
k lines of words.
n & m seperated by a space [Number of lines (n) and the maximum width of each line (m)].

Output:
Maximum number of words that can be arranged into n lines.

Example:
I/p:
8
i
hello
how
going
u
whatsapp
help
hmm
5 5

O/p:
7

Explanation:
i_how
hello
going
u_hmm
help_

_ -> represents space
7 words in total have been placed in 5 lines with maximum width of 5 characters for each line
"""

# Defines the recursive function to try placing words in different lines and maximize the word count.
# -> i      : The current index of the word being processed.
# -> n_lines: A list where each element tracks the current total length of words in a particular line.
# -> count  : The count of words successfully placed across the lines.
# -> words  : The list of words to distribute.
def justify_words(i, n_lines, count, words):
    # Declares result as a global variable to track the maximum number of words successfully placed.
    global result

    # Base case: If all words have been processed.
    if i == len(words):
        # Update the global result with the maximum of the current result and the current count.
        result = max(result, count)
        # Exit the recursion.
        return
    
    # Implements a pruning condition (backtracking):
    # If the maximum possible words we could place (count + (len(words) - i)) is less than or equal to the current result, further exploration is unnecessary.
    if count + (len(words) - i) <= result:
        # Exit the recursion.
        return

    # Loops through each line to try placing the current word (words[i]).
    for j in range(n):

        # Try placing words in empty lines
        # If the current line j is empty.
        if n_lines[j] == 0:
            # Place the word in the line by setting its length as the line's total length.
            n_lines[j] = len(words[i])
            #Recursively process the next word, incrementing the count.
            justify_words(i + 1, n_lines, count + 1, words)
            # Backtrack by resetting the line's total length to 0 after exploring this option.
            n_lines[j] = 0  
            # Break the loop to avoid placing the word in other empty lines.
            break

        # Try placing words in non-empty lines    
        # Checks if the word can fit into the current line j. The condition ensures there is enough space, including one space between words. 
        elif n_lines[j] + 1 + len(words[i]) <= m:
            # Add the word and a space to the line's total length.
            n_lines[j] += 1 + len(words[i])
            # Recursively process the next word, incrementing the count.
            justify_words(i + 1, n_lines, count + 1, words)
            # Backtrack by removing the word and space from the line after exploring this option.
            n_lines[j] -= 1 + len(words[i]) 

    # Skip the current word without placing it in any line. Recursively moves to the next word without changing the count.
    justify_words(i + 1, n_lines, count, words)

# Number of words provided in the input sequence.
k = int(input())
# Words.
words = []
for i in range(k):
    words.append(input().strip())
# Number of lines (n) and the maximum width of each line (m).
n, m = map(int, input().split())

# Filters out words that are longer than the maximum line width (m).
words = [w for w in words if len(w) <= m]

# This sorts the words list based on the custom key specified in the 'key' argument.
# A lambda function is a short, anonymous function that takes an input x (in this case, a word from the words list). It returns a tuple (-len(x), x) as the sorting key 
# for each word.
# -> -len(x) : This calculates the negative length of the word. Sorting prioritizes longer words because the negative sign reverses the natural order of integers 
# (ascending).
# -> x       : This is the word itself. In case two words have the same length, they are sorted alphabetically (ascending order) as a tie-breaker.
words.sort(key=lambda x: (-len(x), x))

# Initializes a list of size n, with each element set to 0. This represents the total length of words in each line, initially empty.
n_lines = [0] * n
# Sets the initial maximum word count to 0
result = 0

# Calls the recursive function with:
# -> 0      : Starting index for the words list.
# -> n_lines: The empty lines array.
# -> 0      : Initial count of placed words.
# -> words  : The list of words.
justify_words(0, n_lines, 0, words)

print(result, end = "")

