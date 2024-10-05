from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Contact Management System")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#6666ff")

FIRSTNAME = StringVar()
EMAIL = StringVar()
AGE = StringVar()
CONTACT = StringVar()

def is_valid_phone_number(phone):
    return phone.isdigit() and len(phone) == 10

def is_valid_email(email):
    return "@" in email and "." in email

def is_valid_name(name):
    return name.isalpha()

def Database():
    conn = sqlite3.connect("contact.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, firstname TEXT, email TEXT, age TEXT, contact TEXT)")
    cursor.execute("SELECT * FROM `member` ORDER BY `firstname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
    if (
        FIRSTNAME.get() == ""
        or EMAIL.get() == ""
        or AGE.get() == ""
        or CONTACT.get() == ""
    ):
        result = tkMessageBox.showwarning(
            "", "Please Complete The Required Field", icon="warning"
        )
    elif not is_valid_phone_number(CONTACT.get()):
        result = tkMessageBox.showwarning(
            "", "Phone number should contain exactly 10 digits", icon="warning"
        )
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contact.db")
        cursor = conn.cursor()
        # Swap 'age' and 'email' assignments only during insertion
        cursor.execute("INSERT INTO `member` (firstname, email, age, contact) VALUES(?, ?, ?, ?)", (str(FIRSTNAME.get()), str(AGE.get()), str(EMAIL.get()), str(CONTACT.get())))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `firstname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        EMAIL.set("")
        AGE.set("")
        CONTACT.set("")

def UpdateData():
    if not is_valid_phone_number(CONTACT.get()):
        result = tkMessageBox.showwarning(
            "", "Phone number should contain exactly 10 digits", icon="warning"
        )
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contact.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `firstname` = ?, `email` = ?, `age` = ?, `contact` = ? WHERE `mem_id` = ?", (str(FIRSTNAME.get()), str(AGE.get()), str(EMAIL.get()), str(CONTACT.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `firstname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        EMAIL.set("")
        AGE.set("")
        CONTACT.set("")

def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents = (tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    FIRSTNAME.set("")
    EMAIL.set("")
    AGE.set("")
    CONTACT.set("")
    FIRSTNAME.set(selecteditem[1])
    EMAIL.set(selecteditem[2])
    AGE.set(selecteditem[3])
    CONTACT.set(selecteditem[4])

    UpdateWindow = Toplevel()
    UpdateWindow.title("Contact Management System")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) + 450) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)

    lbl_title = Label(FormTitle, text="Updating Contacts", font=('arial', 16), bg="orange", width=300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_email = Label(ContactForm, text="Email", font=('arial', 14), bd=5)
    lbl_email.grid(row=1, sticky=W)
    lbl_age = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
    lbl_age.grid(row=2, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
    lbl_contact.grid(row=3, sticky=W)

    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    email = Entry(ContactForm, textvariable=EMAIL, font=('arial', 14))
    email.grid(row=1, column=1)
    age = Entry(ContactForm, textvariable=AGE, font=('arial', 14))
    age.grid(row=2, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT, font=('arial', 14))
    contact.grid(row=3, column=1)

    btn_updatecon = Button(ContactForm, text="Update", width=50, command=UpdateData)
    btn_updatecon.grid(row=4, columnspan=2, pady=10)

def DeleteData():
    if not tree.selection():
        result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("contact.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    EMAIL.set("")
    AGE.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("Contact Management System")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()

    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)

    lbl_title = Label(FormTitle, text="Adding New Contacts", font=('arial', 16), bg="#66ff66", width=300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_email = Label(ContactForm, text="Email", font=('arial', 14), bd=5)
    lbl_email.grid(row=1, sticky=W)
    lbl_age = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
    lbl_age.grid(row=2, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
    lbl_contact.grid(row=3, sticky=W)

    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    email = Entry(ContactForm, textvariable=EMAIL, font=('arial', 14))
    email.grid(row=1, column=1)
    age = Entry(ContactForm, textvariable=AGE, font=('arial', 14))
    age.grid(row=2, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT, font=('arial', 14))
    contact.grid(row=3, column=1)

    btn_addcon = Button(ContactForm, text="Save", width=50, command=SubmitData)
    btn_addcon.grid(row=4, columnspan=2, pady=10)

Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500, bg="#6666ff")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="#6666ff")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

lbl_title = Label(Top, text="Contact Management System", font=('arial', 16), width=500)
lbl_title.pack(fill=X)

btn_add = Button(MidLeft, text="+ ADD NEW", bg="#66ff66", command=AddNewWindow)
btn_add.pack()
btn_delete = Button(MidRight, text="DELETE", bg="red", command=DeleteData)
btn_delete.pack(side=RIGHT)

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Firstname", "Email", "Age", "Contact"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Email', text="Email", anchor=W)
tree.heading('Age', text="Age", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=90)
tree.column('#4', stretch=NO, minwidth=0, width=120)
tree.column('#5', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

if __name__ == '__main__':
    Database()
    root.mainloop()