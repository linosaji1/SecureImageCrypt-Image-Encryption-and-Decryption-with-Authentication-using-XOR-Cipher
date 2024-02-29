import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import mysql.connector
import threading
import sys
import os

class ImageEncryptor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x250")
        self.root.title("Image Encryption Decryption")
        self.root.configure(bg='black')
        self.root.withdraw()
        self.entry1 = None
        self.entry2 = None
        self.login = None
        self.u = None
        self.p = None

    def encrypt_image(self):
        key = self._generate_key()
        if key is not None:
            file1 = filedialog.askopenfile(mode='r', filetypes=[('jpg file', '*.jpg')])
            if file1 is not None:
                file_name = file1.name
                if self._is_encrypted(file_name):
                    messagebox.showerror("Error", "Selected image is already encrypted.")
                else:
                    self._encrypt_file(file_name, key)
            else:
                messagebox.showerror("Error", "Please Select an image")

    def decrypt_image(self):
        key = self._generate_key()
        if key is not None:
            file1 = filedialog.askopenfile(mode='r', filetypes=[('jpg file', '*.jpg')])
            if file1 is not None:
                file_name = file1.name
                self._decrypt_file(file_name, key)
            else:
                messagebox.showerror("Error", "Please Select an image")

    def _is_encrypted(self, file_name):
        with open(file_name, 'rb') as fi:
            header = fi.read(10)
            return header == b'ENCRYPTED\n'

    def _generate_key(self):
        key1 = self.entry1.get("1.0", "end-1c")
        key2 = self.entry2.get("1.0", "end-1c")
        if key1 and key2:
            return self._generate(key1, key2)
        else:
            messagebox.showerror("Key Error", "Please enter value for key 1 and key 2!")
            return None

    @staticmethod
    def _generate(key1:str, key2:str)->int:
        keys=[]
        for i,j in zip(key1,key2):
            keys.extend(ImageEncryptor._get_key(i))
            keys.extend(ImageEncryptor._get_key(j))
        return int(''.join(keys))

    @staticmethod
    def _get_key(char:str)->list:
        asc=ord(char)
        keys=[]
        while(asc!=0):
            keys.append(str(asc%10))
            asc//=10
        return keys

    def _encrypt_file(self, file_name, key):
        def encrypt_file(file_name, key):
            try:
                with open(file_name, 'rb') as fi:
                    image = bytearray(fi.read())
                for index, values in enumerate(image):
                    image[index] = (values ^ int(key)) % 256
                with open(file_name, 'wb') as fi1:
                    fi1.write(b'ENCRYPTED\n') # Write a header or metadata to identify encryption
                    fi1.write(image)
                print("Saved image as : ", file_name, "and with", key, "as key")
            except Exception as e:
                print(f"An error occurred: {e}")
        encryption_thread = threading.Thread(target=encrypt_file, args=(file_name, key))
        encryption_thread.start()

    def _decrypt_file(self, file_name, key):
        def decrypt_file(file_name, key):
            try:
                with open(file_name, 'rb') as fi:
                    # Skip the header or metadata
                    fi.seek(10)
                    image = bytearray(fi.read())
                for index, values in enumerate(image):
                    image[index] = (values ^ int(key)) % 256
                with open(file_name, 'wb') as fi1:
                    fi1.write(image)
                print("Saved image as : ", file_name, "and using key:", key)
            except Exception as e:
                print(f"An error occurred: {e}")
        decryption_thread = threading.Thread(target=decrypt_file, args=(file_name, key))
        decryption_thread.start()

    @staticmethod
    def authentication(username:str,password:str)->bool:
        if username and password:
            try:
                db=mysql.connector.connect(
                    host="localhost",
                    user="root", #Enter User Name
                    password="Lino123@", #Enter Password
                    database="auth" #Enter database 
                )
                cursor=db.cursor()
                cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",(username,password))
                return cursor.fetchone() is not None
            except mysql.connector.Error as err:
                print(f"Something went wrong: {err}")
                return False

    def main_window(self):
        username = self.u.get()
        password = self.p.get()
        if self.authentication(username, password):
            self.login.destroy()
            self.root.deiconify()
            self._create_labels_and_entries()
            self._create_buttons()
            self.root.mainloop()
        else:
            messagebox.showerror("Authentication Error", "Incorrect username or password.")
            sys.exit(0)

    def _create_labels_and_entries(self):
        tk.Label(self.root, height=1, width=10, text='Enter the key', bg='black', fg='white').place(x=70, y=20)
        tk.Label(self.root, height=1, width=10, text='Key 1:', bg='black', fg='white').place(x=10, y=50)
        self.entry1 = tk.Text(self.root, height=1, width=10)
        self.entry1.place(x=70, y=50)
        tk.Label(self.root, height=1, width=10, text='Key 2:', bg='black', fg='white').place(x=10, y=80)
        self.entry2 = tk.Text(self.root, height=1, width=10)
        self.entry2.place(x=70, y=80)

    def _create_buttons(self):
        b1 = tk.Button(self.root, text="Encrypt", command=self.encrypt_image)
        b1.place(x=60, y=110)
        b2 = tk.Button(self.root, text="Decrypt", command=self.decrypt_image)
        b2.place(x=120, y=110)

if __name__ == "__main__":
    image_encryptor = ImageEncryptor()
    image_encryptor.login = tk.Tk()
    image_encryptor.login.geometry("500x250")
    image_encryptor.login.title("Authentication")
    image_encryptor.login.configure(bg='grey')
    tk.Label(image_encryptor.login, text="Username:", height=1, width=10, bg='grey', fg='black').place(x=10, y=50)
    image_encryptor.u = tk.Entry(image_encryptor.login, width=15)
    image_encryptor.u.place(x=100, y=50)
    tk.Label(image_encryptor.login, text="Password:", height=1, width=10, bg='grey', fg='black').place(x=10, y=80)
    image_encryptor.p = tk.Entry(image_encryptor.login, width=15, show='*')
    image_encryptor.p.place(x=100, y=80)
    b = tk.Button(image_encryptor.login, text="Login", command=image_encryptor.main_window)
    b.place(x=60, y=110)
    image_encryptor.login.mainloop()
