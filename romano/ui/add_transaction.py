# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from ui_add_transaction import Ui_AddTransaction
from mango.models.transaction import Transaction
from error_message_box import ErrorMessageBox

class AddTransaction(QtGui.QDialog):
  def __init__(self, ingredientWarehouses, productWarehouses, transaction_type_id, parent = None):
    super(AddTransaction, self).__init__(parent)
    self.ui = Ui_AddTransaction()
    self.ui.setupUi(self)
    self.setModal(True)
    self.ui.grainWidget.hide()
    
    self.transaction_type_id = transaction_type_id
    
    self.ui.addTransactionButton.clicked.connect(self.createTransaction)
    self.ui.cancelButton.clicked.connect(self.reject)
    self.ui.ingredientButton.clicked.connect(self.showIngredientWarehouses)
    self.ui.productButton.clicked.connect(self.showProductWarehouses)
    self.ui.grainButton.clicked.connect(self.showGrain)
    self.ui.sackButton.clicked.connect(self.showSack)
    self.ui.sackSpinBox.valueChanged.connect(self.updateSackTotal)
    self.ui.kgSackSpinBox.valueChanged.connect(self.updateSackTotal)
    
    self.ingredientWarehousesModel = WarehousesTableModel(ingredientWarehouses, self)
    self.productWarehousesModel = WarehousesTableModel(productWarehouses, self)
    self.ui.warehousesTableView.setModel(self.ingredientWarehousesModel)
    horizontalHeader = self.ui.warehousesTableView.horizontalHeader()
    horizontalHeader.setResizeMode(QtGui.QHeaderView.Stretch)
    
  def createTransaction(self):
    errors = []
    warehousesModel = self.ui.warehousesTableView.model()
    warehouseTableRow = self.ui.warehousesTableView.currentIndex().row()
    if self.ui.sackButton.isChecked():
      total = self.ui.totalSackSpinBox.value()
    else:
      total = self.ui.totalGrainSpinBox.value()
    
    if warehouseTableRow == -1:
      errors.append(u'No se ha seleccionado un almacén')
    if total == 0:
      errors.append('El peso total no puede ser 0')
    
    if not errors:
      self.warehouse = warehousesModel.getWarehouse(warehouseTableRow)
      self.transaction = Transaction(self.transaction_type_id,
                                     self.warehouse.id, total)
      self.accept()
    else:
      ErrorMessageBox(errors).exec_()
    
  def showIngredientWarehouses(self):
    self.ui.warehousesTableView.setModel(self.ingredientWarehousesModel)
    
  def showProductWarehouses(self):
    self.ui.warehousesTableView.setModel(self.productWarehousesModel)
    
  def showGrain(self):
    self.ui.grainWidget.show()
    self.ui.sackWidget.hide()
    
  def showSack(self):
    self.ui.sackWidget.show()
    self.ui.grainWidget.hide()
    
  def updateSackTotal(self):
    total = self.ui.sackSpinBox.value() * self.ui.kgSackSpinBox.value()
    self.ui.totalSackSpinBox.setValue(total)

class WarehousesTableModel(QtCore.QAbstractTableModel):
  def __init__(self, warehouses, parent):
    super(WarehousesTableModel, self).__init__(parent)
    self._warehouses = warehouses
    self._headers = ['Lote', u'Código', 'Nombre', 'Existencia']
    
  def getWarehouse(self, row):
    return self._warehouses[row]
  
  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      if orientation == QtCore.Qt.Horizontal:
        return self._headers[section]
        
  def rowCount(self, parent):
    return len(self._warehouses)
    
  def columnCount(self, parent):
    return len(self._headers)
    
  def data(self, index, role):
    row = index.row()
    column = index.column()
    if role == QtCore.Qt.DisplayRole:
      if column == 0:
        return self._warehouses[row].lot_code
      elif column == 1:
        return self._warehouses[row].content_code
      elif column == 2:
        return self._warehouses[row].content_name
      elif column == 3:
        return "%s Kg" % self._warehouses[row].stock
    elif role == QtCore.Qt.TextAlignmentRole:
      if column == 3:
        return QtCore.Qt.AlignRight
      else:
        return QtCore.Qt.AlignLeft
        
