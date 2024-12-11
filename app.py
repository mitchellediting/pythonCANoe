import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import can
import cantools
import threading

class CANCommunicationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Vector CAN Communication Tool")
        self.master.geometry("800x600")

        # CAN Device Configuration
        self.can_interface = None
        self.dbc_database = None

        # Create UI Components
        self.create_widgets()

    def create_widgets(self):
        # Interface Configuration Frame
        config_frame = ttk.LabelFrame(self.master, text="CAN Interface Configuration")
        config_frame.pack(padx=10, pady=10, fill="x")

        # Interface Selection
        ttk.Label(config_frame, text="CAN Interface:").pack(side="left", padx=5)
        self.interface_var = tk.StringVar()
        self.interface_dropdown = ttk.Combobox(config_frame, textvariable=self.interface_var)
        self.interface_dropdown['values'] = self.get_available_interfaces()
        self.interface_dropdown.pack(side="left", padx=5)

        # DBC File Selection
        ttk.Button(config_frame, text="Load DBC File", command=self.load_dbc_file).pack(side="left", padx=5)

        # Message Sending Frame
        send_frame = ttk.LabelFrame(self.master, text="Send CAN Message")
        send_frame.pack(padx=10, pady=10, fill="x")

        # Message ID Input
        ttk.Label(send_frame, text="Message ID (Hex):").grid(row=0, column=0, padx=5, pady=5)
        self.message_id_entry = ttk.Entry(send_frame)
        self.message_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # DBC Message Selection
        ttk.Label(send_frame, text="DBC Message:").grid(row=1, column=0, padx=5, pady=5)
        self.dbc_message_var = tk.StringVar()
        self.dbc_message_dropdown = ttk.Combobox(send_frame, textvariable=self.dbc_message_var)
        self.dbc_message_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Signal Configuration Area
        self.signal_frame = ttk.Frame(send_frame)
        self.signal_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Send Button
        ttk.Button(send_frame, text="Send Message", command=self.send_can_message).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Received Messages Frame
        receive_frame = ttk.LabelFrame(self.master, text="Received Messages")
        receive_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.received_messages_text = tk.Text(receive_frame, height=10)
        self.received_messages_text.pack(padx=5, pady=5, fill="both", expand=True)

    def get_available_interfaces(self):
        # TODO: Implement actual interface detection
        # For Vector 1630a, you might need to use specific Vector CAN libraries
        return ['can0', 'can1', 'vector_can']

    def load_dbc_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("DBC Files", "*.dbc")])
        if file_path:
            try:
                self.dbc_database = cantools.db.load_file(file_path)
                
                # Populate DBC Message Dropdown
                message_names = [msg.name for msg in self.dbc_database.messages]
                self.dbc_message_dropdown['values'] = message_names
                self.dbc_message_dropdown.bind('<<ComboboxSelected>>', self.on_dbc_message_selected)
                
                messagebox.showinfo("Success", f"Loaded DBC file: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load DBC file: {str(e)}")

    def on_dbc_message_selected(self, event):
        # Clear existing signal entries
        for widget in self.signal_frame.winfo_children():
            widget.destroy()

        # Get selected message
        message_name = self.dbc_message_var.get()
        message = self.dbc_database.get_message_by_name(message_name)

        # Create signal input fields
        self.signal_entries = {}
        for i, signal in enumerate(message.signals):
            ttk.Label(self.signal_frame, text=signal.name).grid(row=i, column=0, padx=5, pady=2)
            entry = ttk.Entry(self.signal_frame)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.signal_entries[signal.name] = entry

        # Automatically set Message ID
        self.message_id_entry.delete(0, tk.END)
        self.message_id_entry.insert(0, hex(message.frame_id))

    def send_can_message(self):
        try:
            # Get message ID
            message_id = int(self.message_id_entry.get(), 16)

            if self.dbc_database:
                # If DBC message is selected, use DBC encoding
                message_name = self.dbc_message_var.get()
                message = self.dbc_database.get_message_by_name(message_name)
                
                # Prepare signal data
                signal_data = {}
                for signal_name, entry in self.signal_entries.items():
                    signal_data[signal_name] = float(entry.get())
                
                # Encode message
                data = self.dbc_database.encode_message(message.name, signal_data)
            else:
                # Manual message sending
                data = [0] * 8  # Default 8-byte message

            # Send CAN message
            can_message = can.Message(arbitration_id=message_id, data=data)
            self.can_interface.send(can_message)

            # Update received messages log
            self.received_messages_text.insert(tk.END, f"Sent: {can_message}\n")

        except Exception as e:
            messagebox.showerror("Send Error", str(e))

    def start_can_bus(self):
        try:
            interface = self.interface_var.get()
            # TODO: Replace with Vector-specific CAN bus initialization
            self.can_interface = can.interface.Bus(channel=interface, bustype='socketcan')
            
            # Start message receiving thread
            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()
        except Exception as e:
            messagebox.showerror("CAN Bus Error", str(e))

    def receive_messages(self):
        # Continuously receive messages
        while True:
            message = self.can_interface.recv()
            self.received_messages_text.insert(tk.END, f"Received: {message}\n")

def main():
    root = tk.Tk()
    app = CANCommunicationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
