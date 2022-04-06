import tkinter as tk
import database
from doctor import Doctor
from patient import Patient
from reception import Reception
import fileworker


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_width = 1300
        app_height = 650
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        self.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y) - 30}')
        self.title("Polyclinic Database")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Doctor, Patient, Reception):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    # Show a frame for the given page name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        menubar = frame.menubar(self)
        self.configure(menu=menubar)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="POLYCLINIC DATABASE", font=('Helvetica', 16), pady=10)
        label.pack(pady=(200, 0))
        button1 = tk.Button(self, text="Doctors menu", font=('Helvetica', 14), width=20, bg="#669", fg='White', bd=1,
                            command=lambda: controller.show_frame("Doctor"))
        button2 = tk.Button(self, text="Patients menu", font=('Helvetica', 14), width=20, bg="#669", fg='White', bd=1,
                            command=lambda: controller.show_frame("Patient"))
        button3 = tk.Button(self, text="Reception menu", font=('Helvetica', 14), width=20, bg="#669", fg='White', bd=1,
                            command=lambda: controller.show_frame("Reception"))
        button4 = tk.Button(self, text="Quit", font=('Helvetica', 14), width=20, bg="#669", fg='White', bd=1,
                            command=quit)
        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()

    def menubar(self, root):
        menubar = tk.Menu(root, tearoff=0)

        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu2 = tk.Menu(fileMenu, tearoff=0)

        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_cascade(label="Export as...", menu=fileMenu2)
        fileMenu2.add_command(label="*.docx", command=fileworker.export_docx)
        fileMenu2.add_command(label="*.xlsx", command=fileworker.export_xlsx)
        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=quit)
        menubar.add_command(label="Help", command=self.show_help)

        return menubar

    def show_help(self):
        text = '''Information for help'''
        window = tk.Toplevel()
        label = tk.Label(window, text=text, font=("Helvetica", 10), bd=1, relief='sunken', justify="left")
        label.pack(pady=10, padx=10, ipady=10, ipadx=10)
        button = tk.Button(window, text='Close', command=window.destroy)
        button.pack(pady=(0, 10))

if __name__ == "__main__":
    database.create_db()
    app = Application()
    app.mainloop()
