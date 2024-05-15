import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import os
import warnings
import cv2
import numpy as np

'''
%%%%%%%%% CONSTANTS %%%%%%%%%
'''
ROTATION_ANGLE = 0
ZOOM_FACTOR = 1.0
offSetA = int(120*ZOOM_FACTOR)
offSetB = int(216*ZOOM_FACTOR)
radiusPot = int(96*ZOOM_FACTOR)
radiusROI = int(80*ZOOM_FACTOR)
offSetX = 0
offSetY = 0
centerTray = [320, 240]

IMAGE = np.ones((1280, 960, 3), np.uint8) * 255
IMAGE_MASK = np.ones((1280, 960, 3), np.uint8) * 255
IMAGE_POT_1 = np.ones((200, 200, 3), np.uint8) * 255
IMAGE_POT_2 = np.ones((200, 200, 3), np.uint8) * 255
IMAGE_POT_3 = np.ones((200, 200, 3), np.uint8) * 255
IMAGE_POT_4 = np.ones((200, 200, 3), np.uint8) * 255
IMAGE_POT_5 = np.ones((200, 200, 3), np.uint8) * 255
IMAGE_POT_6 = np.ones((200, 200, 3), np.uint8) * 255

'''
%%%%%%%%% FUNCTIONS %%%%%%%%%
'''
def open_file():
    file_path = tk.filedialog.askopenfilename(title="Open Image File")
    # check if the file is a valid image file
    if not file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
        # show a warning message in a popup window if the file is not a valid image file
        warnings.warn(f"Invalid image file {file_path}")
        messagebox.showwarning("Invalid Image File", f"Invalid image file {file_path}")
        return
    else:
        ent_path.delete(0, tk.END)
        ent_path.insert(tk.END, file_path)

def load_image():
    global IMAGE
    global IMAGE_MASK
    image_path = ent_path.get()
    if not os.path.exists(image_path):
        warnings.warn(f"Image path {image_path} does not exist.")
        messagebox.showwarning("Invalid Image Path", f"Image path {image_path} does not exist.")
        return
    # load the image
    image = cv2.imread(image_path)
    # convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # change the image to landscape mode
    if image.shape[0] > image.shape[1]:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    # resize the image to 1280x960
    image = cv2.resize(image, (1280, 960))
    IMAGE = image
    IMAGE_MASK = IMAGE.copy()

def display_image(image):
    # make a copy of the image to display
    image_display = image.copy()
    # resize the image to fit the window
    image_display = cv2.resize(image_display, (640, 480))
    # draw the tray on the image
    image_display = drawTray(image_display)
    # convert the image to PIL format
    image_display = Image.fromarray(image_display)
    # create a PhotoImage object from the image
    image_display = ImageTk.PhotoImage(image_display)
    # configure the label to display the image
    lbl_trayImage.config(image=image_display)
    lbl_trayImage.image = image_display

def display_pot_images(image):
    image_display = image.copy()
    #image_display = cv2.resize(image_display, (1280, 960))
    #image_display = rotate_image(image_display)
    centerpots = locate_pots()
    pot1 = split_pots(image_display, centerpots[0])
    pot2 = split_pots(image_display, centerpots[1])
    pot3 = split_pots(image_display, centerpots[2])
    pot4 = split_pots(image_display, centerpots[3])
    pot5 = split_pots(image_display, centerpots[4])
    pot6 = split_pots(image_display, centerpots[5])
    # convert the image to PIL format
    if showPots.get() == "upper":
        # resize the image to fit the window
        imagePot_display1 = cv2.resize(pot1, (200, 200))
        imagePot_display2 = cv2.resize(pot2, (200, 200))
        imagePot_display3 = cv2.resize(pot3, (200, 200))
        imagePot_display1 = Image.fromarray(imagePot_display1)
        imagePot_display2 = Image.fromarray(imagePot_display2)
        imagePot_display3 = Image.fromarray(imagePot_display3)
    else:
        imagePot_display1 = cv2.resize(pot4, (200, 200))
        imagePot_display2 = cv2.resize(pot5, (200, 200))
        imagePot_display3 = cv2.resize(pot6, (200, 200))
        imagePot_display1 = Image.fromarray(imagePot_display1)
        imagePot_display2 = Image.fromarray(imagePot_display2)
        imagePot_display3 = Image.fromarray(imagePot_display3)
    # create a PhotoImage object from the image
    imagePot_display1 = ImageTk.PhotoImage(imagePot_display1)
    imagePot_display2 = ImageTk.PhotoImage(imagePot_display2)
    imagePot_display3 = ImageTk.PhotoImage(imagePot_display3)
    # configure the label to display the image
    lbl_potImage1.config(image=imagePot_display1)
    lbl_potImage2.config(image=imagePot_display2)
    lbl_potImage3.config(image=imagePot_display3)
    lbl_potImage1.image = imagePot_display1
    lbl_potImage2.image = imagePot_display2
    lbl_potImage3.image = imagePot_display3
    return

def load_and_display_image():
    load_image()
    display_image(IMAGE)
    display_pot_images(IMAGE)

def rotate_image(image):
    global ROTATION_ANGLE
    # rotate the image
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), ROTATION_ANGLE, 1)
    rotate_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotate_image

def rotate_cw():
    global ROTATION_ANGLE
    ROTATION_ANGLE -= 1
    rotated_image = rotate_image(IMAGE)
    display_image(rotated_image)
    display_pot_images(rotated_image)

def rotate_ccw():
    global ROTATION_ANGLE
    ROTATION_ANGLE += 1
    rotated_image = rotate_image(IMAGE)
    display_image(rotated_image)
    display_pot_images(rotated_image)

def zoom_in():
    global ZOOM_FACTOR
    global IMAGE
    global IMAGE_MASK
    ZOOM_FACTOR -= 0.05
    if ZOOM_FACTOR < 0.5:
        ZOOM_FACTOR = 0.5
    rescale()
    rotated_image = rotate_image(IMAGE)
    display_image(rotated_image)
    rotated_image_mask = rotate_image(IMAGE_MASK)
    display_pot_images(rotated_image_mask)

def zoom_out():
    global ZOOM_FACTOR
    global IMAGE
    global IMAGE_MASK
    ZOOM_FACTOR += 0.05
    rescale()
    rotated_image = rotate_image(IMAGE)
    display_image(rotated_image)
    rotated_image_mask = rotate_image(IMAGE_MASK)
    display_pot_images(rotated_image_mask)

def move_left():
    global offSetX
    offSetX -= 2
    reposition()
    rotated_image = rotate_image(IMAGE)
    display_image(rotated_image)
    display_pot_images(rotated_image)

def move_right():
    global offSetX
    offSetX += 2
    reposition()
    rotated_image = rotate_image(IMAGE)
    display_image(rotated_image)
    display_pot_images(rotated_image)

def move_up():
    global offSetY
    offSetY -= 2
    reposition()
    rotated_image = rotate_image(IMAGE)
    display_image(rotated_image)
    display_pot_images(rotated_image)

def move_down():
    global offSetY
    offSetY += 2
    reposition()
    rotated_image = rotate_image(IMAGE)
    display_image(rotated_image)
    display_pot_images(rotated_image)

def switch_display():
    rotated_image = rotate_image(IMAGE_MASK)
    display_pot_images(rotated_image)

def check_range(channel):
    if channel == "A" or channel == "ALL":
        # check the channel A range
        channelA_min = sclA_value_min.get()
        channelA_max = sclA_value_max.get()
        if channelA_min >= channelA_max:
            warnings.warn("Invalid channel A range.")
            messagebox.showwarning("Invalid Channel A Range", "Invalid channel A range.")
            return False
    if channel == "H" or channel == "ALL":
        # check the channel H range
        channelH_min = sclH_value_min.get()
        channelH_max = sclH_value_max.get()
        if channelH_min >= channelH_max:
            warnings.warn("Invalid channel H range.")
            messagebox.showwarning("Invalid Channel H Range", "Invalid channel H range.")
            return False
    if channel == "V" or channel == "ALL":
        # check the channel V range
        channelV_min = sclV_value_min.get()
        channelV_max = sclV_value_max.get()
        if channelV_min >= channelV_max:
            warnings.warn("Invalid channel V range.")
            messagebox.showwarning("Invalid Channel V Range", "Invalid channel V range.")
            return False
    return True

def analyze_image():
    if not check_range("ALL"):
        return
    
    global IMAGE
    global IMAGE_MASK
    global IMAGE_POT_1
    global IMAGE_POT_2
    global IMAGE_POT_3
    global IMAGE_POT_4
    global IMAGE_POT_5
    global IMAGE_POT_6
    # get the channel A parameters
    use_channelA = checkbntA_value.get()
    if use_channelA==1:
        channelA_min = sclA_value_min.get()
        channelA_max = sclA_value_max.get()
    else:
        channelA_min = 0
        channelA_max = 255
    # get the channel H parameters
    use_channelH = checkbntH_value.get()
    if use_channelH==1:
        channelH_min = sclH_value_min.get()
        channelH_max = sclH_value_max.get()
    else:
        channelH_min = 0
        channelH_max = 255
    # get the channel V parameters
    use_channelV = checkbntV_value.get()
    if use_channelV==1:
        channelV_min = sclV_value_min.get()
        channelV_max = sclV_value_max.get()
    else:
        channelV_min = 0
        channelV_max = 255
    # get the kernel size
    kernel_size = kernelSize.get()
    # apply the filters
    image = IMAGE.copy()
    # apply median blur
    #image = cv2.medianBlur(image, kernel_size)
    # plot a contrl image in a new window
    #cv2.imshow("Control Image", image)
    # apply the threshold
    channelA = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)[:, :, 1] #all row, col, 2.channel
    channelA = cv2.inRange(channelA, channelA_min, channelA_max)
    channelH = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)[:, :, 0]
    channelH = cv2.inRange(channelH, channelH_min, channelH_max)
    channelV = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)[:, :, 2]
    channelV = cv2.inRange(channelV, channelV_min, channelV_max)
    # apply erdoe
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    channelA = cv2.erode(channelA, kernel, iterations=1)
    channelH = cv2.erode(channelH, kernel, iterations=1)
    # combine the channels
    image = cv2.bitwise_or(channelA, channelH)
    image = cv2.bitwise_and(image, channelV)
    # apply closing
    image = cv2.dilate(image, kernel, iterations=2)
    image = cv2.erode(image, kernel, iterations=3)
    image = cv2.dilate(image, kernel, iterations=3)
    # convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    IMAGE_MASK = image.copy()
    rotated_image = rotate_image(IMAGE)
    rotated_image_mask = rotate_image(IMAGE_MASK)
    display_image(rotated_image)
    display_pot_images(rotated_image_mask)

def rescale():
    global offSetA
    global offSetB
    global radiusPot
    global radiusROI
    global centerTray
    global ZOOM_FACTOR
    offSetA = int(90*ZOOM_FACTOR)
    offSetB = int(162*ZOOM_FACTOR)
    radiusPot = int(72*ZOOM_FACTOR)
    radiusROI = int(60*ZOOM_FACTOR)
    #check boundries
    if centerTray[0] + radiusPot + offSetB > 640:
        ZOOM_FACTOR -= 0.05
        rescale()
    if centerTray[0] - radiusPot - offSetB < 0:
        ZOOM_FACTOR -= 0.05
        rescale()
    if centerTray[1] + radiusPot + offSetA > 480:
        ZOOM_FACTOR -= 0.05
        rescale()
    if centerTray[1] - radiusPot - offSetA < 0:
        ZOOM_FACTOR -= 0.05
        rescale()

def reposition():
    global offSetX
    global offSetY
    global centerTray
    centerTray[0] = 320 + offSetX
    centerTray[1] = 240 + offSetY
    # check upper boundries
    if centerTray[0] + radiusPot + offSetB > 640:
        centerTray[0] = 640 - radiusPot - offSetB
    if centerTray[0] - radiusPot - offSetB < 0:
        centerTray[0] = 0 + radiusPot + offSetB
    if centerTray[1] + radiusPot + offSetA > 480:
        centerTray[1] = 480 - radiusPot - offSetA
    if centerTray[1] - radiusPot - offSetA < 0:
        centerTray[1] = 0 + radiusPot + offSetA


def drawTray(ImageWithoutTray):
    global offSetA
    global offSetB
    global radiusPot
    global centerTray
    x = centerTray[0]
    y = centerTray[1]
    ImageWithTray = ImageWithoutTray.copy()
    cv2.circle(ImageWithTray, (x, y - offSetA), radiusPot, (0, 0, 255), 2)
    cv2.circle(ImageWithTray, (x + offSetB, y- offSetA), radiusPot, (0, 0, 255), 2)
    cv2.circle(ImageWithTray, (x - offSetB, y - offSetA), radiusPot, (0, 0, 255), 2)
    cv2.circle(ImageWithTray, (x, y + offSetA), radiusPot, (0, 0, 255), 2)
    cv2.circle(ImageWithTray, (x + offSetB, y + offSetA), radiusPot, (0, 0, 255), 2)
    cv2.circle(ImageWithTray, (x - offSetB, y + offSetA), radiusPot, (0, 0, 255), 2)
    # drow a cross lines in the mittel of the tray
    cv2.line(ImageWithTray, (x, 0), (x, 480), (0, 255, 0), 2)
    cv2.line(ImageWithTray, (0, y), (640, y), (0, 255, 0), 2)
    return ImageWithTray

def locate_pots():
    global centerTray
    centerpots = []
    x = centerTray[0]
    y = centerTray[1]
    centerPot2 = (x, y - offSetA)
    centerPot3 = (x + offSetB, y - offSetA)
    centerPot1 = (x - offSetB, y - offSetA)
    centerPot5 = (x, y + offSetA)
    centerPot6 = (x + offSetB, y + offSetA)
    centerPot4 = (x - offSetB, y + offSetA)
    centerpots.append(centerPot1)
    centerpots.append(centerPot2)
    centerpots.append(centerPot3)
    centerpots.append(centerPot4)
    centerpots.append(centerPot5)
    centerpots.append(centerPot6)
    return centerpots

def split_pots(image, centerPot, scale=2):
    global radiusPot
    global radiusROI
    x = centerPot[0]
    y = centerPot[1]
    x1 = (x - radiusPot) * scale
    x2 = (x + radiusPot) * scale
    y1 = (y - radiusPot) * scale
    y2 = (y + radiusPot) * scale
    potImage = image[y1:y2, x1:x2]
    mask = np.zeros_like(potImage)
    maskRadius = radiusROI*scale
    maskCenter = (potImage.shape[1]//2, potImage.shape[0]//2)
    cv2.circle(mask, maskCenter, maskRadius, (255, 255, 255), -1)
    roiImage = cv2.bitwise_and(potImage, mask)

    return roiImage

'''
%%%%%%%%% GUI %%%%%%%%%
'''


# create the main window
window = tk.Tk()
# set the window size
window.geometry("800x950")
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
| image | image | image |
| radio button |
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
ent_path.insert(tk.END, "Enter the image file path here")

btn_loadImage = tk.Button(frm_A, width=10, text="load", command=load_and_display_image)
btn_openFile = tk.Button(frm_A, width=10, text="browse", command=open_file)

ent_path.pack(side=tk.LEFT, fill="x", expand=True)
btn_loadImage.pack(side=tk.RIGHT)
btn_openFile.pack(side=tk.RIGHT, after=btn_loadImage)

frm_A.pack(side=tk.TOP, fill="x")

# frame B

frm_B = tk.Frame(window)

lbl_trayImage = tk.Label(frm_B)
#display the empty image
# create empty images (all white) to display in the label
emptyTrayImage = np.ones((480, 640, 3), np.uint8) * 255
image_display = Image.fromarray(drawTray(emptyTrayImage))
image_display = ImageTk.PhotoImage(image_display)
lbl_trayImage.config(image=image_display)

btn_rotateCW = tk.Button(frm_B, width=10, text="Rotate CW", command=rotate_cw)
btn_rotateCCW = tk.Button(frm_B, width=10, text="Rotate CCW", command=rotate_ccw)
btn_zoomIn = tk.Button(frm_B, width=10, text="Zoom In", command=zoom_in)
btn_zoomOut = tk.Button(frm_B, width=10, text="Zoom Out", command=zoom_out)
btn_moveLeft = tk.Button(frm_B, width=10, text="Move Left", command=move_left)
btn_moveRight = tk.Button(frm_B, width=10, text="Move Right", command=move_right)
btn_moveUp = tk.Button(frm_B, width=10, text="Move Up", command=move_up)
btn_moveDown = tk.Button(frm_B, width=10, text="Move Down", command=move_down)

lbl_trayImage.pack(side=tk.TOP)
btn_rotateCW.pack(side=tk.LEFT)
btn_rotateCCW.pack(side=tk.LEFT, after=btn_rotateCW)
btn_zoomIn.pack(side=tk.LEFT, after=btn_rotateCCW)
btn_zoomOut.pack(side=tk.LEFT, after=btn_zoomIn)
btn_moveRight.pack(side=tk.RIGHT)
btn_moveLeft.pack(side=tk.RIGHT, after=btn_moveRight)
btn_moveDown.pack(side=tk.RIGHT, after=btn_moveLeft)
btn_moveUp.pack(side=tk.RIGHT, after=btn_moveDown)

frm_B.pack(side=tk.TOP, fill="x")

# frame C

frm_C1 = tk.Frame(window)

lbl_potImage1 = tk.Label(frm_C1)
lbl_potImage2 = tk.Label(frm_C1)
lbl_potImage3 = tk.Label(frm_C1)

#display the empty image
emptyPotImage = np.ones((200, 200, 3), np.uint8) * 255
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

# lbl_potImage4 = tk.Label(frm_C2)
# lbl_potImage5 = tk.Label(frm_C2)
# lbl_potImage6 = tk.Label(frm_C2)

# lbl_potImage4.config(image=imagePot_display)
# lbl_potImage5.config(image=imagePot_display)
# lbl_potImage6.config(image=imagePot_display)

# lbl_potImage4.pack(side=tk.LEFT)
# lbl_potImage5.pack(side=tk.LEFT, after=lbl_potImage4)
# lbl_potImage6.pack(side=tk.LEFT, after=lbl_potImage5)

showPots = tk.StringVar()

showOption = {
    "upper pots": "upper",
    "lower pots": "lower"
}

lbl_kernelSize = tk.Label(frm_C2, text="show pots:")

lbl_kernelSize.pack(side=tk.LEFT)

for (text, value) in showOption.items():
    tk.Radiobutton(frm_C2, text=text, variable=showPots, value=value, command=switch_display).pack(side=tk.LEFT)

# select the default kernel size 3x3
showPots.set("upper")

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

scl_channelA_min = tk.Scale(frm_D, variable=sclA_value_min, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelA_min.set(0)
scl_channelA_max = tk.Scale(frm_D, variable=sclA_value_max, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelA_max.set(120)

lbl_channelA_min = tk.Label(frm_D, text="Min(default: 0)")
lbl_channelA_max = tk.Label(frm_D, text="Max(default: 120)")

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

scl_channelH_min = tk.Scale(frm_E, variable=sclH_value_min, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelH_min.set(30)
scl_channelH_max = tk.Scale(frm_E, variable=sclH_value_max ,from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelH_max.set(60)


lbl_channelH_min = tk.Label(frm_E, text="Min(default: 30)")
lbl_channelH_max = tk.Label(frm_E, text="Max(default: 60)")

cbnt_channelH.pack(side=tk.LEFT)
lbl_channelH_min.pack(side=tk.LEFT, after=cbnt_channelH)
scl_channelH_min.pack(side=tk.LEFT, after=lbl_channelH_min)
lbl_channelH_max.pack(side=tk.LEFT, after=scl_channelH_min)
scl_channelH_max.pack(side=tk.LEFT, after=lbl_channelH_max)


frm_E.pack(side=tk.TOP, fill="x")

# frame F

frm_F = tk.Frame(window)

checkbntV_value = tk.IntVar()
sclV_value_min = tk.IntVar()
sclV_value_max = tk.IntVar()

cbnt_channelV = tk.Checkbutton(frm_F, text="use Channel V",
                                    variable=checkbntV_value, onvalue=1, offvalue=0,
                                    height=1, width=20)
cbnt_channelV.select()

scl_channelV_min = tk.Scale(frm_F, variable=sclV_value_min, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
scl_channelV_min.set(50)
scl_channelV_max = tk.Scale(frm_F, variable=sclV_value_max ,from_=0, to=255, orient=tk.HORIZONTAL, length=200)
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

bnt_anlyze = tk.Button(frm_G, text="Analyze", font=("Arial",15),width=10, height=10, bd=5, relief="raised", command=analyze_image)
bnt_anlyze.pack(side=tk.RIGHT, fill="both", expand=True)

frm_G.pack(side=tk.LEFT, fill="both", expand=True)

window.mainloop()