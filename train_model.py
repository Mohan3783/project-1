import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

data = {
    "voltage": [220,225,230],
    "current": [0.5,0.6,0.55],
    "power": [110,135,126]
}

df = pd.DataFrame(data)

model = IsolationForest()
model.fit(df)

joblib.dump(model, "model.pkl")
