import customtkinter as ctk
import sounddevice as sd
import numpy as np
import math
import soundfile as sf 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Surround Sound")
        self.resizable(0,0)

        self.file_path="assets/clickNew.mp3"
        self.sensors_delta=5 #in Meters
        self.sound_speed=343 #in MetersPerSeconds
        self.data, self.samplerate = sf.read(self.file_path, dtype='float32')
        
        self.divisions=10
        self.distance=50 #in Meters
        self.single_spacing=self.distance/self.divisions
        self.spacing=500/self.divisions
        self.foo=int((1/self.spacing)*100)+(0.5*int((1/self.spacing)*100))
        self.scaler=(self.distance*self.divisions)/500
        # print(self.foo)


        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)


        self.platform=ctk.CTkFrame(self,width=1000,height=500)
        self.platform.grid(row=0,column=0,sticky="nsew",padx=5,pady=5)
        self.platform.grid_propagate(False)

        self.settings=ctk.CTkFrame(self,width=200,height=500,border_color="red",border_width=1)
        self.settings.grid(row=0,column=1,padx=(3, 5),pady=5,sticky="nsew")
        self.settings.grid_propagate(False)
        self.populatePlatform()


    def populatePlatform(self):
        self.canvas=ctk.CTkCanvas(self.platform,bg="white",width=1000,height=500,highlightthickness=0)
        self.canvas.grid(row=0,column=0,sticky="nsew")
        self.draw_markers(self.divisions+int(self.foo),self.spacing,dash=False)
        self.canvas.bind("<Button-1>",self.click_handler)


    def draw_markers(self,count,spacing,dash=(5,2)):
        self.canvas.delete("all")
        canvasWidth=1000
        canvasHeight=500
        self.canvas.create_line(canvasHeight,0,canvasHeight,canvasHeight,fill="black",width=1)
        self.canvas.create_line(0,canvasHeight-2,canvasWidth,canvasHeight-2,fill="black",width=1)
        center_x,center_y=500,500
        for i in range(count):
            radius=(i+1)*spacing
            self.canvas.create_arc((center_x-radius,center_y-radius),(center_x+radius,center_y+radius),width=1,start=0,extent=180,style=ctk.ARC,dash=dash if dash==True else ())


    def click_handler(self,event):
        print(f"Click at:({event.x},{event.y})")
        cen=500
        x_dist=event.x-cen
        y_dist=event.y-cen
        l_dist=((math.sqrt((x_dist+self.sensors_delta/2)**2+y_dist**2))*self.distance)/500
        r_dist=((math.sqrt((x_dist-self.sensors_delta/2)**2+y_dist**2))*self.distance)/500
        # l_intensity=math.log(l_dist,2)
        # r_intensity=math.log(r_dist,2)
        # l_intensity=l_dist * math.exp(l_dist / cen)
        # r_intensity=r_dist * math.exp(r_dist / cen)
        factor=20
        l_intensity = 1/(l_dist * math.exp(l_dist / (cen * factor)))
        r_intensity = 1/(r_dist * math.exp(r_dist / (cen * factor)))
        print(f"l_intensity:({l_intensity})")
        print(f"r_intensity:({r_intensity})")
        avgDist=(l_dist+r_dist)/2
        # print(f"Distance:({avgDist})")
        l_chan=l_dist/self.sound_speed
        r_chan=r_dist/self.sound_speed
        avgTime=(l_chan+r_chan)/2
        # print(f"Time:({avgTime})")
        # if l_intensity>0.20234080729896867:
        #     l_intensity=0.20234080729896867
        # if r_intensity>0.20234080729896867:
        #     r_intensity=0.20234080729896867

        if l_chan<r_chan:
            l_vol=1/(l_dist*0.5)
            r_vol=1/(0.8+l_dist)       
        elif l_chan>r_chan:
            r_vol=1/(r_dist*0.5)
            l_vol=1/(0.8+r_dist)
        else:
            l_vol=1
            r_vol=1
            # volume for low doent work
            # time for high dont work
        print(f"Left Volume: {l_intensity}")
        print(f"Right Volume: {r_intensity}")
        print(f"l_chan:({l_chan})")
        print(f"r_chan:({r_chan})")
        self.mixer_algo(l_chan,r_chan,l_intensity,r_intensity)
        
        return
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
        print("Done")

if __name__ == "__main__":
    app = App()
    app.mainloop()