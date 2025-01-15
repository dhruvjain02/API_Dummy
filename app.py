from flask import Flask, render_template, request, redirect, send_file, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from docx import Document
from docx.shared import Inches
import io
from datetime import datetime
import base64
import gridfs
import os

app = Flask(__name__)

# MongoDB setup with timeout settings
app.config["MONGO_URI"] = "mongodb+srv://harshal:Harshal2022@cluster0.u5i2m.mongodb.net/form?retryWrites=true&w=majority&appName=Cluster0"
app.config["MONGO_CONNECT_TIMEOUT_MS"] = 30000  # 30 seconds timeout
mongo = PyMongo(app)

# Create GridFS instance within request context
def get_gridfs():
    return gridfs.GridFS(mongo.db)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            # Get GridFS instance
            fs = get_gridfs()
            
            # Extract form data
            form_data = {
                "case_number": request.form.get('case_number'),
                # ... [rest of form data extraction remains the same]
            }

            # Handle image uploads with proper error handling
            image_ids = []
            try:
                print("Files received:", request.files.keys())
                angles = [0, 30, 60, 90, 30, 60, 90]
                
                for i in range(7):
                    image_key = f'image_{i}'
                    if image_key in request.files:
                        image_file = request.files[image_key]
                        if image_file and image_file.filename:
                            image_data = image_file.read()
                            file_id = fs.put(
                                image_data,
                                filename=f"device_image_{i}.jpg",
                                metadata={
                                    "case_number": form_data["case_number"],
                                    "angle": angles[i],
                                    "flipped": i >= 4
                                }
                            )
                            image_ids.append(file_id)
                            print(f"Stored image {i} with ID: {file_id}")
            except Exception as e:
                print(f"Error processing images: {str(e)}")
                raise

            # Add image IDs to form data
            form_data["image_ids"] = image_ids

            # Insert data into MongoDB with error handling
            try:
                mongo.db.device_info.insert_one(form_data)
            except Exception as e:
                print(f"Error inserting into MongoDB: {str(e)}")
                raise

            # Load template from correct path
            template_path = os.path.join(os.path.dirname(__file__), 'Report Format.docx')
            try:
                document = Document(template_path)
            except Exception as e:
                print(f"Error loading template: {str(e)}")
                raise

            # Process document with proper error handling
            try:
                # [Document processing code remains the same]
                pass
            except Exception as e:
                print(f"Error processing document: {str(e)}")
                raise

            # Save document with proper cleanup
            try:
                buffer = io.BytesIO()
                document.save(buffer)
                buffer.seek(0)
                
                # Create response with explicit content type and filename
                filename = f'report_{form_data["case_number"]}.docx'
                response = send_file(
                    buffer,
                    as_attachment=True,
                    download_name=filename,
                    mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                
                # Add cache control headers
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                
                return response
            except Exception as e:
                print(f"Error saving document: {str(e)}")
                raise
            finally:
                buffer.close()

        except Exception as e:
            print(f"Error processing form: {str(e)}")
            app.logger.error(f"Error processing form: {str(e)}")
            flash('An error occurred while processing your form', 'error')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
