from MediDataHub import Hospital
from ui.medidataHubUI import MedidataHubUI
from utilities import Utilities

def main():
    generate_new_data = False # If True generates new data. ALL OLD DATA WILL BE LOST. This is the value that should be used for the first run.
    utility = Utilities()
    
    if generate_new_data: # Generate new data, ajust as needed
        utility.random_datas(
            number_of_patients=100,
            number_of_doctors=100,
            number_of_floors=6,
            rooms_per_floor=20,
            number_of_appointments=300,
            )
    
    hospital = Hospital("1", "1", utility) # You can change the admin credentials here
    hospital.load_data() # Load the data from the files
    ui = MedidataHubUI(utility=utility, hospital=hospital) # Create the UI
    ui.mainloop()
    

if __name__ == "__main__":
    main()
    # pyinstaller --onefile --windowed --icon=icon.ico main.py