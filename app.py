from flask import Flask, render_template, request, redirect, send_file, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from docx import Document
from docx.shared import Inches
import io
import os
from datetime import datetime
import base64
import gridfs

app = Flask(__name__)

# MongoDB setup
app.config["MONGO_URI"] = "mongodb+srv://harshal:Harshal2022@cluster0.u5i2m.mongodb.net/form?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)

# Path to Report Format
REPORT_TEMPLATE = os.path.join(os.getcwd(), 'Report Format.docx')

# Route for rendering the form
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            # Extract form data
            form_data = {
                "case_number": request.form.get('case_number'),
                "date_of_report": request.form.get('date_of_report'),
                "report_prepared_by": request.form.get('report_prepared_by'),
                # Add other fields similarly...
            }

            # Handle image uploads
            image_ids = []
            print("Files received:", request.files.keys())
            
            for i in range(7):
                image_key = f'image_{i}'
                if image_key in request.files:
                    image_file = request.files[image_key]
                    if image_file and image_file.filename:
                        image_data = image_file.read()
                        file_id = fs.put(
                            image_data,
                            filename=f"device_image_{i}.jpg",
                            metadata={"case_number": form_data["case_number"], "angle": i}
                        )
                        image_ids.append(file_id)
                        print(f"Stored image {i} with ID: {file_id}")

            form_data["image_ids"] = image_ids
            mongo.db.device_info.insert_one(form_data)

            # Generate report
            if not os.path.exists(REPORT_TEMPLATE):
                raise FileNotFoundError(f"Report template not found at {REPORT_TEMPLATE}")

            document = Document(REPORT_TEMPLATE)
            
            # Replace placeholders in the document
            for para in document.paragraphs:
                if '[Insert Case Number]' in para.text:
                    para.text = para.text.replace('[Insert Case Number]', form_data['case_number'])
                if '[Insert Date]' in para.text:
                    para.text = para.text.replace('[Insert Date]', form_data['date_of_report'])
                if '[Insert Name and Title]' in para.text:
                    para.text = para.text.replace('[Insert Name and Title]', form_data['report_prepared_by'])

            # Save the document to a temporary directory on Vercel
            temp_path = '/tmp/generated_report.docx'
            document.save(temp_path)
            print(f"Report saved to: {temp_path}")

            # Send the generated document
            return send_file(
                temp_path,
                as_attachment=True,
                download_name=f'report_{form_data["case_number"]}.docx',
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

        except Exception as e:
            print(f"Error processing form: {str(e)}")
            app.logger.error(f"Error processing form: {str(e)}")
            flash('An error occurred while processing your form', 'error')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
