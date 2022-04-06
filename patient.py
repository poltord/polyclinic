import sqlite3
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import fileworker


class Patient(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text="PATIENTS MENU", font=('Helvetica', 16))
        main_frame = MainFrame(self, self.controller)
        button_back = tk.Button(self, text="Back", font=('Helvetica', 14), width=20, bg="#669", fg='White', bd=1, command=lambda: controller.show_frame("StartPage"))

        label.grid(row=0, column=0, pady=(20, 0))
        main_frame.grid(row=1, column=0, pady=25, ipady=5)
        button_back.grid(row=2, column=0)

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

        self.trv = ttk.Treeview(self, columns=(1, 2, 3, 4), show='headings', height=13)
        self.trv.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
        self.trv.bind('<ButtonRelease-1>', self.clicker)
        self.scroll_bar = ttk.Scrollbar(self, orient="vertical")
        self.scroll_bar.grid(row=0, column=3, sticky='ns', padx=(0, 10), pady=10)
        self.scroll_bar.configure(command=self.trv.yview)
        self.trv.configure(yscrollcommand=self.scroll_bar.set)

        self.trv.heading(1, text="ID")
        self.trv.column(1, width=10)
        self.trv.heading(2, text="Name")
        self.trv.column(2, width=200)
        self.trv.heading(3, text="Date of birth")
        self.trv.column(3, width=100)
        self.trv.heading(4, text="Address")
        self.trv.column(4, width=300)
        self.update_trv()

        info_text = """To add a patient, fill out the form and click the 'Add' button.\nTo update/delete a patient, click on desired patient in table and click the 'Update'/'Delete' button."""
        info_label = tk.Label(self, text=info_text, font=("Helvetica", 10), bd=1, relief='sunken', justify="left")
        label1 = tk.Label(self, text="Full name:")
        label2 = tk.Label(self, text="Date of birth (DD.MM.YYYY):")
        label3 = tk.Label(self, text="Address:")
        self.entry1 = tk.Entry(self, width=40)
        self.entry2 = tk.Entry(self, width=40)
        self.entry3 = tk.Entry(self, width=40)
        button_add = tk.Button(self, text="Add", width=20, command=lambda: self.add_patient())
        button_update = tk.Button(self, text="Update", width=20, command=lambda: self.update_patient())
        button_delete = tk.Button(self, text="Delete", width=20, command=lambda: self.delete_patient())
        button_clear = tk.Button(self, text='Clear', anchor='center', width=10, command=lambda: self.clear_fields())

        info_label.grid(row=1, columnspan=3, sticky='we', padx=10, pady=(0, 10), ipadx=10, ipady=5)
        label1.grid(row=2, column=0, sticky='w', padx=10, pady=0)
        label2.grid(row=3, column=0, sticky='w', padx=10, pady=0)
        label3.grid(row=4, column=0, sticky='w', padx=10, pady=0)
        self.entry1.grid(row=2, column=1, sticky='w', padx=0, pady=0)
        self.entry2.grid(row=3, column=1, sticky='w', padx=0, pady=0)
        self.entry3.grid(row=4, column=1, sticky='w', padx=0, pady=0)
        button_add.grid(row=2, column=2, sticky='w', padx=10, pady=0)
        button_update.grid(row=3, column=2, sticky='w', padx=10, pady=0)
        button_delete.grid(row=4, column=2, sticky='w', padx=10, pady=0)
        button_clear.grid(row=5, column=1, padx=10)

    def clear_fields(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)

    def clicker(self, e):
        self.clear_fields()
        selected = self.trv.focus()
        values = self.trv.item(selected, 'values')

        self.entry1.insert(0, values[1])
        self.entry2.insert(0, values[2])
        self.entry3.insert(0, values[3])

    def update_trv(self):
        for i in self.trv.get_children():
            self.trv.delete(i)
        con = sqlite3.connect('polyclinic.db')
        cur = con.cursor()
        for i in cur.execute('SELECT * FROM patient'):
            self.trv.insert('', 'end', values=i)

    def add_patient(self):
        con = sqlite3.connect("polyclinic.db")
        cur = con.cursor()
        pname = self.entry1.get()
        pdob = self.entry2.get()
        padr = self.entry3.get()
        try:
            if pname is None or len(pname) == 0:
                raise ValueError
            if pdob > str(time.strptime(pdob, '%d.%m.%Y')):
                raise ValueError
            if padr is None or len(padr) == 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error!", "Input correct values!")
        else:
            values = (pname, pdob, padr)
            sql = """\
                INSERT INTO patient (patient_name, patient_dob, patient_address)
                VALUES (?,?,?);
            """
            cur.execute(sql, values)
            con.commit()
            cur.close()
            con.close()
            self.clear_fields()
            self.update_trv()

    def update_patient(self):
        con = sqlite3.connect("polyclinic.db")
        cur = con.cursor()
        try:
            pid = self.trv.item(self.trv.selection())['values'][0]
            pname = self.entry1.get()
            pdob = self.entry2.get()
            padr = self.entry3.get()
            if pid is None:
                raise IndexError
            lst = []
            for row in cur.execute('SELECT id FROM patient;'):
                for key in row:
                    lst.append(key)
            if pid not in lst:
                raise ValueError
            if pname is None or len(pname) == 0 or pname.isnumeric():
                raise ValueError
            if pdob > str(time.strptime(pdob, '%d.%m.%Y')):
                raise ValueError
            if padr is None or len(padr) == 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error!", "Input correct values!")
        except IndexError:
            messagebox.showerror("Error!", "Select patient to update!")
        else:
            if messagebox.askyesno("Confirm updation!", "Are you sure?"):
                values = (pname, pdob, padr, pid)
                sql = '''UPDATE patient SET
                   patient_name = ?,
                   patient_dob = ?,
                   patient_address =?
                   WHERE id = ?;
                   '''
                cur.execute(sql, values)
                con.commit()
                cur.close()
                con.close()
                self.clear_fields()
                self.update_trv()

    def delete_patient(self):
        con = sqlite3.connect("polyclinic.db")
        cur = con.cursor()
        try:
            pid = self.trv.item(self.trv.selection())['values'][0]
            if pid is None:
                raise IndexError
            lst = []
            for row in cur.execute('SELECT id FROM patient;'):
                for key in row:
                    lst.append(key)
            if pid not in lst:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error!", "Input correct values!")
        except IndexError:
            messagebox.showerror("Error!", "Select patient to delete!")
        else:
            if messagebox.askyesno("Confirm deletion!", "Are you sure?"):
                cur.execute('DELETE FROM patient WHERE id = ?', (pid, ))
                con.commit()
                cur.close()
                con.close()
                self.clear_fields()
                self.update_trv()
