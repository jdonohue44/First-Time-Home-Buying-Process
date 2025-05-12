# Daniel Chung, dc3561
# Othmane El Houssi, oe2196

from flask import Flask
from flask import render_template
from flask_cors import CORS
from flask import Response, request, jsonify, redirect, url_for
from datetime import datetime
import random

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5000", "http://localhost:8000"])

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
        "checklist": ["Include pre-approval letter", "Consider seller closing cost help",
                      "Negotiate repairs or waive minor ones"],
        "hint": "A strong offer improves your chances, especially in competitive markets.",
        "reinforcement_id": 4
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

reinforcement_data = [
    {
        "id": 0,
        "question": "What is the recommended DTI (Debt-to-Income) ratio for most home loans?",
        "options": ["Exactly 40%", "Under 43%", "Over 50%", "It doesn’t matter"],
        "correctAnswer": "Under 43%",
        "hint": "Lenders generally want to minimize risk—lower DTI is better.",
        "back_page": "preapproval_step",
        "next_page": "progress_timeline",
        "timeline_id": 2
    },
    {
        "id": 1,
        "question": "Which of these statements is NOT part of finding an agent and starting looking?",
        "options": [
            "Share pre-approval letter.",
            "Define search criteria.",
            "Check your credit report.",
            "Tour some homes."
        ],
        "correctAnswer": "Check your credit report.",
        "hint": "This phase is about starting the actual search and working with professionals.",
        "back_page": "find_agent",
        "next_page": "make_offer",
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
        "hint": "Lenders prefer consistent earnings to ensure you can repay the loan.",
        "redirect_to": "preapproval_step"
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
        "hint": "Reserves give lenders confidence you can handle payments after closing.",
        "redirect_to": "preapproval_step"
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
        "hint": "Lenders consider both applicants' credit and financials in joint applications.",
        "redirect_to": "preapproval_step"
    }
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
        "question": "Which type of mortgage offers the lowest interest rate but results in higher monthly payments?",
        "options": [
            "30-Year Fixed",
            "15-Year Fixed",
        ],
        "correctAnswer": "15-Year Fixed",
        "hint": "The rate is about 6.25% annually."
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

learning_flow = [
    "players",
    "players_interactive",
    "preapproval",
    ("reinforcement_question", 0),  # Represent unique reinforcement steps
    "find_agent",
    ("reinforcement_question", 1),
    "make_offer",
    "mortgage",
    "compare",
    "timeline",
    "test_yourself"
]

#======================SIMULATION======================

simulation_explained = [
    ("Listed Price", 
     "The starting point of negotiation. Always compare it with recent sales (comps).",
     "A house listed at $420,000 in a neighborhood where similar homes sold for $400,000 may be overpriced."),
    
    ("Seller Info", 
     "Understand the seller's motivations, such as urgency or flexibility.",
     "A seller relocating for work in two weeks might accept a lower offer for a faster closing."),
    
    ("Competitor Info", 
     "Knowing if others are bidding helps gauge how aggressive you should be.",
     "If another buyer has already made a full-price offer, you may need to go above asking or use an escalation clause."),
    
    ("Preapproval", 
     "Your budget and credibility. A strong preapproval strengthens your offer.",
     "Being preapproved for $450,000 when offering $430,000 shows you're financially prepared."),
    
    ("Location & Market Heat", 
     "Hot markets need fast, often higher bids. Cold ones offer room to negotiate.",
     "In a hot city market, homes sell in days, while in a rural area, homes may sit for months."),
    
    ("Mortgage Rates", 
     "Higher rates affect affordability and may cool buyer competition.",
     "At a 7% interest rate, fewer buyers qualify, giving you more leverage.")
]

scenarios = [
    {
        "id": 1,
        "list_price": 420000,
        "seller_info": "Needs to relocate in 4 weeks, prefers quick close",
        "competition": "One other offer, full asking price",
        "preapproval": 430000,
        "location": "Suburban NJ, very hot market",
        "mortgage_rate": 7.1,
        "questions": [
            {
                "key": "offer_options",
                "text": "Choose your offer:",
                "values": [410000, 420000, 425000],
                "correct": 425000
            },
            {
                "key": "escalation_clause",
                "text": "Escalation Clause?",
                "values": ["Yes (up to $435K)", "No"],
                "correct": "Yes (up to $435K)"
            },
            {
                "key": "closing_speed",
                "text": "Preferred Closing Speed:",
                "values": ["30 days", "45 days"],
                "correct": "30 days"
            },
            {
                "key": "mortgage_type",
                "text": "Mortgage Type:",
                "values": ["Fixed-rate 30yr", "Adjustable-rate (5/1 ARM)"],
                "correct": "Fixed-rate 30yr"
            }
        ]
    },
    {
        "id": 2,
        "list_price": 315000,
        "seller_info": "Elderly owner downsizing, open to flexible offers",
        "competition": "No current offers, home has been on market for 40 days",
        "preapproval": 340000,
        "location": "Upstate NY, cooling market",
        "mortgage_rate": 6.5,
        "questions": [
            {
                "key": "offer_options",
                "text": "Choose your offer:",
                "values": [300000, 310000, 315000],
                "correct": 310000
            },
            {
                "key": "escalation_clause",
                "text": "Escalation Clause?",
                "values": ["Yes (up to $320K)", "No"],
                "correct": "No"
            },
            {
                "key": "closing_speed",
                "text": "Preferred Closing Speed:",
                "values": ["30 days", "60 days"],
                "correct": "60 days"
            },
            {
                "key": "mortgage_type",
                "text": "Mortgage Type:",
                "values": ["Fixed-rate 15yr", "Adjustable-rate (5/1 ARM)"],
                "correct": "Adjustable-rate (5/1 ARM)"
            }
        ]
    },
    {
        "id": 3,
        "list_price": 560000,
        "seller_info": "Investor selling a recently flipped home, wants high price",
        "competition": "Three offers already, one over asking",
        "preapproval": 580000,
        "location": "Austin, TX, fast-growing market",
        "mortgage_rate": 6.8,
        "questions": [
            {
                "key": "offer_options",
                "text": "Choose your offer:",
                "values": [555000, 560000, 570000],
                "correct": 570000
            },
            {
                "key": "escalation_clause",
                "text": "Escalation Clause?",
                "values": ["Yes (up to $585K)", "No"],
                "correct": "Yes (up to $585K)"
            },
            {
                "key": "closing_speed",
                "text": "Preferred Closing Speed:",
                "values": ["20 days", "45 days"],
                "correct": "20 days"
            },
            {
                "key": "mortgage_type",
                "text": "Mortgage Type:",
                "values": ["Fixed-rate 30yr", "Fixed-rate 20yr"],
                "correct": "Fixed-rate 30yr"
            }
        ]
    },
    {
        "id": 4,
        "list_price": 265000,
        "seller_info": "Divorcing couple wants quick sale, open to negotiation",
        "competition": "One lowball offer rejected last week",
        "preapproval": 280000,
        "location": "Rural Pennsylvania, slow market",
        "mortgage_rate": 7.3,
        "questions": [
            {
                "key": "offer_options",
                "text": "Choose your offer:",
                "values": [250000, 260000, 265000],
                "correct": 260000
            },
            {
                "key": "escalation_clause",
                "text": "Escalation Clause?",
                "values": ["Yes (up to $270K)", "No"],
                "correct": "No"
            },
            {
                "key": "closing_speed",
                "text": "Preferred Closing Speed:",
                "values": ["30 days", "50 days"],
                "correct": "30 days"
            },
            {
                "key": "mortgage_type",
                "text": "Mortgage Type:",
                "values": ["Fixed-rate 20yr", "Adjustable-rate (7/1 ARM)"],
                "correct": "Fixed-rate 20yr"
            }
        ]
    }
]

def get_progress(endpoint_name, step_id=None):
    try:
        key = (endpoint_name, step_id) if step_id is not None else endpoint_name
        step = learning_flow.index(key) + 1
        total = len(learning_flow)
        return step, total
    except ValueError:
        return None, None


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
    progress, total = get_progress("timeline")
    return render_template("timeline.html", progress=progress, total_steps=total)


@app.route("/players")
def players():
    progress, total = get_progress("players")
    return render_template("players.html", progress=progress, total_steps=total)


@app.route("/players-interactive")
def players_interactive():
    progress, total = get_progress("players_interactive")
    return render_template("players-interactive.html", progress=progress, total_steps=total)

@app.route('/reinforcement/<int:step_id>', methods=["GET", "POST"])
def reinforcement_question(step_id):
    progress, total_steps = get_progress("reinforcement_question", step_id)
    question = reinforcement_data[step_id]

    user_answer = None
    is_correct = None

    if request.method == "POST":
        user_answer = request.form.get("answer")
        is_correct = (user_answer == question["correctAnswer"])
        user_data.setdefault("reinforcement_answers", {})[str(step_id)] = user_answer

    return render_template(
        'reinforcement.html',
        question=question,
        step_id=step_id,
        progress=progress,
        total_steps=total_steps,
        user_answer=user_answer,
        is_correct=is_correct
    )


@app.route('/progress-timeline/<int:id>')
def progress_timeline(id):
    return render_template("progress-timeline.html", id=id)


@app.route('/preapproval')
def preapproval_step():
    progress, total = get_progress("preapproval")
    return render_template("step-preapproval.html", progress=progress, total_steps=total)


@app.route('/find-agent')
def find_agent():
    progress, total = get_progress("find_agent")
    return render_template("find_agent.html", progress=progress, total_steps=total)


@app.route('/make-offer')
def make_offer():
    progress, total = get_progress("make_offer")
    return render_template("make_offer.html", progress=progress, total_steps=total)


@app.route('/mortgage')
def finalize_mort():
    progress, total = get_progress("mortgage")
    return render_template("finalize_mort.html", progress=progress, total_steps=total)


@app.route('/compare')
def compare():
    progress, total = get_progress("compare")
    return render_template('compare.html', progress=progress, total_steps=total)

@app.route("/simulator_info")
def simulator_info():
    return render_template("simulator_info.html", simulation_explained=simulation_explained)

@app.route("/simulation")
def simulation():
    return render_template("simulator.html")

@app.route("/api/scenario")
def get_scenario():
    scenario = random.choice(scenarios)
    scenario["image_url"] = url_for("static", filename=f"img/house{scenario['id']}.jpg")
    return jsonify(scenario)



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
    progress, total = get_progress("test_yourself")
    return render_template('test_yourself.html', progress=progress, total_steps=total)


# ========== LAUNCH ==========


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
