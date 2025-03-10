import customtkinter as ctk
import math

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Surround Sound")
        self.resizable(0,0)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        self.platform=ctk.CTkFrame(self,width=1000,height=500)
        self.platform.grid(row=0,column=0,sticky="nsew",padx=5,pady=5)
        self.platform.grid_propagate(False)

        self.settings=ctk.CTkFrame(self,width=200,height=500,border_color="red",border_width=1)
        self.settings.grid(row=0,column=1,padx=(3, 5),pady=5,sticky="nsew")
        self.settings.grid_propagate(False)


    def populatePlatform(self):
        self.canvas=ctk.CTkCanvas(self.platform,bg="white",width=1000,height=500,highlightthickness=0)
        self.canvas.grid(row=0,column=0,sticky="nsew")
        
        canvasWidth=1000
        canvasHeight=500

        self.canvas.create_line(canvasHeight,0,canvasHeight,canvasHeight,fill="black",width=1)
        self.canvas.create_line(0,canvasHeight-2,canvasWidth,canvasHeight-2,fill="black",width=1)

        self.draw_markers(6,100,dash=False)
        self.canvas.bind("<Button-1>",self.click_handler)


    def draw_markers(self,count,spacing,dash=(5,2)):
        self.canvas.delete("all")
        center_x,center_y=500,500
        for i in range(count):
            radius=(i+1)*spacing
            self.canvas.create_arc((center_x-radius,center_y-radius),(center_x+radius,center_y+radius),width=1,start=0,extent=180,style=ctk.ARC,dash=dash if dash==True else ())


    def click_handler(self,event):
        print(f"{event.x},{event.y}")

if __name__ == "__main__":
    app = App()
    app.mainloop()