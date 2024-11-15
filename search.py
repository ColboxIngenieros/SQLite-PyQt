from PyQt6 import QtWidgets, uic
from connect_db import DatabaseConnect


class SearchWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Cargamos el archivo UI 
        self.ui = uic.loadUi("./ui/search.ui", self)

        self.connect_db = DatabaseConnect()

        # Referenciamos los elementos de layour 'search by name'
        self.model_name_LW = self.ui.listWidget
        self.input_model_name_LE = self.ui.lineEdit

        # Referenciamos las etiquetas
        self.current_make_label = self.ui.label_2
        self.current_year_label = self.ui.label_4
        self.current_chassis_label = self.ui.label_6
        self.current_region_label = self.ui.label_8
        self.current_key_type_label = self.ui.label_10
        self.current_transponder_type_label = self.ui.label_12
        self.current_programming_label = self.ui.label_14
        self.current_cloning_label = self.ui.label_16

        # Referenciamos los botones
        self.all_vehicles_btn = self.ui.pushButton 
        self.vehicles_programming_btn = self.ui.pushButton_2
        self.vehicles_cloning_btn = self.ui.pushButton_3
        self.vehicles_not_coverage_btn = self.ui.pushButton_4
        self.detail_btn = self.ui.pushButton_5

        # Inicializamos el cuadro de dialogo de busqueda
        self.init_search_dialog()

        # Conectamos las señales a los elementos
        self.input_model_name_LE.textChanged.connect(self.update_vehicle_name_list)
        self.model_name_LW.currentTextChanged.connect(self.search_vehicle_info)

    def init_search_dialog(self):
        """
        Inicializa el cuadro de diálogo de búsqueda rellenando la lista de nombres de vehículos.
        """
        self.input_model_name_LE.clear()
        search_result = self.connect_db.get_vehicle_names("")
        model_name_list = [item[0] for item in search_result]
        self.model_name_LW.clear()
        self.model_name_LW.addItems(model_name_list)

        # Inicializamos los valores de las etiquetas
        self.current_make_label.setText("-")
        self.current_year_label.setText("-")
        self.current_region_label.setText("-")
        self.current_chassis_label.setText("-")
        self.current_key_type_label.setText("-")
        self.current_transponder_type_label.setText("-")
        self.current_programming_label.setText("-")
        self.current_cloning_label.setText("-")        

    def get_more_detail(self):
        model_name_obj = self.ui.listWidget.currentItem()

        if model_name_obj:
            model_name = model_name_obj.text()

            data = self.connect_db.get_data(model_name=model_name)
            self.close()
            return data

        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a vehicle.")
            return
    
    #------------  Funciónes de recuperacion (get) de los datos con sentencias SQL ----------------------------------------------------- 
    def get_programming_vehicles(self):
        data = self.connect_db.get_data(search_flag="PROGRAMMING")
        self.close()

        return data
    
    def get_cloning_vehicles(self):
        data = self.connect_db.get_data(search_flag="CLONING")
        self.close()

        return data
    
    def get_no_coverage_vehicles(self):
        data = self.connect_db.get_data(search_flag="NO_COVERAGE")
        self.close()

        return data

    def get_all_vehicles(self):
        data = self.connect_db.get_data(search_flag="ALL")
        self.close()

        return data


    def search_vehicle_info(self, model_name):
        """
        Busca información del vehículo y actualiza las etiquetas de la interfaz.
        """
        if model_name:
            # Recuperamos la informacion del vehiculo de la base de datos
            search_result = self.connect_db.get_single_vehicle_info(model_name=model_name)

            # Actualizamos los elementos de la interfaz con la informacion recibida
            self.current_make_label.setText(search_result[0])
            self.current_year_label.setText(str(search_result[1]))
            self.current_region_label.setText(search_result[2])
            self.current_chassis_label.setText(search_result[3])
            self.current_key_type_label.setText(search_result[4])
            self.current_transponder_type_label.setText(search_result[5])
            self.current_programming_label.setText(search_result[6])
            self.current_cloning_label.setText(search_result[7])

        else:
            # Limpiamos las etiquetas si no se ha seleccionado ningun vehiculo
            self.current_make_label.setText("-")
            self.current_year_label.setText("-")
            self.current_region_label.setText("-")
            self.current_chassis_label.setText("-")
            self.current_key_type_label.setText("-")
            self.current_transponder_type_label.setText("-")
            self.current_programming_label.setText("-")
            self.current_cloning_label.setText("-")

    def update_vehicle_name_list(self, text):
        """
        Actualiza la lista de nombres de vehículos en función del texto de entrada.
        """
        self.model_name_LW.clear()

        # Recuperamos los nombres de los vehiculos de la base de datos en función del texto de entrada
        search_result = self.connect_db.get_vehicle_names(text)
        model_name_list = [item[0] for item in search_result]
        self.model_name_LW.addItems(model_name_list)
