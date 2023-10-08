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
        self.frameId = 0
        self.scale_down_factor = 4
        self.band_images = []
        self.visualization_image = cv.imread(os.path.join('symphony_of_ether', 'static', 
                'astronomical_objects', object_name, 'visualization.png'))

        for i in range(1, channel_count+1):
            band_image_name = ('band' + str(i) + '.png')
            band_image_path = os.path.join('symphony_of_ether', 'static', 
                'astronomical_objects', object_name, band_image_name)
            band_image = cv.imread(band_image_path)
            band_image = cv.cvtColor(band_image, cv.COLOR_BGR2GRAY)
            self.band_images.append(band_image)
        
        # Clear previous images if any
        temp_images_directory = os.path.join('symphony_of_ether', 'temp_files', 
             'temp_images')
        files = os.listdir(temp_images_directory)
        for file in files:
            file_path = os.path.join(temp_images_directory, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f'Error deleting {file_path}', {e})


    # Function to add padding and text to an image
    def _add_padding_and_text(self, image, text):
        # Add padding to the image
        padding = 10
        image_with_padding = cv.copyMakeBorder(
            image, padding, padding, padding, padding, cv.BORDER_CONSTANT, value=(0, 0, 0)
        )
        # Add text to the bottom of the image
        font = cv.FONT_HERSHEY_DUPLEX
        font_scale = 0.5
        font_thickness = 1
        text_color = (255, 255, 255)  # Black color
        text_size = cv.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = (image_with_padding.shape[1] - text_size[0]) // 2
        text_y = image_with_padding.shape[0] - 2 * padding + text_size[1] + 5
        cv.putText(
            image_with_padding,
            text,
            (text_x, text_y),
            font,
            font_scale,
            text_color,
            font_thickness,
            lineType=cv.LINE_AA,
        )
        return image_with_padding

    def get_sections(self):
        imageSectionsList = []
        visualization_image_copy = self.visualization_image.copy()
        grid_image = np.zeros((2 * self.band_images[0].shape[0] + 40, 2 * self.band_images[0].shape[1] + 40), dtype=np.uint8)
        for idx, img in enumerate(self.band_images):
            img_size_y, img_size_x = img.shape
            circle_radius = self.circle_radius
            circle_thickness = self.circle_thickness
            circle_center_x, circle_center_y = self.circle_center_x, self.circle_center_y

            # Bin the pixels
            img_size_y_binned = int(img_size_y/self.scale_down_factor)
            img_size_x_binned = int(img_size_x/self.scale_down_factor)
            img_resized = cv.resize(img, (img_size_y_binned, img_size_x_binned), interpolation=cv.INTER_NEAREST)

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

            # Create a list of ImageSections
            img_copy = img.copy()
            for row, col in zip(row_indices, col_indices):
                if not(row >= img_size_x_binned or col >= img_size_y_binned):
                    channel = idx + 1
                    intensity = img_resized[row][col]
                    imageSection = ImageSection(x_pos=abs(row - self.circle_center_x), y_pos=abs(col - self.circle_center_y), z_pos=channel, intensity=intensity)
                    imageSectionsList.append(imageSection)

                    # Render a color image with a circle showing the currently sonified points
                    neighborhood_size = int(self.scale_down_factor / 2)
                    x_start = max(0, row*self.scale_down_factor - neighborhood_size)
                    x_end = min(img_size_x, row*self.scale_down_factor + neighborhood_size + 1)
                    y_start = max(0, col*self.scale_down_factor - neighborhood_size)
                    y_end = min(img_size_y, col*self.scale_down_factor + neighborhood_size + 1)
                    if idx == 0:
                        visualization_image_copy[y_start:y_end, x_start:x_end] = (255,255,255)
                    
                    # Render single channel images with a circle showing the currently sonified points
                    img_copy[y_start:y_end, x_start:x_end] = 255
                    if idx == 0:
                        grid_image[:img_size_y+20,:img_size_x+20] = self._add_padding_and_text(img_copy, "3.4 micro meters")
                    elif idx == 1:
                        grid_image[:img_size_y+20,img_size_x+20:] = self._add_padding_and_text(img_copy, "4.6 micro meters")
                    elif idx == 2:
                        grid_image[img_size_y+20:,:img_size_x+20] = self._add_padding_and_text(img_copy, "12.0 micro meters")
                    elif idx == 3:
                        grid_image[img_size_y+20:,img_size_x+20:] = self._add_padding_and_text(img_copy, "22.0 micro meters")
            cv.imwrite(os.path.join('symphony_of_ether', 'temp_files', 
                'temp_images', 'grid', str(self.frameId) + '.png'), grid_image)


            img = cv.resize(img_resized, (img_size_y, img_size_x), interpolation=cv.INTER_NEAREST)
            cv.imwrite(os.path.join('symphony_of_ether', 'temp_files', 
             'temp_images', 'combined', str(self.frameId) + '.png'), visualization_image_copy)
        self.circle_radius += 1
        self.frameId += 1
        return imageSectionsList

temp = ImageSelectionSelector('m108', 4, 10, 10)
sections = temp.get_sections()
while len(sections) != 0:
    sections = temp.get_sections()


