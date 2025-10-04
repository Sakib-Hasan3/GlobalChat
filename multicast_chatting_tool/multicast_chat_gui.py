import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import threading
import socket
import struct
import os
import platform
import wave
import math

# Optional playsound for notifications
try:
    from playsound import playsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

# --- Configuration ---
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5004
NOTIFICATION_SOUND = os.path.join("assets", "notification.wav")

# --- Themes ---
THEMES = {
    "dark": {
        "bg": "#2c2f33",
        "fg": "#ffffff",
        "entry_bg": "#23272a",
        "entry_fg": "#ffffff",
        "button_bg": "#7289da",
        "button_fg": "#ffffff",
        "msg_bg": "#40444b",
        "msg_fg": "#ffffff"
    },
    "light": {
        "bg": "#f5f5f5",
        "fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000",
        "button_bg": "#4CAF50",
        "button_fg": "#ffffff",
        "msg_bg": "#e0e0e0",
        "msg_fg": "#000000"
    }
}

THEME = "dark"
C = THEMES[THEME]

# --- Notification Sound ---
def create_notification_sound():
    if not os.path.exists(NOTIFICATION_SOUND) or os.path.getsize(NOTIFICATION_SOUND) == 0:
        os.makedirs(os.path.dirname(NOTIFICATION_SOUND), exist_ok=True)
        sample_rate = 22050
        duration = 0.3
        frequency = 800
        samples = []
        for i in range(int(sample_rate * duration)):
            t = i / sample_rate
            envelope = 1.0
            if t < 0.05: envelope = t / 0.05
            elif t > duration-0.05: envelope = (duration-t)/0.05
            sample = envelope * math.sin(2*math.pi*frequency*t)
            samples.append(int(sample*32767))
        with wave.open(NOTIFICATION_SOUND,'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            import struct
            for s in samples:
                wav_file.writeframes(struct.pack('<h', s))

# --- Chat App ---
class ChatApp:
    def __init__(self, root, username):
        self.username = username
        self.root = root
        self.root.title(f"Chat - {username}")
        self.root.geometry("550x500")
        self.root.configure(bg=C["bg"])

        # --- Chat Area ---
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg=C["bg"], fg=C["fg"],
                                                   font=("Helvetica", 11), state='disabled', bd=0, highlightthickness=0)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # --- Entry Frame ---
        self.entry_frame = tk.Frame(root, bg=C["bg"])
        self.entry_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        self.msg_entry = tk.Entry(self.entry_frame, bg=C["entry_bg"], fg=C["entry_fg"], font=("Helvetica", 12))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.entry_frame, text="Send", bg=C["button_bg"], fg=C["button_fg"],
                                     font=("Helvetica", 11, "bold"), command=self.send_message, relief=tk.FLAT)
        self.send_button.pack(side=tk.RIGHT)

        # --- Networking ---
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        threading.Thread(target=self.receive_messages, daemon=True).start()

    # --- Send ---
    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg:
            timestamp = datetime.now().strftime("%H:%M:%S")
            full_msg = f"[{timestamp}] [{self.username}] {msg}"
            self.sock.sendto(full_msg.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
            self.msg_entry.delete(0, tk.END)

    # --- Receive ---
    def receive_messages(self):
        while True:
            try:
                data,_ = self.sock.recvfrom(1024)
                msg = data.decode('utf-8')
                self.display_message(msg)
                self.play_notification()
            except:
                break

    # --- Display ---
    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message+"\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    # --- Notification ---
    def play_notification(self):
        if SOUND_AVAILABLE and os.path.exists(NOTIFICATION_SOUND):
            threading.Thread(target=playsound, args=(NOTIFICATION_SOUND,), daemon=True).start()
        else:
            if platform.system()=="Windows":
                import winsound
                winsound.Beep(1000,150)

# --- Main ---
def main():
    create_notification_sound()
    username = input("Enter your name: ")
    root = tk.Tk()
    app = ChatApp(root, username)
    root.mainloop()

if __name__=="__main__":
    main()
