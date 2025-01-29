# Mobile Device Information Capture System

A web application for capturing and documenting mobile device information for forensic purposes. The system allows users to input device details, capture photos from specific angles, and generate standardized reports.

## Features

- Multi-step form for device information capture
- Device photography with angle guides (0°, 30°, 60°, 90°)
- Automated report generation in DOCX format
- User-friendly interface
- Real-time validation

## Installation

### Windows

1. Make sure Python 3.7 or higher is installed:
   ```
   python --version
   ```

2. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-folder>
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Linux/Mac

1. Make sure Python 3.7 or higher is installed:
   ```
   python3 --version
   ```

2. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-folder>
   ```

3. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Create required directories:
   ```
   mkdir -p static/images templates
   ```

2. Set environment variables:
   - Windows:
     ```
     set FLASK_APP=app.py
     set FLASK_ENV=development
     ```
   - Linux/Mac:
     ```
     export FLASK_APP=app.py
     export FLASK_ENV=development
     ```

3. Start the application:
   ```
   python app.py
   ```

4. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

## Usage

1. Click "Let's Get Started" on the landing page
2. Fill in case information
3. Follow the photography guide to capture device images
4. Complete device specifications
5. Submit the form to generate report

## Project Structure
```
project/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── Report Format.docx     # Report template
├── static/
│   └── images/           # Static assets
└── templates/            # HTML templates
    ├── form.html
    ├── index.html
    └── thankyou.html
```

## Troubleshooting

1. **ModuleNotFoundError**:
   - Make sure virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

2. **Template Not Found**:
   - Verify directories are created: `static/images` and `templates`
   - Check file paths are correct

3. **Camera Not Working**:
   - Allow camera permissions in browser
   - Try a different browser (Chrome recommended)

## Support

For any queries, contact:

**Dhruv Jain**  

## License

This project is licensed under the MIT License.
