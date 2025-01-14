from flask import Flask, render_template, request, redirect, send_file, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from docx import Document
from docx.shared import Inches
import io
import os
import gridfs

app = Flask(__name__)

# MongoDB setup
app.config["MONGO_URI"] = "mongodb+srv://harshal:Harshal2022@cluster0.u5i2m.mongodb.net/form?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)

# Path to Report Format
REPORT_TEMPLATE = os.path.join(os.getcwd(), 'Report Format.docx')

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
                "model": request.form.get('model'),
                "color": request.form.get('color'),
                "safety_glass": request.form.get('safety_glass'),
                "back_cover": request.form.get('back_cover'),
                "ram": request.form.get('ram'),
                "internal_memory": request.form.get('internal_memory'),
                "camera_specs": request.form.get('camera_specs'),
                "cameras_check": request.form.get('cameras_check'),
                "battery_percentage": request.form.get('battery_percentage'),
                "sim_slots": request.form.get('sim_slots'),
                "sim_provider": request.form.get('sim_provider'),
                "wifi_connected": request.form.get('wifi_connected'),
                "bluetooth_status": request.form.get('bluetooth_status'),
                "sd_card": request.form.get('sd_card'),
                "sd_capacity": request.form.get('sd_capacity'),
                "mobile_uptime": request.form.get('mobile_uptime'),
                "time_zone": request.form.get('time_zone'),
                "language": request.form.get('language'),
                "installed_apps": request.form.get('installed_apps'),
                "geo_location": request.form.get('geo_location'),
                "build_no": request.form.get('build_no'),
                "kernel_version": request.form.get('kernel_version'),
                "iccid": request.form.get('iccid'),
                "imsi": request.form.get('imsi'),
                "meid": request.form.get('meid'),
                "airplane_mode": request.form.get('airplane_mode')
            }

            # Log received data for debugging
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
                        image_data = image_file.read()
                        file_id = fs.put(
                            image_data,
                            filename=f"device_image_{i}.jpg",
                            metadata={"case_number": form_data["case_number"], "angle": i}
                        )
                        image_ids.append(file_id)

            form_data["image_ids"] = image_ids
            mongo.db.device_info.insert_one(form_data)

            # Generate report
            if not os.path.exists(REPORT_TEMPLATE):
                raise FileNotFoundError(f"Report template not found at {REPORT_TEMPLATE}")

            document = Document(REPORT_TEMPLATE)

            # Replace placeholders in paragraphs
            for para in document.paragraphs:
                for key, value in form_data.items():
                    placeholder = f"[{key}]"
                    if placeholder in para.text:
                        para.text = para.text.replace(placeholder, str(value))

            # Replace placeholders in tables
            for table in document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for key, value in form_data.items():
                            placeholder = f"[{key}]"
                            if placeholder in cell.text:
                                cell.text = cell.text.replace(placeholder, str(value))

            # Insert images into the report
            image_placeholders = {
                '[0]': 0, '[30]': 1, '[60]': 2, '[90]': 3,
                '[240]': 4, '[270]': 5, '[360]': 6
            }
            for table in document.tables:
                for placeholder, idx in image_placeholders.items():
                    if idx < len(image_ids):
                        try:
                            image_data = fs.get(image_ids[idx])
                            img_stream = io.BytesIO(image_data.read())
                            for row in table.rows:
                                for cell in row.cells:
                                    if placeholder in cell.text:
                                        cell.text = ""
                                        run = cell.paragraphs[0].add_run()
                                        run.add_picture(img_stream, width=Inches(2.5))
                        except Exception as e:
                            print(f"Error inserting image {idx}: {e}")

            # Save the report to a temporary directory
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
            flash('An error occurred while processing your form', 'error')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
