import datetime
from time import sleep
import socket
import threading
import time

tello_address = ('192.168.10.1', 8889)

# IP and port of local computer
local_address = ('', 9000)

# Create a UDP connection that we'll send the command to
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the local address and port
sock.bind(local_address)

# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
  # Try to send the message otherwise print the exception
  try:
    sock.sendto(message.encode(), tello_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

  # Delay for a user-defined period of time
  time.sleep(delay)

# Receive the message from Tello
def receive():
  # Continuously loop and listen for incoming messages
  while True:
    # Try to receive the message otherwise print the exception
    try:
      response, ip_address = sock.recvfrom(128)
      print("Received message: " + response.decode(encoding='utf-8'))
    except Exception as e:
      # If there's an error close the socket and break out of the loop
      sock.close()
      print("Error receiving: " + str(e))
      break

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()


# Each leg of the box will be 100 cm. Tello uses cm units by default.
box_leg_distance = 20

# Yaw 90 degrees
yaw_angle = 90

# Yaw clockwise (right)
yaw_direction = "cw"

#Yaw counter clockwise (left)
yaw_direction = "ccw"

# Put Tello into command mode
send("command", 3)

# Send the takeoff command
send("takeoff", 2)

# Yaw right
send("cw " + str(yaw_angle), 3)

# command for flip
send ("flip f", 2)

# Yaw right
send("ccw " + str(yaw_angle), 3)

# Fly Forward 
send("forward " + str(box_leg_distance), 3)

# Move backwards
send("backwards" + str(box_leg_distance), 3)

# Land
send ("land" , 2)

# Print message
print("Mission completed successfully!")

# Close the socket
sock.close()






