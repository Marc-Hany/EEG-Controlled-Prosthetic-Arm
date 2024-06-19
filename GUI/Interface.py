import tkinter as tk
import pandas as pd
import random
import bluetooth
import matplotlib.pyplot as plt

# Load actual and predicted CSV files
actual_file = 'subj11_series5_events.csv'
predicted_file = 'subj11_series5_predictions_processed.csv'

actual_df = pd.read_csv(actual_file)
predicted_df = pd.read_csv(predicted_file)

# List of event columns
event_columns = [
    'HandStart', 
    'FirstDigitTouch', 
    'BothStartLoadPhase', 
    'LiftOff', 
    'Replace', 
    'BothReleased'
]

# Function to find batches of consecutive frames for each event
def find_batches_optimized(df, event_columns, threshold=150):
    event_batches = {event: [] for event in event_columns}
    for event in event_columns:
        event_array = df[event].values
        current_batch = []
        for i, event_value in enumerate(event_array):
            if event_value == 1:
                current_batch.append(i)
                if len(current_batch) == threshold:
                    event_batches[event].append((current_batch[0], current_batch[-1]))
                    current_batch = []
            else:
                current_batch = []
        if len(current_batch) == threshold:
            event_batches[event].append((current_batch[0], current_batch[-1]))
    return event_batches

# Find actual and predicted batches using the optimized function
actual_batches = find_batches_optimized(actual_df, event_columns)
predicted_batches = find_batches_optimized(predicted_df, event_columns)

# Function to calculate overlap ratio
def overlap_ratio(actual_start, actual_end, pred_start, pred_end):
    actual_set = set(range(actual_start, actual_end + 1))
    pred_set = set(range(pred_start, pred_end + 1))
    overlap = len(actual_set & pred_set)
    union = len(actual_set | pred_set)
    return overlap / union if union != 0 else 0


class EventPredictionGUI:
    def __init__(self, window, event_columns):
        self.window = window
        self.start_button = tk.Button(self.window, text="Start", command=self.handle_start_click, font=("Arial", 25), relief=tk.RAISED, bd=5)
        self.start_button.config(width=10, height=30, bg="#FD696E")
        self.start_button.pack(anchor=tk.CENTER, pady=450)

        self.manual_button = tk.Button(self.window, text="Manual", command=self.handle_manual_click, font=("Arial", 25), relief=tk.RAISED, bd=5)
        self.manual_button.config(width=10, height=5, bg="#5383FF")
        self.chosen_eeg_button = tk.Button(self.window, text="Chosen EEG", command=self.handle_chosen_eeg_click, font=("Arial", 25), relief=tk.RAISED, bd=5)
        self.chosen_eeg_button.config(width=10, height=5, bg="#5383FF")
        self.random_eeg_button = tk.Button(self.window, text="Random EEG", command=self.handle_random_eeg_click, font=("Arial", 25), relief=tk.RAISED, bd=5)
        self.random_eeg_button.config(width=10, height=5, bg="#5383FF")
        self.exit_button = tk.Button(self.window, text="EXIT", command=self.handle_exit_click, font=("Arial", 25), relief=tk.RAISED, bd=5)
        self.exit_button.config(width=10, height=5, bg="#FD696E")

        self.event_columns = event_columns
        self.buttons = {}
        self.prediction_label = None

        self.back_button = tk.Button(self.window, text="Back", command=self.handle_start_click,font=("Arial", 25), relief=tk.RAISED, bd=5)
        self.back_button.config(width=10, height=5, bg="#FD696E")
        # Establish Bluetooth connection with ESP32
        self.esp32_address = "C0:49:EF:9B:27:FA"  # Replace with the actual address of your ESP32

    def send_data(self,value):
        try:
            # Create a Bluetooth socket
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((self.esp32_address, 1))  # Connect to the ESP32 device

            # Send the value as a string
            sock.send(str(value))

            # Close the socket
            sock.close()
            print(f"Sent value: {value}")
        except Exception as e:
            print(f"Error: {e}")

    def handle_start_click(self):
        # Clear any existing buttons
        if self.prediction_label:
            self.prediction_label.pack_forget()
        self.back_button.pack_forget()
        for button in self.buttons.values():
            button.pack_forget()
        self.start_button.pack_forget()
        self.manual_button.pack(anchor=tk.CENTER, pady=30)
        self.chosen_eeg_button.pack(anchor=tk.CENTER, pady=30)
        self.random_eeg_button.pack(anchor=tk.CENTER, pady=30)
        self.exit_button.pack(anchor=tk.CENTER, pady=30)
        
    def handle_exit_click(self):
        self.BT_send('b')
        # Clear any existing buttons
        if self.prediction_label:
            self.prediction_label.pack_forget()
        self.back_button.pack_forget()
        for button in self.buttons.values():
            button.pack_forget()
        self.manual_button.pack_forget()
        self.chosen_eeg_button.pack_forget()
        self.random_eeg_button.pack_forget()
        self.exit_button.pack_forget()
        self.start_button.pack(anchor=tk.CENTER, pady=450)
        if self.prediction_label:
            self.prediction_label.pack_forget()
        print("Exit button clicked")
        
    def handle_manual_click(self):
        print("Manual button clicked")
        # Clear any existing buttons
        self.manual_button.pack_forget()
        self.chosen_eeg_button.pack_forget()
        self.random_eeg_button.pack_forget()
        self.exit_button.pack_forget()
        # Create buttons for each Scenario
        scenarios = [
            'Scenario1',
            'Scenario2',
            'Handshake',
            'Grasp and Lift',
        ]
        for scenario in scenarios:
            self.buttons[scenario] = tk.Button(self.window, text=scenario, command=lambda e=scenarios.index(scenario): self.BT_send(e),font=("Arial", 25), relief=tk.RAISED, bd=5)
            self.buttons[scenario].config(width=20, height=4, bg="#06C892")
            self.buttons[scenario].pack(anchor=tk.CENTER, pady=10)
        self.back_button.pack(anchor=tk.CENTER, pady=10)
        

   
    def BT_send(self, scenario):
        
        self.send_data(scenario)

        # Example usage:
        # send_scenario_to_esp32(scenario_number)


    def handle_chosen_eeg_click(self):
        print("Chosen EEG button clicked")
        # Clear any existing buttons
        self.manual_button.pack_forget()
        self.chosen_eeg_button.pack_forget()
        self.random_eeg_button.pack_forget()
        self.exit_button.pack_forget()
        # Create buttons for each event
        for event in self.event_columns:
            self.buttons[event] = tk.Button(self.window, text=event, command=lambda e=event: self.handle_button_click(e),font=("Arial", 25), relief=tk.RAISED, bd=5)
            self.buttons[event].config(width=20, height=3, bg="#06C892")
            self.buttons[event].pack(anchor=tk.CENTER, pady=5)

        # Create label for displaying prediction
        self.prediction_label = tk.Label(self.window, text="", font=("Arial", 20), fg="white", bg="black", relief=tk.SOLID, bd=2)
        self.prediction_label.pack()
        self.back_button.pack(anchor=tk.CENTER, pady=5)    
        

    def handle_button_click(self, event):
        if actual_batches[event]:
            random_batch = random.choice(actual_batches[event])
            actual_start, actual_end = map(int, random_batch)
            best_overlap = 0
            best_pred_event = "No event"
            best_pred_start = None
            best_pred_end = None
            for pred_event in self.event_columns:
                for pred_batch in predicted_batches[pred_event]:
                    pred_start, pred_end = map(int, pred_batch)
                    overlap = overlap_ratio(actual_start, actual_end, pred_start, pred_end)
                    if overlap > best_overlap:
                        best_overlap = overlap
                        best_pred_event = pred_event
                        best_pred_start = pred_start
                        best_pred_end = pred_end
            self.prediction_label.config(text=f"Actual event is: {event}, Predicted event is: {best_pred_event}")
            # send prediction to ESP32
            
            if best_pred_event == "No event":
               pass
            else:
                index = event_columns.index(best_pred_event)+4
            print(index)
            if index==10:
                index='a'
            self.send_data(index)


    def handle_random_eeg_click(self):
        print("Random EEG button clicked")
        # Clear any existing buttons
        self.manual_button.pack_forget()
        self.chosen_eeg_button.pack_forget()
        self.random_eeg_button.pack_forget()
        self.exit_button.pack_forget()
        # Randomly select an event
        event = random.choice(self.event_columns)
         # Create label for displaying prediction
        self.prediction_label = tk.Label(self.window, text="",font=("Arial", 20), fg="white", bg="black", relief=tk.SOLID, bd=2)
        self.prediction_label.pack(anchor=tk.CENTER, pady=120) 
        self.back_button.pack(anchor=tk.CENTER, pady=120)  
        self.handle_button_click(event)
       

        
    
window = tk.Tk()
window.title("Event Prediction GUI")
window.geometry("1680x1050")  # Set the size of the window
window.configure(bg="#F1EBE5")  # Set the background color of the window to #03fca5
event_gui = EventPredictionGUI(window, event_columns)
window.mainloop()
