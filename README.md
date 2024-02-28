# Introduction
* The code uses Tkinter for the GUI.
* It authenticates users against a MySQL database.
* Upon successful authentication, it allows users to encrypt or decrypt images using keys provided.
* Encryption and decryption functions XOR the image bytes with the generated key to perform the operation.
* The generate function generates a key based on the input strings (key1 and key2).
* Threading is used to perform encryption/decryption operations asynchronously.

# Requirements
```
pip install mysql-connector-python
```

# How to Run
* Open a terminal or command prompt.
* Navigate to the directory where your Python script is located.
* Run the script by executing the following command:
	  *python image_enc.py
* Upon running the script, a GUI window will appear for authentication.
* Enter the username and password. This will be validated against the MySQL database.
* If the authentication succeeds, another window will appear for image encryption and decryption.
* After successful authentication, a new window will open.
* You can choose to encrypt or decrypt an image by providing keys in the respective fields and clicking on the "Encrypt" or "Decrypt" buttons.
* The encryption/decryption process will be performed on the selected image file.

  ** Make sure to replace the database credentials (host, user, password) in the code with your actual MySQL database credentials.
