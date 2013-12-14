# -*- coding: utf-8 -*-

from PySide.QtGui import QMessageBox

class ErrorMessageBox(QMessageBox):
  def __init__(self, errors):
    super(ErrorMessageBox, self).__init__()
    errors_list_string = ""
    for error in errors:
      errors_list_string += "- %s \n" % error
    self.setWindowTitle("Error")
    self.setText(errors_list_string)

class NewErrorMessageBox(QMessageBox):
  def __init__(self, errors):
    super(NewErrorMessageBox, self).__init__()
    errors_list_string = ""
    t = {
        'description': "La descripción",
        'number': "El número",
        'start_date': "La fecha de inicio",
        'end_date': "La fecha de finalización",
        'name': "El nombre",
        'prog_batches': "Los baches programados",
        'code': "El código",
        'wet_time': "El tiempo húmedo",
        'dry_time': "El tiempo seco",
        'address': "La dirección",
        'tel1': "El teléfono",
        'license_plate': "La placa",
        'ci_rif': "La Cédula/RIF"
    }
    for field, field_errors in list(errors.items()):
      for field_error in field_errors:
        errors_list_string += "- %s %s\n" % (t[field], field_error)
    self.setWindowTitle("Error")
    self.setText(errors_list_string)
