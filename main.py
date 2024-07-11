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
    if message == errorFlag:
        monitor = True
        errorFlagCount += 1  # Start counting error flags
    if monitor:
        errorCount = messageBuffer.len() - set(messageBuffer).len()
        if (errorCount > 10) and (errorCount < 255): # If duplicate messages in buffer > 10 flag full error
            errorType = "CAN Injection"  # Write potential error type
            endTime = startTime - datetime.datetime.now()  # Record time since first error flag
            if endTime > datetime.timedelta(minutes=10):  # If monitoring for > 10 mins break and record CAN Inject
                # error
                save_data(messageBuffer, startTime, errorType)  # Write error to text file
                break
        if (errorFlagCount > 200):  # If error flag numbers are > 200 then report error
            errorType = "Bus Off"
            save_data(messageBuffer, startTime, errorType)
    if (messageBuffer.len() >= n) and (not monitor):  # Creates a queue like data structure
        messageBuffer.pop(0)

    elif (message in messageBuffer) and (not monitor):  # If multiple messages occur in a short period of time start
        # recording more data
        monitor = True
        startTime = datetime.datetime.now()  # Record error start time

    messageBuffer.append(message)  # Add message to queue

    if keyboard.is_pressed('c'):
        print("Closing Serial")
        serM.close()  # Close serial connection
        break
