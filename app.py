from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from docx import Document
from docx.shared import Inches
import os
import io

app = Flask(__name__)

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

        # Log received form data
        print("Form data received for replacement:")
        for key, value in form_data.items():
            print(f"Key: {key}, Value: {value}")

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

        # Insert images
        image_keys = [
            'image_0', 'image_30', 'image_60', 'image_90', 'image_240', 'image_270', 'image_360'
        ]
        image_placeholders = [
            '[0]', '[30]', '[60]', '[90]', '[240]', '[270]', '[360]'
        ]
        for placeholder, image_key in zip(image_placeholders, image_keys):
            if image_key in request.files:
                image_file = request.files[image_key]
                if image_file and image_file.filename:
                    # Replace placeholder and insert image
                    for table in document.tables:
                        for row in table.rows:
                            for cell in row.cells:
                                if placeholder in cell.text:
                                    cell.text = ""
                                    run = cell.paragraphs[0].add_run()

                                    # Reset the file pointer before reading
                                    image_file.stream.seek(0)
                                    image_stream = io.BytesIO(image_file.read())
                                    run.add_picture(image_stream, width=Inches(2.5))
                                    print(f"Inserted image for {image_key} at {placeholder}")


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
