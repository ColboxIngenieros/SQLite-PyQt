from PyQt6 import QtWidgets, uic
from connect_db import DatabaseConnect


class NewVehicleWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Cargamos el archivo UI 
        self.ui = uic.loadUi("./ui/new_vehicle.ui", self)

        # Obtenemos referencias de los objetos del cuadro de diálogo 'nuevo vehiculo'
        self.new_vehicle_save_btn = self.ui.pushButton
        self.new_vehicle_cancel_btn = self.ui.pushButton_2

        self.make = self.ui.comboBox_3
        self.model_name = self.ui.lineEdit
        self.year = self.ui.lineEdit_3
        self.region = self.ui.comboBox
        self.chassis = self.ui.lineEdit_4
        self.chassis.setMaxLength(5)
        self.key_type = self.ui.comboBox_2
        self.transponder_type = self.ui.lineEdit_2
        self.transponder_type.setMaxLength(6)
        self.programming = self.ui.comboBox_4
        self.cloning = self.ui.comboBox_5

        # Inicializa el objeto ConnectDB para operaciones con la base de datos
        self.connect_db = DatabaseConnect()

    def new_vehicle_data(self):
        # Recuperamos los datos del cuadro de dialogo
        make = self.make.currentText()
        text_model = self.model_name.text()
        model_name = text_model.upper()
        year = self.year.text()
        region = self.region.currentText()
        text_chassis = self.chassis.text()
        chassis = text_chassis.upper()
        key_type = self.key_type.currentText()
        text_t_type = self.transponder_type.text()
        transponder_type = text_t_type.upper()
        programming = self.programming.currentText()
        cloning = self.cloning.currentText()

        # Validamos los datos de entrada
        data_list = [model_name]
        bool_data_list = list(map(lambda item: bool(item), data_list))

        if False in bool_data_list:
            # Si los datos son incompletos, se retorna None
            return None
        else:
            # Creamos un diccionario con todos los datos leidos
            data_dict = {
                "make": make,
                "model_name": model_name,
                "year": year,
                "region": region,
                "chassis": chassis,
                "key_type": key_type,
                "transponder_type": transponder_type,
                "programming": programming,
                "cloning": cloning,
            }

            return data_dict

    def add_new_vehicle(self):
        # Recuperamos los datos del vehiculo
        vehicle_data = self.new_vehicle_data()

        if vehicle_data:
            # Añadimos el nuevo vehiculo a la base de datos
            add_result = self.connect_db.add_new_vehicle(**vehicle_data)

            return add_result

        else:
            # Si los datos son incompletos, retornamos mensaje de advertencia
            return "More data needed to input"

    def clear_data(self):
        # Limpiamos los objetos del cuadro de dialogo
        self.model_name.clear()
        self.year.clear()
        self.chassis.clear()
        self.transponder_type.clear()
