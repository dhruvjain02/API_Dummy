from flask import Flask, render_template, request, redirect, send_file, flash, url_for
from flask_pymongo import PyMongo
from docx import Document
import io
import os
import gridfs

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://harshal:Harshal2022@cluster0.u5i2m.mongodb.net/form?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            # Validate form data
            form_data = {key: request.form.get(key, "N/A") for key in request.form.keys()}
            print("Form data validated:", form_data)

            # Copy template to a temporary location
            REPORT_TEMPLATE = os.path.join(os.getcwd(), 'Report Format.docx')
            temp_template = '/tmp/Report Format.docx'
            if os.path.exists(REPORT_TEMPLATE):
                import shutil
                shutil.copy(REPORT_TEMPLATE, temp_template)
                print(f"Template copied to: {temp_template}")
            else:
                raise FileNotFoundError(f"Template not found: {REPORT_TEMPLATE}")

            # Open and modify the document
            document = Document(temp_template)
            for para in document.paragraphs:
                for key, value in form_data.items():
                    placeholder = f"[{key}]"
                    if placeholder in para.text:
                        para.text = para.text.replace(placeholder, value)

            # Save the document
            temp_path = '/tmp/generated_report.docx'
            document.save(temp_path)
            print(f"Report saved to: {temp_path}")

            # Send the file
            return send_file(
                temp_path,
                as_attachment=True,
                download_name=f'report_{form_data["case_number"]}.docx',
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while processing your form", "error")
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
