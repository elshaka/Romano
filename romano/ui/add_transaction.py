# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from ui_add_transaction import Ui_AddTransaction
from mango.models.transaction import Transaction
from error_message_box import ErrorMessageBox

class AddTransaction(QtGui.QDialog):
  def __init__(self, transaction_type_id, parent = None):
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

    self.ui.sackLineEdit.setValidator(QtGui.QIntValidator(0,999999,self.ui.sackLineEdit))
    self.ui.kgSackLineEdit.setValidator(QtGui.QDoubleValidator(0, 999999, 2, self.ui.kgSackLineEdit))
    self.ui.totalSackLineEdit.setValidator(QtGui.QDoubleValidator(0, 999999, 2, self.ui.totalSackLineEdit))
    self.ui.totalGrainLineEdit.setValidator(QtGui.QDoubleValidator(0, 999999, 2, self.ui.totalGrainLineEdit))

    self.ui.sackLineEdit.textChanged.connect(self.updateSackTotal)
    self.ui.kgSackLineEdit.textChanged.connect(self.updateSackTotal)

    self.ingredientWarehousesModel = WarehousesTableModel([], self)
    self.productWarehousesModel = WarehousesTableModel([], self)
    self.filterWarehousesProxyModel = QtGui.QSortFilterProxyModel()
    self.filterWarehousesProxyModel.setSourceModel(self.ingredientWarehousesModel)
    self.filterWarehousesProxyModel.setFilterKeyColumn(-1)
    self.filterWarehousesProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
    self.ui.warehousesTableView.setModel(self.filterWarehousesProxyModel)
    self.ui.filterLineEdit.textChanged.connect(self.filterWarehousesProxyModel.setFilterRegExp)

    horizontalHeader = self.ui.warehousesTableView.horizontalHeader()
    horizontalHeader.setResizeMode(QtGui.QHeaderView.Stretch)

  def createTransaction(self):
    errors = []
    warehousesModel = self.filterWarehousesProxyModel.sourceModel()
    warehouseFilteredIndex = self.ui.warehousesTableView.currentIndex()
    try:
      if self.ui.sackButton.isChecked():
        total = float(self.ui.totalSackLineEdit.text())
      else:
        total = float(self.ui.totalGrainLineEdit.text())
    except:
      total = 0
    if warehouseFilteredIndex.row() == -1:
      errors.append(u'No se ha seleccionado un almacén')
    if total == 0:
      errors.append('El peso total no puede ser 0')

    if not errors:
      warehouseIndex = self.filterWarehousesProxyModel.mapToSource(warehouseFilteredIndex)
      self.warehouse = warehousesModel.getWarehouse(warehouseIndex.row())
      if self.ui.sackButton.isChecked():
        sacks = float(self.ui.sackLineEdit.text())
        sack_weight = float(self.ui.kgSackLineEdit.text().replace(",","."))
        self.transaction = Transaction(self.transaction_type_id,
                                       self.warehouse.id, True, sack_weight, 
                                       sacks, total)
      else:
        self.transaction = Transaction(self.transaction_type_id,
                                       self.warehouse.id, False, None, 
                                       None, total)
      self.accept()
    else:
      ErrorMessageBox(errors).exec_()

  def showIngredientWarehouses(self):
    self.filterWarehousesProxyModel.setSourceModel(self.ingredientWarehousesModel)

  def showProductWarehouses(self):
    self.filterWarehousesProxyModel.setSourceModel(self.productWarehousesModel)

  def showGrain(self):
    self.ui.grainWidget.show()
    self.ui.sackWidget.hide()

  def showSack(self):
    self.ui.sackWidget.show()
    self.ui.grainWidget.hide()

  def updateSackTotal(self):
    try:
      sack = float(self.ui.sackLineEdit.text())
      kgSack = float(self.ui.kgSackLineEdit.text().replace(",","."))
      total = sack * kgSack
    except:
      total = 0
    self.ui.totalSackLineEdit.setText(str(total))

  def getWarehousesFinished(self, warehouses):
    ingredientWarehouses = []
    productWarehouses = []
    for warehouse in warehouses:
      if warehouse.warehouse_type_id == 1:
        ingredientWarehouses.append(warehouse)
      else:
        productWarehouses.append(warehouse)
    self.ingredientWarehousesModel.refreshWarehouses(ingredientWarehouses)
    self.productWarehousesModel.refreshWarehouses(productWarehouses)

class WarehousesTableModel(QtCore.QAbstractTableModel):
  def __init__(self, warehouses, parent):
    super(WarehousesTableModel, self).__init__(parent)
    self._warehouses = warehouses
    self._headers = ['Lote', u'Código', 'Nombre']#S, 'Existencia']

  def getWarehouse(self, row):
    return self._warehouses[row]

  def refreshWarehouses(self, warehouses):
    self.beginResetModel()
    self._warehouses = warehouses
    self.endResetModel()

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
      #elif column == 3:
      #  return "%s Kg" % self._warehouses[row].stock
    elif role == QtCore.Qt.TextAlignmentRole:
      if column == 3:
        return QtCore.Qt.AlignRight
      else:
        return QtCore.Qt.AlignLeft
