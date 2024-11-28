from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)
cursor = db.cursor(dictionary=True)

@app.route('/students', methods=['GET'])
def get_students():
    cursor.execute("SELECT * FROM StudentPerformanceFactors")
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/students/<int:id>', methods=['GET'])
def get_student_by_id(id):
    query = "SELECT * FROM StudentPerformanceFactors WHERE id = %s"
    cursor.execute(query, (id,))
    student = cursor.fetchone()
    if not student:
        return jsonify({"message": f"No student found with ID {id}"}), 404

    return jsonify(student), 200

@app.route('/students/scores', methods=['GET'])
def get_students_scores():
    cursor.execute("""
        SELECT Gender, AVG(Exam_Score) AS Average_Score
        FROM StudentPerformanceFactors
        GROUP BY Gender
        ORDER BY Average_Score DESC
    """)
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    query = """
        INSERT INTO StudentPerformanceFactors (Hours_Studied, Attendance, Parental_Involvement, 
        Access_to_Resources, Extracurricular_Activities, Sleep_Hours, Previous_Scores, 
        Motivation_Level, Internet_Access, Tutoring_Sessions, Family_Income, Teacher_Quality, 
        School_Type, Peer_Influence, Physical_Activity, Learning_Disabilities, 
        Parental_Education_Level, Distance_from_Home, Gender, Exam_Score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['Hours_Studied'], data['Attendance'], data['Parental_Involvement'],
        data['Access_to_Resources'], data['Extracurricular_Activities'], data['Sleep_Hours'],
        data['Previous_Scores'], data['Motivation_Level'], data['Internet_Access'],
        data['Tutoring_Sessions'], data['Family_Income'], data['Teacher_Quality'],
        data['School_Type'], data['Peer_Influence'], data['Physical_Activity'],
        data['Learning_Disabilities'], data['Parental_Education_Level'],
        data['Distance_from_Home'], data['Gender'], data['Exam_Score']
    )
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Student added successfully!'}), 201

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json
    query = """
        UPDATE StudentPerformanceFactors
        SET Hours_Studied = %s, Attendance = %s, Exam_Score = %s
        WHERE id = %s
    """
    values = (data['Hours_Studied'], data['Attendance'], data['Exam_Score'], id)
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Student updated successfully!'}), 200

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    cursor.execute("DELETE FROM StudentPerformanceFactors WHERE id = %s", (id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"message": f"No student found with ID {id}"}), 404
    return jsonify({"message": f"Student with ID {id} deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=4545)
