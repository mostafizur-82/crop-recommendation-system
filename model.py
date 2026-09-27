import csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle


# =========================================
# 1. Read Dataset
# =========================================

data = []

with open('Crop_recommendation.csv', 'r') as file:

    reader = csv.reader(file)

    for row in reader:
        data.append(row)


print("Total rows:", len(data))

print("\nFirst 5 rows:")
for row in data[:5]:
    print(row)


# =========================================
# 2. Separate Features (X) and Target (y)
# =========================================

X = []
y = []


# Skip the first row because it is the header
for row in data[1:]:

    features = [
        float(row[0]),  # N
        float(row[1]),  # P
        float(row[2]),  # K
        float(row[3]),  # Temperature
        float(row[4]),  # Humidity
        float(row[5]),  # pH
        float(row[6])   # Rainfall
    ]

    target = row[7]     # Crop name

    X.append(features)
    y.append(target)


print("\nTotal features:", len(X))
print("Total labels:", len(y))

print("\nFirst feature:")
print(X[0])

print("\nFirst target:")
print(y[0])


# =========================================
# 3. Split Dataset into Training and Testing
# =========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nDataset Split:")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# =========================================
# 4. Create Random Forest Model
# =========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# =========================================
# 5. Train the Model
# =========================================

model.fit(X_train, y_train)

print("\nModel training completed.")


# =========================================
# 6. Test the Model
# =========================================

y_pred = model.predict(X_test)


# =========================================
# 7. Calculate Accuracy
# =========================================

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy * 100, "%")


# =========================================
# 8. Save the Trained Model
# =========================================

with open('crop_model.pkl', 'wb') as file:

    pickle.dump(model, file)


print("\nModel saved as crop_model.pkl")


# =========================================
# 9. Take User Input and Predict Crop
# =========================================

print("\nEnter the following values:")

N = float(input("Nitrogen (N): "))
P = float(input("Phosphorus (P): "))
K = float(input("Potassium (K): "))
temperature = float(input("Temperature: "))
humidity = float(input("Humidity: "))
ph = float(input("pH: "))
rainfall = float(input("Rainfall: "))

# Create input list
user_input = [[
    N,
    P,
    K,
    temperature,
    humidity,
    ph,
    rainfall
]]

# Predict crop
prediction = model.predict(user_input)

print("\nRecommended Crop:", prediction[0])