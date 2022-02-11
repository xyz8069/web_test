from urllib import response
from aiohttp import request
from flask import Flask, request
import finance

app = Flask(__name__)

@app.route("/")
def index():
    return 'Welcome to use XINXIANJIUCAI service!'

@app.route("/stock/<code>", methods = ['GET'])
def stock_info(code):
    return finance.get_stock_now(code)

@app.route("/stock1", methods = ['GET'])
def stock_info1():
    code = request.args.get('code')
    return finance.get_stock_now(code)

app.run(host = '127.0.0.1', port = 5000)