import tkinter as tk
from tkinter import messagebox
import time
import threading
import os
from pygame import mixer

# Initialize pygame mixer for sound
mixer.init()

# Ensure sound file exists or create it dynamically
def create_bell_sound():
    bell_path = "bell_sound.wav"
    if not os.path.exists(bell_path):
        import wave
        import struct
        
        with wave.open(bell_path, "w") as wave_file:
            wave_file.setnchannels(1)  # Mono
            wave_file.setsampwidth(2)  # 16-bit
            wave_file.setframerate(44100)
            duration = 0.5  # Seconds
            frequency = 440.0  # Hz
            amplitude = 32767  # Max amplitude for 16-bit audio

            num_samples = int(duration * 44100)
            for i in range(num_samples):
                value = amplitude * 0.5 * (1.0 + (-1) ** (i // (44100 // (2 * frequency))))
                packed_value = struct.pack('<h', int(value))
                wave_file.writeframesraw(packed_value)
    return bell_path

bell_sound = create_bell_sound()

# Play the bell sound
def play_bell():
    mixer.music.load(bell_sound)
    mixer.music.play()

# Timer logic
class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")

        self.timer_label = tk.Label(root, text="Timer", font=("Arial", 24))
        self.timer_label.pack(pady=20)

        self.default_buttons_frame = tk.Frame(root)
        self.default_buttons_frame.pack(pady=10)

        self.create_default_timers()

        self.custom_timer_label = tk.Label(root, text="Custom Timer (min):")
        self.custom_timer_label.pack()

        self.custom_timer_entry = tk.Entry(root, justify="center", font=("Arial", 14))
        self.custom_timer_entry.pack()

        self.custom_timer_button = tk.Button(root, text="Start Custom Timer", command=self.start_custom_timer)
        self.custom_timer_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Timer", command=self.stop_timer, state="disabled")
        self.stop_button.pack(pady=10)

        self.running = False

    def create_default_timers(self):
        default_times = [4, 8, 15, 30]  # Minutes
        for t in default_times:
            button = tk.Button(self.default_buttons_frame, text=f"{t} min", command=lambda t=t: self.start_timer(t))
            button.pack(side=tk.LEFT, padx=5)

    def start_timer(self, minutes):
        if self.running:
            messagebox.showwarning("Timer Running", "A timer is already running!")
            return

        self.running = True
        self.stop_button["state"] = "normal"

        def timer_thread():
            seconds = minutes * 60
            while seconds > 0 and self.running:
                mins, secs = divmod(seconds, 60)
                self.timer_label.config(text=f"{mins:02}:{secs:02}")
                time.sleep(1)
                seconds -= 1

            if self.running:
                self.timer_label.config(text="Time's Up!")
                play_bell()

            self.running = False
            self.stop_button["state"] = "disabled"

        threading.Thread(target=timer_thread, daemon=True).start()

    def start_custom_timer(self):
        try:
            minutes = int(self.custom_timer_entry.get())
            if minutes <= 0:
                raise ValueError
            self.start_timer(minutes)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for minutes.")

    def stop_timer(self):
        self.running = False
        self.timer_label.config(text="Timer Stopped")
        self.stop_button["state"] = "disabled"

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

    # Quit mixer safely
    mixer.quit()

