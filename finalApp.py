import customtkinter as ctk
import sounddevice as sd
import numpy as np
import math
import soundfile as sf 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Surround Sound")
        self.resizable(0, 0)

        # Variables
        self.grid_size = 150
        self.grid_lines = "solid"
        self.file_path = "assets/oemTone.mp3"

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        platformFrame = ctk.CTkFrame(self, width=600, height=600, border_color="red", border_width=1)
        platformFrame.grid(row=0, column=0, padx=(5, 5), pady=5)
        platformFrame.grid_propagate(False)

        controlsFrame = ctk.CTkFrame(self, width=340, height=600, border_color="red", border_width=1)
        controlsFrame.grid(row=0, column=1, padx=(0, 5), pady=5)
        controlsFrame.grid_propagate(False)
        controlsFrame.grid_columnconfigure(1, weight=1)

        self.populate_platformFrame(platformFrame)
        self.populate_controlsFrame(controlsFrame)
        self.data, self.samplerate = sf.read(self.file_path, dtype='float32')

    def populate_controlsFrame(self, frame):
        # ctk.CTkLabel(frame, text="Ear Distance:", anchor="w").grid(row=0, column=0, sticky="w", padx=15, pady=(20, 5))
        # self.ear_distance_entry = ctk.CTkEntry(frame)
        # self.ear_distance_entry.insert(0, str(self.ear_distance))
        # self.ear_distance_entry.grid(row=0, column=2, sticky="e", padx=15, pady=(20, 5))

        # ctk.CTkLabel(frame, text="Units:", anchor="w").grid(row=1, column=0, sticky="w", padx=15, pady=5)
        # self.units_var = ctk.StringVar(value=self.units)
        # ctk.CTkOptionMenu(frame, variable=self.units_var, values=["cm", "m", "km"]).grid(row=1, column=2, sticky="e", padx=15, pady=5)

        ctk.CTkLabel(frame, text="Grid Size:", anchor="w").grid(row=2, column=0, sticky="w", padx=15, pady=5)
        self.grid_size_entry = ctk.CTkEntry(frame)
        self.grid_size_entry.insert(0, str(self.grid_size))
        self.grid_size_entry.grid(row=2, column=2, sticky="e", padx=15, pady=5)

        ctk.CTkLabel(frame, text="Grid Lines:", anchor="w").grid(row=3, column=0, sticky="w", padx=15, pady=5)
        self.grid_lines_var = ctk.StringVar(value=self.grid_lines)
        ctk.CTkOptionMenu(frame, variable=self.grid_lines_var, values=["Solid", "Dashed"]).grid(row=3, column=2, sticky="e", padx=15, pady=5)

        ctk.CTkLabel(frame, text="Audio File Path:", anchor="w").grid(row=4, column=0, sticky="w", padx=15, pady=5)
        self.audio_file_entry = ctk.CTkEntry(frame)
        self.audio_file_entry.insert(0, self.file_path)
        self.audio_file_entry.grid(row=4, column=2, sticky="e", padx=15, pady=5)

        ctk.CTkButton(frame, text="Update Settings", command=self.update_settings).grid(row=5, column=2, sticky="nesw", padx=15, pady=5)

    def update_settings(self):
        try:
            # self.ear_distance = float(self.ear_distance_entry.get())
            # self.units = self.units_var.get()
            self.grid_size = int(self.grid_size_entry.get())
            self.grid_lines = self.grid_lines_var.get()
            self.file_path = self.audio_file_entry.get()
        except ValueError:
            print("Invalid input. Please check your values.")
        self.draw_grid()

    def populate_platformFrame(self, frame):
        self.canvas = ctk.CTkCanvas(frame, width=600, height=600, bg="white")
        self.canvas.pack(side="left", padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        width = int(self.canvas.cget("width"))
        height = int(self.canvas.cget("height"))
        
        # Draw axis
        self.canvas.create_line(width // 2, 0, width // 2, height, fill="black", width=2)
        self.canvas.create_line(0, height // 2, width, height // 2, fill="black", width=2)
        self.dash_pattern = (2, 2) if self.grid_lines.lower() == "dashed" else None

        # Draw grid lines
        # step = self.grid_size
        # for i in range(0, width, step):
            
        #     self.canvas.create_line(i, 0, i, height, fill="gray", dash=dash_pattern)
        # for i in range(0, height, step):
        #     self.canvas.create_line(0, i, width, i, fill="gray", dash=dash_pattern)

        self.canvasDivisions=10
        self.canvasSize=600

        self.scaler=self.canvasSize/self.canvasDivisions

        self.canvasStep=self.canvasSize/self.canvasDivisions
        for i in range(1, self.canvasDivisions):
            for j in range(1, self.canvasDivisions):
                x = i * self.canvasStep
                y = j * self.canvasStep
                self.canvas.create_line(x, 0, x, self.canvasSize, fill="black", dash=self.dash_pattern)
                self.canvas.create_line(0, y, self.canvasSize, y, fill="black", dash=self.dash_pattern)

        coords = [(300,300),(0,0),(300,0),(600,0),(300,0),(180,180),(420,180)]
        for i in coords:
            left_delay, right_delay, left_volume, right_volume = self.calculate_delay_and_volume(i[0], i[1])
                

    def on_click(self, event):
        click_x, click_y = event.x, event.y
        print(f"Click at {click_x},{click_y}")
        
        left_delay, right_delay, left_volume, right_volume = self.calculate_delay_and_volume(click_x, click_y)
        # print(f"received data")
        # print(f"starting audio change")
        self.play_stereo_sound(left_delay, right_delay, left_volume, right_volume)

    def play_stereo_sound(self, left_delay, right_delay, left_volume, right_volume):
        try:
            # print(f"starting audio change")
            # data, samplerate = sf.read(self.file_path, dtype='float32')

            # Apply delay as samples
            left_delay_samples = int(left_delay * self.samplerate)
            right_delay_samples = int(right_delay * self.samplerate)
            # print(f"done sampling audio")
            # print(f"starting audio delay")
            # Create delayed signals
            left_channel = np.zeros((len(self.data) + left_delay_samples, 2))
            right_channel = np.zeros((len(self.data) + right_delay_samples, 2))
            # print(f"done audio delay")
            # print(f"starting audio volume")

            left_channel[left_delay_samples:left_delay_samples + len(self.data), 0] = self.data[:, 0] * left_volume
            right_channel[right_delay_samples:right_delay_samples + len(self.data), 1] = self.data[:, 1] * right_volume
            # print(f"done audio volume")
            # print(f"starting audio mixing")
            # Mix the channels
            combined_length = max(len(left_channel), len(right_channel))
            mixed_signal = np.zeros((combined_length, 2))
            mixed_signal[:len(left_channel)] += left_channel
            mixed_signal[:len(right_channel)] += right_channel
            # print(f"done audio mixing")

            # Stream the audio
            # print(f"starting audio playing")
            sd.play(mixed_signal, self.samplerate)
            # print(f"still playing")
            sd.wait()
            # print(f"done audio mixing")
        
        except Exception as e:
            print(f"Error playing sound: {e}")

    def calculate_delay_and_volume(self, click_x, click_y):
        try:
            print(f"Coord:{click_x},{click_y}")
            # we find the middle of the platform
            # print(f"Doing coordinates")
            center_x = int(self.canvas.cget("width")) // 2
            center_y = int(self.canvas.cget("height")) // 2
            x_dist = click_x - center_x
            y_dist = click_y - center_y
            # x_dist = x_dist * x_dist
            # print(f"Doing squarerooting")
            left_distance = math.sqrt((x_dist + 0.5 / 2)**2 + y_dist**2)
            right_distance = math.sqrt((x_dist - 0.5 / 2)**2 + y_dist**2)
            # print(f"Doing delaying")
            # print(f"left_distance: {left_distance}")
            # print(f"right_distance: {right_distance}")

            
            left_distance = left_distance / self.scaler
            right_distance = right_distance / self.scaler



            # volume for low doent work
            # time for high dont work
            
            left_delay = (left_distance / 343) * 30
            right_delay = (right_distance / 343) * 30

            if left_delay<right_delay:
                left_volume=1
                print(f"delays diffs:{right_delay - left_delay}")
                right_volume=(right_delay+left_delay) * 1
            elif left_delay>right_delay:
                right_volume=1
                print(f"delays diffs:{left_delay - right_delay}")
                left_volume=(left_delay+right_delay) * 1
            else:
                left_volume=1
                right_volume=1




            # left_delay=0.008000008 # sounds interesting
            # left_delay=0.005
            # right_delay=0
            # volume_decay=0.34
            # left_volume = 1 / (1 + left_distance)
            # right_volume = 1 / (1 + right_distance)
            # the delay needs to work with the volume, neither can be constant. Try finding the theta of said relation

            # left_volume = 1
            # right_volume = 1

            # print(f"returning data")
            print(f"left_delay: {left_delay}")
            print(f"right_delay: {right_delay}")
            print(f"left_volume: {left_volume}")
            print(f"right_volume: {right_volume}")
            return left_delay, right_delay, left_volume, right_volume
        except Exception as e:
            print(f"Error playing sound: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
