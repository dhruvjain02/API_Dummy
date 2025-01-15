@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            # Extract form data (keeping existing form_data dictionary code)
            form_data = {
                # ... (existing form data extraction)
            }

            # Handle image uploads with proper error checking
            image_ids = []
            print("Files received:", request.files.keys())
            angles = [0, 30, 60, 90, 30, 60, 90]  # Last three are for flipped
            
            for i in range(7):
                image_key = f'image_{i}'
                if image_key in request.files:
                    image_file = request.files[image_key]
                    if image_file and image_file.filename:
                        try:
                            # Read and verify image data
                            image_data = image_file.read()
                            if not image_data:
                                raise ValueError(f"Empty image data for {image_key}")
                            
                            # Store in GridFS with proper error handling
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
                            print(f"Error processing image {i}: {str(e)}")
                            # Continue with other images if one fails
                            continue

            # Add image IDs to form data
            form_data["image_ids"] = image_ids

            # Insert data into MongoDB
            mongo.db.device_info.insert_one(form_data)

            # Generate report with proper error handling
            try:
                document = Document('./Report Format.docx')
                
                # Helper function to replace text in tables
                def replace_table_placeholder(table, placeholder, value):
                    if value is None:
                        value = ""  # Handle None values gracefully
                    for row in table.rows:
                        for cell in row.cells:
                            if placeholder in cell.text:
                                cell.text = cell.text.replace(placeholder, str(value))

                # Update document content with proper error checking
                for table in document.tables:
                    if len(table.rows) >= 8:  # Table with 7 images plus header
                        image_placeholders = {
                            '[0]': 0, '[30]': 1, '[60]': 2, '[90]': 3,
                            '[240]': 4, '[270]': 5, '[360]': 6
                        }
                        
                        for placeholder, idx in image_placeholders.items():
                            if idx < len(image_ids):
                                try:
                                    # Get image from GridFS with proper error handling
                                    image_data = fs.get(image_ids[idx])
                                    if not image_data:
                                        continue
                                        
                                    img_stream = io.BytesIO(image_data.read())
                                    
                                    # Find and replace placeholder with image
                                    for row in table.rows:
                                        for cell in row.cells:
                                            if placeholder in cell.text:
                                                cell.text = ""
                                                run = cell.paragraphs[0].add_run()
                                                try:
                                                    run.add_picture(
                                                        img_stream, 
                                                        width=Inches(2.5)
                                                    )
                                                except Exception as e:
                                                    print(f"Error adding picture: {str(e)}")
                                                    continue
                                except Exception as e:
                                    print(f"Error processing GridFS image {idx}: {str(e)}")
                                    continue

                    # Update other placeholders
                    for field, value in form_data.items():
                        if field != "image_ids":
                            replace_table_placeholder(table, f'[Insert {field.title().replace("_", " ")}]', value)

                # Save document to buffer with proper error handling
                buffer = io.BytesIO()
                document.save(buffer)
                buffer.seek(0)

                # Send file with proper headers
                return send_file(
                    buffer,
                    as_attachment=True,
                    download_name=f'report_{form_data["case_number"]}.docx',
                    mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )

            except Exception as e:
                print(f"Error generating document: {str(e)}")
                raise

        except Exception as e:
            print(f"Error processing form: {str(e)}")
            app.logger.error(f"Error processing form: {str(e)}")
            flash('An error occurred while processing your form', 'error')
            return redirect(url_for('index'))
