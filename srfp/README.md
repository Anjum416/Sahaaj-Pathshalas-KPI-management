# Sahaaj Pathshalas KPI Management System

A comprehensive web application for managing and tracking Key Performance Indicators (KPIs) for Sahaaj Pathshalas educational centers.

## Features

### 📊 KPI Dashboard
- **Real-time KPI Display**: Shows current month's KPIs in an intuitive card layout
- **Interactive Charts**: Visual representation of trends using Chart.js
  - Monthly Student Engagement Tracker
  - Tutor Deployment Pie Chart
  - Classroom Utilization Overview
  - Section-wise Distribution

### 📝 Data Input Methods
- **Manual Entry**: Web form for individual tutor data entry
- **Bulk Upload**: CSV file upload with drag-and-drop functionality
- **Data Validation**: Ensures data integrity with client and server-side validation

### 📈 KPI Calculations
The system automatically calculates 5 key metrics:
1. **Number of Students**: Total students across all centers
2. **Number of Tutors**: Unique tutors providing services
3. **Number of Classrooms**: Unique classroom configurations
4. **Percentage of Senior Classrooms**: Ratio of senior classrooms to total
5. **Class X Pass Rate**: Students who passed Class X (placeholder for future integration)

### 📋 Reports & Analytics
- **Detailed Reports**: Comprehensive breakdown of KPI calculations
- **Historical Data**: Track performance over time
- **Export Options**: CSV, Excel, and PDF export (coming soon)

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Data Processing**: Pandas

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download
```bash
# If using git
git clone <repository-url>
cd srfp

# Or simply navigate to your project directory
cd /path/to/srfp
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### Dashboard
- **View Current KPIs**: The main dashboard displays all 5 KPIs for the current month
- **Interactive Charts**: Click on chart elements for detailed information
- **Auto-refresh**: Data updates automatically every 30 seconds
- **Manual Refresh**: Use the refresh button for immediate updates

### Adding Data

#### Manual Entry
1. Click "Add Tutor Data" on the dashboard
2. Fill in the required fields:
   - **Tutor Name**: Full name of the tutor
   - **Center Name**: Name of the educational center
   - **Section**: Junior, Senior, or Both
   - **Total Students**: Number of students (5-50 range)
   - **Attendance Date**: Date of attendance
3. Click "Submit" to save the data

#### Bulk Upload via CSV
1. Click "Upload CSV" on the dashboard
2. Prepare your CSV file with these columns:
   ```
   name,center_name,section,total_students,attendance_date
   ```
3. Drag and drop or select your CSV file
4. Click "Upload" to process the data

### Reports
- **KPI Summary**: View detailed breakdown of each KPI calculation
- **Recent Entries**: See the latest tutor data entries
- **Export Options**: Download data in various formats (coming soon)

## Data Structure

### Tutor Model
```python
{
    'id': 'Primary key',
    'name': 'Tutor name',
    'center_name': 'Center name',
    'section': 'Junior/Senior/Both',
    'total_students': 'Number of students (5-50)',
    'attendance_date': 'Date of attendance'
}
```

### KPI Definitions
1. **Number of Students**: Sum of all students across all tutors
2. **Number of Tutors**: Count of unique tutor names
3. **Number of Classrooms**: Count of unique (center, section) combinations
4. **Senior Classroom Percentage**: (Senior classrooms / Total classrooms) × 100
5. **Class X Pass Rate**: Number of students who passed Class X (placeholder)

## API Endpoints

- `GET /`: Main dashboard
- `GET /api/kpi-data`: Monthly KPI data for charts
- `GET /api/current-kpis`: Current month's KPI summary
- `GET /api/tutor-stats`: Section-wise tutor statistics
- `GET/POST /tutor-input`: Manual tutor data entry
- `GET/POST /upload-csv`: CSV file upload
- `GET /reports`: Detailed reports page

## File Structure

```
srfp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── dashboard.html    # Main dashboard
│   ├── tutor_input.html  # Manual entry form
│   ├── upload_csv.html   # CSV upload form
│   └── reports.html      # Reports page
└── uploads/              # Uploaded files directory
```

## Configuration

The application uses the following default configuration:
- **Database**: SQLite (`kpi_database.db`)
- **Upload Folder**: `uploads/`
- **Max File Size**: 16MB
- **Port**: 5000
- **Debug Mode**: Enabled

## Future Enhancements

- [ ] Class X results integration
- [ ] Excel and PDF export functionality
- [ ] Email notifications
- [ ] User authentication and roles
- [ ] Advanced analytics and forecasting
- [ ] Mobile-responsive design improvements
- [ ] API documentation
- [ ] Unit tests and integration tests

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Port Already in Use**: Change the port in `app.py`
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

3. **Database Errors**: Delete `kpi_database.db` and restart the application

4. **Upload Issues**: Ensure the `uploads/` directory exists and has write permissions

### Support

For technical support or feature requests, please contact the development team.

## License

This project is developed for Sahaaj Pathshalas educational centers.

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Developed for**: Sahaaj Pathshalas KPI Management
