import tkinter as tk
from PIL import ImageTk, Image
import os
import warnings
import cv2
import numpy as np

'''
%%%%%%%%% FUNCTIONS %%%%%%%%%
'''

'''
def open_file():
    file_path = tk.filedialog.askopenfilename(title="Open Image File")
    # check if the file is a valid image file
    if not file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
        warnings.warn(f"Invalid image file {file_path}")
        return
    else:
        ent_path.delete(0, tk.END)
        ent_path.insert(tk.END, file_path)

def load_image():
    image_path = ent_path.get()
    if not os.path.exists(image_path):
        warnings.warn(f"Image path {image_path} does not exist.")
        return
    # load the image
    image = cv2.imread(image_path)
    # convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # make a copy of the image to display
    image_display = image.copy()
    # resize the image to fit the window
    image_display = cv2.resize(image_display, (640, 480))
    # convert the image to PIL format
    image_display = Image.fromarray(image_display)
    # create a PhotoImage object from the image
    image_display = ImageTk.PhotoImage(image_display)
    # configure the label to display the image
    lbl_trayImage.config(image=image_display)
    lbl_trayImage.image = image_display
'''

# constants
ROTATION_ANGLE = 0.0
ZOOM_FACTOR = 1.0

# create empty images (all white) to display in the label
emptyTrayImage = np.ones((480, 640, 3), np.uint8) * 255
emptyPotImage = np.ones((200, 200, 3), np.uint8) * 255
#draw a blue circle in the empty tray image
offSetA = int(90*ZOOM_FACTOR)
offSetB = int(162*ZOOM_FACTOR)
radiusPot = int(72*ZOOM_FACTOR)
radiusROI = int(60*ZOOM_FACTOR)

cv2.circle(emptyTrayImage, (320, 240 - offSetA), radiusPot, (0, 0, 255), 2)
cv2.circle(emptyTrayImage, (320 + offSetB, 240-offSetA), radiusPot, (0, 0, 255), 2)
cv2.circle(emptyTrayImage, (320 - offSetB, 240-offSetA), radiusPot, (0, 0, 255), 2)
cv2.circle(emptyTrayImage, (320, 240 + offSetA), radiusPot, (0, 0, 255), 2)
cv2.circle(emptyTrayImage, (320 + offSetB, 240 + offSetA), radiusPot, (0, 0, 255), 2)
cv2.circle(emptyTrayImage, (320 - offSetB, 240 + offSetA), radiusPot, (0, 0, 255), 2)



'''
%%%%%%%%% GUI %%%%%%%%%
'''


# create the main window
window = tk.Tk()
# set the window size
window.geometry("800x1200")
# set the window size to be fixed
window.resizable(False, False)
# set the window title
window.title("Tray Image Processor")

'''
Layout:


+-----------------------------------+
frame_A: file path
| entry | button | button |
-------------------------------------
frame_B: tray image
label(tray image)
| image |
| button | button | button | button | button | button | button | button |
-------------------------------------
frame_C: pot images
| image | image | image | image | image | image |
-------------------------------------
frame_D: parameters

+-----------------------------------+


Variable Name Prefix
label -> lbl
button -> btn
frame -> frm
entry -> ent
text -> txt
'''

# frame A
frm_A = tk.Frame(window)

ent_path = tk.Entry(frm_A)
ent_path.insert(tk.END, "Copy the image file path here")

btn_loadImage = tk.Button(frm_A, width=10, text="load")
btn_openFile = tk.Button(frm_A, width=10, text="browse")

ent_path.pack(side=tk.LEFT, fill="x", expand=True)
btn_loadImage.pack(side=tk.RIGHT)
btn_openFile.pack(side=tk.RIGHT, after=btn_loadImage)

frm_A.pack(side=tk.TOP, fill="x")

# frame B

frm_B = tk.Frame(window)

lbl_trayImage = tk.Label(frm_B)
#display the empty image
image_display = Image.fromarray(emptyTrayImage)
image_display = ImageTk.PhotoImage(image_display)
lbl_trayImage.config(image=image_display)

btn_rotateCW = tk.Button(frm_B, width=10, text="Rotate CW")
btn_rotateCCW = tk.Button(frm_B, width=10, text="Rotate CCW")
btn_zoomIn = tk.Button(frm_B, width=10, text="Zoom In")
btn_zoomOut = tk.Button(frm_B, width=10, text="Zoom Out")
btn_moveLeft = tk.Button(frm_B, width=10, text="Move Left")
btn_moveRight = tk.Button(frm_B, width=10, text="Move Right")
btn_moveUp = tk.Button(frm_B, width=10, text="Move Up")
btn_moveDown = tk.Button(frm_B, width=10, text="Move Down")

lbl_trayImage.pack(side=tk.TOP)
btn_rotateCW.pack(side=tk.LEFT)
btn_rotateCCW.pack(side=tk.LEFT, after=btn_rotateCW)
btn_zoomIn.pack(side=tk.LEFT, after=btn_rotateCCW)
btn_zoomOut.pack(side=tk.LEFT, after=btn_zoomIn)
btn_moveLeft.pack(side=tk.RIGHT)
btn_moveRight.pack(side=tk.RIGHT, after=btn_moveLeft)
btn_moveUp.pack(side=tk.RIGHT, after=btn_moveRight)
btn_moveDown.pack(side=tk.RIGHT, after=btn_moveUp)

frm_B.pack(side=tk.TOP, fill="x")

# frame C

frm_C1 = tk.Frame(window)

lbl_potImage1 = tk.Label(frm_C1)
lbl_potImage2 = tk.Label(frm_C1)
lbl_potImage3 = tk.Label(frm_C1)

#display the empty image
imagePot_display = Image.fromarray(emptyPotImage)
imagePot_display = ImageTk.PhotoImage(imagePot_display)

lbl_potImage1.config(image=imagePot_display)
lbl_potImage2.config(image=imagePot_display)
lbl_potImage3.config(image=imagePot_display)

lbl_potImage1.pack(side=tk.LEFT)
lbl_potImage2.pack(side=tk.LEFT, after=lbl_potImage1)
lbl_potImage3.pack(side=tk.LEFT, after=lbl_potImage2)

frm_C1.pack(side=tk.TOP)


frm_C2 = tk.Frame(window)

lbl_potImage4 = tk.Label(frm_C2)
lbl_potImage5 = tk.Label(frm_C2)
lbl_potImage6 = tk.Label(frm_C2)

lbl_potImage4.config(image=imagePot_display)
lbl_potImage5.config(image=imagePot_display)
lbl_potImage6.config(image=imagePot_display)

lbl_potImage4.pack(side=tk.LEFT)
lbl_potImage5.pack(side=tk.LEFT, after=lbl_potImage4)
lbl_potImage6.pack(side=tk.LEFT, after=lbl_potImage5)

frm_C2.pack(side=tk.TOP)

# frame D

frm_D = tk.Frame(window)

checkbntA_value = tk.IntVar()
sclA_value_min = tk.IntVar()
sclA_value_max = tk.IntVar()


cbnt_channelA = tk.Checkbutton(frm_D, text="use Channel A",
                               variable=checkbntA_value, onvalue=1, offvalue=0,
                               height=1, width=20)
cbnt_channelA.select()

scl_channelA_min = tk.Scale(frm_D, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelA_min.set(0)
scl_channelA_max = tk.Scale(frm_D, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelA_max.set(30)

lbl_channelA_min = tk.Label(frm_D, text="Min(default: 0)")
lbl_channelA_max = tk.Label(frm_D, text="Max(default: 30)")

cbnt_channelA.pack(side=tk.LEFT)
lbl_channelA_min.pack(side=tk.LEFT, after=cbnt_channelA)
scl_channelA_min.pack(side=tk.LEFT, after=lbl_channelA_min)
lbl_channelA_max.pack(side=tk.LEFT, after=scl_channelA_min)
scl_channelA_max.pack(side=tk.LEFT, after=lbl_channelA_max)

frm_D.pack(side=tk.TOP, fill="x")

# frame E

frm_E = tk.Frame(window)

checkbntH_value = tk.IntVar()
sclH_value_min = tk.IntVar()
sclH_value_max = tk.IntVar()

cbnt_channelH = tk.Checkbutton(frm_E, text="use Channel H",
                                 variable=checkbntH_value, onvalue=1, offvalue=0,
                                 height=1, width=20)
cbnt_channelH.select()

scl_channelH_min = tk.Scale(frm_E, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelH_min.set(20)
scl_channelH_max = tk.Scale(frm_E, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelH_max.set(40)


lbl_channelH_min = tk.Label(frm_E, text="Min(default: 20)")
lbl_channelH_max = tk.Label(frm_E, text="Max(default: 40)")

cbnt_channelH.pack(side=tk.LEFT)
lbl_channelH_min.pack(side=tk.LEFT, after=cbnt_channelH)
scl_channelH_min.pack(side=tk.LEFT, after=lbl_channelH_min)
lbl_channelH_max.pack(side=tk.LEFT, after=scl_channelH_min)
scl_channelH_max.pack(side=tk.LEFT, after=lbl_channelH_max)


frm_E.pack(side=tk.TOP, fill="x")

# frame F

frm_F = tk.Frame(window)

checkbntV_value = tk.IntVar()

cbnt_channelV = tk.Checkbutton(frm_F, text="use Channel V",
                                    variable=checkbntV_value, onvalue=1, offvalue=0,
                                    height=1, width=20)
cbnt_channelV.select()

scl_channelV_min = tk.Scale(frm_F, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelV_min.set(50)
scl_channelV_max = tk.Scale(frm_F, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelV_max.set(250)


lbl_channelV_min = tk.Label(frm_F, text="Min(default: 50)")
lbl_channelV_max = tk.Label(frm_F, text="Max(default: 250)")

cbnt_channelV.pack(side=tk.LEFT)
lbl_channelV_min.pack(side=tk.LEFT, after=cbnt_channelV)
scl_channelV_min.pack(side=tk.LEFT, after=lbl_channelV_min)
lbl_channelV_max.pack(side=tk.LEFT, after=scl_channelV_min)
scl_channelV_max.pack(side=tk.LEFT, after=lbl_channelV_max)


frm_F.pack(side=tk.TOP, fill="x")

# frame G

frm_G = tk.Frame(window)

kernelSize = tk.IntVar()

kernelOption = {
    "3x3": 3,
    "5x5": 5,
    "7x7": 7,
    "9x9": 9
}

lbl_kernelSize = tk.Label(frm_G, text="Kernel Size:")

lbl_kernelSize.pack(side=tk.LEFT)

for (text, value) in kernelOption.items():
    tk.Radiobutton(frm_G, text=text, variable=kernelSize, value=value).pack(side=tk.LEFT)

# select the default kernel size 3x3
kernelSize.set(5)

bnt_anlyze = tk.Button(frm_G, text="Analyze", font=("Arial",15),width=20, height=20, bd=2, relief="raised")
bnt_anlyze.pack(side=tk.RIGHT)

frm_G.pack(side=tk.LEFT, fill="both", expand=True)

window.mainloop()