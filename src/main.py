import TrayImageProcessor

def main():
    # create an instance of the TrayImageProcessor
    imgp = TrayImageProcessor.TrayImageProcessor()
    # get the image from the directory
    image, imagename = imgp.get_image()
    # locate the pots in the image
    centrer_of_pots = imgp.locate_pots()
    # show the control image
    imgp.show_control_image(image, centrer_of_pots, save_image=True, show_image=True)
    # split the image into multiple ROIs
    split_images = imgp.split_multi_roi(centrer_of_pots, image)
    # get the watering points for each ROI
    for cnt, img in enumerate(split_images):
        # get the watering points for each ROI
        watering_points_list = imgp.random_watering_points(img, num_watering_points=10 ,save_image=True, show_image=True, filename=str(cnt+1))
        # convert the ROI points to real world coordinates
        real_world_coordinates = imgp.roi2real(watering_points_list, centrer_of_pots[cnt])
        # save the real world coordinates to a csv file
        imgp.save_points_to_csv(real_world_coordinates, filename=str(cnt+1))
    # delete the image from the directory
    imgp.drop_image(imagename)

if __name__ == "__main__":
    main()