import time
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Controller
from pynput.keyboard import Key
import threading
import tkinter as tk
from tkinter import ttk

class AutoClicker:
    def __init__(self):
        self.recording = False
        self.playing = False
        self.clicks = []  # Will now store (x, y, button, timestamp) tuples
        self.mouse_controller = Controller()
        self.mouse_listener = None
        self.keyboard_listener = None
        self.playback_thread = None
        self.playback_interval = 9 * 60  # default 9 minutes
        self.recording_start_time = None
        self.next_playback_time = None
        
        # Create and setup the window
        self.root = tk.Tk()
        self.root.title("AutoClicker")
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)  # Handle window closing
        
        # Create and pack widgets
        self.status_label = ttk.Label(self.root, text="Status: Ready", font=('Courier', 10))
        self.status_label.pack(pady=5)
        
        self.clicks_label = ttk.Label(self.root, text="Clicks recorded: 0", font=('Courier', 10))
        self.clicks_label.pack(pady=5)
        
        # Interval input frame
        interval_frame = ttk.Frame(self.root)
        interval_frame.pack(pady=5)
        
        ttk.Label(interval_frame, text="Playback interval (seconds):", font=('Courier', 10)).pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value="540")  # 9 minutes in seconds
        self.interval_entry = ttk.Entry(interval_frame, textvariable=self.interval_var, width=6, font=('Courier', 10))
        self.interval_entry.pack(side=tk.LEFT, padx=5)
        
        self.timer_label = ttk.Label(self.root, text="Next playback in: --:--", font=('Courier', 10))
        self.timer_label.pack(pady=5)
        
        self.instructions = """
F8: Start/Stop recording
F9: Start/Stop playback
        """
        self.instructions_label = ttk.Label(self.root, text=self.instructions, font=('Courier', 10))
        self.instructions_label.pack(pady=5)

    def on_key_press(self, key):
        try:
            if key == Key.f8:
                if not self.recording:
                    self.start_recording()
                else:
                    self.stop_recording()
            elif key == Key.f9:
                if not self.playing:
                    self.start_playback()
                else:
                    self.stop_playback()
        except Exception as e:
            print(f"Error handling key press: {e}")

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")
        self.root.update()

    def update_clicks(self):
        self.clicks_label.config(text=f"Clicks recorded: {len(self.clicks)}")
        self.root.update()

    def update_timer(self):
        if self.playing and self.next_playback_time:
            remaining = self.next_playback_time - time.time()
            if remaining > 0:
                minutes = int(remaining // 60)
                seconds = int(remaining % 60)
                self.timer_label.config(text=f"Next playback in: {minutes:02d}:{seconds:02d}")
            else:
                self.timer_label.config(text="Next playback in: 00:00")
        else:
            self.timer_label.config(text="Next playback in: --:--")
        self.root.update()

    def get_playback_interval(self):
        try:
            seconds = float(self.interval_var.get())
            return max(0.1, seconds)  # Minimum 0.1 seconds
        except ValueError:
            return 9 * 60  # Default to 9 minutes if invalid input

    def on_click(self, x, y, button, pressed):
        if pressed and self.recording:
            current_time = time.time()
            if self.recording_start_time is None:
                self.recording_start_time = current_time
                relative_time = 0
            else:
                relative_time = current_time - self.recording_start_time
            self.clicks.append((x, y, button, relative_time))
            self.update_clicks()
            print(f"Recorded click at ({x}, {y}) at {relative_time:.3f}s")

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.clicks = []
            self.recording_start_time = None
            self.mouse_listener = mouse.Listener(on_click=self.on_click)
            self.mouse_listener.start()
            self.update_status("Recording...")
            print("Recording started... Press F8 to stop recording.")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            if self.mouse_listener:
                self.mouse_listener.stop()
            self.update_status("Ready")
            print(f"Recording stopped. {len(self.clicks)} clicks recorded.")

    def playback_sequence(self):
        while self.playing:
            if not self.clicks:
                break
                
            last_time = 0
            for x, y, button, click_time in self.clicks:
                if not self.playing:
                    break
                    
                # Wait for the correct time to perform the click
                time_to_wait = click_time - last_time
                if time_to_wait > 0:
                    # Check for stop condition every 0.1 seconds during wait
                    for _ in range(int(time_to_wait * 10)):
                        if not self.playing:
                            return
                        time.sleep(0.1)
                
                if not self.playing:
                    break
                    
                self.mouse_controller.position = (x, y)
                self.mouse_controller.click(button)
                last_time = click_time
                
            # Set the next playback time
            self.playback_interval = self.get_playback_interval()
            self.next_playback_time = time.time() + self.playback_interval
            
            # Wait for the playback interval before repeating, checking for stop every 0.1 seconds
            for _ in range(int(self.playback_interval * 10)):
                if not self.playing:
                    return
                self.update_timer()
                time.sleep(0.1)

    def start_playback(self):
        if not self.playing and self.clicks:
            self.playing = True
            self.playback_interval = self.get_playback_interval()
            self.next_playback_time = time.time() + self.playback_interval
            self.playback_thread = threading.Thread(target=self.playback_sequence)
            self.playback_thread.start()
            self.update_status("Playing...")
            print("Playback started... Press F9 to stop playback.")

    def stop_playback(self):
        if self.playing:
            self.playing = False
            if self.playback_thread:
                self.playback_thread.join()
            self.update_status("Ready")
            self.next_playback_time = None
            self.update_timer()
            print("Playback stopped.")

    def run(self):
        # Start keyboard listener for global hotkeys
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        # Start the tkinter main loop
        self.root.mainloop()

    def exit_program(self):
        self.stop_recording()
        self.stop_playback()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        print("Exiting...")
        self.root.quit()
        raise KeyboardInterrupt

if __name__ == "__main__":
    try:
        clicker = AutoClicker()
        clicker.run()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.") 