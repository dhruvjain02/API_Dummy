from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from docx import Document
from docx.shared import Inches
import os
import shutil
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Extract form data
        form_data = {key: request.form.get(key, "N/A") for key in request.form.keys()}
        print("Form data received:", form_data)

        # Path to the report template
        REPORT_TEMPLATE = os.path.join(os.getcwd(), 'Report Format.docx')
        temp_template = '/tmp/Report Format.docx'

        # Copy the template to a temporary directory
        if os.path.exists(REPORT_TEMPLATE):
            shutil.copy(REPORT_TEMPLATE, temp_template)
            print(f"Template copied to: {temp_template}")
        else:
            raise FileNotFoundError(f"Template not found at {REPORT_TEMPLATE}")

        # Open the template document
        document = Document(temp_template)

        # Replace placeholders in paragraphs
        for para in document.paragraphs:
            for key, value in form_data.items():
                placeholder = f"[{key}]"
                if placeholder in para.text:
                    print(f"Replacing placeholder: {placeholder} with value: {value}")
                    para.text = para.text.replace(placeholder, value)

        # Replace placeholders in tables
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in form_data.items():
                        placeholder = f"[{key}]"
                        if placeholder in cell.text:
                            print(f"Replacing placeholder: {placeholder} in table cell with value: {value}")
                            cell.text = cell.text.replace(placeholder, value)

        # Save the modified report to the /tmp directory
        temp_path = '/tmp/generated_report.docx'
        document.save(temp_path)
        print(f"Report successfully saved to: {temp_path}")

        # Send the modified document as a downloadable file
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=f'report_{form_data.get("case_number", "default")}.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        print(f"Error generating the report: {e}")
        flash("An error occurred while generating your report.", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
