# To Do List

## Documentation (UPDATE ALL THE DOCSTRINGS)

- [ ] UI
- [ ] Person
- [ ] Doctor
- [ ] Patient
- [ ] Space
- [ ] Appointment

## Administrator Role

- [ ] UI of Administrator
- [ ] Control the functions of the Administrator
  - [ ] Add, modify and delete doctors
  - [ ] Add, modify and delete rooms
  - [ ] Cancel Appointment

## Appointment System

- [ ] Relate the classes for correct program functionality (technically done, needs debbuging)
- [ ] Implementation in UI
  - [ ] Show appointments (done)
  - [ ] Cancel appointments (done)
  - [ ] Modify appointments
  - [ ] Request new appointment
  - [ ] Accept / Decline appointments.
- [ ] Notifications!
  - [ ] Show notifications
  - [ ] Create a notification? Like a message system

## Doctor UI

- [ ] Not done, however it is almost the same as the patient except for:
  - [ ] Accepting/declining appointments
  - [ ] The consultation system
    - [ ] Add new consult
    - [ ] View previous consults
    - [ ] See patient medical history
    - [ ] NO registration screen nor modification/deleition

### Schedule System

- [ ] The creation is done (utilities.py) but no system to do modifications.
- [ ] Also, need debbuging.

### Room System

- [ ] Room class is defined, but the addition, deleition and schedule modification is not implemented yet.

### Notification System

- [ ] Control instancing
- [ ] Implementation in ui

## Prescriptions

- [ ] Drugs are in the system (maybe we will download it from the internet)
- [ ] Adding, modifiying, deleting drugs is not implemented.
- [ ] Consultation system
- [ ] Appointments
- May be implemented ?

## Consultation System

- [ ] Construct patient history
- [ ] Consult patient history
- [ ] Prescriptions

## Patient UI

- [ ] Change password (undebbuged, for some reason it does not work)
- [ ] Forget your password? Security question? ??

### Assigned Doctor

## Database

- [ ] Save the notifications and drugs (drug is finished but undebbuged)

- [ ] Add relationship between the doctors, the patients, the appointments... (DONE)

## Take Out the Test Modules

## Minor changes

- [ ] add confirmation to ensure that the appointment has been successfully created and deleted (instead of str, return boolean)
- [ ] change change_status (appointments) return to bool
- [ ] appointment class change_date_time method need to be modified
- [ ] appointment class change_doctor method has to ensure that doctor is available at that time
- [ ] appointment class change_patient method does not really make sense, does it? Maybe we should take it off
- [ ] appointment class change_room has to ensure that room is available
- [ ] I think when data is created, some entities are overlapping (such as appointments in unavailable rooms or two appointment at the same time, needs to be reviewed and fixed) *