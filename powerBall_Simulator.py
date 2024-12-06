# Import necessary libraries
import random
import streamlit as st
from collections import OrderedDict

# Define the available balls
blue_ball = list(range(1, 36))
power_ball = list(range(1, 21))

# Streamlit UI to get user inputs
st.title('Australian PowerBall Simulator')

# Game Mode selection
game_mode = st.radio("Game Mode:", ['QuickPick', 'Marked Entry'])

# Number of tickets and games
tickets = st.number_input('Tickets:', min_value=1, value=1)
games = st.number_input('Games:', min_value=1, value=1)

# Variables to track the total spent and earnings
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

# Update the labels for easy user interpretability display
times_won_labels = {
    "7+P": "7 Standard Balls + PowerBall",
    "7": "7 Standard Balls",
    "6+P": "6 Standard Balls + PowerBall",
    "6": "6 Standard Balls",
    "5+P": "5 Standard Balls + PowerBall",
    "5": "5 Standard Balls",
    "4+P": "4 Standard Balls + PowerBall",
    "3+P": "3 Standard Balls + PowerBall",
    "2+P": "2 Standard Balls + PowerBall"
}

# User selects numbers for 'Marked Entry' game mode
user_blues = set()
user_PB = None

if game_mode == 'Marked Entry':
    st.write('Select 7 Numbers:')
    user_blues = st.multiselect('Select 7 Numbers:', blue_ball, max_selections=7)
    
    if len(user_blues) != 7:
        st.warning("Please select exactly 7 numbers.")

    user_PB = st.selectbox('Select Powerball:', power_ball)

# Play button to run the game
if st.button('Play Games'):
    if game_mode == 'Marked Entry' and len(user_blues) != 7:
        st.error("You need to select exactly 7 Standard balls to proceed.")
    else:
        # Run the game simulation
        for _ in range(games):
            winning_blues = set(random.sample(blue_ball, 7))
            winning_PB = random.choice(power_ball)

            winning_numbers = {'blues': winning_blues, 'PB': winning_PB}

            for ticket in range(tickets):
                total_spent += 1.35

                # Generate random numbers for the 'Quickpick' game mode
                if game_mode == 'QuickPick':
                    my_blues = set(random.sample(blue_ball, 7))
                    my_PB = random.choice(power_ball)
                else:
                    my_blues = set(user_blues)
                    my_PB = user_PB

                my_numbers = {'blues': my_blues, 'PB': my_PB}

                # Calculate winnings
                blue_matches = len(my_numbers['blues'].intersection(winning_numbers['blues']))
                power_matches = my_numbers['PB'] == winning_numbers['PB']
                
                win_amt = 0

                if blue_matches == 7:
                    if power_matches:
                        win_amt = 22852522.41
                        times_won['7+P'] += 1
                    else:
                        win_amt = 128161.72
                        times_won['7'] += 1
                elif blue_matches == 6:
                    if power_matches:
                        win_amt = 6026.19
                        times_won['6+P'] += 1
                    else:
                        win_amt = 459.55
                        times_won['6'] += 1
                elif blue_matches == 5:
                    if power_matches:
                        win_amt = 160.45
                        times_won['5+P'] += 1
                    else:
                        win_amt = 42.51
                        times_won['5'] += 1
                elif blue_matches == 4:
                    if power_matches:
                        win_amt = 71.58
                        times_won['4+P'] += 1
                elif blue_matches == 3:
                    if power_matches:
                        win_amt = 17.89
                        times_won['3+P'] += 1
                elif blue_matches == 2:
                    if power_matches:
                        win_amt = 10.88
                        times_won['2+P'] += 1

                earnings += win_amt

        # Reorder the dictionary based on the desired hierarchy
        ordered_times_won = OrderedDict((key, times_won[key]) for key in times_won_labels)

         # Create a table-compatible data format
        table_data = [
            {"Winning Combination": times_won_labels[key], "Count": value}
            for key, value in ordered_times_won.items()
        ]
        
        # Results
        st.write(f"Spent: ${total_spent:.2f}")
        st.write(f"Earnings: ${earnings:.2f}")

         # Display the table
        st.table(table_data)
