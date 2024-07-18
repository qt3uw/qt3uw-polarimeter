import customtkinter as ctk
import tkinter as tk
from GUItester import guitester
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import time
from scraptest import tester
from Visualization import PolarimeterVisualization

class Redirect:
    def __init__(self, root):
        self.widget = root

    def write(self, string):
        self.widget.insert(ctk.END, string)
        self.widget.see(ctk.END)  

# class MyApp(tk.Frame):
    
#     def __init__(self, root):

#         super().__init__(
#             root,
#             bg='black'
#         )

#         self.main_frame = self
#         self.main_frame.pack(fill=tk.BOTH, expand = True)
#         self.main_frame.columnconfigure(0, weight = 1)
#         self.main_frame.rowconfigure(0, weight = 1)

#     def create_widgets(self):

#         self.label_gif1 = ctk.CTkLabel(
#             self.main_frame,
#             bg = 'black',
#             borer=0,
#             highlightthickness=0
#         )

#         self.button = ctk.CTkButton(
#             self.main_frame,
#             text='button',
#             width = 10,
#             height = 2 
#         )

#         root = tk.Tk()
#         root.title('My app')
#         root.geometry('800x500')
#         root.resizable(width=False,height=False)
#         my_app_instance = MyApp(root)
#         root.mainloop()


#         self.button.grid(column=0, row=1)

#         self.label_gif1.grid(column=0, row=0)
#         self.gif_frames = app._get_frames('C:\\Users\\alope\\Desktop\\qt3uw-polarimeter\\src\\animated.gif')
        
#         self._play_gif(self.label_gif1, self.gif_frames)

#         # root.after(100, self._play_gif, self.label_gif1, self.gif_frames)


#     def _get_frames(self, img):
#         with Image.open(img) as gif:
#             index = 0
#             frames = []
#             while True:
#                 try:
#                     gif.seek(index)
#                     frame = ImageTk.PhotoImage(gif)
#                     frames.append(frame)
#                 except EOFError:
#                     break

#                 index += 1
            
#             return frames 
        
#     def _play_gif(self, label, frames):

#         for frame in frames:
#             label.config(
#                 image = frame
#             )
#             time.sleep(.05)

#     def _play_gif(self, label, frames):

#         total_delay = 50
#         delay_frames = 100
#         for frame in frames:
#             root.after(total_delay, self._next_frame, frame, label)
#             total_delay += delay_frames
    
#     def _next_frame(self, frame, label):
#         label.config(
#             image=frame
#         )


gui = guitester()
t = tester()
# gui.visualization()

# Create root window
window = ctk.CTk()
# app = MyApp(root = tk.Tk())

window.title('Polarimeter app')
window.geometry('800x500')
ctk.set_appearance_mode('dark')

label = ctk.CTkLabel(
    window, 
    text = 'ACTIONS', 
    height=50,
    width=200,
    fg_color = 'transparent',
    text_color = ('black', 'white'))

label.place(x=50, y=50)


initbutton = ctk.CTkButton(window, 
                       text = 'Initialize Hardware', 
                       fg_color = 'light blue', 
                       text_color = 'black', 
                       height=50,
                       width=200,
                       command = gui.Initialize_hardware,
                    #    command = t.init_hardware,
                       corner_radius=50)
initbutton.place(x=50,y=100)


flucbutton = ctk.CTkButton(window,
                           text = 'laser fluctuation',
                           fg_color = 'light blue', 
                           text_color = 'black', 
                           height=50,
                           width=200,
                           command = gui.measurerange,
                        #    command = t.measurelaser,
                           corner_radius=50)
flucbutton.place(x=50, y=300)

calibrationbutton = ctk.CTkButton(window,
                                  text = 'QWP Calibration',
                                  fg_color = 'light blue',
                                  text_color = 'black',
                                  height = 50,
                                  width = 200,
                                  command = print("this button works"),
                                  corner_radius=50)

calibrationbutton.place(x=50,y=400)


runbutton = ctk.CTkButton(window,
                          text = 'Measure POL State',
                          fg_color = 'light blue', 
                          text_color = 'black', 
                          height=50,
                          width=200,
                          command = gui.run_polarimeter,
                        #   command = t.run_p,
                          corner_radius=50
                          )

runbutton.place(x=50, y=200)



textarea = ctk.CTkTextbox(window, width = 500, height = 200, fg_color = "#2e2e2e", text_color ='white')
textarea.place(x= 300, y = 300)


# Animation is broken

# ctk.CTkButton(window, text = "Plot", command = gui.visualization).pack(pady = 10)





sys.stdout = Redirect(textarea)

window.mainloop()
sys.stdout = sys.__stdout__
