from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://mongo:27017/')
db = client['students_db']
student_collection = db['students']


def add(student=None):
    query = {'first_name': student.first_name, 'last_name': student.last_name}
    if student_collection.find_one(query):
        return 'already exists', 409

    result = student_collection.insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)
    return student.student_id, 200


def get_by_id(student_id=None, subject=None):
    student = student_collection.find_one({'_id': ObjectId(student_id)})
    if not student:
        return 'not found'
    student['student_id'] = str(student['_id'])
    del student['_id']
    return student


def delete(student_id=None):
    result = student_collection.delete_one({'_id': ObjectId(student_id)})
    if result.deleted_count == 0:
        return 'not found'
    return student_id
