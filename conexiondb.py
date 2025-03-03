import mysql.connector

conexion = mysql.connector.connect(user='root', password='', 
        database='prueba') #conexión a la base de datos


cursor = conexion.cursor() #cursor es un objeto que permite ejecutar sentencias SQL

consulta = "SELECT * FROM clientes" #consulta a la base de datos
cursor.execute(consulta) #ejecuta la consulta

while True:
        row = cursor.fetchone() #obtiene la siguiente fila
        if not row: #si no hay más filas, termina el ciclo
                break #si no hay más filas, termina el ciclo
        print(row) #muestra la fila
        
conexion.close() #cierra la conexiónrg