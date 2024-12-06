import random
import streamlit as st
import pandas as pd

# Define number ranges
white_ball_numbers = list(range(1, 36))
power_ball_numbers = list(range(1, 21))

# Initialize session state for ticket selections
if "tickets" not in st.session_state:
    st.session_state["tickets"] = []

if "current_ticket" not in st.session_state:
    st.session_state["current_ticket"] = 0

if "selection" not in st.session_state:
    st.session_state["selection"] = {"whites": [], "powerball": None}

if "results" not in st.session_state:
    st.session_state["results"] = {"Spent": 0, "Earnings": 0, "Wins": {}}


# Helper functions
def add_ticket():
    """Save the current ticket to the list and reset the selection."""
    st.session_state["tickets"].append(st.session_state["selection"])
    st.session_state["selection"] = {"whites": [], "powerball": None}
    st.session_state["current_ticket"] += 1


def reset_all():
    """Reset all tickets and selections."""
    st.session_state["tickets"] = []
    st.session_state["selection"] = {"whites": [], "powerball": None}
    st.session_state["current_ticket"] = 0
    st.session_state["results"] = {"Spent": 0, "Earnings": 0, "Wins": {}}


def fast_fill():
    """Fill all remaining tickets automatically."""
    for _ in range(len(st.session_state["tickets"]), 10):  # Assume 10 tickets max
        auto_whites = random.sample(white_ball_numbers, 7)
        auto_powerball = random.choice(power_ball_numbers)
        st.session_state["tickets"].append({"whites": auto_whites, "powerball": auto_powerball})
    st.session_state["current_ticket"] = len(st.session_state["tickets"])


def simulate_game():
    """Simulate a PowerBall draw and calculate winnings."""
    results = {"Spent": 0, "Earnings": 0, "Wins": {f"{i+1} Wins": 0 for i in range(9)}}
    winning_white_balls = random.sample(white_ball_numbers, 7)
    winning_powerball = random.choice(power_ball_numbers)

    st.write(f"Winning Numbers: {winning_white_balls}, PowerBall: {winning_powerball}")

    for ticket in st.session_state["tickets"]:
        results["Spent"] += 1.35
        white_matches = len(set(ticket["whites"]) & set(winning_white_balls))
        power_match = ticket["powerball"] == winning_powerball

        # Assign prizes based on matches (dummy payout values for example)
        if white_matches == 7 and power_match:
            results["Earnings"] += 10000000
            results["Wins"]["1 Wins"] += 1
        elif white_matches == 7:
            results["Earnings"] += 500000
            results["Wins"]["2 Wins"] += 1
        elif white_matches == 6 and power_match:
            results["Earnings"] += 5000
            results["Wins"]["3 Wins"] += 1
        elif white_matches == 6:
            results["Earnings"] += 500
            results["Wins"]["4 Wins"] += 1
        elif white_matches == 5 and power_match:
            results["Earnings"] += 100
            results["Wins"]["5 Wins"] += 1
        elif white_matches == 5:
            results["Earnings"] += 50
            results["Wins"]["6 Wins"] += 1
        elif white_matches == 4 and power_match:
            results["Earnings"] += 20
            results["Wins"]["7 Wins"] += 1
        elif white_matches == 3 and power_match:
            results["Earnings"] += 10
            results["Wins"]["8 Wins"] += 1
        elif white_matches == 2 and power_match:
            results["Earnings"] += 5
            results["Wins"]["9 Wins"] += 1

    st.session_state["results"] = results


# UI Layout
st.title("Australian PowerBall Simulator")

# Header with Fast Fill and Clear All options
col1, col2 = st.columns([1, 1])
if col1.button("⚡ Fast select unfilled"):
    fast_fill()
if col2.button("🗑️ Clear all"):
    reset_all()

# Ticket layout
st.subheader("Ticket Selection")
for i, ticket in enumerate(st.session_state["tickets"]):
    st.write(f"Ticket {i + 1}:")
    st.write(f"White Balls: {', '.join(map(str, ticket['whites']))}")
    st.write(f"PowerBall: {ticket['powerball']}")

# Current ticket selection
if st.session_state["current_ticket"] < 10:  # Limit to 10 tickets
    st.write(f"Ticket {st.session_state['current_ticket'] + 1}:")
    selection = st.session_state["selection"]

    # White ball selection
    st.write("Select 7 numbers (White Balls):")
    for num in white_ball_numbers:
        selected = st.checkbox(f"{num}", value=num in selection["whites"], key=f"white_{num}")
        if selected and num not in selection["whites"] and len(selection["whites"]) < 7:
            selection["whites"].append(num)
        elif not selected and num in selection["whites"]:
            selection["whites"].remove(num)

    # Proceed to PowerBall selection if 7 numbers selected
    if len(selection["whites"]) == 7:
        st.write("Select 1 number (PowerBall):")
        for num in power_ball_numbers:
            selected = st.radio(f"{num}", selection["powerball"], key=f"power_{num}")
            if selected:
                selection["powerball"] = num

        # If PowerBall is selected, add ticket and move to the next
        if selection["powerball"]:
            st.success(f"Ticket {st.session_state['current_ticket'] + 1} completed!")
            add_ticket()

# Game simulation button
if st.button("Simulate PowerBall Draw"):
    simulate_game()
    st.subheader("Results")
    st.write(f"Total Spent: ${st.session_state['results']['Spent']:.2f}")
    st.write(f"Total Earnings: ${st.session_state['results']['Earnings']:.2f}")
    st.write("Wins Breakdown:")
    for key, value in st.session_state["results"]["Wins"].items():
        st.write(f"{key}: {value}")

# Allow downloading results as CSV
if st.session_state["results"]["Spent"] > 0:
    df = pd.DataFrame([st.session_state["results"]])
    st.download_button("Download Results", df.to_csv(index=False), "results.csv", "text/csv")
