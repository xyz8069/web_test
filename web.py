from flask import Flask, render_template, request, send_file
import finance

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return send_file('templates/index.html')

@app.route("/stock/<code>", methods = ['GET'])
def stock_info(code):
    print(1)
    return finance.get_stock_now(code)

@app.route("/stock1", methods = ['GET'])
def stock_info1():
    code = request.args.get('code')
    return finance.get_stock_now(code)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5000)