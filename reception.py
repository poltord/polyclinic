import sqlite3
import datetime
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import fileworker


class Reception(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        label = tk.Label(self, text="RECEPTION MENU", font=('Helvetica', 16))
        main_frame = MainFrame(self, self.controller)
        second_frame = SecondFrame(self, self.controller)
        button = tk.Button(self, text="Back", font=('Helvetica', 14), width=20, bg="#669", fg='White', bd=1,
                           command=lambda: controller.show_frame("StartPage"))

        label.grid(row=0, column=0, columnspan=2, pady=(20, 0))
        main_frame.grid(row=1, column=0, pady=25, ipady=5, padx=5, sticky='e')
        second_frame.grid(row=1, column=1, pady=25, ipady=5, padx=5, sticky='w')
        button.grid(row=2, column=0, columnspan=2, pady=(0, 10))

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
        tk.LabelFrame.__init__(self, parent, text="\t      Patient's table\t\t\t\t\t\t      Doctor's table")
        self.controller = controller

        self.trv = ttk.Treeview(self, columns=(1, 2), show='headings', height=13)
        self.trv.grid(row=0, column=0, pady=10, padx=10)
        self.trv.bind('<ButtonRelease-1>', self.patient_clicker)
        self.scroll_bar = ttk.Scrollbar(self, orient="vertical")
        self.scroll_bar.grid(row=0, column=1, sticky='ns', pady=10)
        self.scroll_bar.configure(command=self.trv.yview)
        self.trv.configure(yscrollcommand=self.scroll_bar.set)
        self.trv.heading(1, text="ID")
        self.trv.column(1, width=10)
        self.trv.heading(2, text="Full name")
        self.trv.column(2, width=200)

        self.trv2 = ttk.Treeview(self, columns=(1, 2, 3), show='headings', height=13)
        self.trv2.grid(row=0, column=2, pady=10, padx=10)
        self.scroll_bar2 = ttk.Scrollbar(self, orient="vertical")
        self.scroll_bar2.grid(row=0, column=3, sticky='ns', padx=(0, 10), pady=10)
        self.trv2.configure(yscrollcommand=self.scroll_bar2.set)
        self.scroll_bar2.configure(command=self.trv2.yview)
        self.trv2.bind('<ButtonRelease-1>', self.doctor_clicker)
        self.trv2.heading(1, text="ID")
        self.trv2.column(1, width=10)
        self.trv2.heading(2, text="Full name")
        self.trv2.column(2, width=200)
        self.trv2.heading(3, text="Speciality")
        self.trv2.column(3, width=150)
        self.update_trv()

        info_text = """To register, select a patient and doctor from the tables and click the 'Add' button."""
        info_label = tk.Label(self, text=info_text, font=("Helvetica", 10), bd=1, relief='sunken', justify="left")
        label1 = tk.Label(self, text="Patient's id:")
        label2 = tk.Label(self, text="Doctor's id:")
        self.entry1 = tk.Entry(self, width=10)
        self.entry2 = tk.Entry(self, width=10)
        button_add = tk.Button(self, text="Add", width=10, command=lambda: self.sign_up())
        button_clear = tk.Button(self, text='Clear', anchor='center', width=10, command=lambda: self.clear_fields())

        info_label.grid(row=1, column=0, columnspan=3, sticky='we', padx=10, pady=(0, 10), ipadx=10, ipady=5)
        label1.grid(row=2, column=0, sticky='w', padx=10)
        label2.grid(row=3, column=0, sticky='w', padx=10, pady=(0, 62))
        self.entry1.grid(row=2, column=0, columnspan=2, padx=(90, 0))
        self.entry2.grid(row=3, column=0, columnspan=2, padx=(90, 0), pady=(0, 62))
        button_add.grid(row=2, column=2, sticky='w', padx=10, pady=0)
        button_clear.grid(row=3, column=2, sticky='w', padx=10, pady=(0, 62))

        self.photo = tk.PhotoImage(file=r"C:\Users\kripi\Downloads\refresh.png")
        refresh_button = tk.Button(self, image=self.photo, command=lambda: self.update_trv())
        refresh_button.grid(row=2, column=2)

    def clear_fields(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)

    def doctor_clicker(self, e):
        self.entry2.delete(0, END)
        selected = self.trv2.focus()
        values = self.trv2.item(selected, 'values')
        self.entry2.insert(0, values[0])

    def patient_clicker(self, e):
        self.entry1.delete(0, END)
        selected = self.trv.focus()
        values = self.trv.item(selected, 'values')
        self.entry1.insert(0, values[0])

    def update_trv(self):
        for i in self.trv.get_children():
            self.trv.delete(i)
        for i in self.trv2.get_children():
            self.trv2.delete(i)
        con = sqlite3.connect('polyclinic.db')
        cur = con.cursor()
        for i in cur.execute('SELECT * FROM patient'):
            self.trv.insert('', 'end', values=i)
        for i in cur.execute('SELECT * FROM doctor'):
            self.trv2.insert('', 'end', values=i)

    def sign_up(self):
        con = sqlite3.connect("polyclinic.db")
        cur = con.cursor()
        try:
            # Getting a patient and doctor ids
            pid = self.entry1.get()
            plst = []
            for row in cur.execute('SELECT id FROM patient;'):
                for key in row:
                    plst.append(key)
            if int(pid) not in plst:
                raise ValueError
            did = self.entry2.get()
            dlst = []
            for row in cur.execute('SELECT id FROM doctor;'):
                for key in row:
                    dlst.append(key)
            if int(did) not in dlst:
                raise ValueError
        except ValueError:
            print('>>> Incorrect input!')
        else:
            # Setting date and time
            now = datetime.datetime.now()
            curdate = now.strftime("%d.%m.%Y, %H:%M")

            # Formation of a receipt
            for row in cur.execute('''\
                    SELECT doctor_name, doctor_speciality, appointment_cost, payroll_percentage, 
                           patient_name, patient_dob, patient_address
                    FROM doctor, patient
                    WHERE doctor.id = ? AND patient.id = ?;
                    ''', (did, pid)):
                dname, dspec, acost, pperc, pname, pdob, padr = row
                text = f"""---------------------------------------RECEIPT---------------------------------------\n
Doctor: {dname}, {dspec}. Cost: {acost}.\n
Patient: {pname}, {pdob}, {padr}.\n
Date: {curdate}\n
-------------------------------------------------------------------------------------------"""
                window = tk.Toplevel()
                label = tk.Label(window, text=text, font=("Helvetica", 10), bd=1, relief='sunken', justify="left")
                label.pack(pady=10, padx=10, ipady=10, ipadx=10)
                button = Button(window, text='Close', command=window.destroy)
                button.pack(pady=(0, 10))
                # Setting doctor salary
                salary = pperc/100*acost
                cur.execute('UPDATE doctor SET salary = ? + salary WHERE id = ?;', (round(salary, 2), did))
                con.commit()

            # Adding new receipt
            cur.execute('INSERT INTO receipt (reception_date, patient_id, doctor_id) VALUES (?,?,?)', (curdate, pid, did))
            con.commit()
            cur.close()
            con.close()


class SecondFrame(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent, text="Receipt's table", labelanchor="n")
        self.controller = controller
        self.grid_columnconfigure(2, weight=1)

        self.trv = ttk.Treeview(self, columns=(1, 2, 3, 4), show='headings', height=13)
        self.trv.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
        self.trv.bind('<ButtonRelease-1>', self.clicker)
        self.trv.bind('<Double-Button-1>', self.show_receipt)
        self.scroll_bar = ttk.Scrollbar(self, orient="vertical")
        self.scroll_bar.grid(row=0, column=3, sticky='ns', pady=10)
        self.scroll_bar.configure(command=self.trv.yview)
        self.trv.configure(yscrollcommand=self.scroll_bar.set)
        self.trv.heading(1, text="ID")
        self.trv.column(1, width=10)
        self.trv.heading(2, text="Date")
        self.trv.column(2, width=120, anchor='center')
        self.trv.heading(3, text="Patient's ID")
        self.trv.column(3, width=100, anchor='center')
        self.trv.heading(4, text="Doctor's ID")
        self.trv.column(4, width=100, anchor='center')

        self.update_trv()

        info_text = """To update/delete, select a receipt from the table and click the 'Update'/'Delete' buttons.\nDouble click to view the receipt."""
        info_label = tk.Label(self, text=info_text, font=("Helvetica", 10), bd=1, relief='sunken', justify="left")
        label1 = tk.Label(self, text="Patient's id:")
        label2 = tk.Label(self, text="Doctor's id:")
        self.entry1 = tk.Entry(self, width=10)
        self.entry2 = tk.Entry(self, width=10)
        button_update = tk.Button(self, text="Update", width=10, command=lambda: self.update_receipt())
        button_delete = tk.Button(self, text="Delete", width=10, command=lambda: self.delete_receipt())
        button_clear = tk.Button(self, text='Clear', anchor='center', width=10, command=lambda: self.clear_fields())

        info_label.grid(row=1, column=0, columnspan=3, sticky='we', padx=10, pady=(0, 10), ipadx=10, ipady=5)
        label1.grid(row=2, column=0, sticky='w', padx=10)
        label2.grid(row=3, column=0, sticky='w', padx=10)
        self.entry1.grid(row=2, column=1)
        self.entry2.grid(row=3, column=1)
        button_update.grid(row=2, column=2, sticky='w', padx=10, pady=0)
        button_delete.grid(row=3, column=2, sticky='w', padx=10, pady=0)
        button_clear.grid(row=4, column=1, padx=10, pady=10)

        self.photo = tk.PhotoImage(file=r"C:\Users\kripi\Downloads\refresh.png")
        refresh_button = tk.Button(self, image=self.photo, command=lambda: self.update_trv())
        refresh_button.grid(row=2, column=2)

    def show_receipt(self, e):
        con = sqlite3.connect('polyclinic.db')
        cur = con.cursor()

        did = self.entry2.get()
        pid = self.entry1.get()

        cur.execute(f'''\
                        SELECT doctor_name, doctor_speciality, appointment_cost, payroll_percentage, 
                               patient_name, patient_dob, patient_address, reception_date
                        FROM doctor, patient, receipt
                        WHERE doctor.id = {did} AND patient.id = {pid} AND receipt.id={self.trv.item(self.trv.selection())['values'][0]};
                        ''')
        row = cur.fetchone()
        dname, dspec, acost, pperc, pname, pdob, padr, rdate = row
        text = f"""-------------------------------------RECEIPT #{self.trv.item(self.trv.selection())['values'][0]}-------------------------------------\n
Doctor: {dname}, {dspec}. Cost: {acost}.\n
Patient: {pname}, {pdob}, {padr}.\n
Date: {rdate}\n
-------------------------------------------------------------------------------------------"""

        window = tk.Toplevel()
        label = tk.Label(window, text=text, font=("Helvetica", 10), bd=1, relief='sunken', justify="left")
        label.pack(pady=10, padx=10, ipady=10, ipadx=10)
        button = tk.Button(window, text='Close', command=window.destroy)
        button.pack(pady=(0, 10))
        cur.close()
        con.close()

    def clear_fields(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)

    def clicker(self, e):
        self.clear_fields()
        selected = self.trv.focus()
        values = self.trv.item(selected, 'values')
        self.entry1.insert(0, values[2])
        self.entry2.insert(0, values[3])

    def update_trv(self):
        for i in self.trv.get_children():
            self.trv.delete(i)
        con = sqlite3.connect('polyclinic.db')
        cur = con.cursor()
        for i in cur.execute('SELECT * FROM receipt'):
            self.trv.insert('', 'end', values=i)
        cur.close()
        con.close()

    def update_receipt(self):
        con = sqlite3.connect("polyclinic.db")
        cur = con.cursor()
        try:
            rid = self.trv.item(self.trv.selection())['values'][0]
            lst = []
            for row in cur.execute('SELECT id FROM receipt;'):
                for key in row:
                    lst.append(key)
            if int(rid) not in lst:
                raise ValueError
            if int(rid) is None:
                raise IndexError


            # Getting new doctor and patient ids
            pid = self.entry1.get()
            plst = []
            for row in cur.execute('SELECT id FROM patient;'):
                for key in row:
                    plst.append(key)
            if int(pid) not in plst:
                raise ValueError


            did = self.entry2.get()
            dlst = []
            for row in cur.execute('SELECT id FROM doctor;'):
                for key in row:
                    dlst.append(key)
            if int(did) not in dlst:
                raise ValueError
        except ValueError:
            print(">>> Incorrect input!")
        except IndexError:
            messagebox.showerror("Error!", "Select receipt to update!")
        else:
            if messagebox.askyesno("Confirm deletion!", "Are you sure?"):
                # Updating old doctor salary
                cur.execute('SELECT doctor_id FROM receipt WHERE id = ?', (rid,))
                doc_id = cur.fetchone()
                cur.execute('SELECT salary, appointment_cost, payroll_percentage FROM doctor WHERE doctor.id = ?', doc_id)
                values = cur.fetchone()
                salary, acost, pperc = values
                new_salary = salary - (pperc / 100 * acost)
                cur.execute('UPDATE doctor SET salary = ? WHERE id = ?', (new_salary, doc_id[0]))
                con.commit()

                # Setting new values in updated receipt
                now = datetime.datetime.now()
                curdate = now.strftime("%d.%m.%Y %H:%M")
                cur.execute('UPDATE receipt SET reception_date = ?, patient_id = ?, doctor_id = ? WHERE id = ?', (curdate, pid, did, rid))
                con.commit()

                # Updating new doctor salary
                for val in cur.execute('SELECT appointment_cost, payroll_percentage FROM doctor WHERE id = ?', (did, )):
                    p_perc, a_cost = val
                    salary = p_perc / 100 * a_cost
                    cur.execute('UPDATE doctor SET salary = ? + salary WHERE id = ?;', (round(salary, 2), did))
                    con.commit()
                cur.close()
                con.close()
                self.clear_fields()
                self.update_trv()

    # Function to delete patient
    def delete_receipt(self):
        con = sqlite3.connect("polyclinic.db")
        cur = con.cursor()
        try:
            # Getting receipt id to delete
            rid = self.trv.item(self.trv.selection())['values'][0]
            lst = []
            for row in cur.execute('SELECT id FROM receipt;'):
                for key in row:
                    lst.append(key)
            if int(rid) not in lst:
                raise ValueError
            if int(rid) is None:
                raise IndexError
        except ValueError:
            print('>>> Incorrect input!')
        except IndexError:
            messagebox.showerror("Error!", "Select receipt to delete!")
        else:
            if messagebox.askyesno("Confirm deletion!", "Are you sure?"):
                # Updating doctor salary
                cur.execute('SELECT doctor_id FROM receipt WHERE id = ?', (rid,))
                doc_id = cur.fetchone()
                cur.execute('SELECT salary, appointment_cost, payroll_percentage FROM doctor WHERE id = ?', doc_id)
                values = cur.fetchone()
                salary, acost, pperc = values
                new_salary = salary - (pperc / 100 * acost)
                cur.execute('UPDATE doctor SET salary = ? WHERE id = ?', (new_salary, doc_id[0]))
                con.commit()

                # Deleting receipt
                cur.execute('DELETE FROM receipt WHERE id = ?', (rid, ))
                con.commit()
                cur.close()
                con.close()
                self.clear_fields()
                self.update_trv()
