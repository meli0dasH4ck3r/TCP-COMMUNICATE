# **TCP Chat Application**

## **Overview**

The **TCP Chat** is a client-server communication system built using Python's `socket` and `threading` libraries. It allows multiple clients to connect to a centralized server, exchange messages, and supports administrative commands like user bans and kicks.

---

## **Features**

- **Real-time Messaging**: Instant communication between multiple clients.
- **Admin Controls**:
  - Kick users from the server.
  - Ban users and prevent them from rejoining.
- **Authentication**: Admins are verified with a secure password.
- **Customizable Servers**: Clients can add and connect to multiple servers.
- **Threaded Communication**: Handles multiple clients simultaneously without blocking.

---

## **Project Structure**

```plaintext
.
├── server.py       # Server-side script to manage connections and messaging
├── client.py       # Client-side script for user interaction
├── bans.txt        # List of banned users
├── servers.json    # Stores client-saved servers
```

---

## **Getting Started**

### **Prerequisites**

- Python 3.x

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/meli0dasH4ck3r/TCP-CHAT.git
   ```
2. Navigate to the project directory:
   ```bash
   cd TCP-CHAT
   ```
3. Install required dependencies (if any):
   ```bash
   pip install -r requirements.txt  # (Optional if dependencies are added later)
   ```

---

## **Usage**

### **1. Running the Server**

Start the server using the following command:
```bash
python3 server.py
```

The server will:
- Listen on `127.0.0.1` and port `5555` by default.
- Accept multiple client connections.
- Manage admin commands and banned users.

### **2. Running the Client**

Start the client application:
```bash
python3 client.py
```

#### **Client Options**
- **Connect to an existing server**: Choose a nickname and start chatting.
- **Add a new server**: Save server details (IP and port) for future use.

---

## **Admin Commands**

Admins can execute special commands during chat:

| **Command**      | **Description**                   |
|------------------|-----------------------------------|
| `/kick <name>`   | Kick a user from the chat.        |
| `/ban <name>`    | Ban a user from the chat server.  |

**Note**: Only users with the nickname `admin` and correct password can execute these commands.

---

## **Configuration**

### **Server Settings**
- **Host**: `127.0.0.1` (default, configurable in `server.py`).
- **Port**: `5555` (default, configurable in `server.py`).

### **Client Settings**
- Servers are stored in `servers.json`. Add or edit server details through the client UI.

---

## **Example**

### **Server Output**
```plaintext
Server is Listening ...
Connected with ('127.0.0.1', 54321)
Nickname of the client is Client1
Client1 joined the Chat
```

### **Client Output**
```plaintext
Choose Your Nickname: Client1
Connected to the Server!
Client2: Hello everyone!
Client1: Hi Client2!
```

---

## **Contributing**

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`feature/your-feature-name`).
3. Commit your changes.
4. Open a pull request.

---

## **License**

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

---

## **Contact**

For any inquiries or issues, feel free to contact:
- **Name**: NGUYEN Viet Khoi
- **Email**: nguyenvietkhoi.work@gmail.com
- **GitHub**: [meli0dasH4ck3r](https://github.com/meli0dasH4ck3r)
