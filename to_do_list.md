# To Do List

## Documentation

- UI
- Person
- Doctor
- Patient
- Space
- Appointment
- Data

## Administrator Role

- UI of Administrator
- Create class / define it correctly
- Control the functions of the Administrator
  - Add, modify and delete doctors
  - Add, modify and delete rooms
  - Cancel Appointment

## Appointment System

- Relate the classes for correct program functionality
- Implementation in UI
- Notifications!

## Doctor UI

- Login, register

### Schedule System

### Room System

- Create rooms

### Notification System

- Control instancing
- Implementation in ui

## Prescriptions

- May be implemented ?

## Consultation System

- Construct patient history
- Save patient history
- Consult patient history
- Prescriptions

## Patient UI

- Change password
- Forget your password? Security question? ??

### Assigned Doctor

## Error handling

- Check if name and surname is isalpha()

## Database

- Set default values (preexisting database) DONE
- Maybe we should export the attributes changing the names directly (undo the name_mangling in get all atributes method)

## Take Out the Test Modules

delete user return to main sceen

add confirmation from hospital class that the patient/doctor has been successfully deleted, created?

add confirmation to ensure that the appointment has been successfully created and deleted (instead of str, return boolean)

change change_status (appointments) return to bool

appointment class change_date_time method need to be modified

appointment class change_doctor method has to ensure that doctor is available at that time

appointment class change_patient method does not really make sense, does it? Maybe we should take it off

appointment class change_room has to ensure that room is available
