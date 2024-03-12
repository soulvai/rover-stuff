import asyncio
import websockets
import cv2
import numpy as np
import base64
from tkinter import *
from PIL import Image, ImageTk

class MultiClientHandler:
    def __init__(self, ips_and_ports):
        self.ips_and_ports = ips_and_ports
        self.app = Tk()
        self.app.title("ROVER CAMERA FEED")
        self.app.geometry("890x640")
        self.app.bind('<Escape>', lambda e: self.app.quit())
        
        self.error_image = ImageTk.PhotoImage(image=Image.open("./image.png").resize((400, 300)))

        self.label_widgets = [Label(self.app, image=self.error_image, bd=5, relief=SUNKEN, padx=5, pady=5) for _ in range(len(ips_and_ports))]
        for row in range(2):
            for col in range(2):
                index = row * 2 + col
                if index < len(ips_and_ports):
                    self.label_widgets[index].grid(row=row, column=col)

    async def connect_and_receive(self, ip, port, label_widget):
        while True:
            try:
                uri = f"ws://{ip}:{port}"
                async with websockets.connect(uri) as websocket:
                    print(f"Websocket Connection Found for {ip}:{port}...Feeding...")
                    while True:
                        try:
                            frame_data = await websocket.recv()

                            buffer = base64.b64decode(frame_data)
                            np_arr = np.frombuffer(buffer, dtype=np.uint8)

                            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            frame_resized = cv2.resize(frame_rgb, (400, 300))

                            photo_image = ImageTk.PhotoImage(image=Image.fromarray(frame_resized))
                            label_widget.photo_image = photo_image
                            label_widget.configure(image=photo_image)

                            self.app.update()

                        except websockets.exceptions.ConnectionClosed:
                            print(f"Connection closed for {ip}:{port}. Showing error image.")
                            label_widget.configure(image=self.error_image)
                            self.app.update()
                            break

            except Exception as e:
                print(f"Error for {ip}:{port}: {e}. Retrying...")
                await asyncio.sleep(1)

    async def client_handler(self):
        tasks = [self.connect_and_receive(ip, port, label_widget) for (ip, port), label_widget in zip(self.ips_and_ports, self.label_widgets)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":

    ips_and_ports = [("192.168.0.109", 8765), 
                     ("192.168.0.109", 8766), 
                     ("192.168.0.109", 8767), 
                     ("192.168.0.109", 8768)]
    
    multi_client_handler = MultiClientHandler(ips_and_ports)
    asyncio.run(multi_client_handler.client_handler())
