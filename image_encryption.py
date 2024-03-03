# Import necessary libraries
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image
import shutil
import mysql.connector
import threading
import os
import sys

# Define the ImageEncryptor class
class ImageEncryptor:
    def __init__(self):
        # Initialize the Tkinter window
        self.root = tk.Tk()
        self.root.geometry("500x250")
        self.root.title("Image Encryption Decryption")
        self.root.configure(bg='black')
        self.root.withdraw()

        # Initialize variables for the encryption keys and login credentials
        self.entry1 = None
        self.entry2 = None
        self.login = None
        self.u = None
        self.p = None

    # Function to encrypt an image
    def encrypt_image(self):
        # Generate the encryption key
        key = self._generate_key()
        if key is not None:
            # Open a file dialog to select the image file
            file1 = filedialog.askopenfile(mode='r', filetypes=[('jpg file', '*.jpg')])
            if file1 is not None:
                file_name = file1.name
                # Check if the image is already encrypted
                if self._is_encrypted(file_name):
                    messagebox.showerror("Error", "Selected image is already Encrypted or Corrupted.")
                else:
                    # Encrypt the image
                    self._encrypt_file(file_name, key)
            else:
                messagebox.showerror("Error", "Please Select an image")

    # Function to decrypt an image
    def decrypt_image(self):
        # Generate the decryption key
        key = self._generate_key()
        if key is not None:
            # Open a file dialog to select the image file
            file1 = filedialog.askopenfile(mode='r', filetypes=[('jpg file', '*.jpg')])
            if file1 is not None:
                file_name = file1.name
                # Check if the image is encrypted
                if self._is_encrypted(file_name):
                    # Decrypt the image
                    self._decrypt_file(file_name, key)
                else:
                    messagebox.showerror("Error", "Selected image is not encrypted.")
            else:
                messagebox.showerror("Error", "Please Select an image")
                
    # Function to check if an image is encrypted
    def _is_encrypted(self,file_name):
        try:
            # Try to open and verify the image
            img = Image.open(file_name)
            img.verify()
            return False
        except Exception:
            # If an error occurs, the image is encrypted
            return True
        

    # Function to generate an encryption/decryption key
    def _generate_key(self):
        # Get the values of the two keys from the Tkinter entries
        key1 = self.entry1.get("1.0", "end-1c")
        key2 = self.entry2.get("1.0", "end-1c")
        if key1 and key2:
            # Generate the key
            return self._generate(key1, key2)
        else:
            messagebox.showerror("Key Error", "Please enter value for key 1 and key 2!")
            return None

    # Static method to generate a key from two strings
    @staticmethod
    def _generate(key1:str, key2:str)->int:
        keys=[]
        # For each pair of characters in the two keys
        for i,j in zip(key1,key2):
            # Convert the characters to ASCII values and add them to the keys list
            keys.append(str(ord(i)))
            keys.append(str(ord(j)))
        # Join the keys list into a single string and convert it to an integer
        return int(''.join(keys))

    # Function to encrypt a file
    def _encrypt_file(self, file_name, key):
        # Define a function to encrypt a file
        def encrypt_file(file_name, key):
            try:
                # Open the file in binary mode and read its contents
                with open(file_name, 'rb') as fi:
                    image = bytearray(fi.read())
                # For each byte in the image
                for index, values in enumerate(image):
                    # XOR the byte with the key and take the modulus 256
                    image[index] = (values ^ int(key)) % 256
                # Write the encrypted image back to the file
                with open(file_name, 'wb') as fi1:
                    fi1.write(image)
                print("Saved image as : ", file_name, "and with", key, "as key")
            except Exception as e:
                print(f"An error occurred: {e}")
        # Start a new thread to encrypt the file
        encryption_thread = threading.Thread(target=encrypt_file, args=(file_name, key))
        encryption_thread.start()

        # Function to decrypt a file
    def _decrypt_file(self, file_name, key):
        # Define a function to decrypt a file
        def decrypt_file(file_name, key):
            try:
                # Get the base name of the file
                fname = os.path.basename(file_name)
                # Create a temporary file name
                file_name1 = file_name.strip(fname)+'temp.jpg'
                # Copy the file to the temporary file
                shutil.copy2(file_name, file_name1)
                # Open the temporary file in binary mode and read its contents
                with open(file_name1, 'rb') as fi:
                    image = bytearray(fi.read())
                # For each byte in the image
                for index, values in enumerate(image):
                    # XOR the byte with the key and take the modulus 256
                    image[index] = (values ^ int(key)) % 256
                # Write the decrypted image back to the temporary file
                with open(file_name1, 'wb') as fi1:
                    fi1.write(image)
                # Check if the temporary file is encrypted
                assert not self._is_encrypted(file_name1)
                # Remove the original file
                os.remove(file_name)
                # Rename the temporary file to the original file name
                os.rename(file_name1, file_name)
                print("Saved image as : ", file_name, "and using key:", key)
            except Exception as e:
                # Show an error message if the key is invalid
                messagebox.showerror("Error", "Key is Invalid.")
                # Remove the temporary file
                os.remove(file_name1)
                print(e)
                
        # Start a new thread to decrypt the file
        decryption_thread = threading.Thread(target=decrypt_file, args=(file_name, key))
        decryption_thread.start()

    # Static method to authenticate a user
    @staticmethod
    def authentication(username:str,password:str)->bool:
        if username and password:
            try:
                # Connect to the database
                db=mysql.connector.connect(
                    host="localhost",
                    user="root", #Enter User Name
                    password="", #Enter Password
                    database="" #Enter database 
                )
                cursor=db.cursor()
                # Execute a SQL query to check if the user exists in the database
                cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",(username,password))
                return cursor.fetchone() is not None
            except mysql.connector.Error as err:
                print(f"Something went wrong: {err}")
                return False

    # Function to create the main window
    def main_window(self):
        # Get the username and password from the Tkinter entries
        username = self.u.get()
        password = self.p.get()
        # Authenticate the user
        if self.authentication(username, password):
            # Destroy the login window and show the main window
            self.login.destroy()
            self.root.deiconify()
            # Create the labels and entries for the keys
            self._create_labels_and_entries()
            # Create the buttons for encryption and decryption
            self._create_buttons()
            # Start the main event loop
            self.root.mainloop()
        else:
            # Show an error message if the authentication failed
            messagebox.showerror("Authentication Error", "Incorrect username or password.")
            # Exit the program
            sys.exit(0)

    # Function to create the labels and entries for the keys
    def _create_labels_and_entries(self):
        # Create the labels and entries for the keys
        tk.Label(self.root, height=1, width=10, text='Enter the key', bg='black', fg='white').place(x=70, y=20)
        tk.Label(self.root, height=1, width=10, text='Key 1:', bg='black', fg='white').place(x=10, y=50)
        self.entry1 = tk.Text(self.root, height=1, width=10)
        self.entry1.place(x=70, y=50)
        tk.Label(self.root, height=1, width=10, text='Key 2:', bg='black', fg='white').place(x=10, y=80)
        self.entry2 = tk.Text(self.root, height=1, width=10)
        self.entry2.place(x=70, y=80)

    # Function to create the buttons for encryption and decryption
    def _create_buttons(self):
        # Create the buttons for encryption and decryption
        b1 = tk.Button(self.root, text="Encrypt", command=self.encrypt_image)
        b1.place(x=60, y=110)
        b2 = tk.Button(self.root, text="Decrypt", command=self.decrypt_image)
        b2.place(x=120, y=110)

# Main function
if __name__ == "__main__":
    # Create an instance of the ImageEncryptor class
    image_encryptor = ImageEncryptor()
    # Create the login window
    image_encryptor.login = tk.Tk()
    image_encryptor.login.geometry("500x250")
    image_encryptor.login.title("Authentication")
    image_encryptor.login.configure(bg='grey')
    # Create the labels and entries for the username and password
    tk.Label(image_encryptor.login, text="Username:", height=1, width=10, bg='grey', fg='black').place(x=10, y=50)
    image_encryptor.u = tk.Entry(image_encryptor.login, width=15)
    image_encryptor.u.place(x=100, y=50)
    tk.Label(image_encryptor.login, text="Password:", height=1, width=10, bg='grey', fg='black').place(x=10, y=80)
    image_encryptor.p = tk.Entry(image_encryptor.login, width=15, show='*')
    image_encryptor.p.place(x=100, y=80)
    # Create the login button
    b = tk.Button(image_encryptor.login, text="Login", command=image_encryptor.main_window)
    b.place(x=60, y=110)
    # Start the main event loop
    image_encryptor.login.mainloop()
