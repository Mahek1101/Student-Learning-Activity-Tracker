// Student Learning Activity and Course Relationship Tracker
// Neo4j Database Demonstration Queries


// 1. View All Students
MATCH (s:Student)
RETURN s
ORDER BY s.student_id;


// 2. View All Courses
MATCH (c:Course)
RETURN c
ORDER BY c.course_id;


// 3. View All Learning Activities
MATCH (a:LearningActivity)
RETURN a
ORDER BY a.activity_id;


// 4. Display Complete Database Graph
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m;


// 5. Display Student Enrollment Relationships
MATCH (s:Student)-[r:ENROLLED_IN]->(c:Course)
RETURN s, r, c;


// 6. Display Learning Activity Relationships
MATCH (s:Student)-[r1:COMPLETED]->(a:LearningActivity)
      -[r2:FOR_COURSE]->(c:Course)
RETURN s, r1, a, r2, c;


// 7. Display Student Enrollment Details
MATCH (s:Student)-[:ENROLLED_IN]->(c:Course)
RETURN s.name AS StudentName,
       c.course_name AS CourseName
ORDER BY s.name;


// 8. Display Learning Activity Details
MATCH (s:Student)-[:COMPLETED]->(a:LearningActivity)
      -[:FOR_COURSE]->(c:Course)
RETURN s.name AS StudentName,
       a.title AS ActivityTitle,
       c.course_name AS CourseName,
       a.duration AS Duration;


// 9. Display Learning History for Student ID 4
MATCH (s:Student {student_id: 4})
      -[:COMPLETED]->(a:LearningActivity)
      -[:FOR_COURSE]->(c:Course)
RETURN s.name AS StudentName,
       a.title AS ActivityTitle,
       a.activity_date AS ActivityDate,
       a.duration AS Duration,
       c.course_name AS CourseName;


// 10. Count Nodes by Type
MATCH (n)
RETURN labels(n)[0] AS NodeType,
       count(n) AS Total;


// 11. Count Relationships by Type
MATCH ()-[r]->()
RETURN type(r) AS RelationshipType,
       count(r) AS Total;


// 12. Display Available Node Labels
CALL db.labels();


// 13. Display Available Relationship Types
CALL db.relationshipTypes();