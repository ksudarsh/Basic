from flask import Flask, jsonify, request
import os
import re

app = Flask(__name__)

def list_files(path, page_num, page_size, search_string=None):
    all_files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            # if search_string is None or full_path has the search_string (case insensitive) then append to all_files
            if search_string is None or re.search(search_string, full_path, re.IGNORECASE):
                all_files.append(full_path)
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    page_files = all_files[start_index:end_index]
    total_pages = (len(all_files) + page_size - 1) // page_size
    return {"page_num": page_num, "page_files": page_files, "total_pages": total_pages}

@app.route('/files/<path:directory>')
def list_files_paginated(directory):
    try:
        page_num = int(request.args.get("page_num", 1))
        page_size = int(request.args.get("page_size", 10))
        search_string = request.args.get("search_string", None)
        files = list_files(directory, page_num, page_size, search_string)
        return jsonify(files)
    except:
        return "Directory not found", 404
