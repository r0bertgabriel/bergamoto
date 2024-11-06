import datetime
import sqlite3
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import signal
import io
import time
import threading

def create_table():
    conn = sqlite3.connect('horarios.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS horarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  pin TEXT,
                  date TEXT,
                  time TEXT,
                  photo BLOB)''')
    conn.commit()
    conn.close()

def insert_record(name, pin, timestamp, photo_blob):
    date = timestamp.strftime("%d-%m-%Y")
    time = timestamp.strftime("%H:%M:00")
    conn = sqlite3.connect('horarios.db')
    c = conn.cursor()
    c.execute("INSERT INTO horarios (name, pin, date, time, photo) VALUES (?, ?, ?, ?, ?)", (name, pin, date, time, photo_blob))
    conn.commit()
    conn.close()

def capture_photo():
    img_blob = None

    def take_photo():
        nonlocal img_blob
        ret, frame = cam.read()
        if ret:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            with io.BytesIO() as output:
                img.save(output, format="PNG")
                img_blob = output.getvalue()
            messagebox.showinfo("Photo Capture", "Photo captured")
            cam.release()
            cv2.destroyAllWindows()
            root.quit()  # Use quit instead of destroy to properly exit the mainloop
        else:
            messagebox.showerror("Error", "Failed to grab frame")

    def show_frame():
        if not cam.isOpened() or not root.winfo_exists():
            return
        ret, frame = cam.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk  # Keep a reference to avoid garbage collection
            lmain.configure(image=imgtk)
        if root.winfo_exists():
            lmain.after(10, show_frame)

    cam = cv2.VideoCapture(0)
    root = tk.Tk()
    root.title("Photo Capture")

    frame = tk.Frame(root)
    frame.pack()

    lmain = tk.Label(frame)
    lmain.pack()

    capture_button = tk.Button(frame, text="Capture Photo", command=take_photo)
    capture_button.pack()

    show_frame()
    root.mainloop()
    cam.release()
    cv2.destroyAllWindows()
    root.destroy()  # Ensure the Tkinter window is properly destroyed
    return img_blob

class Employee:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.records = []

    def clock_in(self):
        now = datetime.datetime.now()
        today_records = [record for record in self.records if record.date() == now.date()]
        if len(today_records) >= 4:
            messagebox.showwarning("Limit Reached", "You have already made 4 records today.")
            return

        self.records.append(now)
        photo_blob = capture_photo()
        insert_record(self.name, self.pin, now, photo_blob)
        self.analyze_records()
        time.sleep(1)  # Wait for 1 second before asking for the next PIN

    def analyze_records(self):
        if len(self.records) == 2:
            pass
        elif len(self.records) == 3:
            pass
        elif len(self.records) == 4:
            pass
        else:
            pass

def main():
    create_table()
    employees = {
        "1234": Employee("Alice", "1234"),
        "5678": Employee("Bob", "5678"),
        "9101": Employee("Charlie", "9101")
    }

    def signal_handler():
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        pin = input("Digite seu PIN: ")
        if pin in employees:
            employee = employees[pin]
            threading.Thread(target=employee.clock_in).start()
            time.sleep(3)  # Wait for 3 seconds before asking for the PIN again
        else:
            pass

if __name__ == "__main__":
    main()