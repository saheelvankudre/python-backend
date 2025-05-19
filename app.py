from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import io
import traceback
import os  # Import for reading environment variables

app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get("code", "")
    user_input = data.get("input", "")

    output = io.StringIO()
    error_message = ""
    error_line = None

    try:
        # Redirect stdout and stdin to capture outputs
        sys.stdout = output
        sys.stdin = io.StringIO(user_input)
        exec(code, {})
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        if tb:
            error_line = tb[-1].lineno
        error_message = f"{type(e).__name__}: {str(e)}"
    finally:
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__

    return jsonify({
        "output": output.getvalue(),
        "error": error_message,
        "line_number": error_line
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
