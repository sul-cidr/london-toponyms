

import os

from flask import Flask
from rq_dashboard import RQDashboard


# RQ dashboard:
app = Flask(__name__)
RQDashboard(app)


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))
