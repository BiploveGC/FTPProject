**Simplified FTP Client-Server**

**Project Overview**

This project implements a simplified FTP (File Transfer Protocol) system using Python. It includes:

- Server (serv.py): Handles client commands and facilitates file transfers.
- Client (cli.py): Connects to the server to interact via FTP commands (ls, get, put, quit).

Group members:
1. Andrew Arsenault: AndrewJOropeza@gmail.com
2. Biplove GC: gcbiplove123@gmail.com
3. Stella Kim: Skim28@csu.fullerton.edu
4. Eduardo Casas: casaseddy23@gmail.com
 
**Programming Language:** Python

**Requirements**
- Python 3.7 or higher
- Standard Python libraries (socket, os, system, etc)

**Steps to run:**

1. Open the terminal
2. Navigate the server directory

   cd server

4. Start the server

   python serv.py <PORT>

   e.g. python3 serv.py 12345

6. Open another terminal
7. Naviage the client direectory
   
   cd client
   
8. Start the client
  
   python3 cli.py <SERVER_IP> <PORT>

   e.g. python3 cli.py 127.0.0.1 12345

**FTP commands**

1. ls: List all files in the server directory.
3. get <filename>: Download a file from the server.
4. put <filename>: Upload a file to the server.
5. quit: Disconnect from the server.

**Screenshots**
![image](https://github.com/user-attachments/assets/60f91054-e160-4847-a711-c6b1443c69a9)






