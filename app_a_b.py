from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)
# Define Test Cases
test_cases = [
    {"input": {"fever": True, "cough": True, "sore_throat": False}, "expected": "cold"},
    {"input": {"fever": True, "cough": True, "sore_throat": True}, "expected": "flu"},
    {"input": {"fever": False, "cough": True, "sore_throat": True}, "expected": "strep throat"},
    {"input": {"fever": False, "cough": False, "sore_throat": False}, "expected": "healthy"}
]

# Define Rule Set A (Version A)
def version_a_func(inputs):
    if inputs["fever"] and inputs["cough"] and not inputs["sore_throat"]:
        return "cold"
    elif inputs["fever"] and inputs["cough"] and inputs["sore_throat"]:
        return "flu"
    elif not inputs["fever"] and inputs["cough"] and inputs["sore_throat"]:
        return "strep throat"
    else:
        return "healthy"

# Define Rule Set B (Version 😎
def version_b_func(inputs):
    if inputs["fever"] and inputs["cough"]:
        return "flu" if inputs["sore_throat"] else "cold"
    elif not inputs["fever"] and inputs["cough"] and inputs["sore_throat"]:
        return "strep throat"
    else:
        return "healthy"
    


    # A/B Testing Logic
def ab_test(test_cases, version_a_func, version_b_func):
    """Split test cases between two versions and calculate performance."""
    a_results, b_results = [], []

    for i, case in enumerate(test_cases):
        if i % 2 == 0:  # Assign even-indexed cases to Version A
            result = version_a_func(case["input"])
            a_results.append(result == case["expected"])
        else:  # Assign odd-indexed cases to Version B
            result = version_b_func(case["input"])
            b_results.append(result == case["expected"])

    a_accuracy = sum(a_results) / len(a_results) if a_results else 0
    b_accuracy = sum(b_results) / len(b_results) if b_results else 0

    return a_accuracy, b_accuracy

# Flask Routes
@app.route('/')
def home():
    """Render the home page."""
    return render_template('index_a_b.html')

@app.route('/ab_test')
def perform_ab_test():
    """Perform A/B testing and return results."""
    a_accuracy, b_accuracy = ab_test(test_cases, version_a_func, version_b_func)

    results = {
        "Version A Accuracy": a_accuracy,
        "Version B Accuracy": b_accuracy,
    }

    return jsonify(results)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
