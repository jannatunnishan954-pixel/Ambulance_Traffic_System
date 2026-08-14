import sqlite3
connection = sqlite3.connect('ambulance.db')
cursor=connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS ambulances 
    (id INTEGER PRIMARY KEY, 
    driver_name TEXT, 
    hospital TEXT, 
    current_location TEXT, 
    status TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS emergencies
    (id INTEGER PRIMARY KEY, 
    patient_name TEXT, 
    location TEXT, 
    priority TEXT,
    status TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS traffic 
    (id INTEGER PRIMARY KEY,
    location TEXT,
    traffic_level TEXT,
    estimated_delay INTEGER)''')
# cursor.execute('''Alter TABLE emergencies ADD COLUMN ambulance_id INTEGER''')
# connection.commit()
# print('add colomn ambulance_id to emergencies table')
print('1. Add ambulance\n2. View ambulances\n3. Exit\n4. Update ambulance status\n5. Delete ambulance\n6. Add emergency\n7. View emergencies\n8. Assign ambulance to emergency\n9. Update emergency status\n10. Make ambulance available\n11. Add traffic information\n12. View traffic information')
while True:
    choice=input("Enter your choice: ")
    if choice=='1':
        driver_name=input("Enter driver name: ")
        hospital=input("Enter hospital name: ")
        current_location=input("Enter current location: ")
        status='Available'
        new_ambulance=(driver_name, hospital, current_location, status)
        
        cursor.execute('''INSERT INTO ambulances (driver_name, hospital, current_location, status) VALUES (?, ?, ?, ?)''', new_ambulance)
        connection.commit()
    elif choice=='2':
        cursor.execute("SELECT * FROM ambulances")
        ambulances=cursor.fetchall()
        for item in ambulances:
            print(f"ID: {item[0]} | Driver Name: {item[1]} | Hospital: {item[2]} | Current Location: {item[3]} | Status: {item[4]}")
    elif choice=='4':
        ambulance_id=int(input("Enter ambulance ID to update: "))
        new_status=input("Enter new status: ")
        cursor.execute("UPDATE ambulances SET status=? WHERE id=?", (new_status, ambulance_id))
        connection.commit()
        print('Ambulance status updated successfully.')
    elif choice=='5':
        ambulance_id=int(input("Enter ambulance ID to delete: "))
        cursor.execute("DELETE FROM ambulances WHERE id=?", (ambulance_id,))
        connection.commit()
        print('Ambulance deleted successfully.')
    elif choice=='6':
         patient_name=input("Enter patient name: ")
         location=input("Enter emergency location: ")
         priority=input("Enter priority: ")
         status='Pending'
         new_emergency=(patient_name, location, priority, status)
         cursor.execute('''INSERT INTO emergencies (patient_name, location, priority, status) VALUES (?, ?, ?, ?)''', new_emergency)
         connection.commit()
         print('Emergency added successfully.')
    elif choice=='7':
        cursor.execute("SELECT * FROM emergencies")
        emergencies=cursor.fetchall()
        for item in emergencies:
            print(f"ID: {item[0]} | Patient Name: {item[1]} | Location: {item[2]} | Priority: {item[3]} | Status: {item[4]}")
    elif choice=='8':
        emergency_id=int(input('Enter emergency ID to assign ambulance:'))
        ambulance_id=int(input('Enter ambulance ID to assign:'))
        cursor.execute('UPDATE emergencies SET ambulance_id=?, status=? WHERE id=?', (ambulance_id, 'Assigned', emergency_id))
        cursor.execute('UPDATE ambulances SET status=? WHERE id=?', ('Busy', ambulance_id))
        connection.commit()
        print('Ambulance assigned successfully.')
    elif choice=='9':
        emergency_id=int(input('Enter emergency ID to update status:'))
        new_status=input('Enter new status:')
        cursor.execute('UPDATE emergencies SET status=? WHERE id=?', (new_status, emergency_id))
        connection.commit()
        print('Emergency status updated successfully.')
    elif choice=='10':
        ambulance_id=int(input('Enter ambulance ID to make available:'))
        cursor.execute('UPDATE ambulances SET status=? WHERE id=?', ('Available', ambulance_id))
        connection.commit()
        print('Ambulance made available successfully.')
    elif choice=='11':
        location=input('Enter traffic location:')
        traffic_level=input('Enter traffic level (Low/Medium/High): ')
        estimated_delay=int(input('Enter estimated delay in minutes: '))
        new_traffic=(location, traffic_level, estimated_delay)
        cursor.execute('INSERT INTO traffic (location, traffic_level, estimated_delay) VALUES (?, ?, ?)', new_traffic)
        connection.commit()
        print('Traffic information added successfully.')
    elif choice=='12':
    elif choice=='3':
            print("Exiting..")
            break
connection.close()