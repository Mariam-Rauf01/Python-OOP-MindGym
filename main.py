import streamlit as st
import random

# ------------------- Initialize Session State -------------------
def init_state():
    defaults = {
        'name_entered': False,
        'name': '',
        'score': 0,
        'history': [],
        'step': 'start',
        'last_result': '',
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# ------------------- Reset Game -------------------
def reset_game():
    keys_to_keep = ['name_entered', 'name']
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.step = 'menu'
    st.session_state.last_result = ''

# ------------------- Challenges -------------------

def math_challenge():
    if 'math_question' not in st.session_state:
        range_limit = 20 + (st.session_state.score // 10)
        a, b = random.randint(1, range_limit), random.randint(1, range_limit)
        st.session_state.math_question = (a, b)
        st.session_state.math_answer = a + b
        # Remove previous input so the widget resets
        if "math_input" in st.session_state:
            del st.session_state["math_input"]

    a, b = st.session_state.math_question
    st.write(f"🧮 What is {a} + {b}?")

    with st.form(key='math_form'):
        answer = st.text_input("Your answer:", key="math_input")
        submitted = st.form_submit_button("Submit Answer")

    if submitted:
        if answer.strip().lstrip('-').isdigit():
            if int(answer) == st.session_state.math_answer:
                st.session_state.last_result = "✅ Correct! +10 points"
                st.session_state.score += 10
                st.session_state.history.append(("Math", 10))
            else:
                st.session_state.last_result = f"❌ Incorrect. Answer was {st.session_state.math_answer}"
        else:
            st.session_state.last_result = "❌ Please enter a valid number."

        # Clean up for next question
        del st.session_state.math_question
        del st.session_state.math_answer
        if "math_input" in st.session_state:
            del st.session_state["math_input"]
        st.session_state.step = "result"

def logic_challenge():
    riddles = [
        ("What has to be broken before you can use it?", "egg"),
        ("I speak without a mouth and hear without ears. What am I?", "echo"),
        ("What has many keys but can’t open a single lock?", "piano"),
    ]
    if 'riddle' not in st.session_state:
        st.session_state.riddle, st.session_state.answer = random.choice(riddles)
        if "logic_input" in st.session_state:
            del st.session_state["logic_input"]

    st.write(f"🧩 Riddle: {st.session_state.riddle}")

    with st.form(key='logic_form'):
        answer = st.text_input("Your answer:", key="logic_input")
        submitted = st.form_submit_button("Submit Answer")

    if submitted:
        if st.session_state.answer.lower() in answer.lower():
            st.session_state.last_result = "✅ Correct! +10 points"
            st.session_state.score += 10
            st.session_state.history.append(("Logic", 10))
        else:
            st.session_state.last_result = f"❌ Incorrect. Answer was: {st.session_state.answer}"

        del st.session_state.riddle
        del st.session_state.answer
        if "logic_input" in st.session_state:
            del st.session_state["logic_input"]
        st.session_state.step = "result"

def memory_challenge():
    if 'sequence' not in st.session_state:
        st.session_state.sequence = [random.randint(0, 9) for _ in range(5)]
        st.session_state.show_sequence = True
        if "memory_input" in st.session_state:
            del st.session_state["memory_input"]

    if st.session_state.get('show_sequence', False):
        st.write("🧠 Memorize this sequence:")
        st.write(" ".join(map(str, st.session_state.sequence)))
        if st.button("Hide & Enter Sequence"):
            st.session_state.show_sequence = False
    else:
        with st.form(key='memory_form'):
            user_input = st.text_input("Enter the sequence:", key="memory_input")
            submitted = st.form_submit_button("Submit Answer")

        if submitted:
            correct = "".join(map(str, st.session_state.sequence))
            if user_input.strip() == correct:
                st.session_state.last_result = "✅ Correct! +10 points"
                st.session_state.score += 10
                st.session_state.history.append(("Memory", 10))
            else:
                st.session_state.last_result = f"❌ Incorrect. Correct was: {correct}"

            del st.session_state.sequence
            del st.session_state.show_sequence
            if "memory_input" in st.session_state:
                del st.session_state["memory_input"]
            st.session_state.step = "result"

# ------------------- Result + Back to Menu -------------------
def show_result():
    st.subheader("📢 Result")
    st.info(st.session_state.last_result)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Back to Menu"):
            st.session_state.step = 'menu'
            st.session_state.last_result = ''
    with col2:
        if st.button("🔁 Restart Game"):
            reset_game()

# ------------------- Main UI -------------------
st.title("🧠 MindGym – Daily Brain Trainer")

if not st.session_state.name_entered:
    st.subheader("🎉 Enter your name to begin")
    name = st.text_input("Name:")
    if st.button("Start"):
        if name.strip():
            st.session_state.name = name.strip()
            st.session_state.name_entered = True
            st.session_state.step = 'menu'
        else:
            st.warning("Please enter your name to continue.")
else:
    st.sidebar.title(f"👤 {st.session_state.name}")
    st.sidebar.markdown(f"**Score:** {st.session_state.score}")
    st.sidebar.button("🔁 Restart", on_click=reset_game)

    st.markdown(f"### Current Score: **{st.session_state.score}**")

    step = st.session_state.step

    if step == 'menu':
        st.subheader("🎯 Choose Your Challenge:")
        if st.button("🧮 Math Challenge"):
            st.session_state.step = "math"
            st.session_state.last_result = ''
        if st.button("🧠 Memory Challenge"):
            st.session_state.step = "memory"
            st.session_state.last_result = ''
        if st.button("🧩 Logic Challenge"):
            st.session_state.step = "logic"
            st.session_state.last_result = ''
        if st.button("📊 View My Stats"):
            st.subheader("📈 Your Stats")
            st.write(f"**Total Score:** {st.session_state.score}")
            if st.session_state.history:
                for ch_type, pts in st.session_state.history:
                    st.write(f"- {ch_type}: +{pts} points")
            else:
                st.write("No challenges completed yet.")

    elif step == "math":
        math_challenge()
    elif step == "memory":
        memory_challenge()
    elif step == "logic":
        logic_challenge()
    elif step == "result":
        show_result()
