from flask import Flask, render_template, request, redirect, url_for, jsonify
from neo4j import GraphDatabase
import os

app = Flask(__name__)

# Neo4j database connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")

if not NEO4J_PASSWORD:
    raise RuntimeError("Please set the NEO4J_PASSWORD environment variable.")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

@app.route("/")
def home():
    with driver.session(database="neo4j") as session:

        students = session.run(
            "MATCH (s:Student) RETURN count(s) AS total"
        ).single()["total"]

        courses = session.run(
            "MATCH (c:Course) RETURN count(c) AS total"
        ).single()["total"]

        activities = session.run(
            "MATCH (a:LearningActivity) RETURN count(a) AS total"
        ).single()["total"]

    return render_template(
        "index.html",
        students=students,
        courses=courses,
        activities=activities
    )

@app.route("/students")
def students_page():
    with driver.session(database="neo4j") as session:
        result = session.run("""
            MATCH (s:Student)
            RETURN s.student_id AS student_id,
                   s.name AS name,
                   s.email AS email
            ORDER BY s.student_id
        """)

        students = [record.data() for record in result]

    return render_template("students.html", students=students)

@app.route("/add-student", methods=["POST"])
def add_student():
    student_id = int(request.form["student_id"])
    name = request.form["name"].strip()
    email = request.form["email"].strip()

    with driver.session(database="neo4j") as session:
        session.run("""
            MERGE (s:Student {student_id: $student_id})
            SET s.name = $name,
                s.email = $email
        """,
        student_id=student_id,
        name=name,
        email=email).consume()

    return redirect(url_for("students_page"))

@app.route("/delete-student/<int:student_id>", methods=["POST"])
def delete_student(student_id):

    with driver.session(database="neo4j") as session:

        session.run("""
            MATCH (s:Student {student_id: $student_id})

            OPTIONAL MATCH (s)-[:COMPLETED]->(a:LearningActivity)

            WITH s, collect(DISTINCT a) AS activities

            FOREACH (activity IN activities |
                DETACH DELETE activity
            )

            DETACH DELETE s
        """, student_id=student_id).consume()

    return redirect(url_for("students_page"))

@app.route("/edit-student/<int:student_id>")
def edit_student(student_id):

    with driver.session(database="neo4j") as session:
        result = session.run("""
            MATCH (s:Student {student_id: $student_id})
            RETURN s.student_id AS student_id,
                   s.name AS name,
                   s.email AS email
        """, student_id=student_id)

        record = result.single()

        if record is None:
            return "Student not found", 404

        student = record.data()

    return render_template("edit_student.html", student=student)

@app.route("/update-student/<int:student_id>", methods=["POST"])
def update_student(student_id):

    name = request.form["name"].strip()
    email = request.form["email"].strip()

    with driver.session(database="neo4j") as session:
        session.run("""
            MATCH (s:Student {student_id: $student_id})
            SET s.name = $name,
                s.email = $email
        """,
        student_id=student_id,
        name=name,
        email=email).consume()

    return redirect(url_for("students_page"))

@app.route("/test-db")
def test_database():
    try:
        with driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (n) RETURN count(n) AS total"
            )
            count = result.single()["total"]

        return f"Neo4j Connected Successfully! Total Nodes: {count}"

    except Exception as e:
        return f"Database Connection Error: {e}", 500

@app.route("/courses")
def courses_page():

    with driver.session(database="neo4j") as session:
        result = session.run("""
            MATCH (c:Course)
            RETURN c.course_id AS course_id,
                   c.course_name AS course_name,
                   c.credits AS credits
            ORDER BY c.course_id
        """)

        courses = [record.data() for record in result]

    return render_template("courses.html", courses=courses)

@app.route("/add-course", methods=["POST"])
def add_course():

    course_id = int(request.form["course_id"])
    course_name = request.form["course_name"].strip()
    credits = int(request.form["credits"])

    with driver.session(database="neo4j") as session:
        session.run("""
            MERGE (c:Course {course_id: $course_id})
            SET c.course_name = $course_name,
                c.credits = $credits
        """,
        course_id=course_id,
        course_name=course_name,
        credits=credits).consume()

    return redirect(url_for("courses_page"))

@app.route("/delete-course/<int:course_id>", methods=["POST"])
def delete_course(course_id):

    with driver.session(database="neo4j") as session:
        session.run("""
            MATCH (c:Course {course_id: $course_id})
            DETACH DELETE c
        """, course_id=course_id).consume()

    return redirect(url_for("courses_page"))

@app.route("/edit-course/<int:course_id>")
def edit_course(course_id):

    with driver.session(database="neo4j") as session:
        result = session.run("""
            MATCH (c:Course {course_id: $course_id})
            RETURN c.course_id AS course_id,
                   c.course_name AS course_name,
                   c.credits AS credits
        """, course_id=course_id)

        record = result.single()

        if record is None:
            return "Course not found", 404

        course = record.data()

    return render_template("edit_course.html", course=course)

@app.route("/update-course/<int:course_id>", methods=["POST"])
def update_course(course_id):

    course_name = request.form["course_name"].strip()
    credits = int(request.form["credits"])

    with driver.session(database="neo4j") as session:
        session.run("""
            MATCH (c:Course {course_id: $course_id})
            SET c.course_name = $course_name,
                c.credits = $credits
        """,
        course_id=course_id,
        course_name=course_name,
        credits=credits).consume()

    return redirect(url_for("courses_page"))

@app.route("/enrollments")
def enrollments_page():

    with driver.session(database="neo4j") as session:

        students_result = session.run("""
            MATCH (s:Student)
            RETURN s.student_id AS student_id,
                   s.name AS name
            ORDER BY s.name
        """)
        students = [record.data() for record in students_result]

        courses_result = session.run("""
            MATCH (c:Course)
            RETURN c.course_id AS course_id,
                   c.course_name AS course_name
            ORDER BY c.course_name
        """)
        courses = [record.data() for record in courses_result]

        enrollments_result = session.run("""
            MATCH (s:Student)-[:ENROLLED_IN]->(c:Course)
            RETURN s.student_id AS student_id,
                   s.name AS student_name,
                   c.course_id AS course_id,
                   c.course_name AS course_name
            ORDER BY s.name
        """)
        enrollments = [record.data() for record in enrollments_result]

    return render_template(
        "enrollments.html",
        students=students,
        courses=courses,
        enrollments=enrollments
    )

@app.route("/add-enrollment", methods=["POST"])
def add_enrollment():

    student_id = int(request.form["student_id"])
    course_id = int(request.form["course_id"])

    with driver.session(database="neo4j") as session:
        session.run("""
            MATCH (s:Student {student_id: $student_id})
            MATCH (c:Course {course_id: $course_id})
            MERGE (s)-[:ENROLLED_IN]->(c)
        """,
        student_id=student_id,
        course_id=course_id).consume()

    return redirect(url_for("enrollments_page"))

@app.route("/remove-enrollment/<int:student_id>/<int:course_id>", methods=["POST"])
def remove_enrollment(student_id, course_id):

    with driver.session(database="neo4j") as session:
        session.run("""
            MATCH (s:Student {student_id: $student_id})
                  -[r:ENROLLED_IN]->
                  (c:Course {course_id: $course_id})
            DELETE r
        """,
        student_id=student_id,
        course_id=course_id).consume()

    return redirect(url_for("enrollments_page"))

@app.route("/activities")
def activities_page():

    with driver.session(database="neo4j") as session:

        # Get all students
        students_result = session.run("""
            MATCH (s:Student)
            RETURN s.student_id AS student_id,
                   s.name AS name
            ORDER BY s.name
        """)
        students = [record.data() for record in students_result]

        # Get all courses
        courses_result = session.run("""
            MATCH (c:Course)
            RETURN c.course_id AS course_id,
                   c.course_name AS course_name
            ORDER BY c.course_name
        """)
        courses = [record.data() for record in courses_result]

        # Get learning activities and their relationships
        activities_result = session.run("""
            MATCH (s:Student)-[:COMPLETED]->(a:LearningActivity)
                  -[:FOR_COURSE]->(c:Course)

            RETURN a.activity_id AS activity_id,
                   s.name AS student_name,
                   c.course_name AS course_name,
                   a.title AS title,
                   a.activity_type AS activity_type,
                   a.activity_date AS activity_date,
                   a.duration AS duration,
                   a.description AS description

            ORDER BY a.activity_id ASC
        """)

        activities = [record.data() for record in activities_result]

    return render_template(
        "activities.html",
        students=students,
        courses=courses,
        activities=activities
    )

@app.route("/add-activity", methods=["POST"])
def add_activity():

    activity_id = int(request.form["activity_id"])
    student_id = int(request.form["student_id"])
    course_id = int(request.form["course_id"])

    title = request.form["title"].strip()
    activity_type = request.form["activity_type"]
    activity_date = request.form["activity_date"]
    duration = int(request.form["duration"])
    description = request.form["description"].strip()

    with driver.session(database="neo4j") as session:

        result = session.run("""
            MATCH (s:Student {student_id: $student_id})
                  -[:ENROLLED_IN]->
                  (c:Course {course_id: $course_id})

            WHERE NOT EXISTS {
                MATCH (existing:LearningActivity {
                    activity_id: $activity_id
                })
            }

            CREATE (a:LearningActivity {
                activity_id: $activity_id,
                title: $title,
                activity_type: $activity_type,
                activity_date: $activity_date,
                duration: $duration,
                description: $description
            })

            CREATE (s)-[:COMPLETED]->(a)
            CREATE (a)-[:FOR_COURSE]->(c)

            RETURN a.activity_id AS created_id
        """,
        activity_id=activity_id,
        student_id=student_id,
        course_id=course_id,
        title=title,
        activity_type=activity_type,
        activity_date=activity_date,
        duration=duration,
        description=description)

        created = result.single()

    if created is None:
        return redirect(url_for("activities_page", error="invalid_activity"))

    return redirect(url_for("activities_page"))

@app.route("/edit-activity/<int:activity_id>")
def edit_activity(activity_id):

    with driver.session(database="neo4j") as session:

        # Get the selected activity and its relationships
        activity_result = session.run("""
            MATCH (s:Student)-[:COMPLETED]->(a:LearningActivity)
                  -[:FOR_COURSE]->(c:Course)
            WHERE a.activity_id = $activity_id

            RETURN a.activity_id AS activity_id,
                   s.student_id AS student_id,
                   c.course_id AS course_id,
                   a.title AS title,
                   a.activity_type AS activity_type,
                   a.activity_date AS activity_date,
                   a.duration AS duration,
                   a.description AS description
        """, activity_id=activity_id)

        record = activity_result.single()

        if record is None:
            return "Learning activity not found", 404

        activity = record.data()

        # Get all students for the dropdown
        students_result = session.run("""
            MATCH (s:Student)
            RETURN s.student_id AS student_id,
                   s.name AS name
            ORDER BY s.name
        """)

        students = [record.data() for record in students_result]

        # Get all courses for the dropdown
        courses_result = session.run("""
            MATCH (c:Course)
            RETURN c.course_id AS course_id,
                   c.course_name AS course_name
            ORDER BY c.course_name
        """)

        courses = [record.data() for record in courses_result]

    return render_template(
        "edit_activity.html",
        activity=activity,
        students=students,
        courses=courses
    )

@app.route("/update-activity/<int:activity_id>", methods=["POST"])
def update_activity(activity_id):

    student_id = int(request.form["student_id"])
    course_id = int(request.form["course_id"])

    title = request.form["title"].strip()
    activity_type = request.form["activity_type"]
    activity_date = request.form["activity_date"]
    duration = int(request.form["duration"])
    description = request.form["description"].strip()

    with driver.session(database="neo4j") as session:

        session.run("""
            MATCH (a:LearningActivity {activity_id: $activity_id})
            MATCH (s:Student {student_id: $student_id})
            MATCH (c:Course {course_id: $course_id})

            SET a.title = $title,
                a.activity_type = $activity_type,
                a.activity_date = $activity_date,
                a.duration = $duration,
                a.description = $description

            WITH a, s, c

            OPTIONAL MATCH (old_student:Student)-[r1:COMPLETED]->(a)
            DELETE r1

            WITH a, s, c

            OPTIONAL MATCH (a)-[r2:FOR_COURSE]->(old_course:Course)
            DELETE r2

            WITH a, s, c

            MERGE (s)-[:COMPLETED]->(a)
            MERGE (a)-[:FOR_COURSE]->(c)
        """,
        activity_id=activity_id,
        student_id=student_id,
        course_id=course_id,
        title=title,
        activity_type=activity_type,
        activity_date=activity_date,
        duration=duration,
        description=description).consume()

    return redirect(url_for("activities_page"))

@app.route("/delete-activity/<int:activity_id>", methods=["POST"])
def delete_activity(activity_id):

    with driver.session(database="neo4j") as session:

        session.run("""
            MATCH (a:LearningActivity {activity_id: $activity_id})
            DETACH DELETE a
        """, activity_id=activity_id).consume()

    return redirect(url_for("activities_page"))

@app.route("/history")
def learning_history():

    selected_student_id = request.args.get("student_id", type=int)

    with driver.session(database="neo4j") as session:

        # Get all students for the dropdown
        students_result = session.run("""
            MATCH (s:Student)
            RETURN s.student_id AS student_id,
                   s.name AS name
            ORDER BY s.name
        """)

        students = [record.data() for record in students_result]

        activities = []
        total_activities = 0
        total_duration = 0
        total_courses = 0

        if selected_student_id is not None:

            # Get learning activities for the selected student
            activities_result = session.run("""
                MATCH (s:Student {student_id: $student_id})
                      -[:COMPLETED]->(a:LearningActivity)
                      -[:FOR_COURSE]->(c:Course)

                RETURN a.activity_id AS activity_id,
                       c.course_name AS course_name,
                       a.title AS title,
                       a.activity_type AS activity_type,
                       a.activity_date AS activity_date,
                       a.duration AS duration,
                       a.description AS description,
                       c.course_id AS course_id

                ORDER BY a.activity_date DESC
            """, student_id=selected_student_id)

            activities = [
                record.data() for record in activities_result
            ]

            # Calculate learning statistics
            total_activities = len(activities)

            total_duration = sum(
                activity["duration"] or 0
                for activity in activities
            )

            total_courses = len(set(
                activity["course_id"]
                for activity in activities
            ))

    return render_template(
        "history.html",
        students=students,
        selected_student_id=selected_student_id,
        activities=activities,
        total_activities=total_activities,
        total_duration=total_duration,
        total_courses=total_courses
    )

@app.route("/student-courses/<int:student_id>")
def student_courses(student_id):

    with driver.session(database="neo4j") as session:

        result = session.run("""
            MATCH (s:Student {student_id: $student_id})
                  -[:ENROLLED_IN]->
                  (c:Course)

            RETURN c.course_id AS course_id,
                   c.course_name AS course_name

            ORDER BY c.course_name
        """, student_id=student_id)

        courses = [record.data() for record in result]

    return jsonify(courses)

if __name__ == "__main__":
    app.run(debug=True)