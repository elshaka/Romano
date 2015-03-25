# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from .ui_add_transaction import Ui_AddTransaction
from mango.models.transaction import Transaction
from .error_message_box import ErrorMessageBox

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
    self.ui.ingredientButton.clicked.connect(self.showLots)
    self.ui.productButton.clicked.connect(self.showProductLots)
    self.ui.grainButton.clicked.connect(self.showGrain)
    self.ui.sackButton.clicked.connect(self.showSack)

    self.ui.sackLineEdit.setValidator(QtGui.QIntValidator(0,999999,self.ui.sackLineEdit))
    self.ui.kgSackLineEdit.setValidator(QtGui.QDoubleValidator(0, 999999, 2, self.ui.kgSackLineEdit))
    self.ui.totalSackLineEdit.setValidator(QtGui.QDoubleValidator(0, 999999, 2, self.ui.totalSackLineEdit))
    self.ui.totalGrainLineEdit.setValidator(QtGui.QDoubleValidator(0, 999999, 2, self.ui.totalGrainLineEdit))

    self.ui.sackLineEdit.textChanged.connect(self.updateSackTotal)
    self.ui.kgSackLineEdit.textChanged.connect(self.updateSackTotal)

    self.lotsModel = LotsTableModel([], self)
    self.productLotsModel = LotsTableModel([], self)
    self.filterLotsProxyModel = QtGui.QSortFilterProxyModel()
    self.filterLotsProxyModel.setSourceModel(self.lotsModel)
    self.filterLotsProxyModel.setFilterKeyColumn(-1)
    self.filterLotsProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
    self.ui.lotsTableView.setModel(self.filterLotsProxyModel)
    self.ui.lotsTableView.setItemDelegate(MultilineItemDelegate(self))
    self.ui.filterLineEdit.textChanged.connect(self.filterLotsProxyModel.setFilterRegExp)

    horizontalHeader = self.ui.lotsTableView.horizontalHeader()
    horizontalHeader.resizeSection(0, 200)
    horizontalHeader.resizeSection(1, 250)
    horizontalHeader.setResizeMode(2, QtGui.QHeaderView.Stretch)

  def createTransaction(self):
    errors = []
    lotsModel = self.filterLotsProxyModel.sourceModel()
    lotFilteredIndex = self.ui.lotsTableView.currentIndex()
    content_type = 1
    if self.ui.productButton.isChecked():
      content_type = 2
    try:
      if self.ui.sackButton.isChecked():
        total = float(self.ui.totalSackLineEdit.text())
      else:
        total = float(self.ui.totalGrainLineEdit.text())
    except:
      total = 0
    if lotFilteredIndex.row() == -1:
      errors.append('No se ha seleccionado un lote')
    if total == 0:
      errors.append('El peso total no puede ser 0')

    if not errors:
      lotIndex = self.filterLotsProxyModel.mapToSource(lotFilteredIndex)
      self.lot = lotsModel.getLot(lotIndex.row())
      if self.ui.sackButton.isChecked():
        sacks = float(self.ui.sackLineEdit.text())
        sack_weight = float(self.ui.kgSackLineEdit.text().replace(",","."))
        self.transaction = Transaction(self.transaction_type_id, content_type,
                                       self.lot.id, True, sack_weight, 
                                       sacks, total)
      else:
        self.transaction = Transaction(self.transaction_type_id, content_type,
                                       self.lot.id, False, None, 
                                       None, total)
      self.transaction.content_comment = self.lot.comment
      self.accept()
    else:
      ErrorMessageBox(errors).exec_()

  def showLots(self):
    self.filterLotsProxyModel.setSourceModel(self.lotsModel)

  def showProductLots(self):
    self.filterLotsProxyModel.setSourceModel(self.productLotsModel)

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

  def getLotsFinished(self, lots):
    self.lotsModel.refreshLots(lots)
  
  def getProductLotsFinished(self, product_lots):
    self.productLotsModel.refreshLots(product_lots)

class LotsTableModel(QtCore.QAbstractTableModel):
  def __init__(self, lots, parent):
    super(LotsTableModel, self).__init__(parent)
    self._lots = lots
    self._headers = ['Código Lote', 'Nombre', 'Comentario']

  def getLot(self, row):
    return self._lots[row]

  def refreshLots(self, lots):
    self.beginResetModel()
    self._lots = lots
    self.endResetModel()

  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      if orientation == QtCore.Qt.Horizontal:
        return self._headers[section]

  def rowCount(self, parent):
    return len(self._lots)

  def columnCount(self, parent):
    return len(self._headers)

  def data(self, index, role):
    row = index.row()
    column = index.column()
    if role == QtCore.Qt.DisplayRole:
      if column == 0:
        return self._lots[row].code
      elif column == 1:
        return self._lots[row].content_name
      elif column == 2:
        return self._lots[row].comment
    elif role == QtCore.Qt.TextAlignmentRole:
      if column == 3:
        return QtCore.Qt.AlignRight
      else:
        return QtCore.Qt.AlignLeft

class MultilineItemDelegate(QtGui.QStyledItemDelegate):
  def __init__(self, parent):
    super(MultilineItemDelegate, self).__init__(parent)

  def sizeHint(self, option, index):
    result = QtGui.QStyledItemDelegate(option, index)
    result.setHeight(result.height() * 2)
    return result

  def drawDisplay(self, painter, option, rect, text):
    painter.drawText(rect, text, option)
