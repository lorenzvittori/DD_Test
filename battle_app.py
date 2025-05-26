URL = "https://lorenzvittori-dropduchy-battlebot-battle-app-zc9ips.streamlit.app/"

import streamlit as st
import numpy as np
import battle_engine

def parse_input(text):
    if not text:
        return np.array([])
    try:
        return np.array([int(i) for i in text.strip().split() if i.strip().isdigit()])
    except ValueError:
        return np.array([])

# Funzione per azzerare tutti i campi
def reset_fields():
    st.session_state["blue_archers"] = ""
    st.session_state["blue_swordsmen"] = ""
    st.session_state["blue_axemen"] = ""
    st.session_state["red_archers"] = ""
    st.session_state["red_swordsmen"] = ""
    st.session_state["red_axemen"] = ""
    st.session_state["boss"] = ""

# Pulsante reset in cima
cols = st.columns([1, 4])
with cols[0]:
    if st.button("🔄 Reset"):
        reset_fields()

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

# Istruzioni
st.markdown(
    "<p style='text-align: center; font-size: 14px; margin-top: 0; margin-bottom: 0px;'>"
    "Enter the armies below.<br>Multiple armies of the same type should be separated by spaces."
    "</p>", unsafe_allow_html=True
)
st.markdown("<hr style='margin: 6px 0'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h2 style='color: #1f77b4; text-align: center; margin-bottom: 4px;'>Blue Team</h2>", unsafe_allow_html=True)
    st.markdown("<span style='color: #1f77b4; font-weight: bold;'>🏹 - Archers</span>", unsafe_allow_html=True)
    blue_archers = st.text_input("", key="blue_archers", label_visibility="collapsed", placeholder="4 12")

    st.markdown("<span style='color: #1f77b4; font-weight: bold; margin-top:4px;'>🗡️ - Swordsmen</span>", unsafe_allow_html=True)
    blue_swordsmen = st.text_input("", key="blue_swordsmen", label_visibility="collapsed", placeholder="6")

    st.markdown("<span style='color: #1f77b4; font-weight: bold; margin-top:4px;'>🪓 - Axemen</span>", unsafe_allow_html=True)
    blue_axemen = st.text_input("", key="blue_axemen", label_visibility="collapsed", placeholder="")

with col2:
    st.markdown("<h2 style='color: #d62728; text-align: center; margin-bottom: 4px;'>Red Team</h2>", unsafe_allow_html=True)
    st.markdown("<span style='color: #d62728; font-weight: bold;'>🏹 - Archers</span>", unsafe_allow_html=True)
    red_archers = st.text_input("", key="red_archers", label_visibility="collapsed", placeholder="18 18 5")

    st.markdown("<span style='color: #d62728; font-weight: bold; margin-top:4px;'>🗡️ - Swordsmen</span>", unsafe_allow_html=True)
    red_swordsmen = st.text_input("", key="red_swordsmen", label_visibility="collapsed", placeholder="26 7")

    st.markdown("<span style='color: #d62728; font-weight: bold; margin-top:4px;'>🪓 - Axemen</span>", unsafe_allow_html=True)
    red_axemen = st.text_input("", key="red_axemen", label_visibility="collapsed", placeholder="9")

st.markdown("<hr style='margin: 6px 0'>", unsafe_allow_html=True)

# Boss centrato come Blue/Red Team
st.markdown("<h2 style='text-align: center; color: #000000; margin-bottom: 4px;'>Boss</h2>", unsafe_allow_html=True)
boss = st.text_input("", key="boss", label_visibility="collapsed", placeholder="20 160")

st.markdown("<hr style='margin: 6px 0'>", unsafe_allow_html=True)

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
        'archi': np.concatenate((BlueArchers_list, RedArchers_list)) if BlueArchers_list.size + RedArchers_list.size > 0 else np.array([]),
        'spade': np.concatenate((BlueSwordsmen_list, RedSwordsmen_list)) if BlueSwordsmen_list.size + RedSwordsmen_list.size > 0 else np.array([]),
        'asce': np.concatenate((BlueAxemen_list, RedAxemen_list)) if BlueAxemen_list.size + RedAxemen_list.size > 0 else np.array([]),
        'boss': Boss_list
    }

    Emoji_Dict = {
        'archi': "🏹", 
        'spade':"🗡️",
        'asce': "🪓"
    }

    if sum(len(value) for value in Situation_Dict.values()) > 1:
        battle_order, result = battle_engine.BestResult(Situation_Dict)
        st.success(f"⚔️ Optimized result: {result.num} {result.troop.capitalize()}")

        st.markdown("### Optimal battle sequence:")
        armies_str = "  ↷ ".join(f"{int(army.num)}({Emoji_Dict[army.troop]})" for army in battle_order.armies)
        st.write(armies_str)
        #st.markdown("<span style='color: #1f77b4; font-weight: bold; margin-top:4px;'>🗡️ - Swordsmen</span>", unsafe_allow_html=True)
        #st.markdown(armies_str, unsafe_allow_html=True)
    else:
        st.warning("Please enter valid troops!")
