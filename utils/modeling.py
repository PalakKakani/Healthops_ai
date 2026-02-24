import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # simpler than XGBoost
from sklearn.metrics import accuracy_score, roc_auc_score

def train_model(data):
    # Drop ID columns
    X = data.drop(columns=['patient_id', 'risk_flag'], errors='ignore')
    
    # Convert categorical to dummy variables
    X = pd.get_dummies(X, drop_first=True)

    y = data['risk_flag']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = {
        'Accuracy': accuracy_score(y_test, y_pred),
        'ROC-AUC': roc_auc_score(y_test, y_pred) if len(y.unique()) > 1 else 0.5
    }

    return model, metrics