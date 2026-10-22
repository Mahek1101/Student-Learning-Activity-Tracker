// Student Learning Activity and Course Relationship Tracker
// Neo4j Database Setup
// Run this script on a fresh Neo4j database.

// Step 1: Create uniqueness constraints

CREATE CONSTRAINT student_id_unique IF NOT EXISTS
FOR (s:Student)
REQUIRE s.student_id IS UNIQUE;

CREATE CONSTRAINT course_id_unique IF NOT EXISTS
FOR (c:Course)
REQUIRE c.course_id IS UNIQUE;

CREATE CONSTRAINT activity_id_unique IF NOT EXISTS
FOR (a:LearningActivity)
REQUIRE a.activity_id IS UNIQUE;


// Step 2: Create sample students

MERGE (s:Student {student_id: 1})
SET s.name = 'Parker',
    s.email = 'parker@example.com';

MERGE (s:Student {student_id: 2})
SET s.name = 'John Smith',
    s.email = 'john@example.com';

MERGE (s:Student {student_id: 3})
SET s.name = 'Emma Wilson',
    s.email = 'emma@example.com';

MERGE (s:Student {student_id: 4})
SET s.name = 'Mahek Patel',
    s.email = 'mahek@example.com';

MERGE (s:Student {student_id: 5})
SET s.name = 'Yashvi',
    s.email = 'yashvi@example.com';

MERGE (s:Student {student_id: 6})
SET s.name = 'Noah',
    s.email = 'noah@example.com';


// Step 3: Create sample courses

MERGE (c:Course {course_id: 101})
SET c.course_name = 'Advanced Database Systems',
    c.credits = 3;

MERGE (c:Course {course_id: 102})
SET c.course_name = 'Cybersecurity Fundamentals',
    c.credits = 3;

MERGE (c:Course {course_id: 103})
SET c.course_name = 'Python Programming',
    c.credits = 3;

MERGE (c:Course {course_id: 104})
SET c.course_name = 'Computer Networks',
    c.credits = 3;

MERGE (c:Course {course_id: 105})
SET c.course_name = 'Data Structures',
    c.credits = 3;

// Step 4: Create student enrollment relationships

// Parker
MATCH (s:Student {student_id: 1})
MATCH (c:Course {course_id: 101})
MERGE (s)-[:ENROLLED_IN]->(c);

MATCH (s:Student {student_id: 1})
MATCH (c:Course {course_id: 102})
MERGE (s)-[:ENROLLED_IN]->(c);


// John Smith
MATCH (s:Student {student_id: 2})
MATCH (c:Course {course_id: 104})
MERGE (s)-[:ENROLLED_IN]->(c);


// Emma Wilson
MATCH (s:Student {student_id: 3})
MATCH (c:Course {course_id: 102})
MERGE (s)-[:ENROLLED_IN]->(c);

MATCH (s:Student {student_id: 3})
MATCH (c:Course {course_id: 103})
MERGE (s)-[:ENROLLED_IN]->(c);

MATCH (s:Student {student_id: 3})
MATCH (c:Course {course_id: 105})
MERGE (s)-[:ENROLLED_IN]->(c);


// Mahek Patel
MATCH (s:Student {student_id: 4})
MATCH (c:Course {course_id: 103})
MERGE (s)-[:ENROLLED_IN]->(c);

MATCH (s:Student {student_id: 4})
MATCH (c:Course {course_id: 104})
MERGE (s)-[:ENROLLED_IN]->(c);


// Yashvi
MATCH (s:Student {student_id: 5})
MATCH (c:Course {course_id: 101})
MERGE (s)-[:ENROLLED_IN]->(c);


// Noah
MATCH (s:Student {student_id: 6})
MATCH (c:Course {course_id: 103})
MERGE (s)-[:ENROLLED_IN]->(c);

MATCH (s:Student {student_id: 6})
MATCH (c:Course {course_id: 105})
MERGE (s)-[:ENROLLED_IN]->(c);

// Step 5: Create sample learning activities

MERGE (a:LearningActivity {activity_id: 201})
SET a.title = 'Advanced SQL Query Practice',
    a.activity_type = 'Practice',
    a.activity_date = '2026-10-14',
    a.duration = 90,
    a.description = 'Practiced advanced SQL queries.';

MERGE (a:LearningActivity {activity_id: 202})
SET a.title = 'TCP/IP Protocol Quiz',
    a.activity_type = 'Quiz',
    a.activity_date = '2026-10-15',
    a.duration = 45,
    a.description = 'Completed a quiz on TCP/IP protocols.';

MERGE (a:LearningActivity {activity_id: 203})
SET a.title = 'Python File Handling',
    a.activity_type = 'Practice',
    a.activity_date = '2026-10-16',
    a.duration = 30,
    a.description = 'Practiced Python file operations.';

MERGE (a:LearningActivity {activity_id: 204})
SET a.title = 'Network Configuration',
    a.activity_type = 'Lab',
    a.activity_date = '2026-10-17',
    a.duration = 150,
    a.description = 'Configured computer networks.';

MERGE (a:LearningActivity {activity_id: 205})
SET a.title = 'Cybersecurity Study',
    a.activity_type = 'Study',
    a.activity_date = '2026-10-18',
    a.duration = 60,
    a.description = 'Studied cybersecurity fundamentals.';

MERGE (a:LearningActivity {activity_id: 206})
SET a.title = 'Network Security Basics',
    a.activity_type = 'Study',
    a.activity_date = '2026-10-19',
    a.duration = 75,
    a.description = 'Studied basic network security concepts.';


// Step 6: Connect students to learning activities and courses

MATCH (s:Student {student_id: 1})
MATCH (a:LearningActivity {activity_id: 201})
MATCH (c:Course {course_id: 101})
MERGE (s)-[:COMPLETED]->(a)
MERGE (a)-[:FOR_COURSE]->(c);

MATCH (s:Student {student_id: 2})
MATCH (a:LearningActivity {activity_id: 202})
MATCH (c:Course {course_id: 104})
MERGE (s)-[:COMPLETED]->(a)
MERGE (a)-[:FOR_COURSE]->(c);

MATCH (s:Student {student_id: 3})
MATCH (a:LearningActivity {activity_id: 203})
MATCH (c:Course {course_id: 103})
MERGE (s)-[:COMPLETED]->(a)
MERGE (a)-[:FOR_COURSE]->(c);

MATCH (s:Student {student_id: 4})
MATCH (a:LearningActivity {activity_id: 204})
MATCH (c:Course {course_id: 104})
MERGE (s)-[:COMPLETED]->(a)
MERGE (a)-[:FOR_COURSE]->(c);

MATCH (s:Student {student_id: 5})
MATCH (a:LearningActivity {activity_id: 205})
MATCH (c:Course {course_id: 102})
MERGE (s)-[:COMPLETED]->(a)
MERGE (a)-[:FOR_COURSE]->(c);

MATCH (s:Student {student_id: 4})
MATCH (a:LearningActivity {activity_id: 206})
MATCH (c:Course {course_id: 104})
MERGE (s)-[:COMPLETED]->(a)
MERGE (a)-[:FOR_COURSE]->(c);