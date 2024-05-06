
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from multiprocessing import Process, Queue

# Load dataset
df = pd.read_csv("C:\\Users\\bohnt\Desktop\\AdvTopicPROJ\\1Import\\insurance.csv", encoding='utf-8')
df = df.drop_duplicates()

# Encoding categorical variables
df['sex'] = df['sex'].map({'male': 0, 'female': 1})
df['smoker'] = df['smoker'].map({'yes': 1, 'no': 0})
df['region'] = df['region'].map({'northwest': 0, 'northeast': 1, 'southeast': 2, 'southwest': 3})
x = df.drop(columns=['charges'])
y = df['charges']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train the Random Forest regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

# Prediction function
def predict_charges(input_data, output):
    predicted_charges = model.predict([input_data])[0]
    output.put(predicted_charges)

# User input function
def get_user_input():
    sex = int(input("Enter sex (0 for male, 1 for female): "))
    region = int(input("Enter region (0 for northwest, 1 for northeast, 2 for southeast, 3 for southwest): "))
    smoker = int(input("Enter smoker status (0 for no, 1 for yes): "))
    children = int(input("Enter number of children: "))
    age = float(input("Enter age: "))
    bmi = float(input("Enter BMI: "))
    return [sex, region, smoker, children, age, bmi]

# Main function to predict charges for multiple users
def predictions():
    num_users = int(input("Enter the number of users: "))
    user_inputs = [get_user_input() for _ in range(num_users)]
    processes = []
    outputs = Queue()

    # Start a process for each user input
    for input_data in user_inputs:
        process = Process(target=predict_charges, args=(input_data, outputs))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Retrieve predicted charges from the queue
    predicted_charges = []
    while not outputs.empty():
        predicted_charges.append(outputs.get())

    # Print predicted charges for each user
    for i, charge in enumerate(predicted_charges):
        print(f"Predicted Charges for User {i + 1}: ${round(charge, 2)}")

if __name__ == "__main__":
    predictions()

