import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pyfiglet
from colorama import Fore
import subprocess

MIN_QUESTIONS_TO_PREDICT = 15
PREDICTION_THRESHOLD = 0.5


def image_character(character):
    predicted_character = character + '.webp'
    subprocess.run(['open', predicted_character])


def ask_question(question):
    response = input(Fore.YELLOW + question + " (yes/no): \n").strip().lower()
    if response == 'yes':
        return 1
    elif response == 'no':
        return -1
    else:
        print("Invalid answer. Please answer 'yes' or 'no'. ")
        return ask_question(question)


def choose_next_question(model, responses):
    feature_importances = model.feature_importances_
    sorted_features = sorted(range(len(feature_importances)), key=lambda i: feature_importances[i], reverse=True)

    for feature_index in sorted_features:
        feature = X.columns[feature_index]
        if responses[feature] == 0:
            return feature
    return None

def welcome():
    print(
        Fore.YELLOW + "************************************************************************************************************************************************************************")
    print(
        Fore.LIGHTYELLOW_EX + "Welcome to | Welcome to | Welcome to | Welcome to | Welcome to | Welcome to | Welcome to | Welcome to | Welcome to | Welcome to | Welcome to | Welcome to | Welcome to | \n\n\n")
    print(Fore.LIGHTCYAN_EX + pyfiglet.figlet_format("AKINATOR", justify="center", width=160, font="broadway"))
    print(
        Fore.YELLOW + "\n\n\n************************************************************************************************************************************************************************\n")


def predict_character(model, X):
    responses = {col: 0 for col in X.columns}
    while True:
        next_question = choose_next_question(model, responses)
        if next_question is None:
            break
        response = ask_question(next_question)
        responses[next_question] = response

        user_input = pd.DataFrame([responses])
        if len([resp for resp in responses.values() if resp != 0]) >= MIN_QUESTIONS_TO_PREDICT:
            prediction_probs = model.predict_proba(user_input)[0]
            max_prob = max(prediction_probs)
            if max_prob > PREDICTION_THRESHOLD:
                predicted_character = model.classes_[prediction_probs.argmax()]
                print(Fore.MAGENTA + "I think your character might be " + predicted_character + ". Am I right?")
                correct_or_no = input("Is this correct? (yes/no): \n").strip().lower()
                if correct_or_no == "yes":
                    print("I guessed it!\n")
                    image_character(predicted_character)
                    break
            # else:
            #     print("I'm not confident enough yet. Let's continue.")

def main():
    welcome()
    while True:
        ans = input(Fore.YELLOW + "Choose one of following:\n1.Start the game.\n2.Characters.\n3.About me.\n\n")
        ans = int(ans)

        if ans == 1:
            print(Fore.MAGENTA + pyfiglet.figlet_format("Think of a character and I will try to guess who it is!\n",
                                                        justify="center", width=160, font="digital"))
            predict_character(model, X)
        elif ans == 2:
            print(
                pyfiglet.figlet_format("\nList of characters from dataset:\n", justify="center", width=40, font="term"))
            for character in data['Character']:
                print(pyfiglet.figlet_format(f"-------------{character}-------------", justify="left", width=50,
                                             font="term"))

        elif ans == 3:
            print(
                Fore.CYAN + "\n\nI am Zhanashova Zhanna CS student of SDU university, and that's my final project for Machine Learning course, console-based Akinator game."
                            "\nI hope that this analog game was funny for you.\nAlso I hope that this project will be so good for my teacher, and he put a high grade for this :)\n\n")
        else:
            print("Invalid answer.Please enter the number of options...")


# Load your dataset
data = pd.read_csv('disney_characters.csv')

X = data.drop('Character', axis=1)  # Features (questions)
y = data['Character']  # Target (character name)

# Create and train the decision tree
model = DecisionTreeClassifier()
model.fit(X, y)

# Run the program
main()
