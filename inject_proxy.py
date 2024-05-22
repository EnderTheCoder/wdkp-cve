"""
@Time: 2024/5/22 0:24
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: inject_proxy.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from flask import Flask, render_template, request

from request import UnparsableRequestException
from sys_request import FetchTableRequest

app = Flask(__name__)


@app.route('/')
def index():
    try:
        res = FetchTableRequest(request.args.get("table")).send()
        print(res)
        return res
    except UnparsableRequestException as e:
        print(e.message)
        raise e


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
