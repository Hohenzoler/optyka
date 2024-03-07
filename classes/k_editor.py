import subprocess
import sys
import os
from classes.python_highlighter import PythonHighlighter
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QFileSystemModel, QTreeView, \
    QVBoxLayout, QWidget, QDockWidget, QMessageBox, QMenu, QInputDialog, QLineEdit, QSplashScreen, QDialog, QTabWidget, \
    QLabel, QPlainTextEdit, QPushButton
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QKeySequence

class TerminalWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.command_history = []  # Maintain a history of entered commands
        self.command_index = 0  # Index to navigate through command history

        self.initUI()

    def initUI(self):
        self.terminalTextEdit = QTextEdit(self)
        self.terminalTextEdit.setReadOnly(True)

        self.commandLineEdit = QLineEdit(self)
        self.commandLineEdit.installEventFilter(self)  # Install event filter for command line

        self.runButton = QPushButton('Run', self)
        self.runButton.clicked.connect(self.runCommand)

        layout = QVBoxLayout(self)
        layout.addWidget(self.terminalTextEdit)
        layout.addWidget(self.commandLineEdit)
        layout.addWidget(self.runButton)

    def runCommand(self):
        command = self.commandLineEdit.text()
        self.command_history.append(command)  # Add command to history
        self.command_index = len(self.command_history)  # Set index to the latest command

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output, error = process.communicate()

        self.terminalTextEdit.insertPlainText(f"> {command}\n")
        self.terminalTextEdit.insertPlainText(output)
        self.terminalTextEdit.insertPlainText(error)
        self.terminalTextEdit.insertPlainText("\n")

        # Clear the command line after running the command
        self.commandLineEdit.clear()

    def eventFilter(self, obj, event):
        # Handle key events for command line
        if obj == self.commandLineEdit and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Up:
                # Navigate up in command history
                if self.command_index > 0:
                    self.command_index -= 1
                    self.commandLineEdit.setText(self.command_history[self.command_index])
            elif event.key() == Qt.Key_Down:
                # Navigate down in command history
                if self.command_index < len(self.command_history) - 1:
                    self.command_index += 1
                    self.commandLineEdit.setText(self.command_history[self.command_index])
            elif event.key() == Qt.Key_Return:
                # Run the command
                self.runCommand()
                return True  # Consume the Return key event
            elif event.key() == Qt.Key_Escape:
                # Clear the command line
                self.commandLineEdit.clear()
                return True  # Consume the Escape key event

        return super().eventFilter(obj, event)

class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_file_path = None
        self.highlighter = None  # Placeholder for the highlighter
        self.textEdit.setTabStopWidth(4 * self.textEdit.fontMetrics().width(' '))

        # Set a custom font with antialiasing
        font = QFont()
        font.setStyleHint(QFont.TypeWriter)
        font.setFamily("Courier")
        font.setPointSize(12)
        font.setStyleStrategy(QFont.PreferAntialias)  # Enable antialiasing
        self.textEdit.setFont(font)

        self.initTerminal()

    def showSplashScreen(self):
        splash = QSplashScreen()
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # Apply style from style.qss to the splash screen
        with open('classes/style.qss', 'r') as file:
            splash.setStyleSheet(file.read())

        # Set a custom font with larger size
        font = QFont()
        font.setPointSize(24)
        splash.setFont(font)

        splash.showMessage("KB Editor", Qt.AlignCenter | Qt.AlignCenter, Qt.white)
        splash.show()

        splash.finish(self)

    def initUI(self):
        self.showSplashScreen()
        # Load the style sheet
        with open('classes/style.qss', 'r') as file:
            self.setStyleSheet(file.read())

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        font = self.textEdit.font()
        font.setStyleHint(QFont.TypeWriter)
        font.setFamily("Courier")
        font.setPointSize(12)
        self.textEdit.setFont(font)

        newAction = QAction('New', self)
        newAction.triggered.connect(self.newFile)

        openAction = QAction('Open', self)
        openAction.triggered.connect(self.openFile)

        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.saveFile)

        saveAsAction = QAction('Save As', self)
        saveAsAction.triggered.connect(self.saveFileAs)

        undoAction = QAction('Undo', self)
        undoAction.triggered.connect(self.textEdit.undo)

        redoAction = QAction('Redo', self)
        redoAction.triggered.connect(self.textEdit.redo)



        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(undoAction)
        fileMenu.addAction(redoAction)

        # Add "About" menu
        aboutMenu = menubar.addMenu('About')
        aboutAction = QAction('About', self)
        aboutAction.triggered.connect(self.showAboutDialog)
        aboutMenu.addAction(aboutAction)

        # Add "Import Stylesheet" action to the "About" menu
        importStylesheetAction = QAction('Import Stylesheet', self)
        importStylesheetAction.triggered.connect(self.importCustomStylesheet)
        aboutMenu.addAction(importStylesheetAction)

        newShortcut = QKeySequence.New
        openShortcut = QKeySequence.Open
        saveShortcut = QKeySequence.Save
        saveAsShortcut = QKeySequence.SaveAs
        undoShortcut = QKeySequence.Undo
        redoShortcut = QKeySequence.Redo

        # Create actions for keyboard shortcuts
        newAction.setShortcut(newShortcut)
        openAction.setShortcut(openShortcut)
        saveAction.setShortcut(saveShortcut)
        saveAsAction.setShortcut(saveAsShortcut)
        undoAction.setShortcut(undoShortcut)
        redoAction.setShortcut(redoShortcut)


        self.setupFileExplorer()

        self.fileTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileTreeView.customContextMenuRequested.connect(self.showContextMenu)

        self.fileTreeView.installEventFilter(self)

        self.renaming_item = None

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Simple Code Editor')
        self.show()

    def importCustomStylesheet(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        stylesheet_path, _ = QFileDialog.getOpenFileName(self, "Import Custom Stylesheet", "",
                                                         "QSS Files (*.qss);;All Files (*)",
                                                         options=options)

        if stylesheet_path:
            with open(stylesheet_path, 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)

    def initTerminal(self):
        self.terminalWidget = TerminalWidget()

        terminalDock = QDockWidget("Terminal", self)
        terminalDock.setWidget(self.terminalWidget)

        self.addDockWidget(Qt.BottomDockWidgetArea, terminalDock)

    def showAboutDialog(self):
        aboutDialog = QDialog(self)
        aboutDialog.setWindowTitle('About Knoblauch Baguette Editor')

        versionLabel = QLabel('Knoblauch Baguette Editor Beta v0.4')

        aboutDialogLayout = QVBoxLayout()
        aboutDialogLayout.addWidget(versionLabel)
        aboutDialog.setLayout(aboutDialogLayout)

        aboutDialog.exec_()

    def setupFileExplorer(self):
        fileModel = QFileSystemModel()
        root_path = os.getcwd()
        fileModel.setRootPath(root_path)

        fileTreeView = QTreeView()
        fileTreeView.setModel(fileModel)
        fileTreeView.setRootIndex(fileModel.index(root_path))

        for column in range(1, 4):
            fileTreeView.header().setSectionHidden(column, True)

        fileExplorerLayout = QVBoxLayout()
        fileExplorerLayout.addWidget(fileTreeView)

        fileExplorerWidget = QWidget()
        fileExplorerWidget.setLayout(fileExplorerLayout)

        dock = QDockWidget("File Explorer", self)
        dock.setWidget(fileExplorerWidget)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        fileTreeView.doubleClicked.connect(self.openFileFromExplorer)

        self.fileModel = fileModel
        self.fileTreeView = fileTreeView

    def newFile(self):
        new_file_name, ok = QInputDialog.getText(self, "New File", "Enter the name of the new file (with extension):",
                                                 QLineEdit.Normal, "")

        if ok and new_file_name:
            new_file_path = os.path.join(os.getcwd(), new_file_name)
            with open(new_file_path, 'w') as file:
                file.write("")

            self.current_file_path = new_file_path
            self.textEdit.clear()

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "Python Files (*.py);;HTML Files (*.html);;Text Files (*.txt);;All Files (*)",
                                                   options=options)

        if file_name:
            self.loadFile(file_name)

    def loadFile(self, file_name):
        with open(file_name, 'r') as file:
            self.textEdit.setPlainText(file.read())
            self.current_file_path = file_name

        _, file_extension = os.path.splitext(file_name)
        if file_extension == '.py':
            self.highlighter = PythonHighlighter(self.textEdit.document())
        else:
            self.highlighter = None

    def saveFile(self):
        if self.current_file_path:
            with open(self.current_file_path, 'w') as file:
                file.write(self.textEdit.toPlainText())
        else:
            self.saveFileAs()

    def saveFileAs(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                   "Python Files (*.py);;HTML Files (*.html);;Text Files (*.txt);;All Files (*)",
                                                   options=options)

        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.textEdit.toPlainText())
            self.current_file_path = file_name

    def openFileFromExplorer(self, index: QModelIndex):
        self.current_file_path = self.fileModel.filePath(index)
        if os.path.isfile(self.current_file_path):
            _, file_extension = os.path.splitext(self.current_file_path)
            if file_extension == '.py':
                with open(self.current_file_path, 'r') as file:
                    self.textEdit.setPlainText(file.read())
                self.highlighter = PythonHighlighter(self.textEdit.document())
            else:
                self.highlighter = None
                with open(self.current_file_path, 'r') as file:
                    self.textEdit.setPlainText(file.read())

    def showContextMenu(self, pos):
        index = self.fileTreeView.indexAt(pos)

        if index.isValid():
            menu = QMenu(self)
            open_action = QAction('Open', self)
            open_action.triggered.connect(lambda: self.openFileFromExplorer(index))
            menu.addAction(open_action)
            delete_action = QAction('Delete', self)
            delete_action.triggered.connect(lambda: self.deleteFileFromExplorer(index))
            menu.addAction(delete_action)
            rename_action = QAction('Rename', self)
            rename_action.triggered.connect(lambda: self.renameFileFromExplorer(index))
            menu.addAction(rename_action)
        else:
            menu = QMenu(self)
            new_file_action = QAction('New File', self)
            new_file_action.triggered.connect(self.showNewFileDialog)
            menu.addAction(new_file_action)

        menu.exec_(self.fileTreeView.mapToGlobal(pos))

    def renameFileFromExplorer(self, index):
        item = self.fileModel.index(index.row(), 0, index.parent())
        item_path = self.fileModel.filePath(item)
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter a new name (with extension):", QLineEdit.Normal,
                                            os.path.basename(item_path))
        if ok and new_name:
            new_item_path = os.path.join(os.path.dirname(item_path), new_name)
            if os.path.exists(new_item_path):
                QMessageBox.critical(self, "Error", "A file with that name already exists.")
            else:
                os.rename(item_path, new_item_path)

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress and event.key() == Qt.Key_Return:
            if self.renaming_item:
                self.renameFileFromExplorer(self.renaming_item)
                self.renaming_item = None
        return False

    def deleteFileFromExplorer(self, index: QModelIndex):
        file_path = self.fileModel.filePath(index)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Failed to delete the file: {str(e)}")
            else:
                self.fileModel.remove(index)

    def showNewFileDialog(self):
        new_file_name, ok = QInputDialog.getText(self, "New File", "Enter the name of the new file (with extension):",
                                                 QLineEdit.Normal, "")
        if ok and new_file_name:
            new_file_path = os.path.join(os.getcwd(), new_file_name)
            with open(new_file_path, 'w') as file:
                file.write("")

    def createNewFile(self):
        new_file_name, _ = QFileDialog.getSaveFileName(self, "Create New File", "", "Text Files (*.txt);;All Files (*)")
        if new_file_name:
            with open(new_file_name, 'w') as file:
                file.write("")

    def closeEvent(self, event):
        if self.current_file_path:
            with open(self.current_file_path, 'r') as file:
                file_content = file.read()

            if self.textEdit.toPlainText() != file_content:
                reply = QMessageBox.question(self, 'Unsaved Changes',
                                             'You have unsaved changes. Do you want to save before exiting?',
                                             QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                             QMessageBox.Save)

                if reply == QMessageBox.Save:
                    self.saveFile()
                elif reply == QMessageBox.Cancel:
                    event.ignore()  # The application will not be closed
                    return
                # If the user chooses Discard, the application will close without saving.

        event.accept()  #


def excepthook(exc_type, exc_value, traceback):
    """
    Global exception handler to display an error dialog.
    """
    QMessageBox.critical(None, "Unhandled Exception",
                         f"An unhandled exception occurred:\n{exc_type.__name__}: {exc_value}")
    print(f"An unhandled exception occurred:\n{exc_type.__name__}: {exc_value}")


# Set the global exception hook
sys.excepthook = excepthook

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Enable anti-aliasing for the entire application
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    editor = CodeEditor()
    sys.exit(app.exec_())