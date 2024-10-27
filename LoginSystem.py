import customtkinter
from PIL import Image, ImageTk
import json
import hashlib
import os

database = "database.json"
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("800x800")
root.title("Simple Login System")
backArrow = customtkinter.CTkImage(light_image=Image.open("left_arrow.png"), size=(15, 15))

global initialFrame, signUpScreenFrame, loginScreenFrame, signUpSubmitFrame, loginSubmitFrame, errorFrame, registrationFrame, loginSuccessFrame
initialFrame = customtkinter.CTkFrame(root)
signUpScreenFrame = customtkinter.CTkFrame(root)
loginScreenFrame = customtkinter.CTkFrame(root)
signUpSubmitFrame = customtkinter.CTkFrame(root)
loginSubmitFrame = customtkinter.CTkFrame(root)
errorFrame = customtkinter.CTkFrame(root)
registrationFrame = customtkinter.CTkFrame(root)
loginSuccessFrame = customtkinter.CTkFrame(root)

passwordMinLength = 5
passwordMaxLength = 25
usernameMinLength = 3
usernameMaxLength = 18

#COMPLETE
def signUpScreen():
    global usernameEntry, passwordEntry, signUpScreenFrame, initialFrame

    if initialFrame is not None:
        initialFrame.destroy()

    signUpScreenFrame = customtkinter.CTkFrame(master=root, width=300, height=225)
    signUpScreenFrame.pack(expand=True)
    signUpScreenFrame.pack_propagate(False)

    label = customtkinter.CTkLabel(master=signUpScreenFrame, text="Sign up", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    usernameEntry = customtkinter.CTkEntry(master=signUpScreenFrame, placeholder_text="Username")
    usernameEntry.pack(pady=12, padx=10)

    passwordEntry = customtkinter.CTkEntry(master=signUpScreenFrame, placeholder_text="Password", show="*")
    passwordEntry.pack(pady=12, padx=10)

    submit = customtkinter.CTkButton(master=signUpScreenFrame, text="Submit", command=lambda: register(usernameEntry.get(), passwordEntry.get()))
    submit.pack(pady=12, padx=10)

    backButton = customtkinter.CTkButton(master=signUpScreenFrame, text="", image=backArrow, width=30, height=30, command=initialScreen)
    backButton.place(x=10, y=10)

#COMPLETE
def loginScreen():
    global usernameEntry, passwordEntry, loginScreenFrame, initialFrame
    if initialFrame is not None:
        initialFrame.destroy()

    loginScreenFrame = customtkinter.CTkFrame(master=root, width=300, height=275)
    loginScreenFrame.pack(expand=True)
    loginScreenFrame.pack_propagate(False)

    label = customtkinter.CTkLabel(master=loginScreenFrame, text="Login", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    usernameEntry = customtkinter.CTkEntry(master=loginScreenFrame, placeholder_text="Username")
    usernameEntry.pack(pady=12, padx=10)

    passwordEntry = customtkinter.CTkEntry(master=loginScreenFrame, placeholder_text="Password", show="*")
    passwordEntry.pack(pady=12, padx=10)

    submit = customtkinter.CTkButton(master=loginScreenFrame, text="Submit", command=lambda: loginCheck(usernameEntry.get(), passwordEntry.get()))
    submit.pack(pady=12, padx=10)

    checkbox = customtkinter.CTkCheckBox(master=loginScreenFrame, text="Remember Me")
    checkbox.pack(pady=12, padx=10)

    backButton = customtkinter.CTkButton(master=loginScreenFrame, text="", image=backArrow, width=30, height=30, command=initialScreen)
    backButton.place(x=10, y=10)

#COMPLETE
def initialScreen():
    global initialFrame, signUpScreenFrame, loginScreenFrame
    clearFrames()

    initialFrame = customtkinter.CTkFrame(master=root, width=250, height=175)
    initialFrame.pack(expand=True)
    initialFrame.pack_propagate(False)

    label = customtkinter.CTkLabel(master=initialFrame, text="Welcome", font=("Roboto", 24))
    label.pack(pady=20, padx=20)

    signUpButton = customtkinter.CTkButton(master=initialFrame, text="Sign Up", command=signUpScreen)
    signUpButton.pack(padx=20)

    loginButton = customtkinter.CTkButton(master=initialFrame, text="Login", command=loginScreen)
    loginButton.pack(pady=20, padx=20)

#COMPLETE
def errorScreen(type):
    global errorFrame
    clearFrames()
    errorFrame = customtkinter.CTkFrame(master=root, width=300, height=250)
    errorLabel = customtkinter.CTkLabel(master=errorFrame, text_color="red", font=("Roboto", 12))
    label = customtkinter.CTkLabel(master=errorFrame, font=("Roboto", 24))
    usernameEntry = customtkinter.CTkEntry(master=errorFrame, placeholder_text="Username")
    passwordEntry = customtkinter.CTkEntry(master=errorFrame, placeholder_text="Password", show="*")
    submit = customtkinter.CTkButton(master=errorFrame, text="Submit")
    backButton = customtkinter.CTkButton(master=errorFrame, text="", image=backArrow, width=30, height=30, command=initialScreen)
    checkbox = customtkinter.CTkCheckBox(master=errorFrame, text="Remember Me")

    if type == "reg:none":
        errorLabel.configure(text=f"Sign up failed! Need to input a username or password.")
        errorFrame.configure(width=325)
    elif type == "reg:user:taken":
        errorLabel.configure(text=f"Sign up failed! Username is taken!")
    elif type == "reg:pass:short":
        errorLabel.configure(text=f"Sign up failed! Password is less than {passwordMinLength} characters!")
    elif type == "reg:pass:long":
        errorLabel.configure(text=f"Sign up failed! Password is more than {passwordMaxLength} characters!")
    elif type == "reg:user:short":
        errorLabel.configure(text=f"Sign up failed! Username is less than {usernameMinLength} characters!")
    elif type == "reg:user:long":
        errorLabel.configure(text=f"Sign up failed! Username is more than {usernameMaxLength} characters!")
    elif type == "log:none":
        errorLabel.configure(text=f"Login failed! Need to input a username or password.")
        errorFrame.configure(width=325)
    elif type == "log:user:DNE":
        errorLabel.configure(text=f"Login failed! Username does not exist!")
    elif type == "log:pass:inc":
        errorLabel.configure(text=f"Login failed! Password is incorrect!")

    errorFrame.pack(expand=True)
    errorFrame.pack_propagate(False)

    if type[0:3] == "reg":
        label.configure(text="Sign up")
        submit.configure(command = lambda: register(usernameEntry.get(), passwordEntry.get()))
    elif type[0:3] == "log":
        label.configure(text="Login")
        submit.configure(command=lambda: loginCheck(usernameEntry.get(), passwordEntry.get()))

    label.pack(pady=12, padx=10)
    usernameEntry.pack(pady=12, padx=10)
    passwordEntry.pack(pady=12, padx=10)
    errorLabel.pack(padx=10)
    submit.pack(pady=12, padx=10)
    backButton.place(x=10, y=10)

    if type[0:3] == "log":
        checkbox.pack(pady=12, padx=10)

#COMPLETE
def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

#COMPLETE
def register(username, password):
    global registrationFrame
    clearFrames()
    database = loadDatabase()

    if username in database:
        errorScreen("reg:user:taken")
    else:
        if username == "" or password == "":
            errorScreen("reg:none")
        elif passwordMaxLength >= len(password) >= passwordMinLength and usernameMinLength <= len(username) <= usernameMaxLength:
            encryptedPassword = encrypt(password)
            database[username] = encryptedPassword
            saveDatabase(database)

            clearFrames()
            registrationFrame = customtkinter.CTkFrame(master=root, width=500, height=225)
            registrationFrame.pack(expand=True)
            registrationFrame.pack_propagate(False)

            label = customtkinter.CTkLabel(master=registrationFrame, text="Sign up successful! Congratulations!",
                                           font=("Roboto", 24))
            label.pack(padx=20, pady=60)

            backButton = customtkinter.CTkButton(master=registrationFrame, text="", image=backArrow, width=50,
                                                 height=30, command=initialScreen)
            backButton.pack(padx=20)
        elif len(password) < passwordMinLength:
            errorScreen("reg:pass:short")
        elif len(password) > passwordMaxLength:
            errorScreen("reg:pass:long")
        elif len(username) < usernameMinLength:
            errorScreen("reg:user:short")
        elif len(username) > usernameMaxLength:
            errorScreen("reg:user:long")

#COMPLETE
def loginCheck(username, password):
    global loginSuccessFrame
    users = loadDatabase()
    encryptedPassword = encrypt(password)
    clearFrames()
    loginSuccessFrame = customtkinter.CTkFrame(master=root, width=500, height=225)
    label = customtkinter.CTkLabel(master=loginSuccessFrame, text="Login successful! Welcome!", font=("Roboto", 24))
    backButton = customtkinter.CTkButton(master=loginSuccessFrame, text="", image=backArrow, width=50, height=30, command=initialScreen)

    if username in users and users[username] == encryptedPassword:
        loginSuccessFrame.pack(expand=True)
        loginSuccessFrame.pack_propagate(False)
        label.pack(padx=20, pady=60)
        backButton.pack(padx=20)
    elif username == "" or password == "":
        errorScreen("log:none")
    elif username not in users:
        errorScreen("log:user:DNE")
    elif users[username] != encryptedPassword:
        errorScreen("log:pass:inc")

#COMPLETE
def loadDatabase():
    if os.path.exists("database.json"):
        with open("database.json", 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("JSON file is empty or corrupted. Starting with a new database.")
                return {}
    else:
        return {}

#COMPLETE
def saveDatabase(database):
    with open("database.json", 'w') as f:
        json.dump(database, f, indent=4)

#COMPLETE
def clearFrames():
    global initialFrame, signUpScreenFrame, loginScreenFrame, errorFrame, registrationFrame, loginSuccessFrame
    errorFrame.destroy()
    registrationFrame.destroy()
    loginSuccessFrame.destroy()
    initialFrame.destroy()
    signUpScreenFrame.destroy()
    loginScreenFrame.destroy()

def changeTheme(newTheme):
    customtkinter.set_appearance_mode(newTheme)

theme = customtkinter.CTkOptionMenu(root, values=["Light", "Dark", "System"], variable=customtkinter.StringVar(value="Theme"), command=changeTheme)
theme.place(x=20, y=20)

initialScreen()
openIcon = Image.open("lock_icon.png")
iconImage = ImageTk.PhotoImage(openIcon)
root.iconphoto(True, iconImage)

root.mainloop()