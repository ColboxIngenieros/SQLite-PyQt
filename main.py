import sys
from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtGui import QIcon

from connect_db import DatabaseConnect
from new_vehicle import NewVehicleWindow
from update_vehicle_info import UpdateVehicleWindow
from search import SearchWindow


class VehicleApplicationList(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Carga de la ventana principal del programa
        self.ui = uic.loadUi("./ui/main.ui", self)

        # Inicializamos ventanas de diálogo y conexión a la base de datos
        self.new_vehicle_dialog = NewVehicleWindow()
        self.update_vehicle_dialog = UpdateVehicleWindow()
        self.search_dialog = SearchWindow()
        self.connect_db = DatabaseConnect()

        # Definimos acciones para los elementos del menú
        self.actions = {
            self.ui.actionNew_Vehicle: "open_new_vehicle_dialog",
            self.ui.actionSearch: "open_search_dialog",
            self.ui.actionExit: "exit_app",
        }

        # Rellenamos los datos iniciales
        self.init_signal_slot()
        self.update_dashboard()
        self.search_all_vehicles()

    def init_signal_slot(self):
        # Conectamos las acciones a sus respectivas funciones
        for action, function_name in self.actions.items():
            action.triggered.connect(getattr(self, function_name))

        # Conectamos los botones a sus respectivas funciones
        self.search_dialog.detail_btn.clicked.connect(self.search_more_detail)
        self.search_dialog.vehicles_programming_btn.clicked.connect(self.search_programming_vehicles)
        self.search_dialog.vehicles_cloning_btn.clicked.connect(self.search_cloning_vehicles)
        self.search_dialog.vehicles_not_coverage_btn.clicked.connect(self.search_no_coverage_vehicles)
        self.search_dialog.all_vehicles_btn.clicked.connect(self.search_all_vehicles)

        # Conectamos los botones de diálogo del la ventana 'nuevo vehículo' a sus respectivas funciones
        self.new_vehicle_dialog.new_vehicle_save_btn.clicked.connect(self.new_vehicle_save)
        self.new_vehicle_dialog.new_vehicle_cancel_btn.clicked.connect(self.new_vehicle_cancel)

        # Conectamos los botones de la ventana 'update vehiculo' a sus respectivas funciones
        self.update_vehicle_dialog.vehicle_update_button_box.accepted.connect(self.update_vehicle_save)
        self.update_vehicle_dialog.vehicle_update_button_box.rejected.connect(self.update_vehicle_cancel)

    def open_new_vehicle_dialog(self):
        """
        Abre el cuadro de diálogo del nuevo vehículo
        """
        self.new_vehicle_dialog.show()


    def open_search_dialog(self):
        """
        Abre el cuadro de dialogo de busqueda
        """
        self.search_dialog.show()
        self.search_dialog.init_search_dialog()
        self.search_dialog.raise_()

    def exit_app(self):
        """
        Cierra la aplicacion
        """
        self.close()

    def open_update_vehicle_dialog(self, model_name):
        """
        Abre el cuadro de dialogo para actualizar los datos del vehiculo
        """
        self.update_vehicle_dialog.show()
        self.update_vehicle_dialog.init_vehicle_list(model_name=model_name)
        self.update_vehicle_dialog.raise_()

    # ------------------ Función para mostrar nuevos datos en la tabla -------------------------------------------------
    def show_data(self, data, title="Vehicle Application List"):
        """
        Orden de los datos:
            make, vehicle_name, year, region, chassis (VIN), key_type, transponder_type, programming, cloning
        : make > Fabricante
        : vehicle_name > Modelo de vehiculo
        : year > año del vehiculo
        : region > region donde se fabrico
        : chassis > chasis del vehiculo
        : key_type > tipo de llave del vehiculo
        : transponder_type > tipo de transponder que lleva la llave del vehiculo
        : programming > si el vehiculo se puede programar
        : cloning > si el vehiculo se puede clonar
        """
        table = self.ui.tableWidget
        table.setRowCount(0)
        self.ui.label_11.setText(title)

        if data:
            self.update_dashboard()
            row_count = len(data)
            table.setRowCount(row_count)

            for row, vehicle in enumerate(data):
                action_edit = QtGui.QAction(QIcon("./icon/update.svg"),"Edit", self)
                action_delete = QtGui.QAction(QIcon("./icon/delete.svg"),"Delete", self)

                # Conectamos las acciones a sus funciones
                action_edit.triggered.connect(lambda: self.action_edit_triggered(table))
                action_delete.triggered.connect(lambda: self.action_delete_triggered(table))

                # Crea un QMenu
                menu = QtWidgets.QMenu(self)
                # Añade las acciones
                menu.addActions([action_edit, action_delete])

                option_btn = QtWidgets.QPushButton(self)
                option_btn.setText("Select")
                option_btn.setMenu(menu)

                row_data = [
                    vehicle[0], vehicle[1], vehicle[2], vehicle[3], vehicle[4],
                    vehicle[5], vehicle[6],vehicle[7], vehicle[8],option_btn
                ]

                for column, item in enumerate(row_data):
                    if column == 3 or column == 6:
                        table.setColumnWidth(column, 106)
                    elif column == 2 or column == 4:
                        table.setColumnWidth(column,55)
                    else:
                        table.setColumnWidth(column,85)
                      
                    if column != 9:
                        item_obj = QtWidgets.QTableWidgetItem(str(item))
                        table.setItem(row, column, item_obj)
                    else:
                        table.setCellWidget(row, column, item)
        else: 
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)    

    def update_dashboard(self):
        current_vehicles = self.connect_db.get_current_vehicles()[0]
        self.ui.label.setText(str(current_vehicles) + "  Unit(s)")

        coverage_programming = self.connect_db.get_coverage_programming()[0]
        percent_programming = "{:.0f}".format((coverage_programming/current_vehicles)*100)
        self.ui.label_3.setText(str(percent_programming) + "%")

        coverage_cloning = self.connect_db.get_coverage_cloning()[0]
        percent_cloning = "{:.0f}".format((coverage_cloning/current_vehicles)*100)
        self.ui.label_5.setText(str(percent_cloning) + "%")

        not_coverage = self.connect_db.get_not_coverage()[0]
        percent_not_coverage = "{:.0f}".format((not_coverage/current_vehicles)*100)
        self.ui.label_7.setText(str(percent_not_coverage) + "%")


    #------------  Función QAction para las opciones de la tabla -------------------------------------------------------------- 
    def action_edit_triggered(self, table):
        model_name = table.item(table.currentRow(), 1).text()
        self.open_update_vehicle_dialog(model_name=model_name)

    def action_delete_triggered(self, table):
        make_name = table.item(table.currentRow(), 0).text()
        model_name = table.item(table.currentRow(), 1).text()
        choice = QtWidgets.QMessageBox.warning(self, "Delete !!!", f"Are you sure to delete {make_name} {model_name} ?",
                                               QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
        if choice == QtWidgets.QMessageBox.StandardButton.Yes:
            self.connect_db.delete_vehicle(model_name=model_name)

            search_data = self.search_dialog.get_all_vehicles()
            self.show_data(data=search_data, title="Vehicle Application List")

    # ------------  Función para añadir un nuevo vehiculo --------------------------------------------------------------
    def new_vehicle_save(self):
        add_result = self.new_vehicle_dialog.add_new_vehicle()

        if not add_result:
            # Limpiamos los datos del dialogo
            self.new_vehicle_dialog.clear_data()
            self.new_vehicle_dialog.close()

            # Mostramos los datos despues de añadir el vehiculo
            search_data = self.search_dialog.get_all_vehicles()
            self.show_data(data=search_data, title="Vehicle Application List")
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", add_result, QtWidgets.QMessageBox.StandardButton.Ok)

            # Retorna a la ventana principal
            self.new_vehicle_dialog.raise_()

    def new_vehicle_cancel(self):
        self.new_vehicle_dialog.close()
        search_data = self.search_dialog.get_all_vehicles()
        self.show_data(data=search_data, title="Vehicle Application List")

    # ------------  Funciónes para buscar vehiculos o mostrar los listados ----------------------------------------------------------
    
    # Busca los datos de un vehiculos especifico
    def search_more_detail(self):
        data = self.search_dialog.get_more_detail()
        if data:
            self.show_data(data=data, title="Vehicle Single Information")
    
    # Busca los vehiculos que se pueden programra
    def search_programming_vehicles(self):
        data = self.search_dialog.get_programming_vehicles()
        self.show_data(data=data, title="Vehicle Application List Programming")
    
    # Busca los vehiculos que se pueden clonar
    def search_cloning_vehicles(self):
        data = self.search_dialog.get_cloning_vehicles()
        self.show_data(data=data, title="Vehicle Application List Cloning ")
    
    # Busca los vehiculos que no se pueden programar ni clonar
    def search_no_coverage_vehicles(self):
        data = self.search_dialog.get_no_coverage_vehicles()
        self.show_data(data=data, title="Vehicle Application List No Coverage")

    # Busca todos los vehiculos
    def search_all_vehicles(self):
        data = self.search_dialog.get_all_vehicles()
        self.show_data(data=data, title="Vehicle Application List")
    
    # ------------  Funciónes para actualizar los datos de un vehiculo ----------------------------------------------------------
    
    def update_vehicle_save(self):
        update_result = self.update_vehicle_dialog.update_vehicle_info()

        if not update_result:
            self.update_vehicle_dialog.close()

            # Mostramos los datos despues de actualizra el vehiculo
            search_data = self.search_dialog.get_all_vehicles()
            self.show_data(data=search_data, title="Vehicle Applications List")

        else:
            QtWidgets.QMessageBox.warning(self, "Warning", f"Please try again: {update_result}",
                                          QtWidgets.QMessageBox.StandardButton.Ok)

            self.update_vehicle_dialog.raise_()

    def update_vehicle_cancel(self):
        self.update_vehicle_dialog.close()
        search_data = self.search_dialog.get_all_vehicles()
        self.show_data(data=search_data, title="Vehicle Application List")


# -------------- Ejecucion de la app ------------------------------------------------------------------
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = VehicleApplicationList()
    window.show()
    sys.exit(app.exec())
