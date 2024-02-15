# This script is used to generate random watering points for the farmbot tray.

# Import the required libraries
import os # for file operations
import cv2 # for image processing
# from matplotlib import pyplot as plt # for image display if needed
import numpy as np # for numerical operations
from plantcv import plantcv as pcv # for plantcv operations
import time # for calculating the execution time
import random # for generating random numbers
import string # for generating random strings


class ImageProcessor:
    IMAGE_DIR = '../data/farmbot_tray/'
    IMAGE_EXT = ('.jpg', '.jpeg', '.png')
    IMAGE_WIDTH = 1280 # in pixels
    IMAGE_HEIGHT = 960 # in pixels
    TRAY_CENTER_X = 0.0 # in mm, this will be updated later
    TRAY_CENTER_Y = 0.0 # in mm, this will be updated later
    TRAY_CENTER_Z = 0.0 # in mm, this will be updated later
    DIA_OF_POT = 60 # in mm
    DIA_OF_ROI = 50 # in mm DIAMETER OF REGION OF INTEREST (ROI), should be less than DIA_OF_POT
    LENGTH_TRAY_A = 150 # in mm
    LENGTH_TRAY_B = 135 # in mm
    ROTATION_ANGLE = -2 # in degrees
    RATIO_MM2PIX = 3.2 # in pixels per mm
    OFF_SET_CAM_X = 0 # in mm
    OFF_SET_CAM_Y = 5 # in mm

    # getter and setter methods for the class variables
    @property
    def DIA_OF_POT(self):
        return self._DIA_OF_POT

    @DIA_OF_POT.setter
    def DIA_OF_POT(self, value):
        self._DIA_OF_POT = value

    @property
    def DIA_OF_ROI(self):
        return self._DIA_OF_ROI

    @DIA_OF_ROI.setter
    def DIA_OF_ROI(self, value):
        self._DIA_OF_ROI = value

    @property
    def OFF_SET_CAM_X(self):
        return self._OFF_SET_CAM_X

    @OFF_SET_CAM_X.setter
    def OFF_SET_CAM_X(self, value):
        self._OFF_SET_CAM_X = value

    @property
    def OFF_SET_CAM_Y(self):
        return self._OFF_SET_CAM_Y

    @OFF_SET_CAM_Y.setter
    def OFF_SET_CAM_Y(self, value):
        self._OFF_SET_CAM_Y = value

    def rotate(self, x, y, angle):
        x_new = int(x * np.cos(np.radians(angle)))
        y_new = int(y * np.sin(np.radians(angle)))
        return x_new, y_new

    def de_ref(self, x_ref, y_ref, angle, x0, y0):
        a = np.tan(np.radians(angle))*y_ref
        x = x0 + int((x_ref-a)*np.cos(np.radians(angle)))
        y = y0 - int(y_ref/np.cos(np.radians(angle)) + (x_ref-a)*np.sin(np.radians(angle)))
        return x, y
    
    def reverse_de_ref(x, y, angle, x0, y0):
        a = np.tan(np.radians(angle)) * y
        x_ref = x - x0 + a * np.cos(np.radians(angle))
        y_ref = (y0 - y) * np.cos(np.radians(angle)) - (x - x0) * np.sin(np.radians(angle))
        return x_ref, y_ref

    def get_image(self):
        # Get the list of files in the directory
        file_list = os.listdir(self.IMAGE_DIR)

        # Filter out non-image files
        image_files = [file for file in file_list if file.endswith(self.IMAGE_EXT)]

        # Sort the image files alphabetically
        image_files.sort()

        # Read the first image file
        if image_files:
            first_image_path = os.path.join(self.IMAGE_DIR, image_files[0])
            first_image = cv2.imread(first_image_path)
            # Do further processing with the first image
        else:
            print("No image files found in the directory.")

        # Update the tray center coordinates
        filenameparts = image_files[0].split('_')
        self.TRAY_CENTER_X = float(filenameparts[0])
        self.TRAY_CENTER_Y = float(filenameparts[1])
        self.TRAY_CENTER_Z = float(filenameparts[2])
        # check the tray center coordinates, x,y should be positive, z should be 0.0
        if self.TRAY_CENTER_X > 0 and self.TRAY_CENTER_Y > 0 and self.TRAY_CENTER_Z == 0.0:
            print("Tray center coordinates are valid.")
            print("Tray center coordinates: ", "x:", self.TRAY_CENTER_X, "y:", self.TRAY_CENTER_Y)
        else:
            print("Tray center coordinates are not valid.")
        return first_image

    def locate_pots(self):
        # Calculate the middle point of the image
        middle_x = int(self.IMAGE_WIDTH / 2 + self.OFF_SET_CAM_X*self.RATIO_MM2PIX)
        middle_y = int(self.IMAGE_HEIGHT / 2 + self.OFF_SET_CAM_Y*self.RATIO_MM2PIX)

        # Calculate the center of the 6 pots
        center_of_pots = []
            # caleculate the center of the 1. pot
        center_x_1_ref = 0 - self.LENGTH_TRAY_B * self.RATIO_MM2PIX
        center_y_1_ref = (self.LENGTH_TRAY_A * self.RATIO_MM2PIX)/2
        center_x_1, center_y_1 = self.de_ref(center_x_1_ref, center_y_1_ref, self.ROTATION_ANGLE, middle_x, middle_y)
        center_of_pots.append((center_x_1, center_y_1))
            # caleculate the center of the 2. pot
        center_x_2_ref = 0 - self.LENGTH_TRAY_B * self.RATIO_MM2PIX
        center_y_2_ref = -(self.LENGTH_TRAY_A * self.RATIO_MM2PIX)/2
        center_x_2, center_y_2 = self.de_ref(center_x_2_ref, center_y_2_ref, self.ROTATION_ANGLE, middle_x, middle_y)
        center_of_pots.append((center_x_2, center_y_2))
            # caleculate the center of the 3. pot
        center_x_3_ref = 0
        center_y_3_ref = (self.LENGTH_TRAY_A * self.RATIO_MM2PIX)/2
        center_x_3, center_y_3 = self.de_ref(center_x_3_ref, center_y_3_ref, self.ROTATION_ANGLE, middle_x, middle_y)
        center_of_pots.append((center_x_3, center_y_3))
            # caleculate the center of the 4. pot
        center_x_4_ref = 0
        center_y_4_ref = -(self.LENGTH_TRAY_A * self.RATIO_MM2PIX)/2
        center_x_4, center_y_4 = self.de_ref(center_x_4_ref, center_y_4_ref, self.ROTATION_ANGLE, middle_x, middle_y)
        center_of_pots.append((center_x_4, center_y_4))
            # caleculate the center of the 5. pot
        center_x_5_ref = 0 + self.LENGTH_TRAY_B * self.RATIO_MM2PIX
        center_y_5_ref = (self.LENGTH_TRAY_A * self.RATIO_MM2PIX)/2
        center_x_5, center_y_5 = self.de_ref(center_x_5_ref, center_y_5_ref, self.ROTATION_ANGLE, middle_x, middle_y)
        center_of_pots.append((center_x_5, center_y_5))
            # caleculate the center of the 6. pot
        center_x_6_ref = 0 + self.LENGTH_TRAY_B * self.RATIO_MM2PIX
        center_y_6_ref = - (self.LENGTH_TRAY_A * self.RATIO_MM2PIX)/2
        center_x_6, center_y_6 = self.de_ref(center_x_6_ref, center_y_6_ref, self.ROTATION_ANGLE, middle_x, middle_y)
        center_of_pots.append((center_x_6, center_y_6))
        return center_of_pots

    def show_control_image(self, roh_image, center_of_pots, save_image=False):

        # Copy the first image to a control image
        control_image = roh_image.copy()

        # Calculate the middle point of the image
        middle_x = int(self.IMAGE_WIDTH / 2 + self.OFF_SET_CAM_X*self.RATIO_MM2PIX)
        middle_y = int(self.IMAGE_HEIGHT / 2 + self.OFF_SET_CAM_Y*self.RATIO_MM2PIX)

        # Draw the horizontal and vertical refference lines on the image
        # Calculate the start and end point of the horizental line based on the angle
        line_length = int(self.IMAGE_WIDTH/2) # Adjust the length of the line as needed
        start_x_ref = -int(line_length)
        start_y_ref = int(0)
        end_x_ref = int(line_length)
        end_y_ref = int(0)
        # Draw the line on the image
        cv2.line(control_image, self.de_ref(start_x_ref, start_y_ref,self.ROTATION_ANGLE,middle_x,middle_y),
                self.de_ref(end_x_ref, end_y_ref,self.ROTATION_ANGLE,middle_x,middle_y), (0, 255, 0), 2)

        # Calculate the start and end point of the vertical line based on the angle
        line_length = int(self.IMAGE_HEIGHT/2) # Adjust the length of the line as needed
        start_x_ref = int(0)
        start_y_ref = int(line_length)
        end_x_ref = int(0)
        end_y_ref = -int(line_length)
        # Draw the line on the image
        cv2.line(control_image, self.de_ref(start_x_ref, start_y_ref,self.ROTATION_ANGLE,middle_x,middle_y),
                self.de_ref(end_x_ref, end_y_ref,self.ROTATION_ANGLE,middle_x,middle_y), (0, 255, 0), 2)

        # Draw a circle around the center of the pots
        for x,y in center_of_pots:
            cv2.circle(img=control_image, center=(x, y), radius=int(self.DIA_OF_POT*self.RATIO_MM2PIX), color=(0, 0, 255), thickness=2)
            cv2.circle(img=control_image, center=(x, y), radius=int(self.DIA_OF_ROI*self.RATIO_MM2PIX), color=(255, 0, 0), thickness=2)
            cv2.putText(control_image, '1', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3, cv2.LINE_AA)
        # Display the control image
        s = 'Press "c" for capture and "q" for quit'
        cv2.putText(img=control_image, text=s, org=[0,20], fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 0, 255), thickness=1, lineType=cv2.LINE_AA)
        cv2.imshow('Control Image', control_image)
        key = cv2.waitKey(0)
        if key == ord('q'):
            cv2.destroyAllWindows()
        if save_image:
            # Create a directory for saving images if it doesn't exist
            save_dir = 'saved_img'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # Save the control image as a .jpg file
            save_path = os.path.join(save_dir, 'control_image.jpg')
            cv2.imwrite(save_path, control_image)

    def split_roi(self, center_x, center_y, image):
        # Calculate the coordinates of the top-left and bottom-right corners of the ROI
        roi_x1 = int(center_x - self.DIA_OF_POT * self.RATIO_MM2PIX)
        roi_y1 = int(center_y - self.DIA_OF_POT * self.RATIO_MM2PIX)
        roi_x2 = int(center_x + self.DIA_OF_POT * self.RATIO_MM2PIX)
        roi_y2 = int(center_y + self.DIA_OF_POT * self.RATIO_MM2PIX)

        # Crop the ROI from the image
        roi = image[roi_y1:roi_y2, roi_x1:roi_x2]

        # Set pixels outside of the ROI circle to black
        mask = np.zeros_like(roi)
        radius = int(self.DIA_OF_ROI * self.RATIO_MM2PIX)
        center = (roi.shape[1] // 2, roi.shape[0] // 2)  # Set center as the middle of the ROI
        cv2.circle(mask, center, radius, (255, 255, 255), -1) # fill the circle with white color, -1 means fill the circle
        roi = cv2.bitwise_and(roi, mask)

        # Return the ROI
        return roi

    def split_multi_roi(self, center_of_pots, image):
        # Calculate the area of the ROI for each pot
        roi_areas = []
        for center_x, center_y in center_of_pots:
            print(center_x, center_y)
            roi_area = self.split_roi(center_x, center_y, image)
            roi_areas.append(roi_area)
        return roi_areas

    def get_random_watering_points(self, center_of_pots, img, save_image=False, id="none"):
        pcv.params.debug="none"
        # Define the pot center and radius
        pot_x = int(img.shape[1] / 2)
        pot_y = int(img.shape[0] / 2)
        roi_radius = int(self.DIA_OF_ROI * self.RATIO_MM2PIX)
        # Set a timer for the execution time
        start_time = time.time()
        print('############################# START #############################')
        print('processing image:')
        # mask in H channel
        img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_H = img_HSV[:, :, 0]
        img_H_thresh = cv2.inRange(img_H, 20, 40)
        # mask in A channel
        img_LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        img_A = img_LAB[:, :, 1]
        img_A_hist_EQU = cv2.equalizeHist(img_A)
        _, img_A_thresh = cv2.threshold(img_A_hist_EQU, 0, 30, cv2.THRESH_BINARY)
        # mask in V channel
        img_V = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:, :, 2]
        _, img_V_thresh_up = cv2.threshold(img_V, 250, 255, cv2.THRESH_BINARY_INV)
        _, img_V_thresh_down = cv2.threshold(img_V, 50, 255, cv2.THRESH_BINARY)
        img_V_thresh = cv2.bitwise_and(img_V_thresh_up, img_V_thresh_down)
        # combine H A V masks
        img_H_thresh_erode = cv2.erode(img_H_thresh, kernel=np.ones((5, 5), np.uint8), iterations=1)
        img_A_thresh_erode = cv2.erode(img_A_thresh, kernel=np.ones((5, 5), np.uint8), iterations=1)
        img_thresh = cv2.bitwise_or(img_A_thresh_erode, img_H_thresh_erode)
        img_thresh = cv2.bitwise_and(img_thresh, img_V_thresh)
        # closing method to the mask
        mask_dilated = cv2.dilate(img_thresh, kernel=np.ones((5, 5), np.uint8), iterations=2)
        mask_erode = cv2.erode(mask_dilated, kernel=np.ones((5, 5), np.uint8), iterations=3)
        mask_dilated = cv2.dilate(mask_erode, kernel=np.ones((5, 5), np.uint8), iterations=3)
        mask = mask_dilated

        # labeled the regions on the mask image
        _, labeled_mask = cv2.connectedComponents(mask)
        num_mask = np.max(labeled_mask)
        print('{}'.format('\t'),'total', num_mask, 'region(s) found!')

        # just keep the first 10 biggst region on the mask
        count = 0
        region_info={}
        for region_id in range(1,num_mask+1,1):
            mask_region_cnt = cv2.inRange(labeled_mask,region_id,region_id)
            count = cv2.countNonZero(mask_region_cnt)
            region_info[region_id]= (region_id, count)
        list_of_region = list(region_info.values())
        sorted_data = sorted(list_of_region, key=lambda x: x[1], reverse=True)
        sorted_data_cop = sorted_data[:10]

        mask_cop = np.zeros(np.shape(mask),dtype=np.uint8)
        for region_id in sorted_data_cop:
            id = (int)(region_id[0])
            mask_cop+=cv2.inRange(labeled_mask,id,id)

        pcv.plot_image(mask_cop)


        # calculation the center of mass of the region
        # this will locate the plant
        contours, hierarchy = cv2.findContours(mask_cop,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        mask_RGB=cv2.cvtColor(mask_cop,cv2.COLOR_GRAY2BGR)

        # let us define the watering point.
        num_watering_points = 4*7 # 4 time a day and 7 days a week
        # create watering point
        # the previous mask will be enlarged, so that there will be a safty zone, that we will not water the leaves
        mask_with_saftyzone = cv2.dilate(mask_cop, np.ones((15,15), np.uint8), iterations=3)
        watering_points_list = []
        count = 0
        while (count<=num_watering_points):
            angel = random.randint(0,360)
            rel_radius = random.random()
            x_watering_point = (int)(np.cos(np.radians(angel))*(roi_radius)*rel_radius+pot_x)
            y_watering_point = (int)(np.sin(np.rad2deg(angel))*(roi_radius)*rel_radius+pot_y)
            if mask_with_saftyzone[y_watering_point, x_watering_point] != 255:
                watering_points_list.append((x_watering_point, y_watering_point))
                count+=1
            #watering_point_list.append((x_watering_point, y_watering_point))
        if save_image:
            img_out = img.copy()
            # lets draw everything on image
            for i in watering_points_list:
                cv2.circle(img_out,i,2,(0,255,0), -1) # -1 means fill the circle
            cv2.drawContours(img_out, contours, contourIdx=-1, color=(255,0,0), thickness=5)
            # Create a directory for saving images if it doesn't exist
            save_dir = 'saved_img'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            # Save the mask image as a .jpg file
            if id == "none" or id == "":
                # Generate a random name for the image file
                random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
                save_path = os.path.join(save_dir, f'{random_name}.jpg')
            else:
                save_path = os.path.join(save_dir, f'{id}.jpg')
            cv2.imwrite(save_path, img_out)

        end_time = time.time()
        print('{}'.format('\t'),'Execution time:', round(end_time - start_time, 2), 'seconds')
        print('############################# END #############################')
        return watering_points_list

# to do: add a function to save the watering points to a file
# to do: calculate the watering points back to the real world coordinates
