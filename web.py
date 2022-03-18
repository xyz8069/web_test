from flask import Flask, render_template, request, send_file
import finance
import trendline

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return send_file('templates/index.html')

@app.route("/stock/<code>", methods = ['GET'])
def stock_info(code):
    return finance.get_stock_now(code)

@app.route("/stock1", methods = ['GET'])
def stock_info1():
    code = request.args.get('code')
    return finance.get_stock_now(code)

@app.route("/mf/<code>", methods = ['GET'])
def mainforce_info(code):
    df = finance.get_stock_kline(code)
    img = trendline.mainforce_monitor_plot(df)
    return render_template('test.html',  img=img)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5000)