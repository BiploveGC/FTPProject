import os
import socket
import sys

# Command line check
if len(sys.argv) < 3:
    print("COMMAND: python cli.py <SERVER_MACHINE> <PORT_NUMBER>")
    sys.exit()

# Server address and port (from command line)
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a TCP socket for the control channel
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
clientSocket.connect((serverName, serverPort))

while True:
    # Get command from command line (user)
    command = input("Enter command (ls, put <filename>, get <filename>, quit): ")

    # Send command to the server
    clientSocket.send(command.encode())

    # PUT command (client side)
    if command.startswith("put"):
        _, filename = command.split(" ", 1)

        # Check if file exists
        if not os.path.isfile(filename):
            print(f"Error: File '{filename}' does not exist")
            continue

        # Create an ephemeral port for data transfer
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.bind(('', 0))  # Bind to an ephemeral port
        dataPort = dataSocket.getsockname()[1]

        # Print the ephemeral port to verify it
        print(f"Ephemeral port created: {dataPort}")

        # Send the ephemeral port number to the server
        clientSocket.send(str(dataPort).encode())

        # Accept the connection from the server for data transfer
        dataSocket.listen(1)
        connection, addr = dataSocket.accept()

        # Open the file & read its content
        with open(filename, "rb") as file:
            fileData = file.read()

        # Send file size first
        fileSize = len(fileData)
        connection.send(str(fileSize).encode())
        print(f"Sent file size: {fileSize}")

        # Send file data
        connection.send(fileData)
        print(f"Sent file data for '{filename}'.")

        # Close the data connection
        connection.close()
        dataSocket.close()

        # Receive and print response from the server
        response = clientSocket.recv(4096).decode()
        print(f"Server response:\n{response}")

    # GET command (client side)
    elif command.startswith("get"):
        _, filename = command.split(" ", 1)

        # Create an ephemeral port for data transfer
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.bind(('', 0))  # Bind to an ephemeral port
        dataPort = dataSocket.getsockname()[1]

        # Print the ephemeral port to verify it
        print(f"Ephemeral port created: {dataPort}")

        # Send the ephemeral port number to the server
        clientSocket.send(str(dataPort).encode())

        # Accept the connection from the server for data transfer
        dataSocket.listen(1)
        connection, addr = dataSocket.accept()

        # Receive the file size from the server
        fileSize = int(connection.recv(4096).decode())

        # Confirm to the server that the client is ready to receive the file
        connection.send("READY".encode())

        # Receive the file data in chunks
        fileData = b""
        remaining = fileSize
        while remaining > 0:
            chunk = connection.recv(min(4096, remaining))
            if not chunk:
                break
            fileData += chunk
            remaining -= len(chunk)

        # Write the received data to a new file
        with open(filename, "wb") as file:
            file.write(fileData)

        print(f"File '{filename}' received successfully.")

        # Close the data connection
        connection.close()
        dataSocket.close()

    # Handle 'ls' and 'quit' commands
    elif command == "ls":
        response = clientSocket.recv(4096).decode()
        print(f"Server response:\n{response}")

    elif command == "quit":
        response = clientSocket.recv(4096).decode()
        print(f"Server response:\n{response}")
        clientSocket.close()
        break

    # Handle unknown command
    else:
        response = clientSocket.recv(4096).decode()
        print(f"Server response:\n{response}")