# Python CANoe

## Overview

This is a Python-based CAN (Controller Area Network) communication application designed to provide a flexible interface for sending and receiving CAN messages. The application supports DBC file parsing, message simulation, and provides a user-friendly GUI for CAN communication.

## Features

- 🖥️ Cross-platform GUI using Tkinter
- 📂 DBC File Support
  - Load and parse CAN database configuration files
  - Visualize message and signal structures
- 📡 Message Simulation Mode
  - Send custom CAN messages
  - Generate simulated received messages
- 🔧 Flexible Interface
  - Manual message ID entry
  - Signal value configuration
  - Message logging

## Prerequisites

- Python 3.9+
- macOS, Linux, or Windows

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mitchellediting/pythonCANoe.git
cd pythonCANoe
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

## Usage

1. Load a DBC File
   - Click "Load DBC File"
   - Select your CAN database configuration

2. Select a Message
   - Choose from loaded messages
   - Configure signal values

3. Send Messages
   - Click "Send Message"
   - View sent and received messages in the log

## Hardware Support

Currently supports:
- Simulation Mode
- Vector 1630a CAN Device (in development)

## Roadmap

- [ ] Full Vector 1630a hardware support
- [ ] Enhanced DBC file parsing
- [ ] Advanced message filtering
- [ ] Logging and export capabilities

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

Mitchell Curtis - mitchellcurtis15@hotmail.com

Project Link: https://github.com/mitchellediting/pythonCANoe
