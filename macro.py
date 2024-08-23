import itertools
import json
import logging
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, ttk

import keyboard
import pyautogui
from pynput import mouse

CONFIG_FILE = "preset_config.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("automacao.log"), logging.StreamHandler()],
)


class AutomationConfigApp:
    def __init__(self, master):
        self.master = master
        master.title("Configuração de Automação")

        # Variáveis para coordenadas
        self.point_acao = tk.StringVar()
        self.multiplas_caixas = tk.StringVar()
        self.opcao_trigo = tk.StringVar()
        self.opcao_milho = tk.StringVar()
        self.opcao_linho = tk.StringVar()
        self.opcao_cenoura = tk.StringVar()
        self.opcao_cogumelo = tk.StringVar()
        self.opcao_tomate = tk.StringVar()

        # Variável para ciclo de plantação
        self.ciclo_plantacao = tk.StringVar()

        # Caminho do ícone de colheita
        # self.colheita = os.path.join(self.resource_path("colheita.png"))
        self.colheita = "colheita.png"

        # Estado de execução
        self.running = False

        # Criando campos de entrada e botões
        self.create_label_entry_button("Botão de Ação", self.point_acao, 0)
        self.create_label_entry_button("Area de Colheita", self.multiplas_caixas, 1)
        self.create_label_entry_button("Posição Trigo", self.opcao_trigo, 2)
        self.create_label_entry_button("Posição Milho", self.opcao_milho, 3)
        self.create_label_entry_button("Posição Linho", self.opcao_linho, 4)
        self.create_label_entry_button("Posição Cenoura", self.opcao_cenoura, 5)
        self.create_label_entry_button("Posição Cogumelo", self.opcao_cogumelo, 6)
        self.create_label_entry_button("Posição Tomate", self.opcao_tomate, 7)

        # Campo para ciclo de plantação
        ttk.Label(master, text="Ciclo Plantação (separado por vírgulas)").grid(
            row=10, column=0, sticky="W"
        )
        ttk.Entry(master, textvariable=self.ciclo_plantacao, width=50).grid(
            row=10, column=1, sticky="W"
        )

        # Frame para os botões de ações
        button_frame = tk.Frame(master)
        button_frame.grid(row=11, column=0, columnspan=3, pady=10)

        # Botões para salvar, limpar, exportar e importar configurações
        self.save_button = ttk.Button(
            button_frame, text="Salvar Configurações", command=self.save_config
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(
            button_frame, text="Limpar Configurações", command=self.clear_config
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.export_button = ttk.Button(
            button_frame, text="Exportar Configuração", command=self.export_config
        )
        self.export_button.pack(side=tk.LEFT, padx=5)

        self.import_button = ttk.Button(
            button_frame, text="Importar Configuração", command=self.import_config
        )
        self.import_button.pack(side=tk.LEFT, padx=5)

        # Frame para os botões de controle
        control_frame = tk.Frame(master)
        control_frame.grid(row=12, column=0, columnspan=3, pady=10)

        # Botões para iniciar e parar a automação
        self.start_button = ttk.Button(
            control_frame, text="Iniciar", command=self.start_automation
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(
            control_frame, text="Parar", command=self.stop_automation
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Carrega o preset ao iniciar
        self.load_preset()

        # Listener do mouse
        self.listener = None

        keyboard.add_hotkey("f8", self.toggle_automation)

    def create_label_and_entry(self, text, variable, row):
        ttk.Label(self.master, text=text).grid(row=row, column=0, sticky="W")
        ttk.Entry(self.master, textvariable=variable, width=30).grid(
            row=row, column=1, sticky="W"
        )

    def create_label_entry_button(self, text, variable, row, capture_color=False):
        ttk.Label(self.master, text=text).grid(row=row, column=0, sticky="W")
        ttk.Entry(self.master, textvariable=variable, width=30).grid(
            row=row, column=1, sticky="W"
        )
        button = tk.Button(
            self.master,
            text="Capturar",
            command=lambda: self.capture_position(variable, capture_color),
            bg="red",
            fg="white",
        )
        button.grid(row=row, column=2, padx=5, sticky="W")

        # Mapeia o botão com sua variável correspondente para atualizar a cor
        variable.trace_add(
            "write", lambda *args: self.update_button_color(button, variable)
        )

    def capture_position(self, variable, capture_color=False):
        self.master.config(cursor="crosshair")
        self.master.update()

        # Inicia o listener do mouse
        self.listener = mouse.Listener(
            on_click=lambda x, y, button, pressed: self.on_click(
                x, y, variable, pressed, capture_color
            )
        )
        self.listener.start()

    def on_click(self, x, y, variable, pressed, capture_color):
        if pressed:
            variable.set(f"{x},{y}")
            print(f"Capturado: {x},{y}")

            self.master.config(cursor="")
            # Para o listener após capturar a posição
            self.listener.stop()

    def update_button_color(self, button, variable):
        # Muda a cor do botão baseado no valor da variável
        if variable.get():
            button.config(bg="green", fg="white")  # Verde quando há valor
        else:
            button.config(bg="red", fg="white")  # Vermelho quando não há valor

    def save_config(self):
        config = self.get_config()
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
        print("Configuração salva.")

    def load_preset(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                self.set_config(config)
            print("Preset carregado.")

    def get_config(self):
        return {
            "point_acao": self.point_acao.get(),
            "multiplas_caixas": self.multiplas_caixas.get(),
            "opcao_trigo": self.opcao_trigo.get(),
            "opcao_milho": self.opcao_milho.get(),
            "opcao_linho": self.opcao_linho.get(),
            "opcao_cenoura": self.opcao_cenoura.get(),
            "opcao_cogumelo": self.opcao_cogumelo.get(),
            "opcao_tomate": self.opcao_tomate.get(),
            "ciclo_plantacao": [
                plantacao.strip().lower()
                for plantacao in self.ciclo_plantacao.get().split(",")
            ],
        }

    def set_config(self, config):
        self.point_acao.set(config.get("point_acao", ""))
        self.multiplas_caixas.set(config.get("multiplas_caixas", ""))
        self.opcao_trigo.set(config.get("opcao_trigo", ""))
        self.opcao_milho.set(config.get("opcao_milho", ""))
        self.opcao_linho.set(config.get("opcao_linho", ""))
        self.opcao_cenoura.set(config.get("opcao_cenoura", ""))
        self.opcao_cogumelo.set(config.get("opcao_cogumelo", ""))
        self.opcao_tomate.set(config.get("opcao_tomate", ""))
        self.ciclo_plantacao.set(",".join(config.get("ciclo_plantacao", [])))

    def clear_config(self):
        # Redefine todas as variáveis para strings vazias
        self.point_acao.set("")
        self.multiplas_caixas.set("")
        self.opcao_trigo.set("")
        self.opcao_milho.set("")
        self.opcao_linho.set("")
        self.opcao_cenoura.set("")
        self.opcao_cogumelo.set("")
        self.opcao_tomate.set("")
        self.ciclo_plantacao.set("")

    def export_config(self):
        # Abre uma caixa de diálogo para salvar o arquivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            config = self.get_config()
            with open(file_path, "w") as file:
                json.dump(config, file, indent=4)
            print(f"Configuração exportada para {file_path}")

    def import_config(self):
        # Abre uma caixa de diálogo para escolher o arquivo
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                config = json.load(file)
                self.set_config(config)
            print(f"Configuração importada de {file_path}")

    def toggle_automation(self):
        if self.running:
            print("Parando macro")
            self.stop_automation()
        else:
            print("Iniciando macro")
            self.start_automation()

    def start_automation(self):
        self.running = True
        threading.Thread(target=self.run_automation).start()

    def stop_automation(self):
        self.running = False

    def run_automation(self):
        try:

            def parse_position(pos_str):
                return tuple(map(int, pos_str.split(","))) if pos_str else ()

            point_acao = parse_position(self.point_acao.get())
            multiplas_caixas = parse_position(self.multiplas_caixas.get())
            opcao_trigo = parse_position(self.opcao_trigo.get())
            opcao_milho = parse_position(self.opcao_milho.get())
            opcao_linho = parse_position(self.opcao_linho.get())
            opcao_cenoura = parse_position(self.opcao_cenoura.get())
            opcao_cogumelo = parse_position(self.opcao_cogumelo.get())
            opcao_tomate = parse_position(self.opcao_tomate.get())

            ciclo_plantacao = itertools.cycle(self.ciclo_plantacao.get().split(","))

            def get_tipo_plantacao():
                return next(ciclo_plantacao)

            def find_and_click_icon(icon_path, conf=0.8):
                try:
                    icon_location = pyautogui.locateCenterOnScreen(
                        icon_path, confidence=conf
                    )
                    if icon_location is not None:
                        pyautogui.moveTo(icon_location)
                    return icon_location
                except Exception as e:
                    logging.warning(f"Erro ao localizar o ícone: {e}")
                    return None

            def move_to(tecla_direcao):
                time.sleep(0.3)
                pyautogui.keyDown(tecla_direcao)
                time.sleep(0.6)
                pyautogui.keyUp(tecla_direcao)

            def move_to_harvest(loc_harvest):
                center_x = pyautogui.size()[0] // 2
                if loc_harvest.x < center_x:
                    logging.info("Mover pra esquerda")
                    move_to("a")
                    return "d"
                else:
                    logging.info("Mover pra direita")
                    move_to("d")
                    return "a"

            def acao():
                pyautogui.click(multiplas_caixas)
                pyautogui.click(point_acao)
                time.sleep(1)

            def colher():
                acao()

            def plantar(tipo_colheita):
                if tipo_colheita == "milho":
                    pyautogui.click(opcao_milho)
                if tipo_colheita == "trigo":
                    pyautogui.click(opcao_trigo)
                if tipo_colheita == "linho":
                    pyautogui.click(opcao_linho)
                if tipo_colheita == "cenoura":
                    pyautogui.click(opcao_cenoura)
                if tipo_colheita == "cogumelo":
                    pyautogui.click(opcao_cogumelo)
                if tipo_colheita == "tomate":
                    pyautogui.click(opcao_tomate)
                acao()

            while self.running:
                loc_harvest = find_and_click_icon(self.colheita)
                if not loc_harvest:
                    logging.info("Nenhuma Colheita pronta")
                    time.sleep(3)
                    continue

                logging.info("Indo Colher")
                caminho_volta = move_to_harvest(loc_harvest)
                colher()
                time.sleep(0.4)
                plantar(get_tipo_plantacao())
                time.sleep(0.4)
                move_to(caminho_volta)

                time.sleep(3)
        except Exception as e:
            logging.error(e)
            print(f"Erro durante a automação: {e}")

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationConfigApp(root)
    root.mainloop()
