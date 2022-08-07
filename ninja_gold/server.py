from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "This is super secret"

@app.route('/')
def index():
    if 'total_gold' not in session:
            session['total_gold'] = 0
            session['activities'] = [ ]
    return render_template('index.html')

@app.route('/process_money', methods=["POST"])
def process():
    if request.form['building'] == 'farm_gold':
        {# session['activities'] = "" #}
        number = random.randrange(10,21)
        session['total_gold'] += number
        print(f"Gold increased by {number}!")
        {# session['activities'].append(f"Earned {abs(number)} gold from the farm!") #}

    elif request.form['building'] == 'cave_gold':
        {# session['message'] = '' #}
        number = random.randrange(5,11)
        session['total_gold'] += number
        print(f"Gold increased by {number}!")
        {# session['activities'].append(f"Earned {abs(number)} gold from the cave!") #}

    elif request.form['building'] == 'house_gold':
        {# session['message'] = '' #}
        number = random.randrange(2,6)
        session['total_gold'] += number
        print(f"Gold increased by {number}!")
        {# session['activities'].append(f"Earned {abs(number)} gold from the house!") #}

    elif request.form['building'] == 'casino_gold':
        {# session['message'] = '' #}
        number = random.randrange(-50,51)
        session['total_gold'] += number
        if number > 0:
            print(f"Gold increased by {number}!")
            {# session['activities'].append(f"Earned {abs(number)} gold from the casino!") #}
        elif number < 0:
            print(f"Gold decreased by {number}!")
            {# session['activities'].append(f"Lost {abs(number)} gold to the casino!") #}
        else:
            print("Broke even!")

    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)