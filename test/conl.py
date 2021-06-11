from flask import Flask, render_template, request
from werkzeug import secure_filename
import ces
app = Flask(__name__)

@app.route('/upload')
def upload_file():
   return render_template('test.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      ces.get_file(f)
      
      
      f.save(secure_filename(f.filename))
      return "yes"
		
if __name__ == '__main__':
   app.run(debug = True)