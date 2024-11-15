from PyQt6 import QtWidgets, uic
from connect_db import DatabaseConnect


class UpdateVehicleWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Cargamos el archivo UI 
        self.ui = uic.loadUi('./ui/update_vehicle.ui', self)

        # Inicializa el objeto ConnectDB para operaciones con la base de datos
        self.connect_db = DatabaseConnect()

        # Obtenemos referencias de los objetos del cuadro de diálogo 'update vehiculo'
        self.vehicle_update_button_box = self.ui.buttonBox

        self.make = self.ui.comboBox_6
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

    def init_vehicle_list(self, model_name):
        vehicle_data = self.connect_db.get_data(model_name=model_name)
        self.set_data(vehicle_data)

    def set_data(self, vehicle_data):
        """
        Pone los datos del vehiculo en los elementos del cuadro de dialogo

        Args:
            vehicle_data (list): Lista que contiene los datos del vehiculo.
        """

        # Establecemos los valores en la interfaz de usuario en función de los datos del vehiculo proporcionados
        self.make.setCurrentText(str(vehicle_data[0][0]))
        self.model_name.setText(vehicle_data[0][1])
        self.year.setText(str(vehicle_data[0][2]))
        self.region.setCurrentText(str(vehicle_data[0][3]))
        self.chassis.setText(vehicle_data[0][4])
        self.key_type.setCurrentText(str(vehicle_data[0][5]))
        self.transponder_type.setText(vehicle_data[0][6])
        self.programming.setCurrentText(str(vehicle_data[0][7]))
        self.cloning.setCurrentText(str(vehicle_data[0][8]))


    def get_vehicle_data(self):
        """
        Recupera los datos actualizados del vehiculo

        Returns:
            dict: Un diccionario que contiene los datos actualizados del vehiculo.
        """
        make = self.make.currentText()
        model_name = self.model_name.text()
        year = self.year.text()
        region = self.region.currentText()
        text_chassis = self.chassis.text()
        chassis = text_chassis.upper()
        key_type = self.key_type.currentText()
        text_t_type = self.transponder_type.text()
        transponder_type = text_t_type.upper()
        programming = self.programming.currentText()
        cloning = self.cloning.currentText()

        # Comprobamos si se proporcionan todos los datos requeridos
        data_list = [model_name]
        bool_data_list = list(map(lambda item: bool(item), data_list))

        if False in bool_data_list:
            # Mostramos un mensaje de advertencia si falta algún dato
            QtWidgets.QMessageBox.warning(self, "Warning", "Please input all the data",
                                          QtWidgets.QMessageBox.StandardButton.Ok)
            return

        # Crea un diccionario con los datos actualizados del vehiculo
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

    def update_vehicle_info(self):
        vehicle_data = self.get_vehicle_data()
        
        if vehicle_data:
            update_result = self.connect_db.update_vehicle(make = vehicle_data.get("make"),
                                                           model_name = vehicle_data.get("model_name"),
                                                           year = vehicle_data.get("year"),
                                                           region = vehicle_data.get("region"),
                                                           chassis = vehicle_data.get("chassis"),
                                                           key_type = vehicle_data.get("key_type"),
                                                           transponder_type = vehicle_data.get("transponder_type"),
                                                           programming = vehicle_data.get("programming"),
                                                           cloning = vehicle_data.get("cloning"))
            return update_result
        # Si los datos son incompletos, retornamos mensaje de advertencia
        else:
            return "More data needed to input."
