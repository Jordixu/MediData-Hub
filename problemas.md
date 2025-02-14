# Practice 3

## Problem 1

### Problem description

Change password did not work

### Solving process

Print statements at patientChangePassword.py after the change to see if it effectively changed.
Added a try except statement to capture possible errors.
Reviewed the set protected info method.
Saw that we passed as argument str instead of 'str'.

### Solution

Changed str for 'str'

---

## Problem 2

### Problem description

The login screen does not show the messagebox when the wrong password is inputted.

### Solving process

Reviewed the ui code.

### Solution

Saw that the return statement was not correctly indented, corrected the indentation.

---

## Problem 3

### Problem description

Doctor not showing when department and specialty was selected in PatientRequestAppointment frame.

### Solution

Modified selected_doctors() function so that the names are correctly inputted in the combobox.

---

## Problem 4

### Problem description

Availability were not parsed correctly in the .csv saving process (they were saved as datetime objects, not str) and the extraction process (they were extracted as str).

## Solution

New functions in Utility and Foundation classes to parse correctly.