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
    status TEXT,
    ambulance_id INTEGER,
    FOREIGN KEY (ambulance_id) REFERENCES ambulances(id))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS traffic 
    (id INTEGER PRIMARY KEY,
    location TEXT,
    traffic_level TEXT,
    estimated_delay INTEGER)''')
print('1. Add ambulance\n2. View ambulances\n3. Exit\n4. Update ambulance status\n5. Delete ambulance\n6. Add emergency\n7. View emergencies\n8. Assign ambulance to emergency\n9. Update emergency status\n10. Make ambulance available\n11. Add traffic information\n12. View traffic information\n13.Find available ambulance\n14.Find best available ambulance\n15.Assign best ambulance automatically')
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
        print('ambulance added successfully.')
    elif choice=='2':
        cursor.execute("SELECT * FROM ambulances")
        ambulances=cursor.fetchall()
        for item in ambulances:
            print(f"ID: {item[0]} | Driver Name: {item[1]} | Hospital: {item[2]} | Current Location: {item[3]} | Status: {item[4]}")
    elif choice=='4':
        try:
            ambulance_id=int(input("Enter ambulance ID to update: "))
        except ValueError:
            print('please enter a valid number.')
            continue
        new_status=input("Enter new status: ")
        cursor.execute("UPDATE ambulances SET status=? WHERE id=?", (new_status, ambulance_id))
        connection.commit()
        print('Ambulance status updated successfully.')
    elif choice=='5':
        try:
            ambulance_id=int(input("Enter ambulance ID to delete: "))
        except ValueError:
            print('please enter a valid number.')
            continue
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
        try:
            emergency_id=int(input('Enter emergency ID to assign ambulance:'))
        except ValueError:
            print('please enter a valid emergency id number.')
            continue
        try:
            ambulance_id=int(input('Enter ambulance ID to assign:'))
        except ValueError:
            print('please enter a valid ambulance id number.')
            continue
        cursor.execute('SELECT id from emergencies WHERE id=?', (emergency_id,))
        emergency_record=cursor.fetchone()
        if emergency_record is None:
            print('emergency not found')
            continue
        cursor.execute('SELECT  status FROM emergencies WHERE id=?', (emergency_id,))
        emergency_status=cursor.fetchone()
        if emergency_status[0]=='Assigned':
            print('emergency has an already ambulance assigned')
            continue
        cursor.execute('SELECT status FROM ambulances WHERE id=?', (ambulance_id,))
        ambulance_status=cursor.fetchone()
        if ambulance_status is None:
            print('Ambulance not found.')
            continue
        elif ambulance_status[0]!='Available':
            print('Ambulance is not available.')
            continue
        else:
            cursor.execute('UPDATE emergencies SET ambulance_id=?, status=? WHERE id=?', (ambulance_id, 'Assigned', emergency_id))
            cursor.execute('UPDATE ambulances SET status=? WHERE id=?', ('Busy', ambulance_id))
            connection.commit()
            print('Ambulance assigned successfully.')
    elif choice=='9':
        try:
            emergency_id=int(input('Enter emergency ID to update status:'))
        except ValueError:
            print('please enter a valid emergency id number.')
            continue
        new_status=input('Enter new status:')
        cursor.execute('SELECT  ambulance_id FROM emergencies WHERE id=?', (emergency_id,))
        emergency_ambulance_id=cursor.fetchone()
        if emergency_ambulance_id is None:
            print('emergency not found.')
            continue
        if new_status.lower()=='completed':
            if emergency_ambulance_id[0] is not None:
                cursor.execute('UPDATE ambulances SET status=? WHERE id=?',('Available', emergency_ambulance_id[0]))
        cursor.execute('UPDATE emergencies SET status=? WHERE id=?', (new_status, emergency_id))
        connection.commit()
        print('Emergency status updated successfully.')
    elif choice=='10':
        try:
            ambulance_id=int(input('Enter ambulance ID to make available:'))
        except ValueError:
            print('please enter a valid ambulance id number.')
            continue
        cursor.execute('SELECT id FROM ambulances WHERE id=?',(ambulance_id,))
        ambulance_record=cursor.fetchone()
        if ambulance_record is None:
            print('Ambulance not found.')
            continue
        cursor.execute('UPDATE ambulances SET status=? WHERE id=?', ('Available', ambulance_id))
        connection.commit()
        print('Ambulance made available successfully.')
    elif choice=='11':
        location=input('Enter traffic location:')
        traffic_level=input('Enter traffic level (Low/Medium/High): ').lower()
        if traffic_level not in ('low','medium','high'):
            print('invalid traffic level')
            continue
        try:
            estimated_delay=int(input('Enter estimated delay in minutes: '))
        except ValueError:
            print('please enter a number.')
            continue
        new_traffic=(location, traffic_level, estimated_delay)
        cursor.execute('INSERT INTO traffic (location, traffic_level, estimated_delay) VALUES (?, ?, ?)', new_traffic)
        connection.commit()
        print('Traffic information added successfully.')
    elif choice=='12':
        cursor.execute('SELECT * FROM traffic')
        traffic_info=cursor.fetchall()
        for item in traffic_info:
            print(f"ID: {item[0]} | Location: {item[1]} | Traffic Level: {item[2].capitalize()} | Estimated Delay: {item[3]} minutes")
    elif choice=='13':
        cursor.execute('SELECT * FROM ambulances WHERE LOWER(status)=?', ('available',))
        available_ambulances=cursor.fetchall()
        for item in available_ambulances:
            print(f'ID:{item[0]} | Driver name: {item[1]} | Hospital: {item[2]} | Current Location: {item[3]} | Status: {item[4]}')
    elif choice=='14':
        cursor.execute('SELECT * FROM ambulances WHERE LOWER(status)=?', ('available',))
        available_ambulances=cursor.fetchall()
        best_ambulance=None
        lowest_delay=float('inf')
        for ambulance in available_ambulances:
            location=ambulance[3]
            cursor.execute('SELECT estimated_delay FROM traffic WHERE location=? ORDER BY  estimated_delay ASC LIMIT 1', (location,))
            traffic_delay=cursor.fetchone()
            if traffic_delay is None:
                continue
            delay=traffic_delay[0]
            if delay<lowest_delay:
                lowest_delay=delay
                best_ambulance=ambulance
        if best_ambulance is None:
            print('no available ambulance with traffic information found.')
            continue
        else:
            print(f'best ambulance: {best_ambulance[0]} | driver: {best_ambulance[1]} | location: {best_ambulance[3]} | estimated delay: {lowest_delay}')
    elif choice=='15':
        try:
            emergency_id=int(input('enter emergency id to assign ambulance: '))
        except ValueError:
            print('please enter a valid emergency id number.')
            continue
        cursor.execute('SELECT * FROM emergencies WHERE id=?', (emergency_id,))
        emergency=cursor.fetchone()
        if emergency is None:
            print('emergency not found.')
            continue
        if emergency[4].lower() != 'pending':
            print('emergency is not pending.')
            continue
        emergency_location=emergency[2]
        cursor.execute('SELECT * FROM ambulances WHERE LOWER(status)=?', ('available',))
        available_ambulances=cursor.fetchall()
        if not available_ambulances:
            print('no available ambulances.')
            continue
        best_ambulance=None
        lowest_delay=float('inf')
        for ambulance in available_ambulances:
            location=ambulance[3]
            if location.lower() == emergency_location.lower():
                best_ambulance=ambulance
                lowest_delay=0
            cursor.execute('SELECT estimated_delay FROM traffic WHERE location = ? ORDER BY estimated_delay ASC LIMIT 1', (location,))
            traffic_delay=cursor.fetchone()
            if traffic_delay is None:
                continue
            delay=traffic_delay[0]
            if delay<lowest_delay:
                lowest_delay=delay
                best_ambulance=ambulance
        if best_ambulance is None:
            print('no available ambulance with traffic information found.')
            continue
        cursor.execute('UPDATE emergencies SET ambulance_id=?, status=? WHERE id=?', (best_ambulance[0],'Assigned', emergency_id))
        cursor.execute('UPDATE ambulances SET status=? WHERE id=?', ('Busy', best_ambulance[0]))
        connection.commit()
        print(f'Best ambulance assigned successfully. Estimated delay: {lowest_delay} minutes.')
    elif choice=='3':
            print("Exiting..")
            break
connection.close()