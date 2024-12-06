import random
import streamlit as st
import pandas as pd
from collections import OrderedDict
import altair as alt

# Define the available balls
blue_ball = list(range(1, 36))
power_ball = list(range(1, 21))

st.title('Australian PowerBall Simulator')

# Game Mode selection
game_mode = st.radio("Game Mode:", ['QuickPick', 'Marked Entry'])

# Number of tickets and games
tickets = st.number_input('Tickets:', min_value=1, value=1)
games = st.number_input('Games:', min_value=1, value=1)

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

user_blues = set()
user_PB = None

if game_mode == 'Marked Entry':
    st.write('Select 7 Numbers:')
    user_blues = st.multiselect('Select 7 Numbers:', blue_ball, max_selections=7)
    if len(user_blues) != 7:
        st.warning("Please select exactly 7 numbers.")
    user_PB = st.selectbox('Select Powerball:', power_ball)

if st.button('Play Games'):
    # Initialize counters
    total_spent = 0
    earnings = 0
    times_won = {key: 0 for key in times_won_labels}

    # Track frequencies
    standard_ball_frequency = {ball: 0 for ball in blue_ball}
    power_ball_frequency = {ball: 0 for ball in power_ball}

    if game_mode == 'Marked Entry' and len(user_blues) != 7:
        st.error("You need to select exactly 7 Standard balls to proceed.")
    else:
        for _ in range(games):
            winning_blues = set(random.sample(blue_ball, 7))
            winning_PB = random.choice(power_ball)

            # Update frequencies
            for wb in winning_blues:
                standard_ball_frequency[wb] += 1
            power_ball_frequency[winning_PB] += 1

            winning_numbers = {'blues': winning_blues, 'PB': winning_PB}

            for ticket in range(tickets):
                total_spent += 1.35

                # Generate numbers
                if game_mode == 'QuickPick':
                    my_blues = set(random.sample(blue_ball, 7))
                    my_PB = random.choice(power_ball)
                else:
                    my_blues = set(user_blues)
                    my_PB = user_PB

                # Calculate matches
                blue_matches = len(my_blues.intersection(winning_blues))
                power_matches = (my_PB == winning_PB)

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

        # Prepare results
        ordered_times_won = OrderedDict((key, times_won[key]) for key in times_won_labels)
        table_data = [
            {
                "Winning Combination": times_won_labels[key],
                "Earnings Per Draw": f"${prize_values[key]:,.2f}",
                "Count": value,
                "Simulated Payout": f"${value * prize_values[key]:,.2f}"
            }
            for key, value in ordered_times_won.items()
        ]

        # Top frequencies
        top_7_standard = sorted(standard_ball_frequency.items(), key=lambda x: x[1], reverse=True)[:7]
        top_1_power = sorted(power_ball_frequency.items(), key=lambda x: x[1], reverse=True)[:1]

        # Display a combined stats section
        st.subheader("Statistics and Visualizations")

        # Display "Most Frequent Numbers" and "Winnings Breakdown" together
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Most Frequent Numbers (from all games)**")
            st.write(f"Top 7 Standard Balls: {[num for num, freq in top_7_standard]}")
            st.write(f"Top 1 PowerBall: {top_1_power[0][0] if top_1_power else 'None'}")

        with col2:
            st.markdown("**Winnings Breakdown**")
            st.table(table_data)
            st.write(f"Total Spent: ${total_spent:.2f}")
            st.write(f"Total Earnings: ${earnings:.2f}")

        # Prepare data for charts
        df = pd.DataFrame(table_data)

        # Create a long-form DataFrame for frequencies for more flexible plotting
        df_standard = pd.DataFrame(list(standard_ball_frequency.items()), columns=["Ball", "Count"])
        df_standard["Type"] = "Standard"
        df_power = pd.DataFrame(list(power_ball_frequency.items()), columns=["Ball", "Count"])
        df_power["Type"] = "Power"
        
        # Combine into one DataFrame
        df_freq = pd.concat([df_standard, df_power], ignore_index=True)

        # Use tabs to cycle through different charts
        tab1, tab2, tab3 = st.tabs(["Simple Frequency Bar Charts", "Stacked Bar Chart", "Sorted Frequency"])

        with tab1:
            st.markdown("### Simple Frequency Bar Charts")
            # Standard ball frequency chart
            st.write("**Standard Ball Frequency**")
            st.bar_chart(df_standard.set_index("Ball")["Count"])

            # PowerBall frequency chart
            st.write("**PowerBall Frequency**")
            st.bar_chart(df_power.set_index("Ball")["Count"])

        with tab2:
            st.markdown("### Stacked Bar Chart of Frequencies")
            # Create a stacked bar chart using Altair
            chart = (
                alt.Chart(df_freq)
                .mark_bar()
                .encode(
                    x=alt.X("Ball:O", sort="ascending"),
                    y="Count:Q",
                    color="Type:N",
                    tooltip=["Ball", "Count", "Type"]
                )
                .properties(width=600, height=400)
            )
            st.altair_chart(chart, use_container_width=True)

        with tab3:
            st.markdown("### Frequencies Sorted by Count")
            # Sort by frequency (descending)
            df_freq_sorted = df_freq.sort_values("Count", ascending=False)
            chart_sorted = (
                alt.Chart(df_freq_sorted)
                .mark_bar()
                .encode(
                    x=alt.X("Ball:O", sort=None),
                    y="Count:Q",
                    color="Type:N",
                    tooltip=["Ball", "Count", "Type"]
                )
                .properties(width=600, height=400)
            )
            st.altair_chart(chart_sorted, use_container_width=True)

        # Download results as CSV
        st.download_button(
            "Download Results as CSV",
            df.to_csv(index=False),
            "results.csv",
            "text/csv"
        )
