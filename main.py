import serial
import keyboard
import datetime

def saveData(messageBuffer, startTime, errorFlag):
    return 0

serM = serial.Serial("COM6", 115200)  # Open Serial Port for Message content

messageBuffer = []  # List to store past messages for logging
n = 5  # Number of messages saved before event
monitor = False  # Flag for first stage of incident detection
startTime = 0
errorFlag = False

while True:
    message = serM.readline()
    messageBuffer.append(message)
    if (messageBuffer.len() >= n) and (not monitor):  # Creates a queue like data structure
        messageBuffer.pop(0)
    elif (message in messageBuffer) and (not monitor):  # If multiple messages occur in a short period of time start
        # recording more data
        monitor = True
        startTime = datetime.datetime.now()  # Record error start time
        if messageBuffer.len() - set(messageBuffer).len() > 10:  # If duplicate messages in buffer > 10 flag full error
            errorFlag = True
            saveData(messageBuffer, startTime, errorFlag)  # Save data log
    if keyboard.is_pressed('c'):
        print("Closing Serial")
        serM.close()
        break
