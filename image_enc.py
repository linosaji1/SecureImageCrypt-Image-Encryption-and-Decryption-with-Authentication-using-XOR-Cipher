import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import mysql.connector
import threading
import sys

entry1=None
entry2=None
root=tk.Tk()
root.geometry("500x250")
root.title("Image Encryption Decryption")
root.configure(bg='black')
root.withdraw()

def encrypt_image():
    global entry1, entry2
    key = None
    key1 = entry1.get("1.0", "end-1c")
    key2 = entry2.get("1.0", "end-1c")
    if key1 and key2:
        key = generate(key1, key2)
        file1 = filedialog.askopenfile(mode='r', filetypes=[('jpg file', '*.jpg')])
        if file1 is not None:
            file_name = file1.name

            def encrypt_file(file_name, key):
                fi = open(file_name, 'rb')
                image = fi.read()
                fi.close()
                image = bytearray(image)
                for index, values in enumerate(image):
                    image[index] = (values ^ int(key)) % 256
                fi1 = open(file_name, 'wb')
                fi1.write(image)
                fi1.close()

            encryption_thread = threading.Thread(target=encrypt_file, args=(file_name, key))
            encryption_thread.start()
            print("Saved image as : ", file_name, "and with", key, "as key")
        else:
            messagebox.showerror("Error", "Please Select an image")
    else:
        messagebox.showerror("Key Error", "Please enter value for key 1 and key 2!")

def decrypt_image():
    global entry1, entry2
    key = None
    key1 = entry1.get("1.0", "end-1c")
    key2 = entry2.get("1.0", "end-1c")
    if key1 and key2:
        key = generate(key1, key2)
        file1 = filedialog.askopenfile(mode='r', filetypes=[('jpg file', '*.jpg')])
        if file1 is not None:
            file_name = file1.name

            def decrypt_file(file_name, key):
                fi = open(file_name, 'rb')
                image = fi.read()
                fi.close()
                image = bytearray(image)
                for index, values in enumerate(image):
                    image[index] = (values ^ int(key)) % 256
                fi1 = open(file_name, 'wb')
                fi1.write(image)
                fi1.close()

            decryption_thread = threading.Thread(target=decrypt_file, args=(file_name, key))
            decryption_thread.start()
            print("Saved image as : ", file_name, "and using key:", key)
        else:
            messagebox.showerror("Error", "Please Select an image")
    else:
        messagebox.showerror("Key Error", "Please enter value for key 1 and key 2!")

def generate(key1:str,key2:str)->int:
    keys=[]
    for i,j in zip(key1,key2):
        if(len(str(ord(i)))>=2):
            asc=ord(i)
            while(asc!=0):
                keys.append(str(asc%10))
                asc//=10
        else:
            keys.append(str(ord(i)))
        if(len(str(ord(j)))>=2):
            asc=ord(j)
            while(asc!=0):
                keys.append(str(asc%10))
                asc//=10
        else:
            keys.append(str(ord(j)))
    return int(''.join(keys))

def authentication(username:str,password:str)->bool:
    if username and password:
        db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lino123@",
            database="auth"
        )

        cursor=db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",(username,password))
        return cursor.fetchone()
    
def main_window():
    global entry1,entry2
    username=u.get()
    password=p.get()
    if authentication(username,password):
        login.destroy()
        root.deiconify()
        lab=tk.Label(root,height=1,width=10,text='Enter the key',bg='black',fg='white')
        lab.place(x=70,y=20)
        lab=tk.Label(root,height=1,width=10,text='Key 1:',bg='black',fg='white')
        lab.place(x=10,y=50)
        entry1=tk.Text(root,height=1,width=10,)
        entry1.place(x=70,y=50)
        lab=tk.Label(root,height=1,width=10,text='Key 2:',bg='black',fg='white')
        lab.place(x=10,y=80)
        entry2=tk.Text(root,height=1,width=10,)
        entry2.place(x=70,y=80)
        b1=tk.Button(root,text="Encrypt",command=encrypt_image)
        b1.place(x=60,y=110)
        b1=tk.Button(root,text="Decrypt",command=decrypt_image)
        b1.place(x=120,y=110)
        root.mainloop()
    else:
        messagebox.showerror("Authentication Error","Incorrect username or password.")
        sys.exit(0)

if __name__ == "__main__":
    login=tk.Tk()
    login.geometry("500x250")
    login.title("Authentication")
    login.configure(bg='grey')
    tk.Label(login,text="Username:",height=1,width=10,bg='grey',fg='black').place(x=10,y=50)
    u=tk.Entry(login,width=15)
    u.place(x=100,y=50)
    tk.Label(login,text="Password:",height=1,width=10,bg='grey',fg='black').place(x=10,y=80)
    p=tk.Entry(login,width=15,show='*')
    p.place(x=100,y=80)
    b=tk.Button(login,text="Login",command=main_window)
    b.place(x=60,y=110)
    login.mainloop()