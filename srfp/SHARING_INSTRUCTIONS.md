# How to Share and Use the KPI Application

## 🚀 **For You (Current User):**

### **To See the Application:**
1. Open your web browser
2. Go to: `http://localhost:5000` or `http://127.0.0.1:5000`
3. You'll see the KPI Dashboard

### **To Add Data:**
1. **Manual Entry**: Click "Add Tutor Data" → Fill form → Submit
2. **CSV Upload**: Click "Upload CSV" → Upload file with columns: `name,center_name,section,total_students,attendance_date`

---

## 📤 **To Share with Your Guide:**

### **Option 1: Share the Complete Folder**
1. Copy the entire `srfp` folder to a USB drive or cloud storage
2. Share the folder with your guide
3. Include these instructions

### **Option 2: Create a ZIP File**
1. Right-click on the `srfp` folder
2. Select "Send to" → "Compressed (zipped) folder"
3. Share the ZIP file

---

## 📋 **Instructions for Your Guide:**

### **Setup (One-time):**
1. **Install Python** (if not already installed): Download from python.org
2. **Extract the ZIP file** or copy the folder to their computer
3. **Open Command Prompt/Terminal** in the project folder
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Run the application**: `python app.py`

### **Using the Application:**
1. **Open browser** and go to `http://localhost:5000`
2. **Add sample data**:
   - Click "Add Tutor Data"
   - Enter: Tutor Name="Test Tutor", Center="Test Center", Section="Junior", Students=20, Date=today
   - Click Submit
3. **View Dashboard** to see KPIs update
4. **Explore all features**:
   - Dashboard with charts
   - Manual data entry
   - CSV upload
   - Reports page

### **Sample CSV Data:**
Create a file called `sample_data.csv` with this content:
```csv
name,center_name,section,total_students,attendance_date
John Doe,Center A,Junior,25,2024-12-08
Jane Smith,Center B,Senior,30,2024-12-08
Mike Johnson,Center A,Both,40,2024-12-08
```

---

## 🎯 **Key Features to Demonstrate:**

1. **Real-time KPI Dashboard** - Shows 5 key metrics
2. **Interactive Charts** - Student engagement, tutor deployment, classroom utilization
3. **Data Input Methods** - Manual entry and CSV upload
4. **Responsive Design** - Works on desktop and mobile
5. **Auto-refresh** - Data updates automatically
6. **Validation** - Ensures data quality (5-50 students range)

---

## 📞 **If Your Guide Has Issues:**

1. **Port already in use**: Change port in `app.py` line 301 to `port=5001`
2. **Missing modules**: Run `pip install -r requirements.txt`
3. **Database errors**: Delete `instance` folder and restart
4. **Browser issues**: Try different browser (Chrome, Firefox, Edge)

---

## 📁 **Files Included:**
- `app.py` - Main application
- `requirements.txt` - Python dependencies
- `README.md` - Detailed documentation
- `templates/` - Web interface files
- `kpi record.docx` - Original requirements document

**The application is ready to use and demonstrate!** 🎉
