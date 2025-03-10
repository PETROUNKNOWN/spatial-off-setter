import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Surround Sound")
        self.resizable(0, 0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.platform=ctk.CTkFrame(self,width=1001,height=500,border_color="red",border_width=1)
        self.platform.grid(row=0,column=0,padx=(5,3),pady=5,sticky="nsew",ipadx=5,ipady=5)
        self.platform.grid_propagate(False)
        self.platform.columnconfigure(0, weight=1)
        self.platform.rowconfigure(0, weight=1)
        self.canvas=ctk.CTkCanvas(self.platform,bg="white",width=1000,height=500)
        self.canvas.grid(row=0,column=0)
        canvasWidth=1000
        canvasHeight=500
        canvasHeightHalf=canvasHeight//2
        self.canvas.create_line(canvasHeight,0,canvasHeight,canvasHeight,fill="black",width=1)
        self.canvas.create_line(0,canvasHeight,canvasWidth,canvasHeight,fill="black",width=1)

        self.settings=ctk.CTkFrame(self,width=200,height=500,border_color="red",border_width=1)
        self.settings.grid(row=0,column=1,padx=(3,5),pady=5,sticky="nsew")
        self.settings.grid_propagate(False)
        self.settings.columnconfigure(0, weight=1)
        self.settings.rowconfigure(0, weight=1)

        

        

if __name__ == "__main__":
    app = App()
    app.mainloop()