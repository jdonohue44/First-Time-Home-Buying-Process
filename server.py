# Daniel Chung, dc3561
# Othmane El Houss, oe2196

from flask import Flask
from flask import render_template
from flask_cors import CORS
from flask import Response, request, jsonify, redirect, url_for
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5000", "http://localhost:5000"])

# ========== IN-MEMORY USER DATA ==========
user_data = {
    "quiz_answers": {},
    "entry_times": {} 
}

# ========== LEARNING SECTION ==========
learning_steps = [
    {
        "id": 0,
        "title": "Get Pre-Approved by Your Bank",
        "content": [
            "Your bank will review your finances to give you a price range.",
            "DTI Ratio: Usually under 43%",
            "Income Stability: 2+ year consistent history preferred.",
            "Assets: Savings for your down payment and reserves.",
            "Credit Score: 620 minimum for conventional; 740+ gets best rates."
        ],
        "checklist": ["Proof of Income", "Bank Statements", "Credit Report"],
        "hint": "Lenders want stable income, low debt, and savings."
    },
    {
        "id": 1,
        "title": "Tour Homes",
        "content": [
            "Visit houses within your pre-approved amount.",
            "Use your agent to get private showings and advice.",
            "Track what you liked/disliked."
        ],
        "checklist": ["Schedule Tours", "Take Notes", "Compare Options"],
        "hint": "Act fast in hot markets—homes move quickly!"
    },
    {
        "id": 2,
        "title": "Find a Real Estate Agent",
        "content": [
            "Choose someone who knows your target area well.",
            "They help find listings, schedule showings, and handle negotiations."
        ],
        "checklist": ["Define Search Criteria", "Share Pre-Approval Letter", "Start Touring Homes"],
        "hint": "An agent can help you find hidden listings and make competitive offers."
    },
    {
        "id": 3,
        "title": "Make an Offer",
        "content": [
            "Submit your best offer with pre-approval and proof of funds.",
            "Add a short personal note to the seller for a stronger appeal.",
            "Use an escalation clause in hot markets if needed."
        ],
        "checklist": ["Include pre-approval letter", "Consider seller closing cost help", "Negotiate repairs or waive minor ones"],
        "hint": "A strong offer improves your chances, especially in competitive markets."
    },
    {
        "id": 4,
        "title": "Finalize Your Mortgage & Close the Sale",
        "content": [
            "Lock in your interest rate and finalize the paperwork.",
            "Hire a lawyer to review your contracts.",
            "Sign the documents and pay the closing costs to receive the keys!"
        ],
        "checklist": ["Get Lawyer", "Sign Closing Docs", "Pay Closing Costs"],
        "hint": "After this step, you're officially a homeowner!"
    }
]

# ========== QUIZ SECTION ==========

quiz_data = [
    {
        "id": 0,
        "question": "What is the recommended DTI (Debt-to-Income) ratio for most home loans?",
        "options": ["Exactly 40%", "Under 43%", "Over 50%", "It doesn’t matter"],
        "correctAnswer": "Under 43%",
        "hint": "Lenders generally want to minimize risk—lower DTI is better."
    },
    {
        "id": 1,
        "question": "Why is a 2+ year history of income preferred by lenders?",
        "options": [
            "To verify your identity",
            "To show income stability",
            "To check your credit usage",
            "To track your shopping habits"
        ],
        "correctAnswer": "To show income stability",
        "hint": "Lenders prefer consistent earnings to ensure you can repay the loan."
    },
    {
        "id": 2,
        "question": "What do lenders want to see in your bank statements for down payment and reserves?",
        "options": [
            "Loan repayment records",
            "2–6 months of mortgage payments saved",
            "12 months of utility bills",
            "Income tax returns"
        ],
        "correctAnswer": "2–6 months of mortgage payments saved",
        "hint": "Reserves give lenders confidence you can handle payments after closing."
    },
    {
        "id": 3,
        "question": "Which of these statements is incorrect about buying with a partner?",
        "options": [
            "Combined income boosts purchasing power.",
            "Both credit scores and debts are considered.",
            "If one partner has poor credit, it may hurt the application.",
            "Both credit scores and debts aren't considered."
        ],
        "correctAnswer": "Both credit scores and debts aren't considered.",
        "hint": "Lenders consider both applicants' credit and financials in joint applications."
    }
]

quiz_summary = {
    "passThreshold": 75,
    "messages": {
        "pass": "Great job! You're one step closer to owning a home.",
        "fail": "Keep practicing! Review the content and try again."
    }
}

# ========== CHEATSHEET DATA ==========
cheatsheet = {
    "solo": {
        "title": "Buying Alone",
        "points": [
            "You are judged solely on your credit, income, debt, and assets.",
            "Lower qualification if your income isn't high or your credit score isn’t excellent.",
            "If you're strong financially, it's often cleaner and faster.",
            "You have full control over decisions."
        ]
    },
    "partner": {
        "title": "Buying With a Partner",
        "points": [
            "Combined income boosts purchasing power.",
            "Both credit scores and debts are considered.",
            "If one partner has poor credit or high debt, it may hurt more than help.",
            "Lenders assess joint DTI and both employment situations."
        ]
    }
}

# ========== MORTGAGE OPTIONS ==========

mortgage_options = [
    {
        "type": "15-Year Fixed",
        "duration": "15 years",
        "pros": ["Lower interest rate", "Pay off faster", "Less total interest"],
        "cons": ["Higher monthly payments"]
    },
    {
        "type": "30-Year Fixed",
        "duration": "30 years",
        "pros": ["Predictable payments", "Lower monthly cost"],
        "cons": ["Higher total interest paid"]
    },
    {
        "type": "5/1 ARM",
        "duration": "Fixed for 5 years, then adjusts annually",
        "pros": ["Very low initial rate", "Good if selling soon"],
        "cons": ["Rate and payment can rise sharply"]
    },
    {
        "type": "7/1 ARM",
        "duration": "Fixed for 7 years, then adjusts annually",
        "pros": ["Lower rate for longer period", "Balanced short-term option"],
        "cons": ["Potential rate hikes after year 7"]
    },
    {
        "type": "10/1 ARM",
        "duration": "Fixed for 10 years, then adjusts annually",
        "pros": ["Stable rate for a decade", "Good for mid-term plans"],
        "cons": ["Still risky after fixed period", "Less savings than shorter ARMs"]
    }
]

# ========== ROUTES ==========

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/quiz/<int:qid>', methods=["GET", "POST"])
def quiz_page(qid):
    # End condition: if qid is beyond available questions, go to result page
    if qid >= len(quiz_data):
        return redirect("/quiz/result")

    if request.method == "POST":
        answer = request.form.get("answer")
        user_data["quiz_answers"][str(qid)] = answer
        return redirect(f"/quiz/{qid + 1}")

    # No longer subtract 1 here
    question = quiz_data[qid]
    return render_template("quiz.html", question=question, qid=qid, user_data=user_data)

@app.route('/quiz/result')
def quiz_result():
    score = 0
    for qid, q in enumerate(quiz_data):
        user_answer = user_data["quiz_answers"].get(str(qid))
        if user_answer == q["correctAnswer"]:
            score += 1

    percent = int((score / len(quiz_data)) * 100)
    passed = percent >= quiz_summary["passThreshold"]
    message = quiz_summary["messages"]["pass"] if passed else quiz_summary["messages"]["fail"]

    return render_template("result.html",
                           score=percent,
                           message=message,
                           quiz_data=quiz_data,
                           user_data=user_data  # passing answers to use in result.html
                           )

@app.route('/glossary')
def glossary_page():
    return render_template("cheatsheet.html", cheatsheet=cheatsheet)


# ========== API ROUTES ==========
@app.route('/start-learning')
def start_learning():
    return redirect(url_for('learning_step', step_id=0))

@app.route('/learning/<int:step_id>')
def learning_step(step_id):
    if 0 <= step_id < len(learning_steps):
        # Track entry time for the learning step
        user_data["entry_times"][step_id] = datetime.utcnow().isoformat()

        return render_template(
            'learning.html',
            step=learning_steps[step_id],
            step_id=step_id,
            max_id=len(learning_steps) - 1
        )
    return redirect(url_for('start_learning'))

@app.route('/api/cheatsheet')
def get_cheatsheet():
    return jsonify({"cheatsheet": cheatsheet})

@app.route('/api/quiz')
def get_quiz():
    return jsonify(quiz_data)

@app.route('/api/quiz-summary')
def get_quiz_summary():
    return jsonify(quiz_summary)

@app.route('/api/mortgage-options')
def get_mortgage_options():
    return jsonify(mortgage_options)


# ========== LAUNCH ==========


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
