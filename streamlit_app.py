import streamlit as st
import random
from typing import Dict, Set, Tuple

# Placeholders for dynamic values
JACKPOT_AMOUNT = 200000000  # Placeholder for the jackpot amount
PRIZE_POOL_AMOUNTS = {  # Placeholder for the prize amounts for each winning category
    "7+P": 22852522.41,
    "7": 128161.72,
    "6+P": 6026.19,
    "6": 459.55,
    "5+P": 160.45,
    "5": 42.51,
    "4+P": 71.58,
    "3+P": 17.89,
    "2+P": 10.88
}
TICKET_COST = 1.35  # Placeholder for the cost of each ticket

def calc_win_amt(my_numbers: Dict[str, Set[int]], winning_numbers: Dict[str, Set[int]], times_won: Dict[str, int]) -> float:
    """
    Calculate the win amount based on the user's numbers and the winning numbers.
    """
    win_amt = 0
    white_matches = len(my_numbers['whites'].intersection(winning_numbers['whites']))
    power_matches = my_numbers['red'] == winning_numbers['red']

    if white_matches == 7:
        if power_matches:
            win_amt = PRIZE_POOL_AMOUNTS["7+P"] + JACKPOT_AMOUNT
            times_won['7+P'] += 1
        else:
            win_amt = PRIZE_POOL_AMOUNTS["7"]
            times_won['7'] += 1
    elif white_matches == 6:
        if power_matches:
            win_amt = PRIZE_POOL_AMOUNTS["6+P"]
            times_won['6+P'] += 1
        else:
            win_amt = PRIZE_POOL_AMOUNTS["6"]
            times_won['6'] += 1
    elif white_matches == 5:
        if power_matches:
            win_amt = PRIZE_POOL_AMOUNTS["5+P"]
            times_won['5+P'] += 1
        else:
            win_amt = PRIZE_POOL_AMOUNTS["5"]
            times_won['5'] += 1
    elif white_matches == 4 and power_matches:
        win_amt = PRIZE_POOL_AMOUNTS["4+P"]
        times_won['4+P'] += 1
    elif white_matches == 3 and power_matches:
        win_amt = PRIZE_POOL_AMOUNTS["3+P"]
        times_won['3+P'] += 1
    elif white_matches == 2 and power_matches:
        win_amt = PRIZE_POOL_AMOUNTS["2+P"]
        times_won['2+P'] += 1

    return win_amt

def simulate_powerball(tickets_per_game: int, num_games: int) -> Tuple[float, float, Dict[str, int]]:
    """
    Simulate the PowerBall lottery for a given number of tickets and games.
    """
    total_spent = 0
    earnings = 0
    times_won = {
        "7+P": 0,
        "7": 0,
        "6+P": 0,
        "6": 0,
        "5+P": 0,
        "5": 0,
        "4+P": 0,
        "3+P": 0,
        "2+P": 0
    }

    for _ in range(num_games):
        white_drawing = set(random.sample(list(range(1, 36)), 7))
        red_drawing = random.choice(list(range(1, 21)))

        winning_numbers = {'whites': white_drawing, 'red': red_drawing}

        for _ in range(tickets_per_game):
            total_spent += TICKET_COST
            my_whites = set(random.sample(list(range(1, 36)), 7))
            my_red = random.choice(list(range(1, 21)))

            my_numbers = {'whites': my_whites, 'red': my_red}

            win_amt = calc_win_amt(my_numbers, winning_numbers, times_won)
            earnings += win_amt

    return total_spent, earnings, times_won

# Streamlit App
st.title("PowerBall Simulator")
st.write("Welcome to the PowerBall Simulator! Select your options below.")

tickets_per_game = st.number_input("How many tickets would you like to purchase?", min_value=1, step=1)
num_games = st.number_input("How many games would you like to play?", min_value=1, step=1)

if st.button("Simulate"):
    total_spent, earnings, times_won = simulate_powerball(tickets_per_game, num_games)
    st.write(f'Spent: ${total_spent:.2f}')
    st.write(f'Earnings: ${earnings:.2f}')
    st.write("\nResults:")
    st.write("Div | Num Tickets Won")
    st.write("---------------------")
    for division, wins in times_won.items():
        div_number = {
            "7+P": "1",
            "7": "2",
            "6+P": "3",
            "6": "4",
            "5+P": "5",
            "5": "6",
            "4+P": "7",
            "3+P": "8",
            "2+P": "9"
        }[division]
        st.write(f"{div_number}   | {wins}")
