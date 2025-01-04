import sys
from PyQt5.QtWidgets import QApplication
from frontend.pyqt_gui import PyQtGui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PyQtGui()
    window.run()
    sys.exit(app.exec_())

"""from kivy.app import App
from kivy.core.window import Window

from frontend.kivy_gui import KivyGui  # Import the Kivy-based GUI


class MainApp(App):
    def build(self):
        # Optionally set the window size (useful for testing on desktops)
        Window.size = (800, 600)  # Width x Height
        return KivyGui()

if __name__ == '__main__':
    app = KivyGui()
    app.run()"""