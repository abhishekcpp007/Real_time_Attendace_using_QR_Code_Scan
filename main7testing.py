import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading

# File to store QR code data
datafile = "qr_code_data.txt"

# Set to store scanned QR codes
scanned_codes = set()

# Flag to indicate if scanning is stopped
scanning_stopped = False

# Function to record QR code data
def record_data(data_list):
    try:
        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
def scan_qr_code(num_codes=1):
    global scanned_codes, scanning_stopped
    # Create a QR code detector
    detector = cv2.QRCodeDetector()

    cap = cv2.VideoCapture(0)

    while not scanning_stopped:
        scanned_data = []

        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not capture frame from camera.")
            break

        # Detect QR codes in the frame
        data, _, _ = detector.detectAndDecode(frame)

        if data:
            if data not in scanned_codes:
                # Record data
                scanned_codes.add(data)
                scanned_data.append(data)

            if len(scanned_data) >= num_codes:
                # Record scanned data
                record_data(scanned_data)
                scanned_data.clear()

        # Display the frame with detected QR code (if present)
        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to stop scanning
def stop_scanning():
    global scanning_stopped
    scanning_stopped = True

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

# Function to start scanning in a separate thread
def start_scanning_thread():
    scanning_thread = threading.Thread(target=scan_qr_code)
    scanning_thread.start()

# Main UI setup
root = tk.Tk()
root.title("Attendance using QR Code scan")

# Function to set up background image
def set_background():
    background_image = tk.PhotoImage(file="Screenshot 2024-05-22 005605.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = background_image

# Set up background
set_background()

# Heading Label
heading_label = ttk.Label(root, text="Attendance using QR Code scan", font=("Helvetica", 18, "bold"))
heading_label.pack(pady=10)

# Button Frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Style configuration for buttons
style = ttk.Style()
style.configure("TButton", foreground="dark gray", background="blue", font=("Helvetica", 12, "bold"), borderwidth=2)

# Start Scanning Button
scan_button = ttk.Button(button_frame, text="Start Scanning", command=start_scanning_thread)
scan_button.grid(row=0, column=0, padx=5, pady=5)

# Stop Scanning Button
stop_button = ttk.Button(button_frame, text="Stop Scanning", command=stop_scanning)
stop_button.grid(row=0, column=1, padx=5, pady=5)

# Show Data Button
show_data_button = ttk.Button(button_frame, text="Show Data", command=show_data)
show_data_button.grid(row=0, column=2, padx=5, pady=5)

# Close Button
close_button = ttk.Button(button_frame, text="Close", command=close_app)
close_button.grid(row=0, column=3, padx=5, pady=5)

root.mainloop()
