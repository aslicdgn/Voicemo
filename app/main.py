import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Voicemo")
        self.resize(900, 600)

        title = QLabel("Voicemo")
        title.setObjectName("title")

        subtitle = QLabel(
            "Speech emotion analysis for accessible online meetings"
        )
        subtitle.setObjectName("subtitle")

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(subtitle)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()