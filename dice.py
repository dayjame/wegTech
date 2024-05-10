import random

# How many sides do the dice have
SIDE_DICE = 6


# Roll a number of dice and return the results as a list
def dice_roll(num_dice):
    roll_results = []
    for _ in range(num_dice):
        roll = random.randint(1, SIDE_DICE)
        roll_results.append(roll)

    return roll_results,


# Get the number of dice to roll and the bonus from user
# Send the num_dice to the roller function
# Sum the total of the dice and the roll bonus
num_dice = int(input("How many dice do you want to roll? "))
roll_bonus = int(input("What is the bonus? "))
[roll] = dice_roll(num_dice)
score = sum(roll, roll_bonus)

print(roll)
print(score)
