from flask import Flask, jsonify, request
import os
import datetime

app = Flask(__name__)

def list_files(path, page_num, page_size, search_string=None):
    all_files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if search_string is None or search_string.lower() in full_path.lower():
                file_type = "file"
                size = os.path.getsize(full_path)
                try:
                    created = datetime.datetime.fromtimestamp(os.path.getctime(full_path)).isoformat()
                except OSError:
                    created = None
                all_files.append({"path": full_path, "type": file_type, "size": size, "created": created})
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            if search_string is None or search_string.lower() in full_path.lower():
                file_type = "directory"
                size = 0
                try:
                    created = datetime.datetime.fromtimestamp(os.path.getctime(full_path)).isoformat()
                except OSError:
                    created = None
                all_files.append({"path": full_path, "type": file_type, "size": size, "created": created})
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
