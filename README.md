# Student Learning Activity and Course Relationship Tracker

## Project Overview

The Student Learning Activity and Course Relationship Tracker is a web-based application developed using Python, Flask, and Neo4j.

The system allows users to manage students, courses, enrollments, and learning activities. It uses Neo4j, a NoSQL graph database, to store information and represent relationships between students, courses, and learning activities.

The application also provides a dashboard and a learning history feature to track students' academic activities and study time.

## Team Members

- Mahek Patel
- Yashvi Patel
- Rishikesh Pathak

## Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | Neo4j |
| Query Language | Cypher |
| Database Driver | Neo4j Python Driver |
| Code Editor | Visual Studio Code |
| Database Management | Neo4j Desktop |
| Version Control | Git and GitHub |

## Project Features

### 1. Student Management
- Add, view, update, and delete students.
- View courses enrolled by each student.

### 2. Course Management
- Add, view, update, and delete courses.

### 3. Enrollment Management
- Enroll students in courses.
- View and remove enrollments.

### 4. Learning Activity Management
- Add, view, update, and delete learning activities.
- Associate activities with students and courses.

### 5. Learning History
- View activities completed by individual students.
- Calculate total activities and study time.
- Display courses associated with completed activities.

### 6. Dashboard
- Display student, course, and learning activity statistics.

## Neo4j Database Design

The application uses three node types:

1. Student
2. Course
3. LearningActivity

### Relationships

- ENROLLED_IN: Connects students to courses.
- COMPLETED: Connects students to learning activities.
- FOR_COURSE: Connects learning activities to courses.

### Graph Structure

Student → ENROLLED_IN → Course
Student → COMPLETED → LearningActivity → FOR_COURSE → Course

## Database Operations

The application supports the following Neo4j operations:

- CREATE: Add students, courses, enrollments, and activities.
- READ: Retrieve records from the database.
- UPDATE: Modify existing student, course, and activity information.
- DELETE: Remove records and relationships.
- GRAPH TRAVERSAL: Retrieve student learning history.
- AGGREGATION: Calculate total activities and study duration.

## Installation and Setup Instructions

Follow these steps to recreate and run the project.

### Prerequisites

Install the following software:

- Python 3.14
- Neo4j Desktop with a local Neo4j database instance
- Visual Studio Code
- Git 

### Step 1: Download the Project

Clone the GitHub repository:

```bash
git clone https://github.com/Mahek1101/Student-Learning-Activity-Tracker.git
```

Navigate to the project directory:

```bash
cd Student-Learning-Activity-Tracker
```

### Step 2: Install and Configure Neo4j

1. Download and install Neo4j Desktop.
2. Create a local Neo4j database instance.
3. Name the instance `StudentLearningTracker`.
4. Set a password for the `neo4j` user.
5. Start the database instance.
6. Open the Neo4j Query interface.

The application uses the following connection settings:

- URI: `bolt://localhost:7687`
- Username: `neo4j`
- Database: `neo4j`

Ensure that your Neo4j instance uses the same Bolt port.

### Step 3: Create the Database Structure and Sample Data

1. Open `neo4j_setup.cypher` from the project folder.
2. Copy the Cypher statements.
3. Open the Neo4j Query interface.
4. Execute the statements in order, one at a time.

The setup script creates:

- 6 Student nodes
- 5 Course nodes
- 6 LearningActivity nodes
- 12 ENROLLED_IN relationships
- 6 COMPLETED relationships
- 6 FOR_COURSE relationships

Total: 17 nodes and 24 relationships.

Run the setup script on a fresh database to avoid modifying existing data.

### Step 4: Create a Python Virtual Environment

Open a terminal in the project directory.

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 5: Install Python Dependencies

With the virtual environment activated, run:

```bash
python -m pip install -r requirements.txt
```

This installs Flask and the Neo4j Python Driver.

### Step 6: Configure the Neo4j Password

The application reads the Neo4j password from an environment variable.

On macOS or Linux:

```bash
export NEO4J_PASSWORD='YOUR_NEO4J_PASSWORD'
```

On Windows PowerShell:

```powershell
$env:NEO4J_PASSWORD = 'YOUR_NEO4J_PASSWORD'
```

### Step 7: Run the Flask Application

Make sure the Neo4j database is running.

In the terminal, execute:

```bash
python app.py
```
Open your web browser and enter:

`http://127.0.0.1:5000/`

Note: This is a local application. The Flask server and Neo4j database must be running on your computer to access it.

### Step 8: Test the Application

After launching the application, verify the following features:

1. Dashboard: View database statistics.
2. Students: Add, view, edit, and delete students.
3. Courses: Add, view, edit, and delete courses.
4. Enrollments: Enroll students and remove enrollments.
5. Learning Activities: Record, view, edit, and delete activities.
6. Learning History: Select a student to view completed activities and study statistics.

### Step 9: Demonstrate Neo4j Queries

Open `neo4j_queries.cypher` to find demonstration queries.

These queries allow you to:

- Display all students, courses, and learning activities.
- Visualize the complete database graph.
- Display student enrollment relationships.
- Display learning activity relationships.
- Retrieve individual student learning histories.
- Count nodes and relationships.

Execute the queries individually in the Neo4j Query interface.


## Project Structure

```text
project/
│
├── app.py
├── templates/
│   ├── index.html
│   ├── students.html
│   ├── edit_student.html
│   ├── courses.html
│   ├── edit_course.html
│   ├── enrollments.html
│   ├── activities.html
│   ├── edit_activity.html
│   └── history.html
│
├── neo4j_setup.cypher
├── neo4j_queries.cypher
├── requirements.txt
├── Project_Report.pdf
├── Project_Presentation.pptx
├── Student_Learning_Tracker_Project_Report.docx
├── Neo4j_initial_graph.png
├── visualisation.png
├── visualisation1.png
├── .gitignore
└── README.md
```

## Security Notes

- Database passwords are provided through environment variables.
- The `.venv` directory is excluded from Git.
- Environment files containing secrets are excluded through `.gitignore`.
- Use a separate database for testing or recreating the sample data.