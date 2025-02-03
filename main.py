from hospital import Hospital
from ui.medidataHubUI import MedidataHubUI
from datetime import date
from utilities import Utilities

def main():
    generate_new_data = False # If True generates new data. ALL OLD DATA WILL BE LOST. This is the value that should be used for the first run.
    utility = Utilities()
    
    if generate_new_data:
        utility.random_datas() # It is possible to set the number of patients, doctors, and appointments to be generated.
    
    hospital = Hospital("Admin", "Admin", utility) # You can change the admin credentials here
    hospital.load_data() # Load the data from the files
    ui = MedidataHubUI(utility=utility, hospital=hospital) # Create the UI
    ui.mainloop()

if __name__ == "__main__":
    main()  