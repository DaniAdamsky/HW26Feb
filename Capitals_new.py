questions = [
    "What is the capital of France? (1) Paris (2) Lyon (3) Marseille (4) Nice",
    "What is the capital of Italy? (1) Milan (2) Venice (3) Rome (4) Naples",
    "What is the capital of Spain? (1) Barcelona (2) Seville (3) Madrid (4) Valencia",
    "What is the capital of Portugal? (1) Porto (2) Lisbon (3) Faro (4) Braga",
    "What is the capital of Greece? (1) Thessaloniki (2) Athens (3) Patras (4) Heraklion",
    "What is the capital of Netherlands? (1) Rotterdam (2) Utrecht (3) Eindhoven (4) Amsterdam",
    "What is the capital of Belgium? (1) Antwerp (2) Bruges (3) Brussels (4) Ghent",
    "What is the capital of Switzerland? (1) Zurich (2) Geneva (3) Basel (4) Bern",
    "What is the capital of Austria? (1) Salzburg (2) Vienna (3) Graz (4) Innsbruck",
    "What is the capital of Canada? (1) Toronto (2) Vancouver (3) Ottawa (4) Montreal",
    "What is the capital of Brazil? (1) Rio de Janeiro (2) São Paulo (3) Brasília (4) Salvador",
    "What is the capital of Japan? (1) Osaka (2) Tokyo (3) Kyoto (4) Hiroshima",
    "What is the capital of Australia? (1) Sydney (2) Melbourne (3) Canberra (4) Perth",
    "What is the capital of India? (1) Mumbai (2) New Delhi (3) Bangalore (4) Chennai",
    "What is the capital of Egypt? (1) Alexandria (2) Giza (3) Cairo (4) Luxor",
    "What is the capital of Mexico? (1) Guadalajara (2) Monterrey (3) Cancún (4) Mexico City",
    "What is the capital of Argentina? (1) Córdoba (2) Rosario (3) Mendoza (4) Buenos Aires",
    "What is the capital of South Korea? (1) Busan (2) Incheon (3) Seoul (4) Daegu",
    "What is the capital of Sweden? (1) Gothenburg (2) Malmö (3) Uppsala (4) Stockholm",
    "What is the capital of Norway? (1) Bergen (2) Oslo (3) Trondheim (4) Stavanger"
]

answers = [ 1, 3, 3, 2, 2, 4, 3, 4, 2, 3, 3, 2, 3, 2, 3, 4, 4, 3, 4, 2]

import random

#MAIN CODE
score = 0
miss = 0

def get_random_question():
    """returns a random index from the questions list"""
    return random.randint(0, len(questions) - 1)

def display_question(question):
    """prints the question at the given index number"""
    print(questions[question])

def get_user_choice():
    """gets input from the User (1-4)
    Returns the user choice as an Integer"""
    _ = int(input("choose correct answer number (1-4): "))
    if 1 <= _ <= 4:
        return _
    else:
        print("only between 1-4")
        return get_user_choice()

def user_answer_is_correct(question, user_answer):
    """return True if the answer is correct
    returns False otherwise"""
    if user_answer == answers[question]:
        print (answers[question])
        return True
    else:
        #(for bonus):
        #split the whole question into a list
        split_answer = questions[question].split(" ")
        for word in split_answer:
            #added brackets over the answer number and set it as a string
            answer = f"(" + str(answers[question]) + ")"
            if answer == word:
                #when answer number is found in split list save its index
                answer_index = split_answer.index(answer)
                break
        #full answer = answer number index + 1 (the city name)
        full_answer = split_answer[answer_index+1]
        print(f"Answer was {full_answer}")
        return False

def check_if_score_is_5(score):
    """return True if score == 5"""
    if score == 5:
        return True
    else:
        return False

def check_if_miss_is_3(miss):
    """returns True if miss == 3"""
    if miss == 3:
        return True
    else:
        return False

def remove_question(question):
    """removes the question and answer from the list so they won't be asked twice"""
    questions.pop(question)
    answers.pop(question)


while True:
    _index = get_random_question()
    display_question(_index)

    user_choice = get_user_choice()

    if user_answer_is_correct(_index, user_choice):
        score += 1
        print('You are correct')
    else:
        miss += 1
        print('You are wrong!')


    # remove the used question so it will not appear again
    remove_question(_index)

    if check_if_score_is_5(score):
        print('WINNER !!!')
        break

    if check_if_miss_is_3(miss):
        print('YOU LOST !!!')
        break