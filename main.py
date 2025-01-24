from hospital import Hospital
from ui.medidataHubUI import MedidataHubUI
from random_datas import generate_fake_data
from datetime import date


def main():
    hospital = Hospital("Medidata Hospital", "Barcelona")
    hospital.load_data()
    ui = MedidataHubUI(hospital)
    ui.mainloop()


if __name__ == "__main__":
    main()