# Multicast Chatting Tool

A real-time group chat application built with Python using multicast networking. This tool allows multiple users on the same network to communicate in a shared chat room without requiring a central server.

## Features

- **Multicast Communication**: Uses UDP multicast for efficient group messaging
- **Real-time Messaging**: Instant message delivery to all connected users
- **User-friendly GUI**: Clean and intuitive interface built with tkinter
- **Audio Notifications**: Sound alerts for incoming messages
- **Automatic Username Detection**: Uses system username by default
- **Message Timestamps**: All messages include sender and timestamp information
- **Cross-platform**: Works on Windows, macOS, and Linux

## Screenshots

![Chat Interface](assets/screenshot.png)
*Main chat interface showing real-time conversations*

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- playsound library for audio notifications

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd multicast_chatting_tool
   ```

2. **Install dependencies**:
   ```bash
   pip install playsound
   ```

3. **Verify file structure**:
   ```
   multicast_chatting_tool/
   ├── multicast_chat_gui.py
   ├── assets/
   │   └── notification.wav
   └── README.md
   ```

## Usage

### Quick Start

1. **Run the application**:
   ```bash
   python multicast_chat_gui.py
   ```

2. **Start chatting**:
   - The app will automatically use your system username
   - Type messages in the input field at the bottom
   - Press Enter or click "Send" to send messages
   - All users on the same network will receive your messages instantly

### Testing the Application

#### Single Machine Testing
```bash
# Terminal 1
python multicast_chat_gui.py

# Terminal 2  
python multicast_chat_gui.py

# Terminal 3
python multicast_chat_gui.py
```

#### Network Testing
1. Ensure all computers are on the same local network
2. Run the application on each computer:
   ```bash
   python multicast_chat_gui.py
   ```
3. Start sending messages between different machines

#### Troubleshooting Tests

**Test 1: Check if multicast is working**
```python
# Run this in Python console to test multicast reception
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 12345))
mreq = socket.inet_aton('224.0.0.1') + socket.inet_aton('0.0.0.0')
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
print("Listening for multicast messages...")
data, addr = sock.recvfrom(1024)
print(f"Received: {data.decode()} from {addr}")
```

**Test 2: Verify notification sound**
```python
# Test notification sound separately
from playsound import playsound
playsound('assets/notification.wav')
```

**Test 3: Check network connectivity**
```bash
# Windows
ping 224.0.0.1

# Linux/macOS
ping -c 4 224.0.0.1
```

## Configuration

### Network Settings
The application uses these default network settings:
- **Multicast IP**: 224.0.0.1
- **Port**: 12345
- **Interface**: All available interfaces (0.0.0.0)

To modify these settings, edit the constants in `multicast_chat_gui.py`:
```python
MULTICAST_GROUP = '224.0.0.1'  # Change multicast IP
MULTICAST_PORT = 12345         # Change port number
```

### Audio Settings
- Notification sound: `assets/notification.wav`
- Auto-generated if missing or corrupted
- Fallback to system beep if audio fails

## How It Works

### Multicast Networking
- Uses UDP multicast (224.0.0.1) for efficient group communication
- No central server required - all clients communicate directly
- Messages are broadcast to all participants simultaneously

### Message Format
```json
{
  "username": "John",
  "message": "Hello everyone!",
  "timestamp": "2024-10-04 15:30:25"
}
```

### Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client A      │    │   Client B      │    │   Client C      │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ GUI Thread  │ │    │ │ GUI Thread  │ │    │ │ GUI Thread  │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │Listen Thread│ │    │ │Listen Thread│ │    │ │Listen Thread│ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Multicast Group │
                    │   224.0.0.1     │
                    │   Port 12345    │
                    └─────────────────┘
```

## Troubleshooting

### Common Issues

**Issue 1: "Address already in use" error**
```bash
# Solution: Kill existing processes using the port
# Windows:
netstat -ano | findstr :12345
taskkill /F /PID <PID>

# Linux/macOS:
sudo lsof -i :12345
sudo kill -9 <PID>
```

**Issue 2: No messages received**
- Check firewall settings (allow Python/port 12345)
- Verify all devices are on the same network
- Ensure multicast is enabled on your router
- Try running as administrator/root

**Issue 3: Audio notification not working**
- Check if `assets/notification.wav` exists and has content
- Install audio codecs if needed
- The app will auto-generate the sound file if missing

**Issue 4: Permission denied errors**
```bash
# Run with elevated permissions
# Windows (as Administrator):
python multicast_chat_gui.py

# Linux/macOS:
sudo python multicast_chat_gui.py
```

### Network Requirements
- All participants must be on the same local network
- Multicast must be enabled on network switches/routers
- Firewall should allow UDP traffic on port 12345
- Some VPNs may block multicast traffic

## Development

### Project Structure
```
multicast_chatting_tool/
├── multicast_chat_gui.py      # Main application file
├── assets/
│   ├── notification.wav       # Audio notification file
│   └── screenshot.png         # Application screenshot
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

### Key Components

1. **MulticastChatApp Class**: Main application class handling GUI and networking
2. **listen_for_messages()**: Background thread for receiving multicast messages
3. **send_message()**: Function to broadcast messages to the multicast group
4. **create_notification_sound()**: Auto-generates notification audio file

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Technical Details

### Multicast Group Information
- **Address Range**: 224.0.0.0 to 224.0.0.255 (Local Network Control Block)
- **TTL**: 1 (Local network only)
- **Protocol**: UDP (User Datagram Protocol)

### Performance Considerations
- Supports up to 50+ concurrent users on typical networks
- Message size limit: 1024 bytes
- Minimal CPU usage with efficient threading
- Low network overhead due to multicast efficiency

## Support

For support, questions, or bug reports:
1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information about your problem

---

**Note**: This application is designed for educational purposes and local network communication. For production use, consider implementing additional security measures such as message encryption and user authentication.
