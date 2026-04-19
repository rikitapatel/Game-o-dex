import streamlit as st
import pandas as pd
import random
import urllib.parse

# --- CONFIG ---
GAMES_URL = "PASTE_GAMES_CSV_LINK"
FORM_PREFILL = "PASTE_PREFILL_LINK"

DEFAULT_PLAYERS = ["Rikita", "Dony", "Nikil"]

st.set_page_config(page_title="Game-o-dex", page_icon="🎲", layout="centered")

games = pd.read_csv(GAMES_URL)

# --- STATE ---
if "current_game" not in st.session_state:
    st.session_state.current_game = None

# --- FUNCTIONS ---
def pick_game(players):
    df = games[(games["MinPlayers"] <= players) & (games["MaxPlayers"] >= players)]
    return df.sample(1).iloc[0]

def build_form_link(game, players):
    # Replace entry IDs from your form
    return (
        FORM_PREFILL
        .replace("GAME", urllib.parse.quote(game))
        .replace("PLAYERS", urllib.parse.quote(players))
    )

# --- UI ---
st.markdown("## 🎲 Game-o-dex")

mode = st.radio("", ["🎯 Pick", "🎮 Game Night"], horizontal=True)

# --- SWIPE PICK ---
if mode == "🎯 Pick":
    players = st.slider("Players", 1, 10, 4)

    if st.session_state.current_game is None:
        st.session_state.current_game = pick_game(players)

    game = st.session_state.current_game

    st.markdown(f"### 🎲 {game['Game']}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👎 Skip", use_container_width=True):
            st.session_state.current_game = pick_game(players)

    with col2:
        if st.button("👍 Play this", use_container_width=True):
            st.success("Good choice 😄")

# --- GAME NIGHT ---
elif mode == "🎮 Game Night":
    players = st.text_input(
        "Players",
        ", ".join(DEFAULT_PLAYERS)
    )

    player_count = len(players.split(","))

    if st.button("🎲 Pick Game", use_container_width=True):
        st.session_state.current_game = pick_game(player_count)

    if st.session_state.current_game is not None:
        game = st.session_state.current_game["Game"]

        st.markdown(f"### 🎮 {game}")

        form_link = build_form_link(game, players)

        st.link_button("🏁 Log Result", form_link, use_container_width=True)
