import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import fileworker


class Doctor(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text="DOCTORS MENU", font=('Helvetica', 16))
        main_frame = MainFrame(self, self.controller)
        button = tk.Button(self, text="Back", font=('Helvetica', 14), width=20, bg="#669", fg='White', bd=1, command=lambda: controller.show_frame("StartPage"))

        label.grid(row=0, column=0, pady=(20, 0))
        main_frame.grid(row=1, column=0, pady=25, ipady=5)
        button.grid(row=2, column=0, pady=0)

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


class MainFrame(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=0)

        self.photo = tk.PhotoImage(file=r"C:\Users\kripi\Downloads\refresh.png")
        refresh_button = tk.Button(self, image=self.photo, command=lambda: self.update_trv())
        refresh_button.grid(row=0, column=4, padx=(0, 10))
        self.trv = ttk.Treeview(self, columns=(1, 2, 3, 4, 5, 6), show='headings', height=13)
        self.trv.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
        self.scroll_bar = ttk.Scrollbar(self, orient="vertical")
        self.scroll_bar.grid(row=0, column=3, sticky='ns', padx=(0, 10), pady=10)
        self.trv.configure(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.configure(command=self.trv.yview)
        self.trv.bind('<ButtonRelease-1>', self.clicker)

        self.trv.heading(1, text="ID")
        self.trv.column(1, width=10)
        self.trv.heading(2, text="Full name")
        self.trv.column(2, width=200)
        self.trv.heading(3, text="Speciality")
        self.trv.column(3, width=150)
        self.trv.heading(4, text="Appointment cost")
        self.trv.column(4, width=110)
        self.trv.heading(5, text="Payroll percentage")
        self.trv.column(5, width=110)
        self.trv.heading(6, text="Salary")
        self.trv.column(6, width=100)

        self.update_trv()


        info_text = """To add a doctor, fill out the form and click the 'Add' button.\nTo update/delete a doctor, click on desired doctor in table and click the 'Update'/'Delete' button."""
        info_label = tk.Label(self, text=info_text, font=("Helvetica", 10), bd=1, relief='sunken', justify="left")
        label1 = tk.Label(self, text="Full name:")
        label2 = tk.Label(self, text="Speciality:")
        label3 = tk.Label(self, text="Appointment cost:")
        label4 = tk.Label(self, text="Payroll percentage:")
        self.entry1 = tk.Entry(self)
        self.entry2 = tk.Entry(self)
        self.entry3 = tk.Entry(self)
        self.entry4 = tk.Entry(self)
        button_add = tk.Button(self, text="Add", width=20, command=lambda: self.add_doctor())
        button_update = tk.Button(self, text="Update", width=20, command=lambda: self.update_doctor())
        button_delete = tk.Button(self, text="Delete", width=20, command=lambda: self.delete_doctor())
        button_clear = tk.Button(self, text='Clear', width=20, command=lambda: self.clear_fields())

        self.entry1.grid(row=2, column=1, sticky='w', padx=0, pady=0)
        self.entry2.grid(row=3, column=1, sticky='w', padx=0, pady=0)
        self.entry3.grid(row=4, column=1, sticky='w', padx=0, pady=0)
        self.entry4.grid(row=5, column=1, sticky='w', padx=0, pady=0)
        info_label.grid(row=1, columnspan=3, sticky='we', padx=10, pady=(0, 10), ipadx=10, ipady=5)
        label1.grid(row=2, column=0, sticky='w', padx=10, pady=0)
        label2.grid(row=3, column=0, sticky='w', padx=10, pady=0)
        label3.grid(row=4, column=0, sticky='w', padx=10, pady=0)
        label4.grid(row=5, column=0, sticky='w', padx=10, pady=0)
        button_add.grid(row=2, column=2, sticky='w', padx=10, pady=0)
        button_update.grid(row=3, column=2, sticky='w', padx=10, pady=0)
        button_delete.grid(row=4, column=2, sticky='w', padx=10, pady=0)
        button_clear.grid(row=5, column=2, sticky='w',padx=10)

    def clear_fields(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)

    def clicker(self, e):
        self.clear_fields()
        selected = self.trv.focus()
        values = self.trv.item(selected, 'values')

        self.entry1.insert(0, values[1])
        self.entry2.insert(0, values[2])
        self.entry3.insert(0, values[3])
        self.entry4.insert(0, values[4])

    def update_trv(self):
        for i in self.trv.get_children():
            self.trv.delete(i)
        con = sqlite3.connect('polyclinic.db')
        cur = con.cursor()
        for i in cur.execute('SELECT * FROM doctor'):
            self.trv.insert('', 'end', values=i)

    def add_doctor(self):
        con = sqlite3.connect("polyclinic.db")
        cur = con.cursor()
        dname = self.entry1.get()
        dspec = self.entry2.get()
        acost = self.entry3.get()
        perc = self.entry4.get()

        try:
            if dname is None or len(dname) == 0 or dname.isnumeric():
                raise ValueError
            if dspec is None or len(dspec) == 0 or dspec.isnumeric():
                raise ValueError
            if int(acost) < 0:
                raise ValueError
            if int(perc) < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error!", "Input correct values!")
        else:
            values = (dname, dspec, acost, perc)
            sql = """\
                   INSERT INTO doctor (doctor_name, doctor_speciality, appointment_cost, payroll_percentage)
                   VALUES (?,?,?,?);
               """
            cur.execute(sql, values)
            con.commit()
            cur.close()
            con.close()
            self.clear_fields()
            self.update_trv()

    def update_doctor(self):
        con = sqlite3.connect("polyclinic.db")
        cur = con.cursor()
        try:
            did = self.trv.item(self.trv.selection())['values'][0]
            dname = self.entry1.get()
            dspec = self.entry2.get()
            acost = self.entry3.get()
            perc = self.entry4.get()

            if did is None:
                raise IndexError
            if dname is None or len(dname) == 0 or dname.isnumeric():
                raise ValueError
            if dspec is None or len(dspec) == 0 or dname.isnumeric():
                raise ValueError
            if int(acost) < 0:
                raise ValueError
            if int(perc) < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error!", "Input correct values!")
        except IndexError:
            messagebox.showerror("Error!", "Select doctor to update!")
        else:
            if messagebox.askyesno("Confirm updation!", "Are you sure?"):
                cur.execute('UPDATE doctor SET doctor_name = ?, doctor_speciality = ?, appointment_cost = ?, payroll_percentage = ? WHERE id = ?;', (dname, dspec, acost, perc, did))
                con.commit()
                cur.close()
                con.close()
                self.clear_fields()
                self.update_trv()

    def delete_doctor(self):
        con = sqlite3.connect("polyclinic.db")
        cur = con.cursor()
        try:
            did = self.trv.item(self.trv.selection())['values'][0]
            lst = []
            for row in cur.execute('SELECT id FROM doctor;'):
                for key in row:
                    lst.append(key)
            if int(did) not in lst:
                raise ValueError
            if did is None:
                raise IndexError
        except ValueError:
            messagebox.showerror("Error!", "No such doctor!")
        except IndexError:
            messagebox.showerror("Error!", "Select doctor to delete!")
        else:
            if messagebox.askyesno("Confirm deleting!", "Are you sure?"):
                cur.execute('DELETE FROM receipt WHERE doctor_id = ?', (did,))
                con.commit()
                cur.execute('DELETE FROM doctor WHERE id = ?', (did,))
                con.commit()
                cur.close()
                con.close()
                self.clear_fields()
                self.update_trv()
