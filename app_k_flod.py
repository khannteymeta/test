from flask import Flask, jsonify, render_template
from sklearn.model_selection import KFold
from sklearn.metrics import precision_score, recall_score
import numpy as np

app = Flask(__name__)
# Define Test Cases
test_cases = [
    {"input": {"fever": True, "cough": True, "sore_throat": False}, "expected": "cold"},
    {"input": {"fever": True, "cough": True, "sore_throat": True}, "expected": "flu"},
    {"input": {"fever": False, "cough": True, "sore_throat": True}, "expected": "strep throat"},
    {"input": {"fever": False, "cough": False, "sore_throat": False}, "expected": "healthy"}
]

# Convert test cases to numpy arrays
test_cases_input = np.array([case["input"] for case in test_cases])
test_cases_expected = np.array([case["expected"] for case in test_cases])

# Define the Expert System Function
def expert_system_func(inputs):
    """Simple rule-based expert system for diagnosing illnesses."""
    if inputs["fever"] and inputs["cough"] and not inputs["sore_throat"]:
        return "cold"
    elif inputs["fever"] and inputs["cough"] and inputs["sore_throat"]:
        return "flu"
    elif not inputs["fever"] and inputs["cough"] and inputs["sore_throat"]:
        return "strep throat"
    else:
        return "healthy"

# Metrics Evaluation Function
def evaluate_metrics(y_true, y_pred):
    """Calculates accuracy, precision, and recall."""
    accuracy = sum([1 for i in range(len(y_true)) if y_true[i] == y_pred[i]]) / len(y_true)
    precision = precision_score(y_true, y_pred, average="weighted", zero_division=1)
    recall = recall_score(y_true, y_pred, average="weighted", zero_division=1)
    return {"accuracy": accuracy, "precision": precision, "recall": recall}

# Flask Routes
@app.route('/')
def home():
    """Render the home page."""
    return render_template('index_k_fold.html')

@app.route('/cross_validate')
def cross_validate():
    """Perform k-fold cross-validation and return results."""
    kf = KFold(n_splits=3)

    accuracies, precisions, recalls = [], [], []

    for train_index, test_index in kf.split(test_cases_input):
        X_test = test_cases_input[test_index]
        y_test = test_cases_expected[test_index]

        y_pred = [expert_system_func(x) for x in X_test]
        metrics = evaluate_metrics(y_test, y_pred)

        accuracies.append(metrics["accuracy"])
        precisions.append(metrics["precision"])
        recalls.append(metrics["recall"])

    results = {
        "Average Accuracy": np.mean(accuracies),
        "Average Precision": np.mean(precisions),
        "Average Recall": np.mean(recalls),
    }

    return jsonify(results)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
