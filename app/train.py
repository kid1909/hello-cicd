from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path

MODEL_PATH = Path("model.joblib")

def main():
    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")

if __name__ == "__main__":
    main()
