# Import necessary libraries
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

# Initialize session state for cumulative totals
if "total_spent" not in st.session_state:
    st.session_state["total_spent"] = 0
    st.session_state["total_earnings"] = 0

# User selects numbers for 'Marked Entry' game mode
user_tickets = []

if game_mode == 'Marked Entry':
    st.subheader("Ticket Selection")
    for i in range(int(tickets)):
        st.write(f"Ticket {i + 1}")
        user_blues = st.multiselect(f"Select 7 Numbers (Ticket {i + 1}):", blue_ball, max_selections=7, key=f"ticket_{i}_blue")
        user_PB = st.selectbox(f"Select PowerBall (Ticket {i + 1}):", power_ball, key=f"ticket_{i}_PB")
        
        if len(user_blues) == 7:
            user_tickets.append({'blues': set(user_blues), 'PB': user_PB})
        else:
            st.warning(f"Please select exactly 7 numbers for Ticket {i + 1}")

    # Fast fill remaining tickets
    if st.button("Fast Fill Remaining Tickets"):
        for i in range(len(user_tickets), int(tickets)):
            auto_blues = set(random.sample(blue_ball, 7))
            auto_PB = random.choice(power_ball)
            user_tickets.append({'blues': auto_blues, 'PB': auto_PB})
        st.success("All remaining tickets have been filled automatically!")

# Play button to run the game
if st.button('Play Games'):
    if game_mode == 'Marked Entry' and len(user_tickets) != tickets:
        st.error("Please ensure all tickets are filled before proceeding.")
    else:
        # Run the game simulation
        payouts = {label: 0 for label in times_won_labels.values()}
        for _ in range(games):
            winning_blues = set(random.sample(blue_ball, 7))
            winning_PB = random.choice(power_ball)

            winning_numbers = {'blues': winning_blues, 'PB': winning_PB}

            for ticket in range(int(tickets)):
                total_spent += 1.35

                # Get ticket numbers based on mode
                if game_mode == 'QuickPick':
                    my_blues = set(random.sample(blue_ball, 7))
                    my_PB = random.choice(power_ball)
                else:
                    my_blues = user_tickets[ticket]['blues']
                    my_PB = user_tickets[ticket]['PB']

                my_numbers = {'blues': my_blues, 'PB': my_PB}

                # Calculate winnings
                blue_matches = len(my_numbers['blues'].intersection(winning_numbers['blues']))
                power_matches = my_numbers['PB'] == winning_numbers['PB']
                
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

        # Update session totals
        st.session_state["total_spent"] += total_spent
        st.session_state["total_earnings"] += earnings

        # Reorder the dictionary based on the desired hierarchy
        ordered_times_won = OrderedDict((key, times_won[key]) for key in times_won_labels)

        # Create a table-compatible data format
        table_data = [
            {
                "Winning Combination": times_won_labels[key],
                "Count": value,
                "Simulated Payout": f"${value * prize_values[key]:,.2f}"
            }
            for key, value in ordered_times_won.items()
        ]
        
        # Display winning numbers
        st.subheader("Winning Numbers")
        st.write(f"Standard Balls: {sorted(winning_blues)}, PowerBall: {winning_PB}")
        
        # Display table
        st.subheader("Results Table")
        df = pd.DataFrame(table_data)
        st.table(df)

        # Display cumulative stats
        st.subheader("Cumulative Results")
        st.write(f"Total Spent: ${st.session_state['total_spent']:.2f}")
        st.write(f"Total Earnings: ${st.session_state['total_earnings']:.2f}")

        # Display bar chart
        st.subheader("Winnings Breakdown")
        st.bar_chart(df.set_index("Winning Combination")["Count"])

        # Allow users to download results as CSV
        st.download_button(
            "Download Results as CSV",
            df.to_csv(index=False),
            "results.csv",
            "text/csv"
        )
