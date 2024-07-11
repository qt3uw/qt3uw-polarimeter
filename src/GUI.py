import customtkinter as ctk
import tkinter as tk
from GUItester import guitester
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
class Redirect:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(ctk.END, string)
        self.widget.see(ctk.END)  


gui = guitester()
gui.visualization()

# Create root window
window = ctk.CTk()

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
                       corner_radius=50)
initbutton.place(x=50,y=100)


flucbutton = ctk.CTkButton(window,
                           text = 'laser fluctuation',
                           fg_color = 'light blue', 
                           text_color = 'black', 
                           height=50,
                           width=200,
                           command = gui.measurerange,
                           corner_radius=50)
flucbutton.place(x=50, y=300)


runbutton = ctk.CTkButton(window,
                          text = 'Take measurements',
                          fg_color = 'light blue', 
                          text_color = 'black', 
                          height=50,
                          width=200,
                          command = gui.run_polarimeter,
                          corner_radius=50
                          )

runbutton.place(x=50, y=200)



textarea = ctk.CTkTextbox(window, width = 500, height = 200, fg_color = "#2e2e2e", text_color ='white')
textarea.place(x= 300, y = 300)


# Animation is broken

# canvas = FigureCanvasTkAgg(gui.get_figure(), window)
# canvas.draw()
# canvas.get_tk_widget().pack(fill = ctk.BOTH, expand=True)
# canvas.draw_idle()  # Use draw_idle to update the canvas only when idle

sys.stdout = Redirect(textarea)

window.mainloop()

sys.stdout = sys.__stdout__
