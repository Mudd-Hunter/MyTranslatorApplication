# style.py

# ComboBox Styles
COMBOBOX_STYLE = """
    QComboBox {
        background: #f0f0f0;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 10px;
        font: bold 20px;
    }
    QComboBox::drop-down {
        width: 10px;
        background: #f0f0f0;
        border: 1px solid #ccc;
    }
    QComboBox QAbstractItemView {
        border: 6px solid #ccc;
        selection-background-color: #f0f0f0;
        selection-color: #000000;
    }
"""

# TextEdit Styles
TEXT_EDIT_STYLE = """
    QTextEdit {
        background-color: #f0f0f0;
        border: 6px solid #ccc;
        padding: 10px;
        font-size: 18px;
    }
"""

# Button Styles
BUTTON_STYLE = """
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        font-size: 20px;
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: 'blue';
    }
"""

# Label Styles
LABEL_STYLE = """
    QLabel {
        font: 16px Arial;
        color: #333;
    }
"""
