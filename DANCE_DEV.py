"""
DANCE DEV

Description:
-> There are 4 tiles (up, down, right, left).
-> Can move your leg 1 at a time.
-> Initially you can place your leg at any tile.
-> Instructions will contain list of tiles.
-> Find minimum number of times you must move your leg to a different tile.

Constraints:
1 <= n <= 50

Time Limit:
1 sec

Input:
n -> Total number of instructions.
n lines of instructions.

Output:
Minimum number of times you must move your leg to a different tile.

Example:
I/p:
6
down
right
down
up
right
down

O/p:
2

Explanation:
1st and 2nd position in the steps list is initialized as the initial position of the left and right leg, respectively.
left = down, right = right
Then, the 1st and 2nd positio is removed from the steps list as it has been assigned to the left and right leg, respectively.

-------------------------------------------------
Steps        left        right        no_of_steps
-------------------------------------------------
Initially    down        right         0
down         down        right         0
up           up          right         1
right        up          right         1
down         down        right         2

Thus, 2 steps are taken from the initial position
"""

# Number of steps or positions provided in the input sequence.
n = int(input())
# Steps or positions.
steps = []
for i in range(n):
	steps.append(input().strip())
     
# Initializes the 1st and 2nd position in the steps list as the initial position of the left and right leg, respectively.
left = steps[0]
right = steps[1]
# Initializes the counter for the number of leg position updates (no_of_steps) to 0.
no_of_steps = 0

# Removes the 1st and 2nd position from the steps list as it has been assigned to the left and right leg, respectively.
steps.pop(0)
steps.pop(0)

# A flag variable used to check if a valid update for leg position has been made during the inner loop.
flag = 0

# Iterates over each position in the remaining steps list with both its index (i) and value (value).
for i, value in enumerate(steps):

    # Checks if the current step (value) doesn't match the current positions of either the left leg (left) or the right leg (right).
    # no_of_steps is updated only if neither left nor right leg is in the same position as the current step (value)
    if left != value and right != value:

        # Iterates through the remaining steps (starting from the current position i) to check for a future match for either leg.
        for j, values in enumerate(steps[i:]):

            # Checks if the left leg's current position matches a future step (values).
            if left == values:
                # Updates the right leg to the current step's position (value).
                right = value
                # Increments the step count as a leg position was updated
                no_of_steps += 1
                # Sets the flag to indicate a successful update (match was found).
                flag = 1
                # Exits the inner loop since a match was found.
                break

            # Checks if the right leg's current position matches a future step (values).
            elif right == values:
                # Updates the left leg to the current step's position (value).
                left = value
                # Increments the step count as a leg position was updated
                no_of_steps += 1
                # Sets the flag to indicate a successful update (match was found).
                flag = 1
                # Exits the inner loop since a match was found.
                break

        # If no match was found in the inner loop.
        if flag == 0:
            # Updates the left leg to the current step's position (value). It can also be right leg.
            left = value
            # Increments the step count as a leg position was updated
            no_of_steps += 1

    # Resets the flag to 0 for the next iteration of the outer loop.
    flag = 0

print(no_of_steps, end = "")



    
