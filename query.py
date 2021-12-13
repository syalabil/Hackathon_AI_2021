import database


#sql = '''DELETE FROM equipments WHERE id =4 '''
sql = '''UPDATE product SET product_sold = 10 WHERE id = 3'''
conn = database.create_connection()
cur = conn.cursor()
cur.execute(sql)
conn.commit()

