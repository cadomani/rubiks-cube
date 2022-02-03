import os
from flask import Flask, request
import rubik.dispatch as dispatch
from rubik.dispatch import _dispatch

app = Flask(__name__)


@app.route('/rubik')
def server():
    """
    The following code is invoked when the path portion of the URL matches
        /rubik

    Parameters are passed as a URL query:
        /rubik?parm1=value1&parm2=value2
    """
    try:
        # Path query values are url decoded and stored as strings, casting as a dict we get the same result as the loop
        result = _dispatch(dict(request.args.items()))
        print(f"Response --> {result}")
        return str(result)
    except Exception as e:
        return str(e)


# -----------------------------------
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
