import database


sql = '''DELETE FROM equipments WHERE id =4 '''
#sql = '''UPDATE product SET inventory_available = 60 WHERE id = 1'''
conn = database.create_connection()
cur = conn.cursor()
cur.execute(sql)
conn.commit()

