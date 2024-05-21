import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# File to store QR code data
datafile = "qr_code_data.txt"

# Function to record QR code data
def record_data(data_list):
    try:
        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Read existing data from the file
        existing_data = []
        with open(datafile, "r") as file:
            existing_data = file.readlines()

        # Remove duplicate lines
        existing_data = set(existing_data)

        # Write existing data back to the file
        with open(datafile, "w") as file:
            for line in existing_data:
                file.write(line)

        # Append new data along with date and time to the file
        with open(datafile, "a") as file:
            for data in data_list:
                file.write(f"{current_datetime}: {data}\n")

        print("Data recorded:", data_list)
        messagebox.showinfo("Data Recorded", f"Data recorded: {', '.join(data_list)}")
    except Exception as e:
        print("Error recording data:", e)
        messagebox.showerror("Error", f"Error recording data: {str(e)}")

# Function to scan QR codes
def scan_qr_code(num_codes=1, timeout=30):
    # Capture video from the default camera
    cap = cv2.VideoCapture(0)

    # Create a QR code detector
    detector = cv2.QRCodeDetector()

    start_time = datetime.now()

    scanned_data = []

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not capture frame from camera.")
            break

        # Detect QR codes in the frame
        data, _, _ = detector.detectAndDecode(frame)

        if data:
            if data not in scanned_data:
                # Record data
                scanned_data.append(data)

            if len(scanned_data) >= num_codes:
                # Break the loop if desired number of QR codes are scanned
                break

        # Check for timeout
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time >= timeout:
            print("Timeout: QR code scanning stopped.")
            break

        # Display the frame with detected QR code (if present)
        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Record scanned data
    record_data(scanned_data)

# Function to show recorded data
def show_data():
    try:
        # Read data from the file
        with open(datafile, "r") as file:
            data = file.read()

        # Create a new window to display data
        data_window = tk.Toplevel()
        data_window.title("QR Code Data")

        # Create a text widget to display data
        data_text = tk.Text(data_window, height=20, width=50)
        data_text.insert(tk.END, data)
        data_text.pack(padx=10, pady=10)

        # Disable editing
        data_text.configure(state="disabled")
    except Exception as e:
        print("Error reading data:", e)
        messagebox.showerror("Error", f"Error reading data: {str(e)}")

# Function to close the application
def close_app():
    root.destroy()

# Main UI setup
root = tk.Tk()
root.title("Attendance using QR Code scan")

# Heading Label
heading_label = ttk.Label(root, text="Attendance using QR Code scan", font=("Helvetica", 18))
heading_label.pack(pady=10)

# Button Frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Start Scanning Button
scan_button = ttk.Button(button_frame, text="Start Scanning", command=lambda: scan_qr_code(num_codes=2, timeout=30))
scan_button.grid(row=0, column=0, padx=5)

# Show Data Button
show_data_button = ttk.Button(button_frame, text="Show Data", command=show_data)
show_data_button.grid(row=0, column=1, padx=5)

# Close Button
close_button = ttk.Button(button_frame, text="Close", command=close_app)
close_button.grid(row=0, column=2, padx=5)

root.mainloop()
