# Daniel Chung, dc3561

from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect

app = Flask(__name__)

# ========== IN-MEMORY USER DATA ==========
user_data = {
    "page_visits": [],
    "quiz_answers": {}
}

# ========== LEARNING SECTION ==========
learning_steps = [
    {
        "id": "home",
        "title": "Learn How to Buy a Home",
        "content": [
            "A step-by-step guide to buying your first home in under 10 minutes.",
            "Choose whether you're buying solo or with a partner to begin."
        ],
        "options": ["Solo", "With a Partner"]
    },
    {
        "id": "preapproval",
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
        "id": "tour",
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
        "id": "agent",
        "title": "Find a Real Estate Agent",
        "content": [
            "Choose someone who knows your target area well.",
            "They help find listings, schedule showings, and handle negotiations."
        ],
        "checklist": ["Define Search Criteria", "Share Pre-Approval Letter", "Start Touring Homes"],
        "hint": "An agent can help you find hidden listings and make competitive offers."
    },
    {
        "id": "offer",
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
        "id": "mortgage",
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
        "id": 1,
        "question": "What is the recommended DTI (Debt-to-Income) ratio for most home loans?",
        "options": ["Exactly 40%", "Under 43%", "Over 50%", "It doesn’t matter"],
        "correctAnswer": "Under 43%",
        "hint": "Lenders generally want to minimize risk—lower DTI is better."
    },
    {
        "id": 2,
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
        "id": 3,
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
        "id": 4,
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
            "Judged solely on your income and credit",
            "Full control over decisions",
            "Lower qualification without strong finances"
        ]
    },
    "partner": {
        "title": "Buying With a Partner",
        "points": [
            "Combined income increases eligibility",
            "Both credit scores and debts are considered",
            "One partner’s weak finances can hurt application"
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

'''
@app.route('/learn/<step_id>')
def learn_page(step_id):
    timestamp = datetime.now().isoformat()
    user_data["page_visits"].append({"step": step_id, "time": timestamp})
    step = next((s for s in learning_steps if s["id"] == step_id), None)
    if step:
        return render_template("learn.html", step=step)
    else:
        return "Step not found", 404
        
'''

@app.route('/quiz/<int:qid>', methods=["GET", "POST"])
def quiz_page(qid):
    if request.method == "POST":
        answer = request.form.get("answer")
        user_data["quiz_answers"][str(qid)] = answer
        return redirect(f"/quiz/{qid + 1}")

    if qid > len(quiz_data):
        return redirect("/quiz/result")

    question = quiz_data[qid - 1]
    return render_template("quiz.html", question=question, qid=qid)

@app.route('/quiz/result')
def quiz_result():
    score = 0
    for q in quiz_data:
        user_answer = user_data["quiz_answers"].get(str(q["id"]))
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
'''
# ========== API ROUTES ==========

@app.route('/api/learning-steps')
def get_learning_steps():
    return jsonify(learning_steps)

@app.route('/api/cheatsheet')
def get_cheatsheet():
    return jsonify({
        "cheatsheet": cheatsheet
    })

@app.route('/api/roles')
def get_roles():
    return jsonify({
        "roles": people_roles
    })

@app.route('/api/quiz')
def get_quiz():
    return jsonify(quiz_data)

@app.route('/api/quiz-summary')
def get_quiz_summary():
    return jsonify(quiz_summary)

@app.route('/api/mortgage-options')
def get_mortgage_options():
    return jsonify(mortgage_options)

@app.route('/api/cheatsheet')
def get_cheatsheet():
    return jsonify(cheatsheet)

# ========== LAUNCH ==========
'''

if __name__ == '__main__':
    app.run(debug=True)