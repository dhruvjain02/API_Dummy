from flask import Flask, render_template, request, redirect, send_file, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from docx import Document
from docx.shared import Inches
import io
from datetime import datetime
import base64
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

            # Handle image uploads
            image_ids = []
            print("Files received:", request.files.keys())
            angles = [0, 30, 60, 90, 30, 60, 90]  # Last three are for flipped
            
            for i in range(7):
                image_key = f'image_{i}'
                if image_key in request.files:
                    image_file = request.files[image_key]
                    if image_file and image_file.filename:
                        # Read the image data
                        image_data = image_file.read()
                        
                        # Store in GridFS
                        file_id = fs.put(
                            image_data,
                            filename=f"device_image_{i}.jpg",
                            metadata={
                                "case_number": form_data["case_number"],
                                "angle": i,
                                "flipped": i >= 4
                            }
                        )
                        image_ids.append(file_id)
                        print(f"Stored image {i} with ID: {file_id}")

            # Add image IDs to form data
            form_data["image_ids"] = image_ids

            # Insert data into MongoDB
            mongo.db.device_info.insert_one(form_data)

            # Generate report
            document = Document('./Report Format.docx')
            
            # Helper function to replace text in tables
            def replace_table_placeholder(table, placeholder, value):
                for row in table.rows:
                    for cell in row.cells:
                        if placeholder in cell.text:
                            # Remove any other formatting by setting plain text
                            cell.text = cell.text.replace(placeholder, str(value))

            # Update regular placeholders
            for para in document.paragraphs:
                if '[Insert Case Number]' in para.text:
                    para.text = para.text.replace('[Insert Case Number]', form_data['case_number'])
                if '[Insert Date]' in para.text:
                    para.text = para.text.replace('[Insert Date]', form_data['date_of_report'])
                if '[Insert Name and Title]' in para.text:
                    para.text = para.text.replace('[Insert Name and Title]', form_data['report_prepared_by'])

            # Find the angle detection images table and update it
            for table in document.tables:
                if len(table.rows) >= 8:  # Table with 7 images plus header
                    # Map of placeholders to image indices
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
                                
                                # Find and replace placeholder with image
                                for row in table.rows:
                                    for cell in row.cells:
                                        if placeholder in cell.text:
                                            print(f"Found placeholder {placeholder} in cell")
                                            # Clear the cell
                                            cell.text = ""
                                            # Add the image
                                            run = cell.paragraphs[0].add_run()
                                            run.add_picture(
                                                img_stream, 
                                                width=Inches(2.5)
                                            )
                            except Exception as e:
                                print(f"Error processing image {idx}: {str(e)}")

                # Update device specifications
                replace_table_placeholder(table, '[Insert Device Model]', form_data['model'])
                replace_table_placeholder(table, '[Insert Color]', form_data['color'])
                replace_table_placeholder(table, '[Safety Glass Yes or No]', form_data['safety_glass'])
                replace_table_placeholder(table, '[Back Cover Yes or No]', form_data['back_cover'])
                replace_table_placeholder(table, '[Insert RAM]', form_data['ram'])
                replace_table_placeholder(table, '[Insert Internal Memory]', form_data['internal_memory'])
                replace_table_placeholder(table, '[Insert Camera Details]', form_data['camera_specs'])
                replace_table_placeholder(table, '[Insert Cameras Check]', form_data['cameras_check'])
                replace_table_placeholder(table, '[Insert Battery Percentage]', form_data['battery_percentage'])
                replace_table_placeholder(table, '[Insert SIM Slots]', form_data['sim_slots'])
                replace_table_placeholder(table, '[Insert SIM Provider]', form_data['sim_provider'])
                replace_table_placeholder(table, '[Insert Wi-Fi Status]', form_data['wifi_connected'])
                replace_table_placeholder(table, '[Insert Bluetooth Status]', form_data['bluetooth_status'])
                replace_table_placeholder(table, '[Insert SD Card Present]', form_data['sd_card'])
                replace_table_placeholder(table, '[Insert SD Capacity]', form_data['sd_capacity'])
                replace_table_placeholder(table, '[Insert Mobile Uptime]', form_data['mobile_uptime'])
                replace_table_placeholder(table, '[Insert Time Zone]', form_data['time_zone'])
                replace_table_placeholder(table, '[Insert Language]', form_data['language'])
                replace_table_placeholder(table, '[Insert Installed Apps]', form_data['installed_apps'])
                replace_table_placeholder(table, '[Insert Geo Location]', form_data['geo_location'])
                replace_table_placeholder(table, '[Insert Build Number]', form_data['build_no'])
                replace_table_placeholder(table, '[Insert Kernel Version]', form_data['kernel_version'])
                replace_table_placeholder(table, '[Insert ICCID]', form_data['iccid'])
                replace_table_placeholder(table, '[Insert IMSI]', form_data['imsi'])
                replace_table_placeholder(table, '[Insert MEID]', form_data['meid'])
                replace_table_placeholder(table, '[Insert Airplane Mode]', form_data['airplane_mode'])

            # Save document to buffer
            buffer = io.BytesIO()
            document.save(buffer)
            buffer.seek(0)
            

            # Send file
            return send_file(buffer, as_attachment=True, download_name=f'report_{form_data["case_number"]}.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


        except Exception as e:
            print(f"Error processing form: {str(e)}")
            app.logger.error(f"Error processing form: {str(e)}")
            flash('An error occurred while processing your form', 'error')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)