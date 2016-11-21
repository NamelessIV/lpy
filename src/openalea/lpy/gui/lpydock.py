from openalea.vpltk.qt import qt
try:
    from openalea.oalab.shell import get_shell_class
    from openalea.core.interpreter import get_interpreter_class
except :
    from openalea.vpltk.shell.shell import get_shell_class, get_interpreter_class

import debugger_ui
import debugger_right_ui
from objectpanel import LpyObjectPanelDock


Qt = qt.QtCore.Qt
QApplication = qt.QtWidgets.QApplication
QSplitter = qt.QtWidgets.QSplitter
QDockWidget = qt.QtWidgets.QDockWidget
QWidget = qt.QtWidgets.QWidget
QIcon = qt.QtGui.QIcon
QPixmap = qt.QtGui.QPixmap
_translate = qt.QtCore.QCoreApplication.translate

class DebugLeftWidget(QWidget,debugger_ui.Ui_Form):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        debugger_ui.Ui_Form.__init__(self)
        self.setupUi(self)

class DebugRightWidget(QWidget,debugger_right_ui.Ui_Form):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        debugger_right_ui.Ui_Form.__init__(self)
        self.setupUi(self)

def showMessage(self,msg,timeout):
    if hasattr(self,'statusBar'):
        self.statusBar.showMessage(msg,timeout)
    else:
        print(msg)
        
def initDocks(lpywidget):
    prevdock = None
    st = lpywidget.statusBar()
    for i,dock in enumerate([lpywidget.materialDock, lpywidget.scalarDock, lpywidget.descriptionDock, lpywidget.parametersDock]):
        lpywidget.addDockWidget(Qt.LeftDockWidgetArea,dock)
        #lpywidget.menuView.addAction(dock.toggleViewAction())
        dock.statusBar = st
        dock.showMessage = showMessage
        if not prevdock is None:
            lpywidget.tabifyDockWidget(prevdock,dock)
        prevdock = dock
    lpywidget.menuView.addAction(lpywidget.materialDock.toggleViewAction())
    lpywidget.menuView.addAction(lpywidget.scalarDock.toggleViewAction())
    lpywidget.vparameterView = lpywidget.menuView.addMenu("Graphical Parameters")
    lpywidget.menuView.addSeparator()
    lpywidget.menuView.addAction(lpywidget.descriptionDock.toggleViewAction())
    lpywidget.menuView.addAction(lpywidget.parametersDock.toggleViewAction())
   
    lpywidget.addDockWidget(Qt.LeftDockWidgetArea,lpywidget.helpDock)
    action = lpywidget.helpDock.toggleViewAction()
    action.setShortcut(_translate("MainWindow", "F1"))
    lpywidget.helpDock.hide()
    lpywidget.helpDock.setFloating(True)
    icon = QIcon()
    icon.addPixmap(QPixmap(":/images/icons/book.png"),QIcon.Normal,QIcon.Off)
    action.setIcon(icon)
    lpywidget.menuHelp.addSeparator()
    lpywidget.menuHelp.addAction(action)
    lpywidget.tabifyDockWidget(lpywidget.materialDock,lpywidget.parametersDock)
    lpywidget.tabifyDockWidget(lpywidget.parametersDock,lpywidget.descriptionDock)
    # debug dock
    lpywidget.debugDock = QDockWidget("Debugger",lpywidget)
    lpywidget.debugDock.setObjectName("LpyDebugger")
    lpywidget.debugWidget = QSplitter(Qt.Horizontal,lpywidget)
    lpywidget.debugWidget.left = DebugLeftWidget(lpywidget.debugWidget)
    lpywidget.debugWidget.addWidget(lpywidget.debugWidget.left)
    lpywidget.debugWidget.right = DebugRightWidget(lpywidget.debugWidget)
    lpywidget.debugWidget.addWidget(lpywidget.debugWidget.right)
    lpywidget.debugWidget.setEnabled(False)
    lpywidget.debugDock.setWidget(lpywidget.debugWidget)
    lpywidget.addDockWidget(Qt.BottomDockWidgetArea,lpywidget.debugDock)    
    action = lpywidget.debugDock.toggleViewAction()
    lpywidget.menuView.addSeparator()
    lpywidget.menuView.addAction(action)
    lpywidget.debugDock.hide()
    #profiler dock
    lpywidget.addDockWidget(Qt.BottomDockWidgetArea,lpywidget.profilerDock)    
    action = lpywidget.profilerDock.toggleViewAction()
    lpywidget.menuView.addAction(action)
    lpywidget.profilerDock.hide()
    #interpreter dock
    if lpywidget.withinterpreter :
        shellclass = get_shell_class()
        interpreterclass = get_interpreter_class()
        lpywidget.interpreter = interpreterclass()
        lpywidget.shell = shellclass(lpywidget.interpreter, parent=lpywidget.interpreterDock)    
        lpywidget.interpreterDock.setWidget(lpywidget.shell)
        action = lpywidget.interpreterDock.toggleViewAction()
        action.setShortcut(_translate("MainWindow", "Ctrl+P"))
        lpywidget.menuView.addSeparator()
        lpywidget.menuView.addAction(action)
        lpywidget.interpreter.locals['window'] = lpywidget
        lpywidget.interpreter.locals['clear'] = lpywidget.shell.clear
        try:
            exec('from openalea.plantgl.all import *',lpywidget.interpreter.locals,lpywidget.interpreter.locals)
            exec('from openalea.lpy import *',lpywidget.interpreter.locals,lpywidget.interpreter.locals)
            #lpywidget.interpreter.loadcode('from openalea.plantgl.all import *' )
            #lpywidget.interpreter.loadcode('from openalea.lpy import *')
            # lpywidget.interpreter.runcode('from openalea.plantgl.all import *')
            # lpywidget.interpreter.runcode('from openalea.lpy import *')
        except:
            lpywidget.interpreter.runcode('from openalea.plantgl.all import *')
            lpywidget.interpreter.runcode('from openalea.lpy import *')
        lpywidget.addDockWidget(Qt.BottomDockWidgetArea,lpywidget.interpreterDock)
        lpywidget.tabifyDockWidget(lpywidget.debugDock,lpywidget.interpreterDock)
    else:
        lpywidget.interpreter = None
         
