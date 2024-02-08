import random
from datetime import datetime, timedelta

# Function to generate random expiration date
def generate_expiration_date():
    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=random.randint(-60, 365))  # Expires between 30 and 365 days from now
    return expiration_date

# Function to generate cards numbers and values with expiration date
def generate():
    # generate card number with a start '6011' and 10 random digits
    valid_card = '6011' + ''.join(str(random.randint(0, 9)) for _ in range(10))
 
    # generate expiration date
    expiration_date = generate_expiration_date()

    # make the card list of integers so we can do mathematic stuff
    digits = [int(digit) for digit in valid_card]

    # check Luhn validity
    for i in range(0, len(digits), 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    checksum = sum(digits) % 10
    if checksum != 0:
        checksum = 10 - checksum
    valid_card += str(checksum)

    # check card value
     ## values [5,10,25,50,100] five possibilities
    card_value = get_value(valid_card)

    return valid_card, card_value, expiration_date


# Function to check if the card is expired
def is_expired(expiration_date):
    current_date = datetime.now()
    return expiration_date < current_date


def get_value(card):
    digits = [int(digit) for digit in card]
    # check card value
     ## values [5,10,25,50,100] five possibilities
    if digits[13] % 5 == 0:
        return 5
    elif digits[13] % 5 == 1:
        return 10
    elif digits[13] % 5 == 2:
        return 25
    elif digits[13] % 5 == 3:
        return 50
    else:
        return 100


def luhn(card):
    if not card.startswith('6011'):
        return False
    digits = [int(digit) for digit in card[:-1]]
    for i in range(0, len(digits), 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    checksum = (sum(digits) * 9) % 10  # calculate the checksum without the last digit
    return checksum == int(card[-1])   # check last digit


# enter number of charge cards you want to generate
num_cards = int(input("Number of charge cards: "))

# make a list of tuples that contains the cards numbers, their value, and expiration date
valid_charge_cards = [(key, value, expiration_date) for key, value, expiration_date in (generate() for _ in range(num_cards))]
used_cards = set()

for card_info in valid_charge_cards:
    print("Charge card number:", card_info[0], "Value:", card_info[1], "Expiration Date:", card_info[2])

# loop to recharge the card
for _ in range(num_cards):
    # get card number from user
    card = input("\nEnter Charge Card Number: ")

    while True:
        # check length of card
        if len(card) != 15 or not card.isdigit():
            print("WRONG NUMBER Please Try Again")
            card = input("\nEnter Charge Card Number: ")
            continue

        # check if the card has been used
        if card in used_cards:
            print("This card has already been used.")
            card = input("\nEnter Charge Card Number: ")
            continue

        # check fabricated number
        if luhn(card):
            # check if the card is expired
            if not is_expired(next(card_info[2] for card_info in valid_charge_cards if card_info[0] == card)):
                print("Your Balance Has Been Recharged Successfully With", get_value(card), "L.E")
                used_cards.add(card)  # mark the card as used
                break
            else:
                print("This card has expired. Please try another one.")
                card = input("\nEnter Charge Card Number: ")
                continue
        else:
            print("INVALID NUMBER Please Try Again")
            card = input("\nEnter Charge Card Number: ")
            continue
