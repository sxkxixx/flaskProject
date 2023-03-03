from flask import Flask, request, render_template
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD').json()
    currencies = response.get('rates')
    currency_codes = currencies.keys()
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        from_currency = request.form.get('currency_from')
        to_currency = request.form.get('currency_to')
        result = round((currencies[to_currency] / currencies[from_currency]) * amount, 2)
        context = {
            'amount': amount, 'from_currency': from_currency, 'to_currency': to_currency,
            'currencies': currencies, 'result': result
        }
        return render_template('index.html', **context)
    else:
        return render_template('index.html', currencies=currency_codes)


if __name__ == '__main__':
    app.run(debug=True)
