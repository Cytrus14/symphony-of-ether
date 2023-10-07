import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from ImageSection import ImageSection

class ImageSelectionSelector:
    def __init__(self, object_name, channel_count, start_x, start_y):
        self.circle_radius = 0
        self.circle_thickness = 0.5
        self.circle_center_x = start_x
        self.circle_center_y = start_y
        self.channel_count = channel_count
        self.scale_down_factor = 8
        self.band_images = []

        for i in range(1, channel_count+1):
            band_image_name = ('band' + str(i) + '.png')
            band_image_path = os.path.join('symphony_of_ether', 'static', 
                'astronomical_objects', object_name, band_image_name)
            band_image = cv.imread(band_image_path)
            band_image = cv.cvtColor(band_image, cv.COLOR_BGR2GRAY)
            self.band_images.append(band_image)


# img = cv.imread('images_temp_631/m31/test.png')
# img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    def get_sections(self):
        imageSectionsList = []
        for idx, img in enumerate(self.band_images):
            img_size_y, img_size_x = img.shape
            circle_radius = self.circle_radius
            circle_thickness = self.circle_thickness
            circle_center_x, circle_center_y = self.circle_center_x, self.circle_center_y

            # Bin the pixels
            img_size_y_binned = int(img_size_y/self.scale_down_factor)
            img_size_x_binned = int(img_size_x/self.scale_down_factor)
            img = cv.resize(img, (img_size_y_binned, img_size_x_binned), interpolation=cv.INTER_NEAREST)
            img_copy = img.copy()

            # Create a meshgrid of coordinates
            xv, yv = np.meshgrid(np.arange(img_size_x_binned) - circle_center_x, np.arange(img_size_y_binned) - circle_center_y)
            # Calculate the distance from each point to the center
            distance_from_circle_center = np.sqrt(xv**2 + yv**2)
            # Create masks for the inner and outer circle edges
            inner_mask = distance_from_circle_center >= circle_radius - circle_thickness
            outer_mask = distance_from_circle_center <= circle_radius + circle_thickness
            # Combine the mask to create the circle mask
            circle_mask = outer_mask & inner_mask
            # Select image elements within the circle mask
            row_indices, col_indices = np.where(circle_mask)

            # # Select all point within a certain angle range
            # xv, yv = np.meshgrid(np.arange(circle_mask.shape[0]) - circle_center_x, np.arange(circle_mask.shape[1]) - circle_center_y)
            # angles_radians = np.arctan2(yv, xv)
            # angles_degrees = np.degrees(angles_radians)
            # circle_mask_with_angles = (angles_degrees >= selection_angle_start) & (angles_degrees <= selection_angle_stop)
            # row_indices, col_indices = np.where(circle_mask_with_angles)

            # Create a list of ImageSections
            for row, col in zip(row_indices, col_indices):
                if not(row >= img_size_x_binned or col >= img_size_y_binned):
                    channel = idx + 1
                    intensity = img[row][col]
                    imageSection = ImageSection(x_pos=abs(row - self.circle_center_x), y_pos=abs(col - self.circle_center_y), z_pos=channel, intensity=intensity)
                    imageSectionsList.append(imageSection)
                    img_copy[row][col] = 255

            img = cv.resize(img, (img_size_y, img_size_x), interpolation=cv.INTER_NEAREST)
            img_copy = cv.resize(img_copy, (img_size_y, img_size_x), interpolation=cv.INTER_NEAREST)
            # cv.imshow('abc', img_copy)
            # cv.waitKey(30)
        self.circle_radius += 1
        return imageSectionsList

# temp = ImageSelectionSelector('m31', 4, 10, 10)
# while True:
#     sections = temp.get_sections()


