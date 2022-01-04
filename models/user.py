from connection import cursor, connection


class UserModel():
  sql = '''
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE TABLE IF NOT EXISTS users (
      id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
      name text NOT NULL,
      lastname text NOT NULL,
      age integer,
      created_at timestamp DEFAULT now() NOT NULL
    )
  '''

  cursor.execute(sql)
  connection.commit()

  @classmethod
  def find_user(cls, id):
    sql = '''
      SELECT * FROM users WHERE id = '{}'
    '''.format(id)

    cursor.execute(sql)
    result = cursor.fetchall()
    user = result[0][0]
  
    if user:
      userData = []

      for row in result:
        userData.append({
          'id': row[0],
          'name': row[1],
          'lastname': row[2],
          'age': row[3],
          'created_at': str(row[4])
        })

      return userData
    return None

