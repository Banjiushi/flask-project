# 应用文件

from flask import Flask, request, url_for
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    return 'hello'



if __name__ == '__main__':
    app.run(debug=True)