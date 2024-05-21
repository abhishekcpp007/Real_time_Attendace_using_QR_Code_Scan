import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# File to store QR code data
datafile = "qr_code_data.txt"


def record_data(data):
    try:
        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write data along with date and time to the file
        with open(datafile, "a") as file:
            file.write(f"{current_datetime}: {data}\n")

        print("Data recorded:", data)
        messagebox.showinfo("Data Recorded", f"Data recorded: {data}")
    except Exception as e:
        print("Error recording data:", e)
        messagebox.showerror("Error", f"Error recording data: {str(e)}")


def scan_qr_code():
    # Capture video from the default camera
    cap = cv2.VideoCapture(0)

    # Create a QR code detector
    detector = cv2.QRCodeDetector()

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not capture frame from camera.")
            break

        # Detect QR code in the frame
        data, _, _ = detector.detectAndDecode(frame)

        if data:
            # Record data
            record_data(data)

            # Break the loop after finding a QR code
            break

        # Display the frame with detected QR code (if present)
        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def start_scan():
    scan_qr_code()


# Function to close the application
def close_app():
    root.destroy()


# Create the main window
root = tk.Tk()
root.title("Attendance using QR Code scan")

# Create a main heading label
heading_label = ttk.Label(root, text="Attendance using QR Code scan", font=("Helvetica", 18))
heading_label.pack(pady=10)

# Create a frame for buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Create a Start Scanning button
scan_button = ttk.Button(button_frame, text="Start Scanning", command=start_scan)
scan_button.grid(row=0, column=0, padx=5)

# Create a Close button
close_button = ttk.Button(button_frame, text="Close", command=close_app)
close_button.grid(row=0, column=1, padx=5)

# Run the Tkinter event loop
root.mainloop()
