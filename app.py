import streamlit as st
import google.generativeai as genai
import random

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.8-flash")

st.set_page_config(
    page_title="EduBot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 EduBot - AI Learning Assistant")


st.sidebar.title("📚 EduBot Menu")

subject = st.sidebar.selectbox(
    "Choose Subject",
    [
        "Mathematics",
        "Chemistry",
        "English",
        "Hindi Vocal Music",
        "Artificial Intelligence"
    ]
)


quiz_data = {

    "Physics": [

        {
            "question": "What is the formula of Ohm's Law?",
            "options": ["V = IR", "F = ma", "P = VI", "E = mc²"],
            "answer": "V = IR"
        },

        {
            "question": "Who gave the laws of motion?",
            "options": ["Newton", "Einstein", "Bohr", "Faraday"],
            "answer": "Newton"
        },

        {
            "question": "SI unit of current?",
            "options": ["Volt", "Ampere", "Watt", "Ohm"],
            "answer": "Ampere"
        },

        {
            "question": "Unit of force?",
            "options": ["Newton", "Joule", "Watt", "Pascal"],
            "answer": "Newton"
        },

        {
            "question": "Speed of light is?",
            "options": ["3×10⁸ m/s", "3×10⁶ m/s", "300 m/s", "1500 m/s"],
            "answer": "3×10⁸ m/s"
        }
    ],

    "Chemistry": [

        {
            "question": "Atomic number of Carbon?",
            "options": ["6", "8", "12", "14"],
            "answer": "6"
        },

        {
            "question": "pH of pure water?",
            "options": ["5", "6", "7", "8"],
            "answer": "7"
        },

        {
            "question": "Chemical formula of water?",
            "options": ["CO₂", "H₂O", "O₂", "NaCl"],
            "answer": "H₂O"
        },

        {
            "question": "Avogadro number is?",
            "options": [
                "6.022×10²³",
                "3×10⁸",
                "9.8",
                "22.4"
            ],
            "answer": "6.022×10²³"
        },

        {
            "question": "Gas used in photosynthesis?",
            "options": ["Oxygen", "Hydrogen", "Carbon Dioxide", "Nitrogen"],
            "answer": "Carbon Dioxide"
        }
    ],

    "Mathematics": [

        {
            "question": "Derivative of x²?",
            "options": ["2x", "x", "x²", "1"],
            "answer": "2x"
        },

        {
            "question": "Value of sin 90°?",
            "options": ["0", "1", "-1", "0.5"],
            "answer": "1"
        },

        {
            "question": "π approximately equals?",
            "options": ["2.14", "3.14", "4.14", "5.14"],
            "answer": "3.14"
        },

        {
            "question": "Integral of 1 dx?",
            "options": ["x", "1", "0", "x²"],
            "answer": "x"
        },

        {
            "question": "Square root of 144?",
            "options": ["10", "11", "12", "13"],
            "answer": "12"
        }
    ],

    "Artificial Intelligence": [

        {
            "question": "AI stands for?",
            "options": [
                "Artificial Intelligence",
                "Automatic Input",
                "Advanced Internet",
                "Applied Information"
            ],
            "answer": "Artificial Intelligence"
        },

        {
            "question": "Machine Learning is a branch of?",
            "options": [
                "AI",
                "Physics",
                "Chemistry",
                "Mathematics"
            ],
            "answer": "AI"
        },

        {
            "question": "ChatGPT is a?",
            "options": [
                "Chatbot",
                "Game",
                "Browser",
                "Compiler"
            ],
            "answer": "Chatbot"
        },

        {
            "question": "AI learns from?",
            "options": [
                "Data",
                "Food",
                "Water",
                "Electricity"
            ],
            "answer": "Data"
        },

        {
            "question": "Neural networks are inspired by?",
            "options": [
                "Human Brain",
                "Car Engine",
                "Solar System",
                "Calculator"
            ],
            "answer": "Human Brain"
        }
    ]
}


st.sidebar.header("📝 Quiz Mode")

question_data = random.choice(quiz_data[subject])

st.sidebar.write(question_data["question"])

selected_option = st.sidebar.radio(
    "Choose Answer",
    question_data["options"]
)

if st.sidebar.button("Check Answer"):

    if selected_option == question_data["answer"]:
        st.sidebar.success("✅ Correct!")
    else:
        st.sidebar.error(
            f"❌ Wrong! Correct Answer: {question_data['answer']}"
        )


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask any question...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    prompt = f"""
You are EduBot, a helpful educational assistant for students.

You are EduBot, a friendly and intelligent educational helper for students.

You help students learn Mathematics, Chemistry, English, Hindi Vocal Music, Artificial Intelligence, and other subjects.

You are not limited to one subject. Always answer the student's question according to what they ask, regardless of the currently selected subject.

Never describe yourself as a Mathematics chatbot, Chemistry chatbot, or any single-subject chatbot.

If a student asks who you are, say:
"I am EduBot, your AI educational helper! I can help you understand concepts, solve problems, prepare for exams, and explore different subjects."
Your selected subject is: {subject}

- Mathematics: Explain and solve problems step by step.
- Chemistry: Explain concepts, reactions, and equations.
- English: Explain literature, grammar, and writing.
- Hindi Vocal Music: Explain swaras, alankars, ragas, taal,
  and vocal music theory.
- Artificial Intelligence: Explain AI, Python, data science,
  machine learning, and neural networks.
- physics: Explain concepts, laws, and formulas.

Use simple language and keep answers focused.

Question:
{user_input}
"""

    reply = ""

    with st.chat_message("assistant"):
        answer_box = st.empty()

        try:
            response = model.generate_content(prompt, stream=True)

            for chunk in response:
                if chunk.text:
                    reply += chunk.text
                    answer_box.markdown(reply)

        except Exception as e:
            reply = f"Error: {e}"
            answer_box.error(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
