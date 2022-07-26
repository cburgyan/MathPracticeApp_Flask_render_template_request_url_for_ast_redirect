from flask import Flask, render_template, request, url_for
import ast
import random


#{ 'addition': '0', 'subtraction': '0', 'multiplication': '0', 'division': '0' }

from werkzeug.utils import redirect

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
DIGITS = 3
redirect_clock = True
answer = -1
coloring = 'vanilla'
operand1 = -1
operand2 = -1
symbol = ''
temp_coloring = ''
prev_operation = ''


with open('data.txt', 'r') as file:
    file_dict = ast.literal_eval(file.readline())

try:
    print(file_dict[DIGITS])
    print(file_dict)
except Exception as error_message:
    print(error_message)
    file_dict[DIGITS] = {
        'addition': {'correct': 0, 'wrong': 0, 'percent-correct': 0, 'total-time': 0, 'average-time-per-problem': 0},
        'subtraction': {'correct': 0, 'wrong': 0, 'percent-correct': 0, 'total-time': 0, 'average-time-per-problem': 0},
        'multiplication': {'correct': 0, 'wrong': 0, 'percent-correct': 0, 'total-time': 0, 'average-time-per-problem': 0},
        'division': {'correct': 0, 'wrong': 0, 'percent-correct': 0, 'total-time': 0, 'average-time-per-problem': 0},
    }


def update_stats_for_right_or_wrong_answer(operation, answer1, guess1, time1=0):
    #Get Operation-specific Data-set
    stats_of_operation = -1
    if operation == 'addition':
        stats_of_operation = file_dict[DIGITS]['addition']
    elif operation == 'subtraction':
        stats_of_operation = file_dict[DIGITS]['subtraction']
    elif operation == 'multiplication':
        stats_of_operation = file_dict[DIGITS]['multiplication']
    elif operation == 'division':
        stats_of_operation = file_dict[DIGITS]['division']

    #Record success or error
    if str(answer1) == str(guess1):
        stats_of_operation['correct'] += 1
    else:
        stats_of_operation['wrong'] += 1

    #Update Percent-correct for operation
    stats_of_operation['percent-correct'] = '{:.2f}'.format(stats_of_operation['correct'] / (stats_of_operation['correct'] + stats_of_operation['wrong']) * 100)

    #Update total-time and average-time-per-problem
    if time1 != 0:
        stats_of_operation['total-time'] += time1
        stats_of_operation['average-time-per-problem'] = round(stats_of_operation['total-time'] / (stats_of_operation['correct'] + stats_of_operation['wrong']))

    #Update Record
    if stats_of_operation != -1:
        with open('data.txt', 'w') as file:
            file.write(str(file_dict))




@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/practice/<operation>', methods=['POST', 'GET'])
def practice_page(operation):
    global redirect_clock, answer, operand1, operand2, coloring, symbol, temp_coloring, prev_operation

    #Changing operation
    if prev_operation != operation:
        temp_coloring = ''
        prev_operation = operation

    if request.method == 'GET':
        print('GETTing')
        operand1 = random.randint(10 ** (DIGITS - 1), 10 ** DIGITS - 1)
        operand2 = random.randint(10 ** (DIGITS - 1), 10 ** DIGITS - 1)
        if operation == 'addition':
            coloring = 'primary'
            answer = operand1 + operand2
            symbol = "fa-solid fa-plus"
        elif operation == 'subtraction':
            coloring = 'warning'
            answer = operand1 - operand2
            symbol = "fa-solid fa-minus"
        elif operation == 'multiplication':
            coloring = 'info'
            answer = operand1 * operand2
            symbol = "fa-solid fa-xmark"
        elif operation == 'division':
            coloring = 'dark'
            answer = (operand1 / operand2)
            print(answer)
            answer = "{:.5f}".format(answer)
            print(answer)
            symbol = "fa-solid fa-divide"
        else:
            coloring = 'light'
            print('Something went wrong.')
        return render_template('practice.html', operation=operation, banner_color=coloring, operand1=operand1, operand2=operand2, guess='', symbol=symbol, temp_coloring=temp_coloring)
    else:
        print(request.form['guess'])
        try:
            guess = str(request.form['guess'])
        except ValueError:
            guess = str(request.form['guess'])

        if str(answer) == guess:
            update_stats_for_right_or_wrong_answer(operation, answer, guess, time1=0)
            print('Correct')
            temp_coloring = 'success'
            return redirect(url_for('practice_page', operation=operation))
        else:
            update_stats_for_right_or_wrong_answer(operation, answer, guess, time1=0)
            print('Incorrect')
            temp_coloring = 'danger'
            return render_template('practice.html', operation=operation, banner_color=coloring, operand1=operand1, operand2=operand2, guess=str(guess), symbol=symbol, temp_coloring=temp_coloring)


def check_answer():
    return 'hi'


if __name__ == "__main__":
    app.run(debug=True)

