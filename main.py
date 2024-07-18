import serial
import keyboard
import datetime


def save_data(messageBuffer, startTime, errorType):
    f = open("ErrorLog.txt", "a+")
    f.write(str(errorType), str(startTime), str(messageBuffer))  # Write error to file
    f.close()


serM = serial.Serial("COM6", 115200)  # Open Serial Port for Message content

messageBuffer = []  # List to store past messages for logging
n = 5  # Number of messages saved before event
monitor = False  # Flag for first stage of incident detection
startTime = 0
errorType = None
errorFlag = "0x111111"
errorFlagCount = 0

while True:
    message = serM.readline()  # Read message from serial
    if message == errorFlag:  # Start counting error flags after first appearance
        monitor = True  # Start storing all messages (no current limit set)
        startTime = datetime.datetime.now()  # Record time of first error
        errorFlagCount += 1  # Start counting error flags
    if monitor:
        messageBuffer.append(message)  # Add message to log
        if errorFlagCount > 255:  # If error flag numbers are > 255 then report error
            errorType = "Physical Node Removal"
            save_data(messageBuffer, startTime, errorType)  # Write data to non-volatile storage
        if startTime - datetime.datetime.now() > datetime.timedelta(seconds=1):  # Check if time between now and last error flag > 1 second and if so stop monitoring
            monitor = False
            errorFlagCount = 0
            messageBuffer.clear()

    if (messageBuffer.len() >= n) and (not monitor):  # Creates a queue like data structure
        messageBuffer.pop(0)

    messageBuffer.append(message)  # Add message to queue

    if keyboard.is_pressed('c'):
        print("Closing Serial")
        serM.close()  # Close serial connection
        break
