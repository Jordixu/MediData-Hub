from hospital import Hospital
from ui.medidataHubUI import MedidataHubUI
from datetime import date
from utilities import Utilities

def main():
    # If True generates new data. ALL OLD DATA WILL BE LOST
    generate_new_data = True
    utility = Utilities()
    
    if generate_new_data:
        utility.random_datas()
    
    hospital = Hospital("Admin", "Admin", utility)
    hospital.load_data()
    ui = MedidataHubUI(utility=utility, hospital=hospital)
    ui.mainloop()

if __name__ == "__main__":
    main()