from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from docx import Document
from docx.shared import Inches
import os
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

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
            "Insert Color": request.form.get('color', "N/A"),
            "Safety Glass Yes or No": request.form.get('safety_glass', "N/A"),
            "Back Cover Yes or No": request.form.get('back_cover', "N/A"),
            "Insert RAM": request.form.get('ram', "N/A"),
            "Insert Internal Memory": request.form.get('internal_memory', "N/A"),
            "Insert Camera Details": request.form.get('camera_specs', "N/A"),
            "Insert Cameras Check": request.form.get('cameras_check', "N/A"),
            "Insert Battery Percentage": request.form.get('battery_percentage', "N/A"),
            "Insert SIM Slots": request.form.get('sim_slots', "N/A"),
            "Insert SIM Provider": request.form.get('sim_provider', "N/A"),
            "Insert Wi-Fi Status": request.form.get('wifi_connected', "N/A"),
            "Insert Bluetooth Status": request.form.get('bluetooth_status', "N/A"),
            "Insert SD Card Present": request.form.get('sd_card', "N/A"),
            "Insert SD Capacity": request.form.get('sd_capacity', "N/A"),
            "Insert Mobile Uptime": request.form.get('mobile_uptime', "N/A"),
            "Insert Time Zone": request.form.get('time_zone', "N/A"),
            "Insert Language": request.form.get('language', "N/A"),
            "Insert Installed Apps": request.form.get('installed_apps', "N/A"),
            "Insert Geo Location": request.form.get('geo_location', "N/A"),
            "Insert Build Number": request.form.get('build_no', "N/A"),
            "Insert Kernel Version": request.form.get('kernel_version', "N/A"),
            "Insert ICCID": request.form.get('iccid', "N/A"),
            "Insert IMSI": request.form.get('imsi', "N/A"),
            "Insert MEID": request.form.get('meid', "N/A"),
            "Insert Airplane Mode": request.form.get('airplane_mode', "N/A")
        }

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
                    # Handle text replacements
                    for key, value in form_data.items():
                        placeholder = f"[{key}]"
                        if placeholder in cell.text:
                            cell.text = cell.text.replace(placeholder, value)

        # Define image mapping for sequential angles
        angle_mapping = [
            ('image_0', '[0]'),    # 0°
            ('image_1', '[30]'),   # 30°
            ('image_2', '[60]'),   # 60°
            ('image_3', '[90]'),   # 90°
            ('image_4', '[240]'),  # 240°
            ('image_5', '[270]'),  # 270°
            ('image_6', '[360]')   # 360°
        ]

        # Process each image
        for image_key, placeholder in angle_mapping:
            if image_key in request.files:
                image_file = request.files[image_key]
                if image_file and image_file.filename:
                    print(f"Processing {image_key} for angle placeholder {placeholder}")
                    
                    # Find and replace image in all tables
                    for table in document.tables:
                        for row in table.rows:
                            for cell in row.cells:
                                if placeholder in cell.text:
                                    try:
                                        # Clear the cell
                                        cell.text = ""
                                        paragraph = cell.paragraphs[0]
                                        run = paragraph.add_run()
                                        
                                        # Reset file pointer and read image
                                        image_file.seek(0)
                                        image_data = io.BytesIO(image_file.read())
                                        
                                        # Add image with consistent size
                                        run.add_picture(image_data, width=Inches(2.5))
                                        print(f"Successfully inserted {image_key} at {placeholder}")
                                    except Exception as e:
                                        print(f"Error processing image {image_key}: {e}")
                                        continue

        # Save the document to buffer
        buffer = io.BytesIO()
        document.save(buffer)
        buffer.seek(0)

        # Generate filename with case number
        filename = f'report_{form_data["Insert Case Number"]}.docx'

        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        print(f"Error generating report: {e}")
        flash("An error occurred while generating your report. Please try again.", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
