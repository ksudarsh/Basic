from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/files/<path:directory>')
def list_files(directory):
    try:
        files = os.listdir(directory)
        return jsonify(files)
    except:
        return "Directory not found", 404

# if __name__ == '__main__':
#    app.run(debug=True)
