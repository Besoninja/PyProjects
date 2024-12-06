import random
import streamlit as st
import pandas as pd
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

# Update the labels for display
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

# Add prize values for simulated payouts
prize_values = {
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
    # Initialize these counters fresh each run
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

    if game_mode == 'Marked Entry' and len(user_blues) != 7:
        st.error("You need to select exactly 7 Standard balls to proceed.")
    else:
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
                power_matches = (my_numbers['PB'] == winning_numbers['PB'])
                
                win_amt = 0

                if blue_matches == 7:
                    if power_matches:
                        win_amt = prize_values["7+P"]
                        times_won['7+P'] += 1
                    else:
                        win_amt = prize_values["7"]
                        times_won['7'] += 1
                elif blue_matches == 6:
                    if power_matches:
                        win_amt = prize_values["6+P"]
                        times_won['6+P'] += 1
                    else:
                        win_amt = prize_values["6"]
                        times_won['6'] += 1
                elif blue_matches == 5:
                    if power_matches:
                        win_amt = prize_values["5+P"]
                        times_won['5+P'] += 1
                    else:
                        win_amt = prize_values["5"]
                        times_won['5'] += 1
                elif blue_matches == 4:
                    if power_matches:
                        win_amt = prize_values["4+P"]
                        times_won['4+P'] += 1
                elif blue_matches == 3:
                    if power_matches:
                        win_amt = prize_values["3+P"]
                        times_won['3+P'] += 1
                elif blue_matches == 2:
                    if power_matches:
                        win_amt = prize_values["2+P"]
                        times_won['2+P'] += 1

                earnings += win_amt

        # Reorder the dictionary based on the desired hierarchy
        ordered_times_won = OrderedDict((key, times_won[key]) for key in times_won_labels)

        # Create a table-compatible data format
        table_data = [
            {
                "Winning Combination": times_won_labels[key],
                "Potential Earnings": prize_values[],
                "Count": value,
                "Simulated Payout": f"${value * prize_values[key]:,.2f}"
            }
            for key, value in ordered_times_won.items()
        ]
        
        # Display winning numbers (from the last game only)
        st.subheader("Winning Numbers")
        st.write(f"Standard Balls: {sorted(winning_blues)}, PowerBall: {winning_PB}")
        
        # Display table
        st.subheader("Results Table")
        st.table(table_data)

        # Display totals
        st.subheader("Totals for this run")
        st.write(f"Total Spent: ${total_spent:.2f}")
        st.write(f"Total Earnings: ${earnings:.2f}")

        # Display bar chart
        df = pd.DataFrame(table_data)
        st.subheader("Winnings Breakdown")
        st.bar_chart(df.set_index("Winning Combination")["Count"])

        # Allow users to download results as CSV
        st.download_button(
            "Download Results as CSV",
            df.to_csv(index=False),
            "results.csv",
            "text/csv"
        )
