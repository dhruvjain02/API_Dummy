from flask import Flask, render_template, request, redirect, send_file, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from docx import Document
from docx.shared import Inches
import io
from datetime import datetime
import gridfs

app = Flask(__name__)

# MongoDB setup
app.config["MONGO_URI"] = "mongodb+srv://harshal:Harshal2022@cluster0.u5i2m.mongodb.net/form?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)

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
                "case_number": request.form.get('case_number', "N/A"),
                "date_of_report": request.form.get('date_of_report', "N/A"),
                "report_prepared_by": request.form.get('report_prepared_by', "N/A"),
                "model": request.form.get('model', "N/A"),
                "color": request.form.get('color', "N/A"),
                "safety_glass": request.form.get('safety_glass', "N/A"),
                "back_cover": request.form.get('back_cover', "N/A"),
                "ram": request.form.get('ram', "N/A"),
                "internal_memory": request.form.get('internal_memory', "N/A"),
                "camera_specs": request.form.get('camera_specs', "N/A"),
                "cameras_check": request.form.get('cameras_check', "N/A"),
                "battery_percentage": request.form.get('battery_percentage', "N/A"),
                "sim_slots": request.form.get('sim_slots', "N/A"),
                "sim_provider": request.form.get('sim_provider', "N/A"),
                "wifi_connected": request.form.get('wifi_connected', "N/A"),
                "bluetooth_status": request.form.get('bluetooth_status', "N/A"),
                "sd_card": request.form.get('sd_card', "N/A"),
                "sd_capacity": request.form.get('sd_capacity', "N/A"),
                "mobile_uptime": request.form.get('mobile_uptime', "N/A"),
                "time_zone": request.form.get('time_zone', "N/A"),
                "language": request.form.get('language', "N/A"),
                "installed_apps": request.form.get('installed_apps', "N/A"),
                "geo_location": request.form.get('geo_location', "N/A"),
                "build_no": request.form.get('build_no', "N/A"),
                "kernel_version": request.form.get('kernel_version', "N/A"),
                "iccid": request.form.get('iccid', "N/A"),
                "imsi": request.form.get('imsi', "N/A"),
                "meid": request.form.get('meid', "N/A"),
                "airplane_mode": request.form.get('airplane_mode', "N/A")
            }

            # Debug: Log all received form data
            print("Form data received:")
            for key, value in form_data.items():
                print(f"{key}: {value}")

            # Handle image uploads
            image_ids = []
            for i in range(7):
                image_key = f'image_{i}'
                if image_key in request.files:
                    image_file = request.files[image_key]
                    if image_file and image_file.filename:
                        # Read the image data
                        image_data = image_file.read()
                        # Store in GridFS
                        file_id = fs.put(image_data, filename=f"device_image_{i}.jpg")
                        image_ids.append(file_id)
                        print(f"Stored image {i} with ID: {file_id}")

            # Add image IDs to form data
            form_data["image_ids"] = image_ids

            # Generate report
            document = Document('./Report Format.docx')

            # Helper function to replace text in tables
            def replace_table_placeholder(table, placeholder, value):
                for row in table.rows:
                    for cell in row.cells:
                        if placeholder in cell.text:
                            cell.text = cell.text.replace(placeholder, str(value))

            # Replace placeholders in paragraphs
            for para in document.paragraphs:
                for key, value in form_data.items():
                    placeholder = f"[{key}]"
                    if placeholder in para.text:
                        para.text = para.text.replace(placeholder, str(value))

            # Replace placeholders in tables
            for table in document.tables:
                for key, value in form_data.items():
                    placeholder = f"[{key}]"
                    replace_table_placeholder(table, placeholder, value)

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
                if idx < len(image_ids):
                    try:
                        # Get image from GridFS
                        image_data = fs.get(image_ids[idx])
                        img_stream = io.BytesIO(image_data.read())
                        for table in document.tables:
                            for row in table.rows:
                                for cell in row.cells:
                                    if placeholder in cell.text:
                                        cell.text = ""
                                        run = cell.paragraphs[0].add_run()
                                        run.add_picture(img_stream, width=Inches(2.5))
                    except Exception as e:
                        print(f"Error inserting image {idx}: {e}")

            # Save document to buffer
            buffer = io.BytesIO()
            document.save(buffer)
            buffer.seek(0)

            # Send file
            return send_file(buffer, as_attachment=True, download_name=f'report_{form_data["case_number"]}.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        except Exception as e:
            print(f"Error processing form: {str(e)}")
            flash('An error occurred while processing your form.', 'error')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
