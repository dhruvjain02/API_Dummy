
# Mobile Device Information Capture System

This project is a web application designed to capture and process mobile device information for forensic purposes. It uses Flask as the backend framework and MongoDB as the database. The frontend is a multi-step HTML form that allows users to input device details, upload images of the device at specific angles, and generate a report.

---

## Features

- **Multi-Step Form**: Collects detailed information about the mobile device, including system, network, and physical specifications.
- **Image Capture**: Captures device images at specific angles (0°, 30°, 60°, 90°, and flipped views).
- **Report Generation**: Generates a Word report (`.docx`) using a pre-defined template with placeholders replaced by form data and embedded images.
- **MongoDB Integration**: Stores form data and uploaded images in MongoDB using GridFS for image storage.
- **Responsive Design**: Frontend designed for ease of use on multiple devices.

---

## Prerequisites

- Python 3.7+
- MongoDB Atlas (or local MongoDB setup)
- Required Python packages (see [Installation](#installation))

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up MongoDB**
   - Update `app.config["MONGO_URI"]` in `app.py` with your MongoDB connection string.

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the App**
   Open a browser and navigate to `http://127.0.0.1:5000`.

---

## Usage

### Frontend Form (`form.html`)

1. **Case Details**:
   - Input case number, date of report, and preparer's details.

2. **Device Photography**:
   - Capture device images at specified angles using the camera preview.

3. **Device Specifications**:
   - Input details such as model, RAM, internal memory, and camera specifications.

4. **Connectivity & Storage**:
   - Provide details about Wi-Fi, Bluetooth, and SD card status.

5. **System Information**:
   - Input uptime, time zone, language, installed apps, and geolocation status.

6. **Network & Identifiers**:
   - Input ICCID, IMSI, MEID, and airplane mode status.

7. Submit the form to generate a report and download it.

---

## Key Files

1. **Backend: `app.py`**
   - Flask application that handles form submission, image uploads, and report generation.

2. **Frontend: `form.html`**
   - Multi-step form with JavaScript for dynamic navigation and validations.

---

## MongoDB Integration

- **GridFS**: Used to store and retrieve device images.
- **Collections**:
  - `device_info`: Stores metadata and form data.

---

## Report Generation

- **Template**: `Report Format.docx` is used as a base.
- **Dynamic Replacement**: Placeholders in the template are replaced with form data.
- **Images**: Captured images are embedded in the report.

---

## Technologies Used

- **Backend**: Flask, PyMongo, GridFS
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MongoDB Atlas
- **Report Generation**: Python-docx

---

## Future Enhancements

- Add error handling for camera access issues.
- Implement additional validations on form inputs.
- Optimize MongoDB queries and improve GridFS image handling.
- Add support for exporting reports in PDF format.

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

## Contact

For any queries, contact the developer:

**Harshal Thoke**  
[Portfolio](https://harshuthoke.github.io/Harshal_Portfolio/7)
