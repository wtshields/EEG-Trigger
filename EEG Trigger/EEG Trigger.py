import socket
import datetime
import socket

class EEGTrigger:
    def __init__(self, eeg_ip, eeg_port):
        self.eeg_ip = eeg_ip
        self.eeg_port = eeg_port
        self.eeg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.eeg_socket.connect((self.eeg_ip, self.eeg_port))

    def new_test(self, test_name):
        # Code to trigger EEG for a new test
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.send_trigger(f"Triggering EEG for new test: {test_name} at {timestamp}")

    def new_trial(self, trial_name):
        # Code to trigger EEG for a new trial
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.send_trigger(f"Triggering EEG for new trial: {trial_name} at {timestamp}")

    def eeg_response(self, response_name):
        # Code to trigger EEG for an EEG response
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.send_trigger(f"Triggering EEG for EEG response: {response_name} at {timestamp}")

    def send_trigger(self, trigger_message):
        self.eeg_socket.sendall(trigger_message.encode())

    def close_connection(self):
        self.eeg_socket.close()

        # Create a new class to handle receiving messages
        class MessageReceiver:
            def __init__(self, ip, port):
                self.ip = ip
                self.port = port
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.bind((self.ip, self.port))
                self.socket.listen(1)

            def receive_message(self):
                client_socket, client_address = self.socket.accept()
                message = client_socket.recv(1024).decode()
                client_socket.close()
                return message

        receiver = MessageReceiver("localhost", 1234)
        message = receiver.receive_message()
        trigger = EEGTrigger("eeg_device_ip", eeg_device_port)
        trial = 0
        if message == "Start Trial":
            trigger.new_test("Start Test")
        elif message == "Start Test":
            trial += 1
            trigger.new_trial(f"Start Trial {trial}")  # Added missing method call to trigger object
        elif message == "Start Response":
            trigger.eeg_response(f"Start Response {trial}")
        elif message == "End Trial":
                trigger.new_trial(f"End Trial {trial}")
        elif message == "End Test":
                trigger.new_test("End Test")
        elif message == "End Response":
                trigger.eeg_response(f"End Response {trial}")
        else:
            print("Invalid message received")
        receiver.socket.close()