from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import os
from werkzeug.utils import secure_filename
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kpi_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Database Models
class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    center_name = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(20), nullable=False)  # Junior, Senior, Both
    total_students = db.Column(db.Integer, nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tutor {self.name} - {self.center_name}>'

class StudentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    center_name = db.Column(db.String(100), nullable=False)
    class_x_passed = db.Column(db.Boolean, default=False)
    academic_year = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class KPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_students = db.Column(db.Integer, default=0)
    total_tutors = db.Column(db.Integer, default=0)
    total_classrooms = db.Column(db.Integer, default=0)
    senior_classroom_percentage = db.Column(db.Float, default=0.0)
    class_x_passed_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# KPI Calculation Functions
def calculate_kpis(month, year):
    """Calculate KPIs for a specific month and year"""
    
    # Get data for the specified month and year
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date()
    else:
        end_date = datetime(year, month + 1, 1).date()
    
    # Filter tutors for the month
    tutors_data = Tutor.query.filter(
        Tutor.attendance_date >= start_date,
        Tutor.attendance_date < end_date
    ).all()
    
    if not tutors_data:
        return None
    
    # A. Number of Students
    total_students = sum(tutor.total_students for tutor in tutors_data)
    
    # B. Number of Tutors
    unique_tutors = len(set(tutor.name for tutor in tutors_data))
    
    # C. Number of Classrooms
    unique_classrooms = len(set((tutor.center_name, tutor.section) for tutor in tutors_data))
    
    # D. Percentage of Senior Classrooms
    senior_classrooms = len(set(
        (tutor.center_name, tutor.section) 
        for tutor in tutors_data 
        if tutor.section in ['Senior', 'Both']
    ))
    senior_percentage = (senior_classrooms / unique_classrooms * 100) if unique_classrooms > 0 else 0
    
    # E. Number of students who passed Class X (placeholder - to be integrated)
    class_x_passed_count = 0  # This will be integrated with results data
    
    return {
        'total_students': total_students,
        'total_tutors': unique_tutors,
        'total_classrooms': unique_classrooms,
        'senior_classroom_percentage': round(senior_percentage, 1),
        'class_x_passed_count': class_x_passed_count
    }

def get_monthly_data():
    """Get KPI data for dashboard charts"""
    months = []
    students_data = []
    tutors_data = []
    senior_percentage_data = []
    
    # Get last 6 months of data
    current_date = datetime.now()
    for i in range(6):
        month_date = current_date.replace(day=1)
        month_date = month_date.replace(month=((month_date.month - i - 1) % 12) + 1)
        if month_date.month > current_date.month:
            month_date = month_date.replace(year=month_date.year - 1)
        
        month_name = month_date.strftime('%B %Y')
        kpis = calculate_kpis(month_date.month, month_date.year)
        
        if kpis:
            months.append(month_name)
            students_data.append(kpis['total_students'])
            tutors_data.append(kpis['total_tutors'])
            senior_percentage_data.append(kpis['senior_classroom_percentage'])
    
    return {
        'months': months[::-1],  # Reverse to show oldest first
        'students': students_data[::-1],
        'tutors': tutors_data[::-1],
        'senior_percentage': senior_percentage_data[::-1]
    }

# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/kpi-data')
def api_kpi_data():
    """API endpoint for KPI data"""
    monthly_data = get_monthly_data()
    return jsonify(monthly_data)

@app.route('/api/current-kpis')
def api_current_kpis():
    """API endpoint for current month KPIs"""
    current_date = datetime.now()
    kpis = calculate_kpis(current_date.month, current_date.year)
    return jsonify(kpis if kpis else {})

@app.route('/tutor-input', methods=['GET', 'POST'])
def tutor_input():
    """Tutor input form"""
    if request.method == 'POST':
        try:
            # Get form data
            tutor_name = request.form['name']
            center_name = request.form['center_name']
            section = request.form['section']
            total_students = int(request.form['total_students'])
            attendance_date = datetime.strptime(request.form['attendance_date'], '%Y-%m-%d').date()
            
            # Validate total students (5-50 as per document)
            if total_students < 5 or total_students > 50:
                flash('Total students must be between 5 and 50', 'error')
                return redirect(url_for('tutor_input'))
            
            # Create new tutor record
            new_tutor = Tutor(
                name=tutor_name,
                center_name=center_name,
                section=section,
                total_students=total_students,
                attendance_date=attendance_date
            )
            
            db.session.add(new_tutor)
            db.session.commit()
            
            flash('Tutor data submitted successfully!', 'success')
            return redirect(url_for('tutor_input'))
            
        except Exception as e:
            flash(f'Error submitting data: {str(e)}', 'error')
            return redirect(url_for('tutor_input'))
    
    return render_template('tutor_input.html')

@app.route('/upload-csv', methods=['GET', 'POST'])
def upload_csv():
    """CSV upload functionality"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            try:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Read CSV and process data
                df = pd.read_csv(filepath)
                
                # Expected columns: name, center_name, section, total_students, attendance_date
                required_columns = ['name', 'center_name', 'section', 'total_students', 'attendance_date']
                
                if not all(col in df.columns for col in required_columns):
                    flash('CSV must contain columns: name, center_name, section, total_students, attendance_date', 'error')
                    return redirect(request.url)
                
                # Process each row
                for _, row in df.iterrows():
                    try:
                        attendance_date = pd.to_datetime(row['attendance_date']).date()
                        total_students = int(row['total_students'])
                        
                        if total_students < 5 or total_students > 50:
                            continue  # Skip invalid entries
                        
                        new_tutor = Tutor(
                            name=row['name'],
                            center_name=row['center_name'],
                            section=row['section'],
                            total_students=total_students,
                            attendance_date=attendance_date
                        )
                        db.session.add(new_tutor)
                        
                    except Exception as e:
                        continue  # Skip problematic rows
                
                db.session.commit()
                flash(f'Successfully imported {len(df)} records from CSV!', 'success')
                
                # Clean up uploaded file
                os.remove(filepath)
                
            except Exception as e:
                flash(f'Error processing CSV: {str(e)}', 'error')
        
        else:
            flash('Please upload a CSV file', 'error')
        
        return redirect(url_for('upload_csv'))
    
    return render_template('upload_csv.html')

@app.route('/reports')
def reports():
    """Reports page"""
    # Get current month KPIs
    current_date = datetime.now()
    current_kpis = calculate_kpis(current_date.month, current_date.year)
    
    # Get recent tutor entries
    recent_tutors = Tutor.query.order_by(Tutor.created_at.desc()).limit(10).all()
    
    return render_template('reports.html', current_kpis=current_kpis, recent_tutors=recent_tutors)

@app.route('/api/tutor-stats')
def api_tutor_stats():
    """API endpoint for tutor statistics"""
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # Get tutor data for current month
    start_date = datetime(current_year, current_month, 1).date()
    if current_month == 12:
        end_date = datetime(current_year + 1, 1, 1).date()
    else:
        end_date = datetime(current_year, current_month + 1, 1).date()
    
    tutors_data = Tutor.query.filter(
        Tutor.attendance_date >= start_date,
        Tutor.attendance_date < end_date
    ).all()
    
    # Calculate statistics
    total_centers = len(set(tutor.center_name for tutor in tutors_data))
    section_breakdown = {}
    for tutor in tutors_data:
        section_breakdown[tutor.section] = section_breakdown.get(tutor.section, 0) + 1
    
    return jsonify({
        'total_centers': total_centers,
        'section_breakdown': section_breakdown,
        'total_entries': len(tutors_data)
    })

@app.route('/api/recent-activity')
def recent_activity():
    """Get recent tutor activity"""
    try:
        # Get last 10 tutor entries
        recent_tutors = Tutor.query.order_by(Tutor.attendance_date.desc()).limit(10).all()
        
        activity_data = []
        for tutor in recent_tutors:
            activity_data.append({
                'name': tutor.name,
                'center_name': tutor.center_name,
                'section': tutor.section,
                'total_students': tutor.total_students,
                'attendance_date': tutor.attendance_date.strftime('%Y-%m-%d')
            })
        
        return jsonify(activity_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Get local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("🚀 Starting KPI Application for sharing...")
    print(f"📱 Local access: http://127.0.0.1:5000")
    print(f"🌐 Network access: http://{local_ip}:5000")
    print(f"📧 Share this URL with others: http://{local_ip}:5000")
    print("\n✅ Application is now accessible to anyone on your network!")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
