from flask import Flask, render_template, request, url_for
import ast
import random
import time
from werkzeug.utils import redirect


# Constants and Initializations
DIGITS = 3
CORRECT_ANSWERS_PER_RECORD = 50
redirect_clock = True
answer = -1
coloring = 'vanilla'
operand1 = -1
operand2 = -1
symbol = ''
temp_coloring = ''
prev_operation = ''
start_time = -1
stop_time = -1


# Create Flask Object
app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"


def next_stats_record():
    new_dict = {}
    new_dict['number of digits in operands'] = DIGITS
    new_dict['correct'] = 0
    new_dict['wrong'] = 0
    new_dict['percent-correct'] = 0
    new_dict['total-time'] = 0
    new_dict['average-time / problem'] = 0
    new_dict['average-time / correct-answer'] = 0
    new_dict['total-time-for-only-correct-answers'] = 0
    new_dict['average-correct-answer-time / correct-answer'] = 0
    return new_dict


def update_stats_for_right_or_wrong_answer(operation, answer1, guess1, time1=0):
    # Get Operation-specific Data-set
    stats_of_operation = -1
    if operation == 'addition':
        stats_of_operation = file_dict[DIGITS]['addition']
    elif operation == 'subtraction':
        stats_of_operation = file_dict[DIGITS]['subtraction']
    elif operation == 'multiplication':
        stats_of_operation = file_dict[DIGITS]['multiplication']
    elif operation == 'division':
        stats_of_operation = file_dict[DIGITS]['division']

    # Record success or error
    if str(answer1) == str(guess1):
        if stats_of_operation[-1]['correct'] >= CORRECT_ANSWERS_PER_RECORD:
            stats_of_operation.append(next_stats_record())
        stats_of_operation[-1]['correct'] += 1
    else:
        stats_of_operation[-1]['wrong'] += 1

    # Update Percent-correct for operation
    stats_of_operation[-1]['percent-correct'] = float('{:.2f}'.format(stats_of_operation[-1]['correct'] / (stats_of_operation[-1]['correct'] + stats_of_operation[-1]['wrong']) * 100))

    # Update total-time and average-time / problem
    if time1 != 0:
        stats_of_operation[-1]['total-time'] = float('{:.4f}'.format(stats_of_operation[-1]['total-time'] + time1))
        stats_of_operation[-1]['average-time / problem'] = float('{:.4f}'.format(stats_of_operation[-1]['total-time'] / (stats_of_operation[-1]['correct'] + stats_of_operation[-1]['wrong'])))
        if stats_of_operation[-1]['correct'] != 0:
            stats_of_operation[-1]['average-time / correct-answer'] = float('{:.4f}'.format(stats_of_operation[-1]['total-time'] / (stats_of_operation[-1]['correct'])))

        if str(answer1) == str(guess1):
            stats_of_operation[-1]['total-time-for-only-correct-answers'] = float('{:.4f}'.format(stats_of_operation[-1]['total-time-for-only-correct-answers'] + time1))
            stats_of_operation[-1]['average-correct-answer-time / correct-answer'] = float('{:.4f}'.format(stats_of_operation[-1]['total-time-for-only-correct-answers'] / stats_of_operation[-1]['correct']))

    # Update Record
    if stats_of_operation != -1:
        with open('data.txt', 'w') as file:
            file.write(str(file_dict))


def set_operation_specific_variable(operation1):
    global coloring, answer, symbol
    if operation1 == 'addition':
        coloring = 'primary'
        answer = operand1 + operand2
        symbol = "fa-solid fa-plus"
    elif operation1 == 'subtraction':
        coloring = 'warning'
        answer = operand1 - operand2
        symbol = "fa-solid fa-minus"
    elif operation1 == 'multiplication':
        coloring = 'info'
        answer = operand1 * operand2
        symbol = "fa-solid fa-xmark"
    elif operation1 == 'division':
        coloring = 'secondary'
        answer = (operand1 / operand2)
        # print(answer)
        answer = "{:.5f}".format(answer)
        # print(answer)
        symbol = "fa-solid fa-divide"
    else:
        coloring = 'light'
        print('Something went wrong.')


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/practice/<operation>', methods=['POST', 'GET'])
def practice_page(operation):
    global redirect_clock, operand1, operand2, temp_coloring, \
        prev_operation, start_time, stop_time

    # Changing operation
    if prev_operation != operation:
        temp_coloring = ''
        prev_operation = operation

    if request.method == 'GET':
        print('GETTing')

        # Create New Operands
        operand1 = random.randint(10 ** (DIGITS - 1), 10 ** DIGITS - 1)
        operand2 = random.randint(10 ** (DIGITS - 1), 10 ** DIGITS - 1)

        # Find Associated Color and Symbol For Type Of Operation, As Well
        # As Answer
        set_operation_specific_variable(operation)

        # Start Timer and Display Problem
        start_time = time.time()
        return render_template('practice.html', operation=operation, banner_color=coloring, operand1=operand1, operand2=operand2, guess='', symbol=symbol, temp_coloring=temp_coloring)
    else:
        print('POSTing')

        # Stop Timer and Calculate Elapsed Time
        stop_time = time.time()
        elapsed_time = stop_time - start_time

        # Get User's Guess
        guess = str(request.form['guess'])

        # Compare User's Guess to Answer
        if str(answer) == guess:

            # Guess Matches Answer So Adjust Statistics
            update_stats_for_right_or_wrong_answer(operation, answer, guess, time1=elapsed_time)
            # print('Correct')

            # Adjust Banner to Green to Indicate User Success
            temp_coloring = 'success'
            return redirect(url_for('practice_page', operation=operation))

        else:

            # Guess Does NOT Match Answer So Adjust Statistics
            update_stats_for_right_or_wrong_answer(operation, answer, guess, time1=elapsed_time)
            # print('Incorrect')

            # Adjust Banner to Red to Indicate User Error
            temp_coloring = 'danger'
            return render_template('practice.html', operation=operation, banner_color=coloring, operand1=operand1, operand2=operand2, guess=str(guess), symbol=symbol, temp_coloring=temp_coloring)


@app.route('/practice/<operation>/stats')
def stats_page(operation):
    global temp_coloring

    temp_coloring = ''
    return render_template('stats.html', operation=operation, banner_color=coloring, temp_coloring=temp_coloring, dictionary=file_dict, symbol=symbol, correct_answers_per_record=CORRECT_ANSWERS_PER_RECORD)


# Get Data from data.txt (and store it in file_dict,
# but if no data is found in data.txt then initialize file_dict
# to empty dict (in preparation for the next step of creating
# a data record))
try:
    with open('data.txt', 'r') as file:
        file_dict = ast.literal_eval(file.readline())
except SyntaxError as error_message:
    print(error_message)
    file_dict = {}


# Check to assure data records exist for math problems
# with operands that have a certain number of digits (equal to
# the variable "DIGITS") in them (but, if there aren't records
# for that number of digits, then create a new record for it)
try:
    does_it_exist = file_dict[DIGITS]
    # print(file_dict)
except Exception as error_message:
    print(error_message)
    file_dict[DIGITS] = {
        'addition': [next_stats_record()],
        'subtraction': [next_stats_record()],
        'multiplication': [next_stats_record()],
        'division': [next_stats_record()],
    }

if __name__ == "__main__":
    app.run(debug=True)

