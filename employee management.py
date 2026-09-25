import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
from PIL import Image, ImageTk


# ================= DATABASE =================

conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    emp_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL,
    photo TEXT
)
""")

# Create default login
cursor.execute(
    "SELECT * FROM users WHERE username=?",
    ("admin",)
)

if cursor.fetchone() is None:
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "1234")
    )

conn.commit()


# ================= LOGIN =================

def login():
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        login_window.destroy()
        open_employee_system()
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password"
        )


# ================= EMPLOYEE SYSTEM =================

def open_employee_system():

    root = tk.Tk()
    root.title("Employee Management System")
    root.geometry("1100x750")
    root.resizable(False, False)

    # ---------- VARIABLES ----------

    emp_id_var = tk.StringVar()
    name_var = tk.StringVar()
    dept_var = tk.StringVar()
    salary_var = tk.StringVar()

    selected_photo = tk.StringVar()

    # ---------- HEADER ----------

    header = tk.Frame(
        root,
        bg="#1f4e78",
        height=70
    )

    header.pack(fill="x")

    tk.Label(
        header,
        text="EMPLOYEE MANAGEMENT SYSTEM",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#1f4e78"
    ).pack(pady=18)


    # ---------- DASHBOARD ----------

    dashboard = tk.Frame(root)
    dashboard.pack(pady=15)

    total_emp_label = tk.Label(
        dashboard,
        text="Total Employees: 0",
        font=("Arial", 13, "bold"),
        width=25,
        relief="ridge",
        padx=10,
        pady=10
    )

    total_emp_label.grid(row=0, column=0, padx=10)

    total_dept_label = tk.Label(
        dashboard,
        text="Departments: 0",
        font=("Arial", 13, "bold"),
        width=25,
        relief="ridge",
        padx=10,
        pady=10
    )

    total_dept_label.grid(row=0, column=1, padx=10)

    avg_salary_label = tk.Label(
        dashboard,
        text="Average Salary: ₹0",
        font=("Arial", 13, "bold"),
        width=25,
        relief="ridge",
        padx=10,
        pady=10
    )

    avg_salary_label.grid(row=0, column=2, padx=10)


    # ---------- EMPLOYEE FORM ----------

    form_frame = tk.LabelFrame(
        root,
        text="Employee Details",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=15
    )

    form_frame.pack(
        padx=30,
        pady=5,
        fill="x"
    )


    # Employee ID

    tk.Label(
        form_frame,
        text="Employee ID:"
    ).grid(row=0, column=0, padx=10, pady=8)

    tk.Entry(
        form_frame,
        textvariable=emp_id_var,
        width=25
    ).grid(row=0, column=1, padx=10)


    # Name

    tk.Label(
        form_frame,
        text="Name:"
    ).grid(row=0, column=2, padx=10)

    tk.Entry(
        form_frame,
        textvariable=name_var,
        width=25
    ).grid(row=0, column=3, padx=10)


    # Department

    tk.Label(
        form_frame,
        text="Department:"
    ).grid(row=1, column=0, padx=10, pady=8)

    tk.Entry(
        form_frame,
        textvariable=dept_var,
        width=25
    ).grid(row=1, column=1, padx=10)


    # Salary

    tk.Label(
        form_frame,
        text="Salary:"
    ).grid(row=1, column=2, padx=10)

    tk.Entry(
        form_frame,
        textvariable=salary_var,
        width=25
    ).grid(row=1, column=3, padx=10)


    # ---------- PHOTO ----------

    profile_frame = tk.LabelFrame(
        root,
        text="Employee Photo",
        font=("Arial", 11, "bold"),
        padx=15,
        pady=10
    )

    profile_frame.pack(
        padx=30,
        pady=8,
        fill="x"
    )


    photo_label = tk.Label(
        profile_frame,
        text="No photo selected",
        width=20,
        height=6,
        relief="ridge"
    )

    photo_label.pack(
        side="left",
        padx=20
    )


    # ---------- PHOTO FUNCTION ----------

    def choose_photo():

        file_path = filedialog.askopenfilename(
            title="Select Employee Photo",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png")
            ]
        )

        if file_path:

            try:
                image = Image.open(file_path)

                image.thumbnail((130, 130))

                photo = ImageTk.PhotoImage(image)

                photo_label.config(
                    image=photo,
                    text=""
                )

                photo_label.image = photo

                selected_photo.set(file_path)

            except Exception:
                messagebox.showerror(
                    "Error",
                    "Unable to load image."
                )


    tk.Button(
        profile_frame,
        text="Choose Photo",
        command=choose_photo,
        width=15
    ).pack(side="left", padx=10)


    # ---------- CLEAR FUNCTION ----------

    def clear_fields():

        emp_id_var.set("")
        name_var.set("")
        dept_var.set("")
        salary_var.set("")
        selected_photo.set("")

        photo_label.config(
            image="",
            text="No photo selected"
        )

        photo_label.image = None


    # ---------- ADD EMPLOYEE ----------

    def add_employee():

        emp_id = emp_id_var.get().strip()
        name = name_var.get().strip()
        department = dept_var.get().strip()
        salary = salary_var.get().strip()
        photo = selected_photo.get()

        if not emp_id or not name or not department or not salary:

            messagebox.showwarning(
                "Missing Data",
                "Please fill all employee details."
            )

            return

        try:
            salary_value = float(salary)

            if salary_value < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Salary",
                "Enter a valid salary."
            )

            return

        try:

            cursor.execute(
                """
                INSERT INTO employees
                (emp_id, name, department, salary, photo)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    emp_id,
                    name,
                    department,
                    salary_value,
                    photo
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Employee added successfully."
            )

            clear_fields()
            show_all_employees()
            update_dashboard()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Employee ID already exists."
            )


    # ---------- SEARCH EMPLOYEE ----------

    def search_employee():

        emp_id = emp_id_var.get().strip()

        if not emp_id:

            messagebox.showwarning(
                "Search",
                "Enter Employee ID."
            )

            return

        cursor.execute(
            """
            SELECT emp_id, name, department, salary, photo
            FROM employees
            WHERE emp_id=?
            """,
            (emp_id,)
        )

        employee = cursor.fetchone()

        if employee:

            emp_id_var.set(employee[0])
            name_var.set(employee[1])
            dept_var.set(employee[2])
            salary_var.set(employee[3])

            selected_photo.set(employee[4] or "")

            # Show saved photo
            if employee[4] and os.path.exists(employee[4]):

                try:

                    image = Image.open(employee[4])
                    image.thumbnail((130, 130))

                    photo = ImageTk.PhotoImage(image)

                    photo_label.config(
                        image=photo,
                        text=""
                    )

                    photo_label.image = photo

                except:
                    photo_label.config(
                        image="",
                        text="Photo unavailable"
                    )

            else:

                photo_label.config(
                    image="",
                    text="No photo"
                )

                photo_label.image = None

        else:

            messagebox.showerror(
                "Not Found",
                "Employee not found."
            )


    # ---------- UPDATE EMPLOYEE ----------

    def update_employee():

        emp_id = emp_id_var.get().strip()
        name = name_var.get().strip()
        department = dept_var.get().strip()
        salary = salary_var.get().strip()
        photo = selected_photo.get()

        if not emp_id:

            messagebox.showwarning(
                "Update",
                "Enter Employee ID."
            )

            return

        try:
            salary_value = float(salary)
        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter valid salary."
            )

            return

        cursor.execute(
            """
            UPDATE employees
            SET name=?, department=?, salary=?, photo=?
            WHERE emp_id=?
            """,
            (
                name,
                department,
                salary_value,
                photo,
                emp_id
            )
        )

        conn.commit()

        if cursor.rowcount > 0:

            messagebox.showinfo(
                "Success",
                "Employee updated successfully."
            )

            show_all_employees()
            update_dashboard()

        else:

            messagebox.showerror(
                "Error",
                "Employee not found."
            )


    # ---------- DELETE EMPLOYEE ----------

    def delete_employee():

        emp_id = emp_id_var.get().strip()

        if not emp_id:

            messagebox.showwarning(
                "Delete",
                "Enter Employee ID."
            )

            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this employee?"
        )

        if answer:

            cursor.execute(
                "DELETE FROM employees WHERE emp_id=?",
                (emp_id,)
            )

            conn.commit()

            if cursor.rowcount > 0:

                messagebox.showinfo(
                    "Deleted",
                    "Employee deleted successfully."
                )

                clear_fields()
                show_all_employees()
                update_dashboard()

            else:

                messagebox.showerror(
                    "Error",
                    "Employee not found."
                )


    # ---------- BUTTONS ----------

    button_frame = tk.Frame(root)
    button_frame.pack(pady=8)


    tk.Button(
        button_frame,
        text="Add Employee",
        width=15,
        command=add_employee
    ).grid(row=0, column=0, padx=5)


    tk.Button(
        button_frame,
        text="Search",
        width=15,
        command=search_employee
    ).grid(row=0, column=1, padx=5)


    tk.Button(
        button_frame,
        text="Update",
        width=15,
        command=update_employee
    ).grid(row=0, column=2, padx=5)


    tk.Button(
        button_frame,
        text="Delete",
        width=15,
        command=delete_employee
    ).grid(row=0, column=3, padx=5)


    tk.Button(
        button_frame,
        text="Clear",
        width=15,
        command=clear_fields
    ).grid(row=0, column=4, padx=5)


    # ---------- SEARCH / TABLE ----------

    table_frame = tk.LabelFrame(
        root,
        text="Employee Records",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=10
    )

    table_frame.pack(
        padx=30,
        pady=5,
        fill="both",
        expand=True
    )


    columns = (
        "ID",
        "Name",
        "Department",
        "Salary"
    )


    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=6
    )


    tree.heading(
        "ID",
        text="Employee ID"
    )

    tree.heading(
        "Name",
        text="Name"
    )

    tree.heading(
        "Department",
        text="Department"
    )

    tree.heading(
        "Salary",
        text="Salary"
    )


    tree.column(
        "ID",
        width=150
    )

    tree.column(
        "Name",
        width=220
    )

    tree.column(
        "Department",
        width=220
    )

    tree.column(
        "Salary",
        width=180
    )


    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    # ---------- SHOW ALL EMPLOYEES ----------

    def show_all_employees():

        for row in tree.get_children():
            tree.delete(row)

        cursor.execute(
            """
            SELECT emp_id, name, department, salary
            FROM employees
            """
        )

        employees = cursor.fetchall()

        for employee in employees:

            tree.insert(
                "",
                "end",
                values=employee
            )


    # ---------- SELECT TABLE ROW ----------

    def select_employee(event):

        selected = tree.focus()

        if not selected:
            return

        values = tree.item(
            selected,
            "values"
        )

        if values:

            emp_id_var.set(values[0])
            name_var.set(values[1])
            dept_var.set(values[2])
            salary_var.set(values[3])

            search_employee()


    tree.bind(
        "<Double-1>",
        select_employee
    )


    # ---------- PRINT / EXPORT ----------

    def print_employee():

        emp_id = emp_id_var.get().strip()

        if not emp_id:

            messagebox.showwarning(
                "Print",
                "Enter Employee ID."
            )

            return

        cursor.execute(
            """
            SELECT emp_id, name, department, salary
            FROM employees
            WHERE emp_id=?
            """,
            (emp_id,)
        )

        employee = cursor.fetchone()

        if not employee:

            messagebox.showerror(
                "Error",
                "Employee not found."
            )

            return

        file_path = filedialog.asksaveasfilename(
            title="Save Employee Details",
            defaultextension=".txt",
            filetypes=[
                ("Text File", "*.txt")
            ]
        )

        if file_path:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "EMPLOYEE DETAILS\n"
                )

                file.write(
                    "========================\n"
                )

                file.write(
                    f"Employee ID : {employee[0]}\n"
                )

                file.write(
                    f"Name        : {employee[1]}\n"
                )

                file.write(
                    f"Department  : {employee[2]}\n"
                )

                file.write(
                    f"Salary      : ₹{employee[3]}\n"
                )

            messagebox.showinfo(
                "Success",
                "Employee details exported successfully."
            )


    # ---------- BOTTOM BUTTONS ----------

    bottom_frame = tk.Frame(root)
    bottom_frame.pack(pady=10)


    tk.Button(
        bottom_frame,
        text="Export / Print",
        width=18,
        command=print_employee
    ).grid(row=0, column=0, padx=10)


    def logout():

        answer = messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        )

        if answer:

            root.destroy()
            create_login_window()


    tk.Button(
        bottom_frame,
        text="Logout",
        width=18,
        command=logout
    ).grid(row=0, column=1, padx=10)


    # ---------- DASHBOARD UPDATE ----------

    def update_dashboard():

        cursor.execute(
            "SELECT COUNT(*) FROM employees"
        )

        total = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(DISTINCT department) FROM employees"
        )

        departments = cursor.fetchone()[0]

        cursor.execute(
            "SELECT AVG(salary) FROM employees"
        )

        average = cursor.fetchone()[0]

        if average is None:
            average = 0

        total_emp_label.config(
            text=f"Total Employees: {total}"
        )

        total_dept_label.config(
            text=f"Departments: {departments}"
        )

        avg_salary_label.config(
            text=f"Average Salary: ₹{average:.2f}"
        )


    # ---------- STARTUP ----------

    show_all_employees()
    update_dashboard()


    # ---------- CLOSE APPLICATION ----------

    def close_application():

        conn.close()
        root.destroy()


    root.protocol(
        "WM_DELETE_WINDOW",
        close_application
    )

    root.mainloop()


# ================= LOGIN WINDOW =================

def create_login_window():

    global login_window
    global username_entry
    global password_entry

    login_window = tk.Tk()

    login_window.title(
        "Employee Management System - Login"
    )

    login_window.geometry(
        "1100x550"
    )

    login_window.resizable(
        False,
        False
    )


    # ---------- HEADER ----------

    tk.Label(
        login_window,
        text="EMPLOYEE MANAGEMENT SYSTEM",
        font=("Arial", 18, "bold")
    ).pack(pady=25)


    tk.Label(
        login_window,
        text="Login",
        font=("Arial", 15)
    ).pack(pady=5)


    # ---------- USERNAME ----------

    tk.Label(
        login_window,
        text="Username"
    ).pack(pady=(20, 5))


    username_entry = tk.Entry(
        login_window,
        width=30
    )

    username_entry.pack()


    # ---------- PASSWORD ----------

    tk.Label(
        login_window,
        text="Password"
    ).pack(pady=(15, 5))


    password_entry = tk.Entry(
        login_window,
        width=30,
        show="*"
    )

    password_entry.pack()


    # ---------- LOGIN BUTTON ----------

    tk.Button(
        login_window,
        text="LOGIN",
        width=20,
        command=login
    ).pack(pady=25)


    tk.Label(
        login_window,
        text="Default Login: admin / 1234",
        font=("Arial", 9)
    ).pack()


    login_window.mainloop()


# ================= START PROGRAM =================

create_login_window()