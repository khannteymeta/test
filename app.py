from flask import Flask, request, render_template, jsonify
from sklearn.metrics import precision_score,recall_score

#initialize flask app

app = Flask(__name__)

# Step1 : Define Test Case
test_cases =[
    {"input": {"fever": True, "cough": True, "sore_throat": False}, "expected": "cold"},
    {"input": {"fever": True, "cough": True, "sore_throat": True}, "expected": "flu"},
    {"input": {"fever": False, "cough": True, "sore_throat": True}, "expected": "strep throat"},
    {"input": {"fever": False, "cough": False, "sore_throat": False}, "expected": "healthy"}
]

# Step 2 : Define the expert system func
def expert_system_func(inputs):
    """Simple rule-based expert system for diagnosing illnesses."""
    if inputs["fever"] and inputs["cough"] and not inputs["sore_throat"]:
        return "cold"
    
    elif inputs["fever"] and inputs["cough"] and inputs["sore_throat"]:
        return "flu"
    elif not inputs["fever"] and inputs["cough"] and inputs["sore_throat"]:
        return "strep throat"
    
    else :
        return "healthy"
    
# step3 : Implement Evaluation Func
def evaluation_system (expert_system_func, test_cases):
    """Evaluates the system for accuracy."""
    correct = 0
    for case in test_cases:
        result = expert_system_func(case["Input"])
        if result == case["expected"]:
            correct +=1;
            
    accuracy = correct / len(test_cases)
    return accuracy


# Step4 : Implement Matric Calculation
def evaluation_matrics (y_true, y_pred):
    """Calculates accuracy, precision, and recall."""
    accuracy = sum([1 for i in range(len(y_true)) if y_true[i] == y_pred[i]]) / len(y_true)
    precision = precision_score(y_true, y_pred, average="weighted", zero_division=1)
    recall = recall_score(y_true, y_pred, average="weighted", zero_division=1)
    return {"accuracy": accuracy, "precision": precision, "recall": recall}

# Flask Routes
@app.route("/")
def home():
    """Render the home page with the form."""
    return render_template("index.html")

@app.route("/predict", methods =['POST'])
def predict():
    """Handle form submission and return the diagnosis."""
    fever = request.form.get("fever")  == "on"
    cough = request.form.get("cough")  == "on"
    sore_throat = request.form.get("sore_throat")  == "on"
    
    # Get prediction from the expert system
    result = expert_system_func({"fever": fever, "cough": cough, "sore_throat": sore_throat})
    return jsonify({"diagnosis": result})


@app.route('/evaluate', methods=['GET'])
def evaluate():
    """Evaluate the system against predefined test cases."""
    y_true = [case["expected"] for case in test_cases]
    y_pred = [expert_system_func(case["input"]) for case in test_cases]
    # Calculate metrics
    metrics = evaluation_matrics(y_true, y_pred)
    return jsonify(metrics)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)   