import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QComboBox, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon

class DLLInjector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Guns DLL Injector')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 400, 200)

        self.lbl_dll = QLabel('Select the DLL file:', self)
        self.btn_dll = QPushButton('Select', self)
        self.btn_dll.clicked.connect(self.openDLLDialog)

        self.lbl_exe = QLabel('Select the EXE process:', self)
        self.combo_exe = QComboBox(self)
        self.populateEXEComboBox()

        self.btn_inject = QPushButton('Inject DLL', self)
        self.btn_inject.clicked.connect(self.injectDLL)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_dll)
        layout.addWidget(self.btn_dll)
        layout.addWidget(self.lbl_exe)
        layout.addWidget(self.combo_exe)
        layout.addWidget(self.btn_inject)

        self.setLayout(layout)

        self.selected_dll = ""
        self.selected_exe = ""

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton, QComboBox {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover, QComboBox:hover {
                background-color: #45a049;
            }
            QPushButton:pressed, QComboBox:pressed {
                background-color: #3c8039;
            }
        """)

    def populateEXEComboBox(self):
        self.combo_exe.clear()
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].endswith('.exe'):
                self.combo_exe.addItem(proc.info['name'])

    def openDLLDialog(self):
        self.selected_dll, _ = QFileDialog.getOpenFileName(self,"Select the DLL file", "","DLL Files (*.dll);;All Files (*)")

    def injectDLL(self):
        if not self.selected_dll or self.combo_exe.currentIndex() == -1:
            QMessageBox.warning(self, 'Error', 'Please select DLL file and EXE process!')
            return

        selected_exe = self.combo_exe.currentText()

        try:
            import pyinstaller
            pyinstaller.__path__  
            import os
            os.system(f'pyinstaller --add-data "{self.selected_dll};." "{selected_exe}"')
            QMessageBox.information(self, 'Sukces', 'Plik DLL został pomyślnie wstrzyknięty!')
        except ImportError:
            QMessageBox.critical(self, 'Error', 'The pyinstaller library was not installed. Please note the use of "pip install pyinstaller".')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DLLInjector()
    window.show()
    sys.exit(app.exec_())
