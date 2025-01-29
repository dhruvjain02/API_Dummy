# Mobile Device Information Capture System

A comprehensive web application designed for forensic documentation of mobile devices. This Flask-based system enables detailed device information capture, systematic photography, and automated report generation in DOCX format.

## Features

- **Multi-Step Form Interface**
  - Structured data collection across multiple categories
  - Real-time validation and error checking
  - Responsive design for various screen sizes

- **Device Photography System**
  - Systematic capture of device images at specific angles (0°, 30°, 60°, 90°, and flipped views)
  - Live camera preview with angle guides
  - Image quality preservation for documentation

- **Automated Report Generation**
  - Generates professional DOCX reports using customizable templates
  - Automatically embeds captured images
  - Standardized formatting for forensic documentation

- **Comprehensive Data Collection**
  - Device specifications and physical characteristics
  - Network and connectivity information
  - System information and identifiers
  - Security and status indicators

## Prerequisites

- Python 3.7+
- Camera access (built-in or external) for device photography
- Required Python packages (specified in requirements.txt)
- Sufficient storage space for image processing
- Modern web browser with JavaScript enabled

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Directory Structure**
   ```bash
   mkdir -p static/images
   mkdir -p templates
   ```

5. **Configure Template**
   - Ensure "Report Format.docx" is placed in the root directory
   - Verify template contains correct placeholder tags

6. **Set Environment Variables**
   ```bash
   # Development environment
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

7. **Run the Application**
   ```bash
   python app.py
   ```

## Usage

### Landing Page
- Access the application at `http://localhost:5000`
- Click "Let's Get Started" to begin the documentation process

### Documentation Process

1. **Case Information**
   - Enter case number
   - Input report date
   - Provide preparer's information

2. **Device Photography**
   - Follow the angle guides for each required photo
   - Required angles: 0°, 30°, 60°, 90°, and flipped views
   - Verify image quality before proceeding

3. **Device Specifications**
   - Document physical characteristics
   - Record device model and specifications
   - Note safety features and accessories

4. **System Information**
   - Record software versions
   - Document system settings
   - List installed applications

5. **Network & Security**
   - Document connectivity status
   - Record device identifiers
   - Note security settings

### Report Generation
- System automatically generates a DOCX report
- Report includes all documented information and photos
- Downloaded automatically upon form submission

## Technical Details

### Security Measures
- Maximum file size: 16MB
- Allowed image formats: .png, .jpg, .jpeg
- Input validation on all fields
- Secure file handling

### Error Handling
- Comprehensive error logging
- User-friendly error messages
- Automatic cleanup of temporary files

### File Structure
```
project/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── Report Format.docx  # Report template
├── static/
│   └── images/        # Static assets
└── templates/         # HTML templates
    ├── form.html
    ├── index.html
    └── thankyou.html
```

## Deployment

### Development
```bash
python app.py
```

### Production (Vercel)
- Configure vercel.json settings
- Deploy using Vercel CLI or GitHub integration
- Ensure environment variables are set in Vercel dashboard

## Troubleshooting

Common Issues:
1. **Camera Access Denied**
   - Check browser permissions
   - Ensure HTTPS in production

2. **Report Generation Fails**
   - Verify template file presence
   - Check write permissions
   - Validate form data completeness

3. **Image Upload Issues**
   - Verify file size limits
   - Check supported formats
   - Ensure stable connection

## Future Enhancements

- PDF report format option
- Additional device photography angles
- Enhanced image processing capabilities
- Offline mode support
- Multi-language support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For any queries, contact the developer:

**Dhruv Jain**  
