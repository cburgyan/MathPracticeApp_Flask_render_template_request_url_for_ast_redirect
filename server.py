from flask import Flask, render_template
import random

app = Flask(__name__)
DIGITS = 3

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/practice/<operation>')
def practice_page(operation):
    if operation == 'addition':
        coloring = 'primary'
        oper1 = random.randint(10 ** (DIGITS - 1), 10 ** DIGITS - 1)
        oper2 = random.randint(10 ** (DIGITS - 1), 10 ** DIGITS - 1)
        answer = oper1 + oper2
        symbol = "fa-solid fa-plus"
    elif operation == 'subtraction':
        coloring = 'warning'
    elif operation == 'multiplication':
        coloring = 'info'
    elif operation == 'division':
        coloring = 'dark'
    return render_template('practice.html', operation=operation, coloring=coloring, operand1=oper1, operand2=oper2, answer=answer, symbol=symbol)




if __name__ == "__main__":
    app.run(debug=True)