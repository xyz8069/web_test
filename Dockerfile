FROM python:3.7
WORKDIR /Project/webapp

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["gunicorn", "web:app", "-c", "./gunicorn.conf.py"]