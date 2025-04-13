import streamlit as st
import random
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt

# Game setup
CHOICES = ["rock", "paper", "scissors"]
WIN_CONDITIONS = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}

# Image mapping for display
IMAGE_MAPPING = {
    "rock": "rock.png",
    "paper": "paper.png",
    "scissors": "scissor.png"
}

# Session state initialization
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0
if 'draws' not in st.session_state:
    st.session_state.draws = 0
if 'history' not in st.session_state:
    st.session_state.history = []
if 'game_in_progress' not in st.session_state:
    st.session_state.game_in_progress = False

# Helper functions
def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "draw"
    elif WIN_CONDITIONS[user_choice] == computer_choice:
        return "user"
    else:
        return "computer"

def update_score(result):
    if result == "user":
        st.session_state.user_score += 1
    elif result == "computer":
        st.session_state.computer_score += 1
    else:
        st.session_state.draws += 1

def record_history(user_choice, computer_choice, result):
    st.session_state.history.append({
        "Round": len(st.session_state.history) + 1,
        "Your Choice": user_choice.capitalize(),
        "Computer Choice": computer_choice.capitalize(),
        "Result": result.capitalize() if result != "draw" else "Draw"
    })

def reset_game():
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.draws = 0
    st.session_state.history = []
    st.session_state.game_in_progress = False

# UI Components
def show_game_result(user_choice, computer_choice, result):
    # Create a container for the countdown
    countdown_container = st.empty()
    
    # Show countdown with animation
    for i in range(3, 0, -1):
        countdown_container.markdown(f"<h2 style='text-align: center; animation: pulse 1s infinite;'>Showing result in {i}...</h2>", unsafe_allow_html=True)
        sleep(0.5)
    
    # Clear the countdown container
    countdown_container.empty()
    
    # Custom CSS for image alignment
    st.markdown("""
    <style>
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
        padding: 10px;
        height: 100%;
    }
    .vs-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        font-size: 2.5em;
        font-weight: bold;
        padding-top: 60px;  /* Align with the images */
    }
    .player-title {
        font-size: 1.5em;
        margin-bottom: 15px;
        font-weight: bold;
        text-align: center;
    }
    .game-image {
        width: 150px;
        height: 150px;
        object-fit: contain;
        margin: 0 auto;
    }
    .game-result {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 20px auto;
        max-width: 800px;
    }
    .result-text {
        margin-top: 30px;
        text-align: center;
        width: 100%;
    }
    .player-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create game result container with fixed width
    st.markdown("<div class='game-result'>", unsafe_allow_html=True)
    
    # Use more precise column ratios
    col1, col2, col3 = st.columns([1.2,0.6,1.2])
    
    # Determine which player won for animation
    user_won = result == "user"
    computer_won = result == "computer"
    
    with col1:
        st.markdown("<div class='player-section'>", unsafe_allow_html=True)
        st.markdown("<div class='player-title'>You</div>", unsafe_allow_html=True)
        if user_won:
            st.markdown("<div class='winner'>", unsafe_allow_html=True)
        st.image(f"images/{IMAGE_MAPPING[user_choice]}", width=150, use_container_width=False)
        if user_won:
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='vs-container'>VS</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='player-section'>", unsafe_allow_html=True)
        st.markdown("<div class='player-title'>Computer</div>", unsafe_allow_html=True)
        if computer_won:
            st.markdown("<div class='winner'>", unsafe_allow_html=True)
        st.image(f"images/{IMAGE_MAPPING[computer_choice]}", width=150, use_container_width=False)
        if computer_won:
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Game result announcement with better spacing
    st.markdown("<div class='result-text'>", unsafe_allow_html=True)
    if result == "draw":
        st.markdown("<h2 style='text-align: center; color: #FFA500; animation: pulse 2s infinite;'>It's a Draw!</h2>", unsafe_allow_html=True)
    elif result == "user":
        st.markdown("<h2 style='text-align: center; color: #4CAF50; animation: bounce 1s infinite;'>You Win! 🎉</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #F44336; animation: pulse 2s infinite;'>You Lose! 😢</h2>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_stats():
    st.subheader("📊 Game Statistics")
    
    # Score cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Your Score", st.session_state.user_score)
    with col2:
        st.metric("Computer Score", st.session_state.computer_score)
    with col3:
        st.metric("Draws", st.session_state.draws)
    
    # Win rate calculation
    total_games = st.session_state.user_score + st.session_state.computer_score + st.session_state.draws
    if total_games > 0:
        win_rate = (st.session_state.user_score / total_games) * 100
        st.progress(int(win_rate))
        st.caption(f"Your win rate: {win_rate:.1f}%")
    
    # History table
    if st.session_state.history:
        st.subheader("📋 Game History")
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df.set_index("Round"), use_container_width=True)
        
        # Visualization
        st.subheader("📈 Performance Over Time")
        fig, ax = plt.subplots()
        history_df['Your Score'] = history_df['Result'].apply(lambda x: 1 if x == 'User' else 0).cumsum()
        history_df['Computer Score'] = history_df['Result'].apply(lambda x: 1 if x == 'Computer' else 0).cumsum()
        
        ax.plot(history_df['Round'], history_df['Your Score'], label='Your Score', marker='o')
        ax.plot(history_df['Round'], history_df['Computer Score'], label='Computer Score', marker='x')
        ax.set_xlabel('Round')
        ax.set_ylabel('Score')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# Main App
def main():
    st.set_page_config(page_title="Rock Paper Scissors", page_icon="✂️", layout="wide")
    
    # Custom CSS with animations
    st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        width: 100%;
        margin: 5px 0;
        position: relative;
        overflow: hidden;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        color: white !important;
    }
    .stButton>button:active {
        transform: translateY(1px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        color: white !important;
    }
    .stButton>button::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transform: translateX(-100%);
    }
    .stButton>button:hover::after {
        animation: shine 1.5s infinite;
    }
    @keyframes shine {
        100% {
            transform: translateX(100%);
        }
    }
    .title {
        text-align: center;
        color: #2c3e50;
        animation: fadeIn 1s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .result {
        text-align: center;
        font-size: 24px;
        margin: 20px 0;
    }
    .choice-button {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .choice-icon {
        font-size: 32px;
        margin-bottom: 5px;
    }
    .choice-label {
        font-size: 16px;
        font-weight: bold;
    }
    .reset-button {
        background-color: #f44336 !important;
    }
    .reset-button:hover {
        background-color: #d32f2f !important;
        color: white !important;
    }
    .pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .bounce {
        animation: bounce 1s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .rotate {
        animation: rotate 2s infinite linear;
    }
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .game-result {
        animation: slideIn 0.5s ease-out;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .winner {
        animation: winner 1s infinite alternate;
    }
    @keyframes winner {
        from { transform: scale(1); box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); }
        to { transform: scale(1.1); box-shadow: 0 0 20px rgba(76, 175, 80, 0.8); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='title'>🎲 Advanced Rock, Paper, Scissors</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Game area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🕹️ Play Game")
        
        if not st.session_state.game_in_progress:
            if st.button("Start New Game", key="start_game"):
                st.session_state.game_in_progress = True
                st.rerun()
        else:
            st.write("Make your choice:")
            
            # Choice buttons with improved UI and animations
            st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
            
            # Rock button with pulse animation
            if st.button("🪨 Rock", key="rock_button"):
                play_round("rock")
            
            # Paper button with bounce animation
            if st.button("📄 Paper", key="paper_button"):
                play_round("paper")
            
            # Scissors button with rotate animation
            if st.button("✂️ Scissors", key="scissors_button"):
                play_round("scissors")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Reset button with custom styling
            st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
            if st.button("Reset Game", key="reset_button", type="secondary"):
                reset_game()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        show_stats()
    
    # Display game result if available
    if 'last_game' in st.session_state:
        st.markdown("---")
        st.subheader("🎮 Last Game Result")
        show_game_result(
            st.session_state.last_game["user_choice"],
            st.session_state.last_game["computer_choice"],
            st.session_state.last_game["result"]
        )
    
    # Game instructions
    st.markdown("---")
    with st.expander("ℹ️ Game Instructions"):
        st.write("""
        - **Rock** crushes **Scissors**
        - **Scissors** cuts **Paper**
        - **Paper** covers **Rock**
        - Choose your weapon and try to beat the computer!
        - The game keeps track of your performance over time.
        """)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Rock-paper-scissors.svg/1200px-Rock-paper-scissors.svg.png", 
                width=300)

def play_round(user_choice):
    computer_choice = random.choice(CHOICES)
    result = determine_winner(user_choice, computer_choice)
    update_score(result)
    record_history(user_choice, computer_choice, result)
    
    # Instead of calling show_game_result directly, we'll store the result in session state
    # and display it in the main function
    st.session_state.last_game = {
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "result": result
    }
    st.rerun()

if __name__ == "__main__":
    main()