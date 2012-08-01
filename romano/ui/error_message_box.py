from PySide.QtGui import QMessageBox

class ErrorMessageBox(QMessageBox):
  def __init__(self, errors):
    super(ErrorMessageBox, self).__init__()
    errors_list_string = ""
    for error in errors:
      errors_list_string += "- %s \n" % error
    self.setWindowTitle("Error")
    self.setText(errors_list_string)
