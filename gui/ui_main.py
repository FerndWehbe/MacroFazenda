import json
import os

import keyboard  # Biblioteca para capturar eventos de teclado
from pynput import mouse
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)


class UIMainWindow:
    def setup_ui(self, parent: QMainWindow) -> None:
        if not parent.objectName():
            parent.setObjectName("MainWindow")

        parent.resize(960, 540)
        parent.setMinimumSize(640, 360)

        # Carregar traduções do arquivo JSON
        self.translations = self.load_translations("translations.json")

        # Idioma atual (padrão: português)
        self.current_language = "pt"

        # Variáveis de configuração
        self.config = {
            "point_acao": "",
            "multiplas_caixas": "",
            "opcao_trigo": "",
            "opcao_milho": "",
            "opcao_linho": "",
            "opcao_cenoura": "",
            "opcao_cogumelo": "",
            "opcao_tomate": "",
            "ciclo_plantacao": "",
        }

        # Listener do mouse
        self.listener = None

        # Estado de execução da automação
        self.running = False

        # Create Central Widget
        self.central_frame = QFrame()

        # Create Main Layout
        self.main_layout = QVBoxLayout(self.central_frame)

        # Top Layout for Language Selection (aligned to the right)
        self.top_layout = QHBoxLayout()

        # Spacer to push the combo box to the right
        self.top_layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        # Language selection combo box
        self.language_combo = QComboBox(parent)
        self.language_combo.addItems(["Português", "English"])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        self.top_layout.addWidget(self.language_combo)

        # Add top layout to the main layout
        self.main_layout.addLayout(self.top_layout)

        # Content Frame (MainWindow Frame)
        self.content = QFrame()
        self.content.setStyleSheet(
            """
            QFrame {
                border: 2px solid #000000;
                border-radius: 10px;
                background-color: none;
            }
        """
        )

        # Content Layout
        self.content_layout = QVBoxLayout(self.content)

        # Creating labels and input fields
        self.labels = []
        self.inputs = []
        self.buttons_capture = []

        for i in range(8):
            row_layout = QHBoxLayout()
            label = QLabel(parent)
            input_text = QLineEdit(parent)
            button_capture = QPushButton("Capturar", parent)

            self.labels.append(label)
            self.inputs.append(input_text)
            self.buttons_capture.append(button_capture)

            row_layout.addWidget(label)
            row_layout.addWidget(input_text)
            row_layout.addWidget(button_capture)

            self.content_layout.addLayout(row_layout)

            # Conectar o botão de captura de posição do mouse
            button_capture.clicked.connect(lambda _, i=i: self.capture_position(i))

        # Campo específico para Ciclo Plantação (sem botão de captura)
        row_layout = QHBoxLayout()
        label = QLabel(parent)
        input_text = QLineEdit(parent)

        self.labels.append(label)
        self.inputs.append(input_text)

        row_layout.addWidget(label)
        row_layout.addWidget(input_text)
        self.content_layout.addLayout(row_layout)

        # Action Data Frame
        self.data_actions = QFrame()
        self.data_actions.setStyleSheet(
            """
            QFrame {
                border: 2px solid #000000;
                border-radius: 10px;
                background-color: none;
            }
            QLabel {
                border: none;
            }
        """
        )
        self.data_actions_layout = QHBoxLayout(self.data_actions)

        # Adding action buttons in Data Actions Frame
        self.buttons = []

        for action in ["button_1", "button_2", "button_3", "button_4"]:
            action_button = QPushButton(parent)
            self.buttons.append(action_button)
            self.data_actions_layout.addWidget(action_button)

        # Running/Stop Frame
        self.start_stop_frame = QFrame()
        self.start_stop_frame.setStyleSheet(
            """
            QFrame {
                border: 2px solid #000000;
                border-radius: 10px;
                background-color: none;
            }
            QLabel {
                border: none;
            }
        """
        )
        self.start_stop_layout = QHBoxLayout(self.start_stop_frame)

        # Adding start and stop buttons in Start/Stop Frame
        self.start_button = QPushButton(parent)
        self.stop_button = QPushButton(parent)

        self.buttons.append(self.start_button)
        self.buttons.append(self.stop_button)

        self.start_stop_layout.addWidget(self.start_button)
        self.start_stop_layout.addWidget(self.stop_button)

        # Add frames to the main layout
        self.main_layout.addWidget(self.content)
        self.main_layout.addWidget(self.data_actions)
        self.main_layout.addWidget(self.start_stop_frame)

        # Set Central Frame
        parent.setCentralWidget(self.central_frame)

        # Atualizar o texto da interface para o idioma padrão
        self.update_texts()

        # Connect button actions
        self.buttons[0].clicked.connect(self.save_config)
        self.buttons[1].clicked.connect(self.clear_config)
        self.buttons[2].clicked.connect(self.export_config)
        self.buttons[3].clicked.connect(self.import_config)
        self.start_button.clicked.connect(self.start_automation)
        self.stop_button.clicked.connect(self.stop_automation)

        # Carregar o preset salvo ao iniciar
        self.load_preset()

        # Configurar hotkey F8 para iniciar/parar automação
        keyboard.add_hotkey("f8", self.toggle_automation)

    def load_translations(self, file_path):
        """Carrega as traduções de um arquivo JSON."""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            print(f"Arquivo de tradução {file_path} não encontrado!")
            return {}

    def change_language(self):
        # Atualiza o idioma com base na seleção da QComboBox
        if self.language_combo.currentIndex() == 0:
            self.current_language = "pt"
        else:
            self.current_language = "en"
        self.update_texts()

    def update_texts(self):
        # Atualiza o texto de todas as labels e botões com base no idioma atual
        labels_keys = [
            "label_1",
            "label_2",
            "label_3",
            "label_4",
            "label_5",
            "label_6",
            "label_7",
            "label_8",
            "label_9",
        ]
        buttons_keys = [
            "button_1",
            "button_2",
            "button_3",
            "button_4",
            "start_button",
            "stop_button",
        ]
        capture_buttons_text = self.translations.get("capture_button", {}).get(
            self.current_language, "Capturar"
        )

        for i, key in enumerate(labels_keys):
            self.labels[i].setText(
                self.translations.get(key, {}).get(self.current_language, "")
            )

        for i, key in enumerate(buttons_keys):
            self.buttons[i].setText(
                self.translations.get(key, {}).get(self.current_language, "")
            )

        for button in self.buttons_capture:
            button.setText(capture_buttons_text)

    def capture_position(self, index):
        # Captura a posição do mouse e seta no campo correspondente
        parent = self.central_frame.parentWidget()  # Referencia ao QMainWindow
        parent.setCursor(Qt.CrossCursor)

        def on_click(x, y, button, pressed):
            if pressed:
                self.inputs[index].setText(f"{x},{y}")
                print(f"Posição capturada: {x},{y}")
                self.listener.stop()
                parent.setCursor(Qt.ArrowCursor)

        self.listener = mouse.Listener(on_click=on_click)
        self.listener.start()

    def save_config(self):
        # Save the configuration to a JSON file
        config = {
            key: self.inputs[i].text() for i, key in enumerate(self.config.keys())
        }
        with open("preset_config.json", "w") as file:
            json.dump(config, file, indent=4)
        print("Configuração salva.")

    def clear_config(self):
        # Clear the configuration in the UI
        for input_field in self.inputs:
            input_field.clear()

    def export_config(self):
        # Export the configuration to a JSON file
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Exportar Configuração", "", "JSON Files (*.json)"
        )
        if file_path:
            config = {
                key: self.inputs[i].text() for i, key in enumerate(self.config.keys())
            }
            with open(file_path, "w") as file:
                json.dump(config, file, indent=4)
            print(f"Configuração exportada para {file_path}")

    def import_config(self):
        # Import the configuration from a JSON file
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Importar Configuração", "", "JSON Files (*.json)"
        )
        if file_path:
            with open(file_path, "r") as file:
                config = json.load(file)
                for i, key in enumerate(self.config.keys()):
                    value = config.get(key, "")
                    if isinstance(
                        value, list
                    ):  # Se for uma lista (por exemplo, ciclo_plantacao)
                        value = ", ".join(
                            value
                        )  # Converter a lista para uma string separada por vírgulas
                    self.inputs[i].setText(value)
            print(f"Configuração importada de {file_path}")

    def load_preset(self):
        # Carrega o preset salvo
        file_path = "preset_config.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                config = json.load(file)
                for i, key in enumerate(self.config.keys()):
                    self.inputs[i].setText(config.get(key, ""))
            print("Preset carregado.")

    def start_automation(self):
        self.running = True
        print("Automation started")
        self.update_button_styles()

    def stop_automation(self):
        self.running = False
        print("Automation stopped")
        self.update_button_styles()

    def toggle_automation(self):
        if self.running:
            self.stop_automation()
        else:
            self.start_automation()

    def update_button_styles(self):
        if self.running:
            self.start_button.setStyleSheet("background-color: green; color: white;")
            self.stop_button.setStyleSheet("")
        else:
            self.start_button.setStyleSheet("")
            self.stop_button.setStyleSheet("background-color: red; color: white;")
