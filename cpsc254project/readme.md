IMPORTANT: THIS PROGRAM REQUIRES PYCRYPTODOME TO RUN
the version I used is in the project folder
run the following commands to install it 
python3 setup.py build
sudo python3 setup.py install
this worked in wsl 

to run the program on command line:
python3 FileEncryptor.py

To use the program, first press the Generate Keys button and create AES or RSA keys
if the .keys folder does not exist in the project directory it will be created (honestly I might change this later, knowing where a hidden folder is kind of defeats the purpose, but atleast I can showcase the project.)

then in the main window use the combo box to select the key you want to use for encryption/decryption

on the left side of the screen either drag and drop files or select the button to open the file explorer and select the file from there
after that press the encrypt button to generate a .enc file, then press decrypt using the appropriate key in the combo box to generate a .dec file 
