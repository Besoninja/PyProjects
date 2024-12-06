import random
import streamlit as st
import pandas as pd
from collections import OrderedDict
import plotly.graph_objects as go

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

    # Initialize frequency trackers for drawn balls
    standard_ball_frequency = {ball: 0 for ball in blue_ball}
    power_ball_frequency = {ball: 0 for ball in power_ball}

    if game_mode == 'Marked Entry' and len(user_blues) != 7:
        st.error("You need to select exactly 7 Standard balls to proceed.")
    else:
        # Run the games
        for _ in range(games):
            # Draw winning numbers
            winning_blues = set(random.sample(blue_ball, 7))
            winning_PB = random.choice(power_ball)

            # Track frequencies
            for wb in winning_blues:
                standard_ball_frequency[wb] += 1
            power_ball_frequency[winning_PB] += 1

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
                "Earnings Per Draw": f"${prize_values[key]:,.2f}",
                "Count": value,
                "Simulated Payout": f"${value * prize_values[key]:,.2f}"
            }
            for key, value in ordered_times_won.items()
        ]

        # Determine the top 7 standard balls and the top 1 PowerBall
        top_7_standard = sorted(standard_ball_frequency.items(), key=lambda x: x[1], reverse=True)[:7]
        top_1_power = sorted(power_ball_frequency.items(), key=lambda x: x[1], reverse=True)[:1]

        # Prepare dataframes for frequency charts
        df_standard = pd.DataFrame(list(standard_ball_frequency.items()), columns=["Ball", "Count"])
        df_power = pd.DataFrame(list(power_ball_frequency.items()), columns=["Ball", "Count"])

        # Sort for the "Sorted Frequency" tab (descending by frequency)
        df_standard_sorted = df_standard.sort_values(by="Count", ascending=False)
        df_power_sorted = df_power.sort_values(by="Count", ascending=False)

        # Create the radar chart for top 7 standard balls
        radar_categories = [str(num) for num, freq in top_7_standard]
        radar_values = [freq for num, freq in top_7_standard]

        radar_fig = go.Figure(go.Scatterpolar(
            r=radar_values,
            theta=radar_categories,
            fill='toself',
            name='Top 7 Standard Balls Frequency'
        ))
        radar_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=False
        )

        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Frequency Overview", "Winnings Breakdown", "Frequency Charts", "Sorted Frequency", "Radar Chart"])

        with tab1:
            st.subheader("Most Frequent Numbers (from all games)")
            st.write(f"Top 7 Standard Balls: {[num for num, freq in top_7_standard]}")
            st.write(f"Top 1 PowerBall: {top_1_power[0][0] if top_1_power else 'None'}")

        with tab2:
            st.subheader("Results Table")
            st.table(table_data)

            st.subheader("Winnings Breakdown")
            df = pd.DataFrame(table_data)
            st.bar_chart(df.set_index("Winning Combination")["Count"])

        with tab3:
            st.subheader("Frequency Charts")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Standard Ball Frequency")
                st.bar_chart(df_standard.set_index("Ball")["Count"])
            with col2:
                st.write("PowerBall Frequency")
                st.bar_chart(df_power.set_index("Ball")["Count"])

        with tab4:
            st.subheader("Sorted Frequency (Most Frequent to Least Frequent)")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Standard Balls (Sorted)")
                st.bar_chart(df_standard_sorted.set_index("Ball")["Count"])
            with col2:
                st.write("PowerBalls (Sorted)")
                st.bar_chart(df_power_sorted.set_index("Ball")["Count"])

        with tab5:
            st.subheader("Frequency Radar Chart")
            st.plotly_chart(radar_fig, use_container_width=True)

        # Allow users to download results as CSV
        st.download_button(
            "Download Results as CSV",
            df.to_csv(index=False),
            "results.csv",
            "text/csv"
        )
