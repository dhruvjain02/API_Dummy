from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from docx import Document
from docx.shared import Inches
import os
import io
import gridfs
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB setup
app.config["MONGO_URI"] = "mongodb+srv://harshal:Harshal2022@cluster0.u5i2m.mongodb.net/form?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Extract form data
        form_data = {
            "Insert Case Number": request.form.get('case_number', "N/A"),
            "Insert Date": request.form.get('date_of_report', "N/A"),
            "Insert Name and Title": request.form.get('report_prepared_by', "N/A"),
            "Insert Device Model": request.form.get('model', "N/A"),
            "Insert RAM": request.form.get('ram', "N/A"),
            # Add other fields as needed
        }

        # Log form data for debugging
        print("Form data received:", form_data)

        # Handle image uploads
        image_ids = []
        for i in range(7):  # Expecting 7 images for placeholders
            image_key = f'image_{i}'
            if image_key in request.files:
                image_file = request.files[image_key]
                if image_file and image_file.filename:
                    image_data = image_file.read()
                    # Store the image in GridFS
                    file_id = fs.put(image_data, filename=f"device_image_{i}.jpg")
                    image_ids.append(file_id)
                    print(f"Stored image {i} with ID: {file_id}")

        # Load the Word template
        REPORT_TEMPLATE = os.path.join(os.getcwd(), 'Report Format.docx')
        document = Document(REPORT_TEMPLATE)

        # Replace placeholders in paragraphs
        for para in document.paragraphs:
            for key, value in form_data.items():
                placeholder = f"[{key}]"
                if placeholder in para.text:
                    para.text = para.text.replace(placeholder, value)

        # Replace placeholders in tables
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in form_data.items():
                        placeholder = f"[{key}]"
                        if placeholder in cell.text:
                            cell.text = cell.text.replace(placeholder, value)

        # Replace image placeholders
        image_placeholders = {
            '[0]': 0,
            '[30]': 1,
            '[60]': 2,
            '[90]': 3,
            '[240]': 4,
            '[270]': 5,
            '[360]': 6
        }

        for placeholder, idx in image_placeholders.items():
            if idx < len(image_ids):  # Ensure there is an image uploaded for the placeholder
                try:
                    # Retrieve the image from GridFS
                    image_data = fs.get(image_ids[idx])
                    img_stream = io.BytesIO(image_data.read())
                    print(f"Replacing image placeholder: {placeholder} with image ID: {image_ids[idx]}")

                    # Replace the placeholder with the image in the document
                    for table in document.tables:
                        for row in table.rows:
                            for cell in row.cells:
                                if placeholder in cell.text:
                                    print(f"Found placeholder {placeholder} in cell, replacing with image.")
                                    cell.text = ""  # Clear the placeholder text
                                    run = cell.paragraphs[0].add_run()
                                    run.add_picture(img_stream, width=Inches(2.5))
                except Exception as e:
                    print(f"Error inserting image for placeholder {placeholder}: {e}")

        # Save the document to a buffer
        buffer = io.BytesIO()
        document.save(buffer)
        buffer.seek(0)

        # Send the modified report
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'report_{form_data["Insert Case Number"]}.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        print(f"Error generating the report: {e}")
        flash("An error occurred while generating your report.", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
