from tkinter import *
import customtkinter as ct
from PIL import ImageTk, Image
from tkinter import filedialog
import webbrowser
import cv2
import shutil

icon = 'files\icon.ico'
gitimg = "files\\git.png"
openPath = ""
savePath = ""
defaultPath = "files\\cartoonIMG.jpg"

def WinProperties(win):
    win.geometry("700x550+560+240")  # place and scale
    win.title("Cartoonizer")  # name of the window
    win.resizable(False, False)  # deformation of the window
    win.iconbitmap(f'{icon}')  # icon
    ct.set_appearance_mode('dark')
    ct.set_default_color_theme('green')


def ThemeChanger(choice):
    if choice == "dark":
        ct.set_appearance_mode('dark')
        canvas.configure(background='#262626')
    if choice == "light":
        ct.set_appearance_mode('light')
        canvas.configure(background='#C8C8C8')


def Git():
    webbrowser.open('https://github.com/Nick-Vinesmoke', new=2)


def OpenFile():
    global openPath
    openPath = filedialog.askopenfilename()
    if ".jpg" in openPath or ".png" in openPath:
        print(openPath)
        canvas.delete(ALL)
        image = Image.open(f'{openPath}')
        (width, height) = image.size
        while width > 800 or height > 520 :
            image = image.resize((int(width/1.1),int(height/1.1)))
            (width, height) = image.size
        image = ImageTk.PhotoImage(image)
        canvas.create_image(800/2, 529/2, image=image)
        canvas.update(ALL)
    else:
        canvas.delete(ALL)
        error = ct.CTkLabel(master=win, text='I can\' open this file',
                    font=('Arial Rounded MT bold', 36))
        error.place(relx=0.5, rely=0.5, anchor=CENTER)
        error.after(1000, error.destroy)


def ReDrow():
    global openPath
    img = cv2.imread(f"{openPath}")    # reading image

    # Edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)

    # Cartoonization
    color = cv2.bilateralFilter(img, 6, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cv2.imwrite(defaultPath,cartoon)

    # add to canvas
    canvas.delete(ALL)
    image = Image.open(f'{defaultPath}')
    (width, height) = image.size
    while width > 800 or height > 520:
        image = image.resize((int(width / 1.1), int(height / 1.1)))
        (width, height) = image.size
    image = ImageTk.PhotoImage(image)
    canvas.create_image(800 / 2, 529 / 2, image=image)
    canvas.update(ALL)


def SaveImage():
    global savePath
    global defaultPath
    savePath = filedialog.asksaveasfilename(initialdir="files\\", filetypes = [("jpeg files", ".jpg .jpeg"),("png files", ".png")], initialfile="cartoonIMG.jpg")
    try:
        shutil.move(defaultPath, savePath)
    except:
        error = ct.CTkLabel(master=win, text='Error',font=('Arial Rounded MT bold', 36))
        error.place(relx=0.5, rely=0.5, anchor=CENTER)
        error.after(1000, error.destroy)
    else:
        shutil.move(defaultPath, savePath)
        canvas.delete(ALL)
        error = ct.CTkLabel(master=win, text='Saved',font=('Arial Rounded MT bold', 36))
        error.place(relx=0.5, rely=0.5, anchor=CENTER)
        error.after(1000, error.destroy)





win = ct.CTk()
setTheme = ct.StringVar(value="dark")

WinProperties(win)
canvas = Canvas(master=win,width=800, height=520, background='#262626', highlightthickness=0)
canvas.place(relx=0.5, rely=0.52, anchor=CENTER)
gitimage = ct.CTkImage(light_image=Image.open(gitimg),dark_image=Image.open(gitimg),size=(30, 30))
ct.CTkLabel(master=win,text = 'AI which redraw your photos in cartoon style',font=('Arial Rounded MT bold', 24)).place(relx= 0.5,rely= 0.03,anchor=CENTER)
ct.CTkButton(master=win,text = 'load image',font=('Arial Rounded MT bold', 18),command=OpenFile).place(relx= 0.2,rely= 0.1,anchor=CENTER)
ct.CTkButton(master=win,text = 'save image',font=('Arial Rounded MT bold', 18),command=SaveImage).place(relx= 0.5,rely= 0.1,anchor=CENTER)
ct.CTkButton(master=win,text = 'redraw',font=('Arial Rounded MT bold', 18),command=ReDrow).place(relx= 0.8,rely= 0.1,anchor=CENTER)
ct.CTkComboBox(master=win,values=["dark","light"],variable=setTheme,command=ThemeChanger,height = 40).place(relx= 0.186,rely= 0.95,anchor=CENTER)
ct.CTkButton(master=win,text = '',image=gitimage,font=('Arial Rounded MT bold', 18),width = 1,command=Git,corner_radius = 8).place(relx= 0.05,rely= 0.95,anchor=CENTER)

win.mainloop()
