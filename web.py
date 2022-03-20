from flask import Flask, render_template, request, send_file
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import json
import datetime
import filter
import finance
import trendline

app = Flask(__name__)
scheduler = APScheduler()

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
    return render_template('test.html', img = img)

@app.route("/select", methods = ['GET'])
def stock_select():
    with open('select.json') as file:
        data = json.load(file)
        stock_list = data['data']
        select_time = data['date']
    return render_template('select.html', stock_list = stock_list, select_time = select_time)

class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'select_task', # 任务id
            'func': '__main__:select_task', # 任务执行程序
            'args': None, # 执行程序参数
            'trigger': 'cron',                            # 指定任务触发器 cron
            'day_of_week': 'mon-fri',              # 每周1至周5早上6点执行 
            'hour': 16,
            'minute': 00
        }
    ]
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'

def select_task():
    if datetime.datetime.now().weekday() < 5:
        filter.select_stocks()
    else:
        pass

@app.route('/pause')
def pausetask(id):#暂停
    scheduler.pause_job(id)
    return "Success!"

@app.route('/resume')
def resumetask(id):#恢复
    scheduler.resume_job(id)
    return "Success!"

app.config.from_object(SchedulerConfig())
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
scheduler.init_app(app)  # 把任务列表载入实例flask
scheduler.start()

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5000)