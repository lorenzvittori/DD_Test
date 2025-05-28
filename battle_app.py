import streamlit as st
import numpy as np
import battle_engine as engine
import time

@st.cache_data(show_spinner=False)
def cached_best_result(situation):
    return engine.BestResult(situation)

def parse_input(text):
    if not text:
        return np.array([])
    try:
        return np.array([int(i) for i in text.strip().split() if i.strip().isdigit()])
    except ValueError:
        return np.array([])

# Inizializzazione dei campi nella sessione
for key in [
    "blue_archers", "blue_swordsmen", "blue_axemen",
    "red_archers", "red_swordsmen", "red_axemen",
    "boss", "optimized"
]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "optimized" else False

def reset_fields():
    st.session_state["optimized"] = False
    for key in [
        "blue_archers", "blue_swordsmen", "blue_axemen",
        "red_archers", "red_swordsmen", "red_axemen",
        "boss"
    ]:
        st.session_state[key] = ""

# Titolo
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Pirata+One&display=swap" rel="stylesheet">
<h1 style="
    text-align: center;
    color: #000000;
    margin: 0;
    padding-top: 0;
    font-family: 'Pirata One', cursive;
    font-size: 48px;">
    ⚔️ DropDuchy BattleBot ⚔️
</h1>
""", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; font-size: 14px; margin-top: 0; margin-bottom: 0px;'>"
    "Enter the armies below.<br>Multiple armies of the same type should be separated by spaces."
    "</p>", unsafe_allow_html=True
)
st.markdown("<hr style='margin: 6px 0'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<h2 style='color: #1f77b4; text-align: center; margin-bottom: 4px;'>Blue Team</h2>", unsafe_allow_html=True)
    blue_archers = st.text_input("🏹 - Archers", key="blue_archers", placeholder="4 12")
    blue_swordsmen = st.text_input("🗡️ - Swordsmen", key="blue_swordsmen", placeholder="6")
    blue_axemen = st.text_input("🪓 - Axemen", key="blue_axemen", placeholder="")

with col2:
    st.markdown("<h2 style='color: #d62728; text-align: center; margin-bottom: 4px;'>Red Team</h2>", unsafe_allow_html=True)
    red_archers = st.text_input("🏹 - Archers", key="red_archers", placeholder="18 18 5")
    red_swordsmen = st.text_input("🗡️ - Swordsmen", key="red_swordsmen", placeholder="26 7")
    red_axemen = st.text_input("🪓 - Axemen", key="red_axemen", placeholder="9")
    boss = st.text_input("🚩 Boss", key="boss", placeholder="20 160")

st.markdown("<hr style='margin: 6px 0'>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; font-size: 12px; color: #888;'>"
    "⚠️ Note: This code may be inefficient for battles with more than 9 troops."
    "</p>", unsafe_allow_html=True
)

btn = st.button("🤖 Optimize", help="Calculate the best strategy", use_container_width=True)

if btn:
    BlueArchers_list = parse_input(blue_archers)
    BlueSwordsmen_list = parse_input(blue_swordsmen)
    BlueAxemen_list = parse_input(blue_axemen)

    RedArchers_list = -parse_input(red_archers)
    RedSwordsmen_list = -parse_input(red_swordsmen)
    RedAxemen_list = -parse_input(red_axemen)

    Boss_list = -parse_input(boss)

    BlueArchers_list = BlueArchers_list[BlueArchers_list != 0]
    BlueSwordsmen_list = BlueSwordsmen_list[BlueSwordsmen_list != 0]
    BlueAxemen_list = BlueAxemen_list[BlueAxemen_list != 0]

    RedArchers_list = RedArchers_list[RedArchers_list != 0]
    RedSwordsmen_list = RedSwordsmen_list[RedSwordsmen_list != 0]
    RedAxemen_list = RedAxemen_list[RedAxemen_list != 0]

    Boss_list = Boss_list[Boss_list != 0]

    Situation_Dict = {
        'archi': np.concatenate((BlueArchers_list, RedArchers_list)),
        'spade': np.concatenate((BlueSwordsmen_list, RedSwordsmen_list)),
        'asce': np.concatenate((BlueAxemen_list, RedAxemen_list)),
        'boss': Boss_list
    }

    if sum(len(value) for value in Situation_Dict.values()) <= 1:
        st.warning("Please enter valid troops!")
        st.stop()

    result_placeholder = st.empty()
    sequence_placeholder = st.empty()

    st.session_state["optimized"] = False

    with st.spinner("🔄 Searching best strategy..."):
        for stage, army in engine.BestResultGenerator(Situation_Dict):
            color = '#1f77b4' if army.num > 0 else '#d62728' if army.num < 0 else '#aaaa00'
            label = '🏆 Win' if army.num > 0 else '💀 Lose' if army.num < 0 else '⚖️ Draw'

            result_placeholder.markdown(
                f"<h2 style='text-align: center; color: {color};'>{label} ({int(army.num)})</h2>",
                unsafe_allow_html=True
            )

            Emoji_Dict = {
                'archi': "🏹", 
                'spade': "🗡️",
                'asce': "🪓",
                'boss': "<span style='color:#d62728'> Boss</span>"
            }

            armies_str = " ➙ ".join(
                f"<span style='color:{'#1f77b4' if a.num > 0 else '#d62728'}; font-weight: bold; font-size: 20px;'>[{abs(int(a.num))}{Emoji_Dict[a.troop]}]</span>"
                for a in stage.armies
            )

            sequence_placeholder.markdown(
                f"<p style='text-align: center; font-size: 16px;'>{armies_str}</p>",
                unsafe_allow_html=True
            )

            time.sleep(0.1)

    st.session_state["optimized"] = True

    st.markdown(
        "<p style='text-align: center; font-weight: bold; font-size: 18px; color: gray;'>Optimal sequence:</p>",
        unsafe_allow_html=True
    )




if st.session_state.get("optimized", False):
    st.markdown("<hr style='margin: 12px 0'>", unsafe_allow_html=True)
    st.button("🔄 Reset", key="reset_all", use_container_width=True, on_click=reset_fields)
