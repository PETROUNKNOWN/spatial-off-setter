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
        self.sensors_delta = 0.5
        self.sound_speed=343
        self.meter_multiplier=1

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        platformFrame = ctk.CTkFrame(self, width=600, height=600, border_color="red", border_width=1)
        platformFrame.grid(row=0, column=0, padx=(5, 5), pady=5)
        platformFrame.grid_propagate(False)

        controlsFrame = ctk.CTkFrame(self, width=340, height=600, border_color="red", border_width=1)
        controlsFrame.grid(row=0, column=1, padx=(0, 5), pady=5)
        controlsFrame.grid_propagate(False)
        controlsFrame.grid_columnconfigure(1, weight=1)

        self.canvas = ctk.CTkCanvas(platformFrame, width=600, height=600, bg="white")
        self.canvas.pack(side="left", padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.click_handler)
        self.draw_grid()
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
        pass
        

    def draw_grid(self):
        self.canvas.delete("all")
        size=600
        half_size=size//2
        self.canvas.create_line(half_size,0,half_size,size,fill="black",width=2)
        self.canvas.create_line(0,half_size,size,half_size,fill="black",width=2)
        self.dash=(2,2) if self.grid_lines.lower()=="dashed" else None
        self.canvasDivisions=10
        self.canvasSize=600
        self.scaler=self.canvasSize/self.canvasDivisions
        self.canvasStep=self.canvasSize/self.canvasDivisions
        for i in range(1,self.canvasDivisions):
            for j in range(1,self.canvasDivisions):
                x=i*self.canvasStep
                y=j*self.canvasStep
                self.canvas.create_line(x,0,x,self.canvasSize,fill="black",dash=self.dash)
                self.canvas.create_line(0,y,self.canvasSize,y,fill="black",dash=self.dash)

        #Debug
        coords = [(300,300),(0,0),(300,0),(600,0),(300,0),(180,180),(420,180)]
        # for i in coords:
            # left_delay, right_delay, left_volume, right_volume = self.calculate_delay_and_volume(i[0], i[1])
        #Debug
                
    def click_handler(self,event):
        x,y=event.x,event.y
        print(f"Click at {x},{y}")
        l_del,r_del,l_vol,r_vol=self.adjustment_algo(x,y)
        self.mixer_algo(l_del,r_del,l_vol,r_vol)

    def mixer_algo(self,l_del,r_del,l_vol,r_vol):
        l_del_samps=int(l_del*self.samplerate)
        r_del_samps=int(r_del*self.samplerate)
        l_channel=np.zeros((len(self.data)+l_del_samps,2))
        r_channel=np.zeros((len(self.data)+r_del_samps,2))
        l_channel[l_del_samps:l_del_samps+len(self.data),0]=self.data[:,0]*l_vol
        r_channel[r_del_samps:r_del_samps+len(self.data),1]=self.data[:,1]*r_vol
        combined_len=max(len(l_channel),len(r_channel))
        mixed_signal=np.zeros((combined_len,2))
        mixed_signal[:len(l_channel)]+=l_channel
        mixed_signal[:len(r_channel)]+=r_channel
        #Play audio
        sd.play(mixed_signal, self.samplerate)
        sd.wait()

    def adjustment_algo(self,x,y):
        cen=int(self.canvas.cget("height"))//2
        x_dist=x-cen
        y_dist=y-cen
        l_dist=(math.sqrt((x_dist+self.sensors_delta/2)**2+y_dist**2))/self.scaler
        r_dist=(math.sqrt((x_dist-self.sensors_delta/2)**2+y_dist**2))/self.scaler
        l_del=(l_dist/self.sound_speed)*self.meter_multiplier
        r_del=(r_dist/self.sound_speed)*self.meter_multiplier
        if l_del<r_del:
            l_vol=1/(l_dist*0.5)
            r_vol=1/(0.8+l_dist)       
        elif l_del>r_del:
            r_vol=1/(r_dist*0.5)
            l_vol=1/(0.8+r_dist)
        else:
            l_vol=1
            r_vol=1
            # volume for low doent work
            # time for high dont work
        return l_del,r_del,l_vol,r_vol

if __name__ == "__main__":
    app = App()
    app.mainloop()
