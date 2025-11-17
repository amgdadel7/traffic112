import os
from asgiref.wsgi import AsgiToWsgi
from main import app

# Give extra time on cold start in hosted WSGI environments
os.environ.setdefault("INITIAL_LOAD_WAIT", "30")

# Expose WSGI-compatible callable for PythonAnywhere
application = AsgiToWsgi(app)




