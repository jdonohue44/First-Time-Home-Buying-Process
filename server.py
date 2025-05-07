# Daniel Chung, dc3561
# Othmane El Houssi, oe2196

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
        "hint": "Lenders want stable income, low debt, and savings.",
        "reinforcement_id": 0
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
        "hint": "Act fast in hot markets—homes move quickly!",
        "reinforcement_id": 1
    },
    {
        "id": 2,
        "title": "Find a Real Estate Agent",
        "content": [
            "Choose someone who knows your target area well.",
            "They help find listings, schedule showings, and handle negotiations."
        ],
        "checklist": ["Define Search Criteria", "Share Pre-Approval Letter", "Start Touring Homes"],
        "hint": "An agent can help you find hidden listings and make competitive offers.",
        "reinforcement_id": 2
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
        "hint": "A strong offer improves your chances, especially in competitive markets.",
        "reinforcement_id": 3
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

reinforcement_data =[
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
    },
]

quiz_data = [
    {
        "id": 0,
        "question": "What is the main benefit of getting pre-approved before house hunting?",
        "options": [
          "It lets you skip closing costs",
          "It locks in a mortgage rate",
          "It shows sellers you’re a serious buyer",
          "It guarantees the lowest interest rate"
        ],
        "correctAnswer": "It shows sellers you’re a serious buyer",
        "hint": "A pre-approval letter can strengthen your offer."
      },
      {
        "id": 1,
        "question": "Which professional helps you legally review contracts and resolve disputes during the homebuying process?",
        "options": [
          "Real estate agent",
          "Loan officer",
          "Lawyer",
          "Seller"
        ],
        "correctAnswer": "Lawyer",
        "hint": "You’ll need this person to sign off on your closing documents."
      },
      {
        "id": 2,
        "question": "What does a real estate agent do for a first-time homebuyer?",
        "options": [
          "Approves mortgage loans",
          "Handles title transfers",
          "Helps find and negotiate homes",
          "Inspects the property"
        ],
        "correctAnswer": "Helps find and negotiate homes",
        "hint": "They are your guide in touring and bidding on homes."
      },
      {
        "id": 3,
        "question": "Which of the following strategies can make your offer more attractive in a competitive market?",
        "options": [
          "Ask for many repairs",
          "Offer below asking price",
          "Include a personal note to the seller",
          "Skip pre-approval"
        ],
        "correctAnswer": "Include a personal note to the seller",
        "hint": "A thoughtful approach can sway emotional sellers."
      },
      {
        "id": 4,
        "question": "Which type of mortgage offers the lowest initial interest rate, but may adjust over time?",
        "options": [
          "30-Year Fixed",
          "15-Year Fixed",
          "5/1 ARM",
          "10/1 ARM"
        ],
        "correctAnswer": "5/1 ARM",
        "hint": "This option works well if you plan to move in a few years."
      },
      {
        "id": 5,
        "question": "At what stage do you typically sign closing documents and pay final costs?",
        "options": [
          "After touring homes",
          "When making your offer",
          "During final mortgage approval",
          "When closing the sale"
        ],
        "correctAnswer": "When closing the sale",
        "hint": "This is the last step before the home becomes officially yours."
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

@app.route("/single-or-partnered")
def single_or_partnered():
    return render_template("single-or-partnered.html")

@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

@app.route("/players")
def players():
    return render_template("players.html")

@app.route("/players-interactive")
def players_interactive():
    return render_template("players-interactive.html")

@app.route('/reinforcement/<int:step_id>', methods=["GET", "POST"])
def reinforcement_question(step_id):
    step = learning_steps[step_id]
    if "reinforcement_id" in step:
        question = reinforcement_data[step["reinforcement_id"]]
        return render_template('reinforcement.html', question=question, step_id=step_id)
    return redirect(url_for('learning_step', step_id=step_id + 1))

@app.route('/reinforcement/<int:step_id>/answer', methods=["POST"])
def reinforcement_answer(step_id):
    step = learning_steps[step_id]
    question = reinforcement_data[step["reinforcement_id"]]
    user_answer = request.form.get("answer")
    is_correct = (user_answer == question["correctAnswer"])

    # Save answer if tracking
    user_data.setdefault("reinforcement_answers", {})[str(step["reinforcement_id"])] = user_answer

    return render_template(
        "reinforcement_answer.html",
        question=question,
        user_answer=user_answer,
        is_correct=is_correct,
        step_id=step_id
    )

@app.route('/progress-timeline/<int:id>')
def progress_timeline(id):
    return render_template("progress-timeline.html", id=id)

@app.route('/preapproval')
def preapproval_step():
    return render_template("step-preapproval.html")

@app.route('/find-agent')
def find_agent():
    return render_template("find_agent.html")

@app.route('/make-offer')
def make_offer():
    return render_template("make_offer.html")

@app.route('/progress-timeline/4')
def finalize_mort():
    return render_template("finalize_mort.html")

@app.route('/compare')
def compare():
    return render_template('compare.html')

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

@app.route('/test-yourself')
def test_yourself():
    return render_template('test_yourself.html')


# ========== LAUNCH ==========


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
