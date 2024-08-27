
[🇧🇷 Versão em Português](#automação-de-colheita-e-plantio---fazenda-do-lar-ragnarok-origin) | [🇺🇸 English Version](#harvest-and-planting-automation---home-farm-ragnarok-origin)



# Automação de Colheita e Plantio - Fazenda do Lar (Ragnarok Origin)

## Descrição

Esta aplicação foi desenvolvida para automatizar o processo de colheita e plantio na Fazenda do Lar, dentro do jogo **Ragnarok Origin**. Com uma interface gráfica moderna, a aplicação permite configurar as posições dos itens na tela, capturar a posição do mouse e executar macros automatizadas que facilitam tarefas repetitivas, como colheita e plantio. Além disso, a aplicação inclui uma funcionalidade opcional para "Comprar Itens", que pode ser ativada por meio de uma checkbox na interface.

## Funcionalidades

- **Captura de Posições**: Capture as coordenadas na tela para ações específicas, como colheita, plantio e compra de itens.
- **Ciclo de Plantação**: Configure um ciclo de plantação com diferentes tipos de culturas.
- **Automação Completa**: Execute macros para automatizar o processo de colheita e plantio de acordo com as configurações salvas.
- **Seleção de Idioma**: Suporte para múltiplos idiomas, permitindo alternar entre português e inglês.
- **Interface Amigável**: Interface gráfica moderna e minimalista, com suporte a temas claros e escuros.

## Instalação

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie e Ative um Ambiente Virtual**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # No Windows
   source venv/bin/activate  # No Linux/MacOS
   ```

3. **Instale as Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

   > Certifique-se de que o arquivo `requirements.txt` contém todas as dependências necessárias.

## Compilação

Para compilar a aplicação em um único arquivo executável, siga os passos abaixo:

1. **Certifique-se de que o Ambiente Virtual Está Ativado**:
   ```bash
   .\venv\Scripts\activate  # No Windows
   source venv/bin/activate  # No Linux/MacOS
   ```

2. **Execute o PyInstaller**:
   ```bash
   pyinstaller .\app.py --onefile --noconsole
   ```

   Isso criará um executável único dentro da pasta `dist`.

## Uso

Após a compilação, você pode encontrar o executável na pasta `dist`. Execute-o para iniciar a aplicação com a interface gráfica.

## Contribuição

Se você deseja contribuir com este projeto, siga os passos abaixo:

1. **Fork o Repositório**.
2. **Crie uma Branch para Sua Modificação** (`git checkout -b minha-modificacao`).
3. **Commit suas Alterações** (`git commit -m 'Adicionei nova funcionalidade'`).
4. **Envie para o Branch Original** (`git push origin minha-modificacao`).
5. **Crie um Pull Request**.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.



# Harvest and Planting Automation - Home Farm (Ragnarok Origin)

## Description

This application was developed to automate the harvesting and planting process in Home Farm, within the game **Ragnarok Origin**. With a modern graphical interface, the application allows you to configure item positions on the screen, capture mouse position, and execute automated macros that facilitate repetitive tasks such as harvesting and planting. Additionally, the application includes an optional "Buy Items" feature that can be activated via a checkbox in the interface.

## Features

- **Position Capture**: Capture screen coordinates for specific actions, such as harvesting, planting, and buying items.
- **Planting Cycle**: Configure a planting cycle with different types of crops.
- **Complete Automation**: Execute macros to automate the harvesting and planting process according to saved configurations.
- **Language Selection**: Support for multiple languages, allowing you to switch between Portuguese and English.
- **User-Friendly Interface**: Modern and minimalist graphical interface, with support for light and dark themes.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Linux/MacOS
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   > Make sure the `requirements.txt` file contains all the necessary dependencies.

## Compilation

To compile the application into a single executable file, follow the steps below:

1. **Ensure the Virtual Environment is Activated**:
   ```bash
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Linux/MacOS
   ```

2. **Run PyInstaller**:
   ```bash
   pyinstaller .\app.py --onefile --noconsole
   ```

   This will create a single executable file inside the `dist` folder.

## Usage

After compilation, you can find the executable in the `dist` folder. Run it to start the application with the graphical interface.

## Contribution

If you wish to contribute to this project, follow the steps below:

1. **Fork the Repository**.
2. **Create a Branch for Your Modification** (`git checkout -b my-modification`).
3. **Commit Your Changes** (`git commit -m 'Added new feature'`).
4. **Push to the Original Branch** (`git push origin my-modification`).
5. **Create a Pull Request**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
