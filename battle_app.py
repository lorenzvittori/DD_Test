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
<h1 style='font-family: "Pirata One", cursive; text-align: center;'>Battle Optimizer</h1>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin: 6px 0'>", unsafe_allow_html=True)

# Sezione Blue Team
st.markdown("### 🟦 Blue Team")
blue_archers = st.text_input("Archers", key="blue_archers", placeholder="10 20 30")
blue_swordsmen = st.text_input("Swordsmen", key="blue_swordsmen", placeholder="15 25")
blue_axemen = st.text_input("Axemen", key="blue_axemen", placeholder="5 10 15")

# Sezione Red Team
st.markdown("### 🟥 Red Team")
red_archers = st.text_input("Archers", key="red_archers", placeholder="10 20 30")
red_swordsmen = st.text_input("Swordsmen", key="red_swordsmen", placeholder="15 25")
red_axemen = st.text_input("Axemen", key="red_axemen", placeholder="5 10 15")

st.markdown("<hr style='margin: 6px 0'>", unsafe_allow_html=True)

# Boss centrato
st.markdown("<h2 style='text-align: center; color: #000000; margin-bottom: 4px;'>Boss</h2>", unsafe_allow_html=True)
boss = st.text_input("", key="boss", label_visibility="collapsed", placeholder="12 159")

st.markdown("<hr style='margin: 6px 0'>", unsafe_allow_html=True)

# Pulsante Optimize
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

    if sum(len(value) for value in Situation_Dict.values()) > 1:
        battle_order, result = battle_engine.BestResult(Situation_Dict)
        st.success(f"⚔️ Optimized result: {result.num} {result.troop.capitalize()}")

        st.markdown("### Optimal battle sequence:")
        armies_str = " → ".join(f"{army.num}({army.troop.capitalize()})" for army in battle_order.armies)
        st.write(armies_str)
    else:
        st.warning("Please enter valid troops!")

st.markdown("<hr><p style='text-align:center; font-size:12px; color:gray;'>Powered by DropDuchy Battle Engine</p>", unsafe_allow_html=True)
