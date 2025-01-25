from hospital import Hospital
from ui.medidataHubUI import MedidataHubUI
from random_datas import DataGenerator
from datetime import date

def main():
    # If True generates new data. ALL OLD DATA WILL BE LOST
    generate_new_data = True
    
    if generate_new_data:
        DataGenerator.generate_patients()
        DataGenerator.generate_doctors()
        DataGenerator.generate_rooms()
        DataGenerator.generate_appointments()
    
    hospital = Hospital("Admin", "Admin")
    hospital.load_data()
    ui = MedidataHubUI(hospital)
    ui.mainloop()


if __name__ == "__main__":
    main()