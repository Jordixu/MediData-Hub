from hospital import Hospital
from ui.medidataHubUI import MedidataHubUI


def main():
    hospital = Hospital("Medidata Hospital", "Barcelona")
    ui = MedidataHubUI(hospital)
    ui.mainloop()


if __name__ == "__main__":
    main()