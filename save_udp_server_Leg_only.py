import socket
import csv
import time
import json
from datetime import datetime
from threading import Lock
from collections import defaultdict

filename = time.strftime("0023_04_%Y%m%d_%H%M%S")

class UDPServer:
    def __init__(self):
        # UDP server setup
        self.server_ip = '0.0.0.0'  
        self.server_port = 5005
        self.buffer_size = 65536  # Significantly increased buffer size

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((self.server_ip, self.server_port))
        self.udp_socket.setblocking(False)  # Set socket to non-blocking
        print(f"Listening for UDP packets on {self.server_ip}:{self.server_port}")

        # CSV file for raw data
        self.filename = filename
        self.raw_csv = f"{self.filename}_raw.csv"

        # Thread safety
        self.write_lock = Lock()
        self.running = True

        # In-memory storage for logs and packet counts
        self.log_buffer = []
        self.packet_counts = defaultdict(lambda: defaultdict(int))  # Structure: {second: {L_Leg: count, R_Leg: count}}

        # Track last second processed for periodic count printing
        self.last_print_time = time.time()

    def receive_and_process(self):
        while self.running:
            try:
                # Receive data
                data, addr = self.udp_socket.recvfrom(self.buffer_size)
                message = data.decode('utf-8')
                timestamp = time.time()

                # Parse JSON data
                try:
                    decoded_msg = json.loads(message)
                    # print(decoded_msg)
                except json.JSONDecodeError:
                    continue  # Skip invalid JSON messages

                # Count packets based on leg type (L_Leg or R_Leg)
                if 'L_Leg' in decoded_msg:
                    leg_type = 'L_Leg'
                elif 'R_Leg' in decoded_msg:
                    leg_type = 'R_Leg'
                else:
                    continue  # Skip if the leg type is not recognized

                # Increment packet count for the corresponding leg and second
                packet_second = int(timestamp)  # Use the integer part of the timestamp (second part)
                self.packet_counts[packet_second][leg_type] += 1

                # Store raw data in memory
                human_readable_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                self.queue_log_data(human_readable_timestamp, message)

                # Print packet counts for each second at regular intervals (every second)
                current_time = time.time()
                if current_time - self.last_print_time >= 1:  # Print every second
                    self.last_print_time = current_time
                    self.print_packet_counts()

            except BlockingIOError:
                # No data received, continue to the next loop
                continue

            except Exception as e:
                print(f"Error receiving data: {e}")

    def queue_log_data(self, timestamp, message):
        with self.write_lock:
            self.log_buffer.append((timestamp, message))

    def print_packet_counts(self):
        # Print packet counts for L_Leg and R_Leg for each second
        print("Packet counts (per second):")
        # Instead of modifying the dictionary, print it directly
        current_time = int(time.time())  # Get the current second
        for second in sorted(self.packet_counts.keys()):
            if second < current_time:  # Only print for seconds before the current one
                l_leg_count = self.packet_counts[second].get('L_Leg', 0)
                r_leg_count = self.packet_counts[second].get('R_Leg', 0)
                print(f"Second: {second} - L_Leg: {l_leg_count}, R_Leg: {r_leg_count}")

    def write_to_csv(self):
        """Writes the in-memory log buffer to the CSV file."""
        with open(self.raw_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'RawData'])  # Write headers
            writer.writerows(self.log_buffer)
        print(f"Data successfully written to {self.raw_csv}")

    def stop(self):
        self.running = False
        print("Writing data to CSV...")
        self.write_to_csv()


def main():
    server = UDPServer()

    try:
        server.receive_and_process()
    except KeyboardInterrupt:
        print("\nShutdown signal received.")
    finally:
        server.stop()
        server.udp_socket.close()


if __name__ == '__main__':
    main()
