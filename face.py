from flask import Flask, request, render_template
from deepface import DeepFace
import os
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', result='No file uploaded')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', result='No selected file')
        
        timestamp = int(time.time())
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            matches = DeepFace.find(img_path=file_path, db_path='Dataset')
            if matches and isinstance(matches, list) and not matches[0].empty:
                result = os.path.splitext(os.path.basename(matches[0]['identity'].iloc[0]))[0]
            else:
                result = "No match found"
        except Exception as e:
            result = str(e)
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
