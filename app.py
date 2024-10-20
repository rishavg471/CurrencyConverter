from flask import Flask,request
import requests
app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    print(source_currency)
    print(amount)
    print(target_currency)

    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source,target):
    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=[YOUR_API_KEY]".format(source,target)

    response = request.get(url)
    response = response.json()

    return response['{}_{}'.format(source,target)]


if __name__ == "__main__":
    app.run(debug=True)