import cv2

# Specify the data file path
datafile = "qr_code_data.txt"

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
        # Print the decoded data
        print("QR Code data:", data)

        try:
            # Open the data file in append mode and save the data
            with open(datafile, "a") as file:
                file.write(data + "\n")
            print("QR code data saved to file.")
        except Exception as e:
            print("Error saving data to file:", e)

        # Break the loop after finding a QR code
        break

    # Display the frame with detected QR code (if present)
    cv2.imshow("QR Code Scanner", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
