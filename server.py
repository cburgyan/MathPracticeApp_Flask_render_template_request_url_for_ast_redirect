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

        # print(type(guess))
        # print(type(answer))
        # print(guess)
        # print(answer)
        if str(answer) == guess:
            if operation == 'addition':
                file_dict['addition'] = int(file_dict['addition']) + 1
            elif operation == 'subtraction':
                file_dict['subtraction'] = int(file_dict['subtraction']) + 1
            elif operation == 'multiplication':
                file_dict['multiplication'] = int(file_dict['multiplication']) + 1
            elif operation == 'division':
                file_dict['division'] = int(file_dict['division']) + 1
            with open('data.txt', 'w') as file:
                file.write(str(file_dict))
            print('Correct')
            temp_coloring = 'success'
            return redirect(url_for('practice_page', operation=operation))
        else:
            print('Incorrect')
            temp_coloring = 'danger'
            return render_template('practice.html', operation=operation, banner_color=coloring, operand1=operand1, operand2=operand2, guess=str(guess), symbol=symbol, temp_coloring=temp_coloring)


def check_answer():
    return 'hi'


if __name__ == "__main__":
    app.run(debug=True)

