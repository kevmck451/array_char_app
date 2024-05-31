
from app.control.Controller.events import Event

import socket
import threading
import time
import numpy as np

class Sender_Client:
    def __init__(self, host='127.0.0.1', port=12345, name='unknown'):
        chamber_comp_ip = '192.168.1.253'
        self.host = host
        self.port = port
        self.name = name
        self.connected = False
        self.socket = None
        self.cancel_attempt = False
        self.connect_thread = threading.Thread(target=self.ensure_connection, daemon=True)
        self.connect_thread.start()
        self.heartbeat_thread = None
        self.heartbeat_attempt = 0
        self.controller = None
        self.disconnect_thread = None

    def set_controller(self, controller):
        self.controller = controller

    def ensure_connection(self):
        print('Attempting to Connect with TDT Hardware')
        while not self.connected and not self.cancel_attempt:
            print("Waiting for Hardware Connection...")
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                handshake_message = f'{self.name}'
                self.socket.sendall(handshake_message.encode())
                response = self.socket.recv(1024)
                if not response.decode('utf-8') == 'ack': continue
                print(f"Connected to {self.host}:{self.port}")
                self.connected = True
                self.heartbeat_thread = threading.Thread(target=self.heartbeat, daemon=True)
                self.heartbeat_thread.start()
                self.disconnect_thread = threading.Thread(target=self.wait_for_disconnect, daemon=True)
                self.disconnect_thread.start()

            except Exception as e:
                # print(f"Error connecting to the server: {e}")
                time.sleep(1)  # Retry after a delay
        self.cancel_attempt = False

    def heartbeat(self):
        print('heartbeat')
        wait_time = 3
        burst_time = 0.1

        while self.connected:
            # print('beating')
            try:
                self.socket.sendall('heartbeat'.encode())
                time.sleep(burst_time)
                self.socket.sendall('heartbeat'.encode())
                time.sleep(burst_time)
                self.socket.sendall('heartbeat'.encode())
                self.heartbeat_attempt = 0
            except socket.error as e:
                print(f'heartbeat failed attempt: {self.heartbeat_attempt}')
                self.heartbeat_attempt += 1

            if self.heartbeat_attempt == 5:
                print('HARDWARE DISCONNECTED')
                self.connected = False
                self.controller.handle_event(Event.DISCONNECT_HARDWARE)
                # self.connect_thread = threading.Thread(target=self.ensure_connection, daemon=True)
                # self.connect_thread.start()

            time.sleep(wait_time)

    def send_data(self, data):
        if self.connected:
            try:
                if isinstance(data, np.ndarray):
                    data = np.array2string(data)
                self.socket.sendall(data.encode())

                print("event data sent")
            except socket.error as e:
                print(f"Error sending data: {e}")
                self.connected = False
                self.socket.close()
        else:
            print("Not connected. Unable to send data.")



    def wait_for_disconnect(self):
        try:
            response = self.socket.recv(1024).decode()
            print(response)
            if 'server_disconnecting' in response:
                self.connected = False
                self.controller.handle_event(Event.DISCONNECT_HARDWARE)
        except OSError as e:
            if e.errno == 9:  # Bad file descriptor error
                print("Socket already closed.")
            else:
                raise  # Re-raise any unexpected errors

    def close_connection(self):
        self.socket.sendall('disconnecting'.encode())
        self.cancel_attempt = True
        self.connected = False
        if self.socket:
            self.socket.close()
            print("Connection closed")

# Usage example
if __name__ == '__main__':


    # for running mac to mac
    client = Sender_Client('127.0.0.1', name='MacBook')

    # for running mac to tdt hardware
    # client = Sender_Client('192.168.1.253', name='MacBook')

    while not client.connected:
        # print("Waiting for connection...")
        time.sleep(1)

    print("Client connected, can send data now.")
    while True:
        command = input('Enter Command: ')
        if command.lower() == 'exit': break
        client.send_data(command)