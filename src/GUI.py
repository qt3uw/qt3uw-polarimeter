import customtkinter as ctk
import tkinter as tk
from GUItester import guitester
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import time
import Plotting
import polarimeter
import DataAnalysis
import Driver


class Redirect:
    def __init__(self, root):
        self.widget = root

    def write(self, string):
        self.widget.insert(ctk.END, string)
        self.widget.see(ctk.END)  

def clear_text():
    textarea.delete("1.0", ctk.END)
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


# t = tester()
# gui.visualization()

# Create root window
# p = polarimeter.Polarimeter(14,14,14,11400540)
plotting = Plotting.plotting()
# d = Driver.driver()
window = ctk.CTk()
textarea = ctk.CTkTextbox(window, width = 500, height = 200, fg_color = "#2e2e2e", text_color ='white')
textarea.place(x= 300, y = 300)

plot_frame = ctk.CTkFrame(window)
label = ctk.CTkLabel(text = "Polarization Plot", master = plot_frame)
label.pack()


widget_frame = ctk.CTkScrollableFrame(window, width = 250 , height = 500)
widget_label = ctk.CTkLabel(text = 'ACTION', master = widget_frame)
widget_frame.place(x=0,y=0)

# widget_scrollbar =


canvas = FigureCanvasTkAgg(plotting.fig, master = plot_frame)
canvas.get_tk_widget().pack()
plot_frame.place(x = 300, y = 0)

sys.stdout = Redirect(textarea)
gui = guitester()

# app = MyApp(root = tk.Tk())

window.title('Polarimeter app')
window.geometry('800x500')
ctk.set_appearance_mode('dark')

label = ctk.CTkLabel(
    widget_frame, 
    text = 'ACTIONS', 
    height=50,
    width=200,
    fg_color = 'transparent',
    text_color = ('black', 'white'))

label.pack(pady=11)


# initbutton = ctk.CTkButton(widget_frame, 
#                        text = 'Initialize Hardware', 
#                        fg_color = 'light blue', 
#                        text_color = 'black', 
#                        height=50,
#                        width=200,
#                        command = lambda: plotting.D.p.InitializeHardware(),
#                     #    command = t.init_hardware,
#                        corner_radius=50)
# initbutton.place(x=50,y=100)

initbutton = ctk.CTkButton(widget_frame,
                           text='Initialize Hardware',
                           fg_color='light blue',
                           text_color='black',
                           height=50,
                           width=200,
                           command=lambda: plotting.D.p.InitializeHardware(),
                           corner_radius=50)
initbutton.pack(pady=15)


plotbutton = ctk.CTkButton(widget_frame,
                           text = 'update plot',
                           fg_color = 'light blue', 
                           text_color = 'black', 
                           height=50,
                           width=200,
                           command = lambda: plotting.update_plot(),
                        #    command = t.measurelaser,
                           corner_radius=50)
plotbutton.pack(pady=15)

calibrationbutton = ctk.CTkButton(widget_frame,
                                  text = 'Clear Plot',
                                  fg_color = 'light blue',
                                  text_color = 'black',
                                  height = 50,
                                  width = 200,
                                  command = lambda: plotting.clear_plot(),
                                  corner_radius=50)

calibrationbutton.pack(pady = 15)


runbutton = ctk.CTkButton(widget_frame,
                          text = 'Average Plot',
                          fg_color = 'light blue', 
                          text_color = 'black', 
                          height=50,
                          width=200,
                          command = lambda: plotting.average_plot(),
                        #   command = t.run_p,
                          corner_radius=50
                          )

runbutton.pack(pady=15)

mainbutton = ctk.CTkButton(widget_frame, 
                              text = 'Collect Data',
                              fg_color = 'light blue',
                              text_color = 'black',
                              height = 50,
                              width = 200,
                              command = lambda: plotting.D.main(),
                              corner_radius = 50)

mainbutton.pack(pady=15)

clear_text_button = ctk.CTkButton(widget_frame,
                                  text = 'Clear Text',
                                  fg_color= 'light blue',
                                  text_color='black',
                                  height=50,
                                  width=200,
                                  command=lambda:clear_text(),
                                  corner_radius=500)

clear_text_button.pack(pady=15)





# Animation is broken

# ctk.CTkButton(window, text = "Plot", command = gui.visualization).pack(pady = 10)







window.mainloop()
sys.stdout = sys.__stdout__
