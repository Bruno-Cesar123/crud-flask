from flask_restful import Resource, reqparse
from models.user import UserModel
from connection import cursor, connection

class Users(Resource):
  def get(self):
    try:
      sql = '''
        SELECT * FROM users
      '''
      cursor.execute(sql)

      result = cursor.fetchall()

      users = []

      for row in result:
        users.append({
          'id': row[0],
          'name': row[1],
          'lastname': row[2],
          'age': row[3],
          'created_at': str(row[4])
        })
    
      return {'users': users}, 200

    except (Exception) as error:
      return {'message': 'Internal Server error'}, 500
    
  def post(self):
    args = reqparse.RequestParser()
    args.add_argument('name')
    args.add_argument('lastname')
    args.add_argument('age')
    
    user = args.parse_args()

    try:
      sql = '''
        INSERT INTO users (name, lastname, age)
        VALUES('{0}', '{1}', '{2}')
      '''.format(user.name, user.lastname, user.age)

      cursor.execute(sql)
      connection.commit()

      return user, 201

    except (Exception) as error:
      return {"'message': 'Internal Server error'", error}, 400 

class User(Resource):
  def get(self, id):
    try:
      user = UserModel.find_user(id)

      if user:
        return user, 200

    except (Exception) as error:
      cursor.execute('rollback')
      return {'message': 'User not found'}, 404

  def put(self, id):
    args = reqparse.RequestParser()
    args.add_argument('name')
    args.add_argument('lastname')
    args.add_argument('age')

    user = args.parse_args()

    try:
      user_exists = UserModel.find_user(id)

      if user_exists:
        sql = '''
          UPDATE users SET name = '{0}', lastname = '{1}', age = '{2}'
        '''.format(user.name, user.lastname, user.age)

        cursor.execute(sql)
        connection.commit()

        new_user = UserModel.find_user(id)

        return new_user, 200

    except (Exception) as error:
      cursor.execute('rollback')
      return {'message': 'User not found'}, 404

  def delete(self, id):
    try:
      user = UserModel.find_user(id)

      if user:
        sql = '''
          DELETE FROM users WHERE id = '{}'
        '''.format(id)

        cursor.execute(sql)
        connection.commit()
        return {'message': 'User deleted'}

    except (Exception) as error:
      cursor.execute('rollback')
      return {'message': 'User not found'}, 404

    


