import customtkinter as ctk
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Driver


class PolarimeterApp:
    def __init__(self):
        self.Driver = Driver.driver()
        
        # sets up window and plot frame
        self.window = ctk.CTk() 
        self.setup_plot_frame()
        
        # basic window parameters
        self.window.title('Polarimeter App')
        self.window.geometry('800x500')
        ctk.set_appearance_mode('dark')

        # sets up text and button areas 
        self.setup_textarea()
        self.setup_widget_frame()
        
        # Redirects error + output to gui
        sys.stdout = Redirect(self.textarea)
        sys.stderr = Redirect(self.textarea)
        
        # opens gui
        self.window.mainloop()

        # Reset stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


    def setup_textarea(self):
        self.textarea = ctk.CTkTextbox(self.window, width=500, height=200, fg_color="#2e2e2e", text_color='white')
        self.textarea.place(x=300, y=300)
    

    def clear_text(self):
        self.textarea.delete("1.0", ctk.END)


    def open_calibration_window(self):
        calib_window = ctk.CTkToplevel(self.window)
        calib_window.title("Calibration Instructions")
        calib_window.geometry("800x500")

        self.instructions_frame = ctk.CTkFrame(calib_window)
        self.instructions_frame.pack(pady=20, padx=20, fill='x', expand=True, anchor="n")


        # Calibration buttons
        self.setup_calibration_buttons()


        calib_window.transient(self.window)
        calib_window.lift()
    

    def setup_plot_frame(self):
        self.plot_frame = ctk.CTkFrame(self.window)
        

        self.label = ctk.CTkLabel(text="Polarization Plot", master=self.plot_frame)
        self.label.pack()
        
        self.canvas = FigureCanvasTkAgg(self.Driver.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack()

        self.plot_frame.pack(anchor = 'ne')

    

    def setup_widget_frame(self):
        self.widget_frame = ctk.CTkScrollableFrame(self.window, width=250, height=500)
        self.widget_frame.place(x=0, y=0)

        self.setup_main_buttons()
    
    def setup_calibration_buttons(self):
        instructions_label = ctk.CTkLabel(self.instructions_frame, font=("Helvetica", 12), text="CALIBRATION INSTRUCTIONS\n1. Mount horizontally aligned beam splitter or polarizer in front of laser\n2. Leave only Rotator Mount with Polarizer on System then click begin\n**After each run it will give the calibrated angle.**\nUse the polarizer\nadjustment tool to move polarizer to the calibrated angle then leave it there**\n3.Add QWP + rotator mount back and press start\n**Now you can either hardcode this value into\nthe update angle button to update this value**")
        instructions_label.pack(pady=10, anchor="n")

        buttons = [
            {'text': 'Polarizer Calibrate', 'command': lambda: print('polarizer calibration')},
            {'text': 'QWP Calibrate', 'command': lambda: print('QWP calibration')},
            {'text': 'Adjust Polarizer Position', 'command': lambda: print('polarizer rotated')},
            {'text': 'QWP Cali Adjust', 'command': lambda: print('qwp starting position adjusted')}
        ]

        for btn in buttons:
            button = ctk.CTkButton(self.instructions_frame, 
                                   text = btn['text'], 
                                   fg_color = 'light blue', 
                                   text_color = 'black', 
                                   height = 50, width = 200, 
                                   corner_radius=50, 
                                   command = btn['command']
                                   )
            button.pack(pady = 15)
        


     
    def setup_main_buttons(self):
        label = ctk.CTkLabel(self.widget_frame, text='ACTIONS', height=50, width=200, fg_color='transparent', text_color=('black', 'white'))
        label.pack(pady=11)

        buttons = [
            {'text': 'Initialize Hardware', 'command': lambda: self.Driver.InitializeHardware()},
            {'text': 'Collect Data', 'command': lambda: self.Driver.main()},
            {'text': 'Update Plot', 'command': lambda: self.Driver.update_plot(self.Driver.Ex, self.Driver.Ey)},
            {'text': 'Average Plot', 'command': lambda: self.Driver.average_plot()},
            {'text': 'Clear Plot', 'command': lambda: self.Driver.clear_plot()},
            {'text': 'Clear Text', 'command': lambda: self.clear_text()},
            {'text': 'Calibration', 'command': self.open_calibration_window}
        ]

        for btn in buttons:
            button = ctk.CTkButton(self.widget_frame, 
                                   text=btn['text'], 
                                   fg_color='light blue', 
                                   text_color='black', 
                                   height=50, 
                                   width=200, 
                                   corner_radius=50, 
                                   command=btn['command'])
            button.pack(pady=15)

    # place holder function
    def print_user_input():
        global user_input
        print(f"user input: {user_input}")

# Redirect class makes text print to gui
class Redirect:
    def __init__(self, root):
        self.widget = root
    
    def write(self, string):
        self.widget.insert(ctk.END, string)
        self.widget.see(ctk.END)



if __name__ == "__main__":
    app = PolarimeterApp()