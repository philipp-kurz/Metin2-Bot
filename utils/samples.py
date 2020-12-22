import os
import cv2 as cv
from pathlib import Path


class Sample:
    def __init__(self, img_path, coordinates, desired_size):
        self.img_path = img_path
        if not os.path.isfile(img_path):
            raise Exception(f'Image does not exist at specified location: {img_path}')
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.w = coordinates[2]
        self.h = coordinates[3]
        self.img = cv.imread(self.img_path)[self.y : self.y + self.h, self.x : self.x + self.w]

        self.desired_size = desired_size
        if self.desired_size is not None:
            self.img_resized = cv.resize(self.img, desired_size)

    def display_img(self, resized=False):
        if resized and self.desired_size is None:
            raise Exception('Cannot display resized image, because desired size was not specified!')
        if resized:
            cv.imshow(f'Resized image: {self.desired_size[0]}x{self.desired_size[1]}', self.img_resized)
        else:
            cv.imshow(f'Image: {self.w}x{self.h}', self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()


class Samples:

    def __init__(self, pos_txt_file, desired_size=None):
        self.pos_txt_file = pos_txt_file
        self.desired_size = desired_size

        if not os.path.isfile(pos_txt_file):
            raise Exception(f'Specified label file does not exist: {pos_txt_file}')

        self.samples = []
        file_handle = open(self.pos_txt_file, 'r')
        lines = file_handle.readlines()
        for line in lines:
            parts = line.rstrip().split(' ')
            img_path = parts[0]
            num_pos = int(parts[1])
            assert len(parts) == (2 + 4 * num_pos), 'Corrupt positive labels file'
            for i in range(num_pos):
                coordinates = (int(parts[2 + 4*i]), int(parts[3 + 4*i]), int(parts[4 + 4*i]), int(parts[5 + 4*i]))
                sample = Sample(img_path, coordinates, self.desired_size)
                self.samples.append(sample)

    def display_images(self, resized=False):
        if resized and self.desired_size is None:
            raise Exception('Cannot display resized image, because desired size was not specified!')
        for sample in self.samples:
            sample.display_img(resized=resized)

    def generate_negs_from_samples(self, output_folder):
        # Check if output folder exists and create if necessary
        output_folder = Path(output_folder)
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        # Iterate over all samples
        for sample in self.samples:
            assert os.path.isfile(sample.img_path)

            # Check if negative has already been created from this original image and load respectively
            filename = 'neg_' + sample.img_path.split('/')[-1]
            filepath = output_folder / filename
            full_image = None
            if os.path.isfile(filepath):
                full_image = cv.imread(str(filepath))
            else:
                full_image = cv.imread(sample.img_path)

            # Black out area of positive sample
            top_left = (sample.x, sample.y)
            bottom_right = (sample.x + sample.w, sample.y + sample.h)
            color = (0, 0, 0)  # Black
            cv.rectangle(full_image, top_left, bottom_right, color, cv.FILLED)
            cv.imwrite(str(filepath), full_image)

    def generate_sample_statistics(self):
        widths = []
        heights = []
        ratios = []
        for sample in self.samples:
            widths.append(sample.w)
            heights.append(sample.h)
            ratios.append(sample.h / sample.w)
        widths = sorted(widths)
        heights = sorted(heights)
        average_width = sum(widths) / len(widths)
        average_height = sum(heights) / len(heights)
        average_ratio = sum(ratios) / len(ratios)
        return average_ratio, widths, heights

    def export_samples(self, output_folder, resized=False):
        output_folder = Path(output_folder)
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        for sample in self.samples:
            filename = f'pos_resized={resized}_' + sample.img_path.split('/')[-1]
            filepath = output_folder / filename
            if not resized:
                cv.imwrite(str(filepath), sample.img)
            else:
                cv.imwrite(str(filepath), sample.img_resized)



def generate_negative_description_file(folder):
    # open the output file for writing. will overwrite all existing data in there
    with open('neg.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir(folder):
            f.write(folder + filename + '\n')
    # python
    # from utils.samples import generate_negative_description_file
    # generate_negative_description_file('classifier/negative_total/')

# Open annotation tool
# C:/Users/Philipp/Development/OpenCV_CLI_Tools/opencv_annotation.exe --annotations=classifier/pos_2020_12_22_01.txt --images=classifier/positive_2020_12_22_01/

# Create vector file of positive samples
# C:/Users/Philipp/Development/OpenCV_CLI_Tools/opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec

# Train cascade classifier
# C:/Users/Philipp/Development/OpenCV_CLI_Tools/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -numPos 120 -numNeg 60 -numStages 10 -miniHitRate 0.5 -maxFalseAlarmRate 0.5
# C:/Users/Philipp/Development/OpenCV_CLI_Tools/opencv_traincascade.exe -data classifier/cascade/ -vec pos.vec -bg neg.txt -w 20 -h 32 -numPos 240 -numNeg 480 -numStages 15 -minHitRate 0.5 -maxFalseAlarmRate 0.5 -acceptanceRatioBreakValue 0.0005
# C:/Users/Philipp/Development/OpenCV_CLI_Tools/opencv_traincascade.exe -data classifier/cascade/ -vec pos.vec -bg neg.txt -w 20 -h 32 -numPos 160 -numNeg 1000 -numStages 15 -minHitRate 0.5 -maxFalseAlarmRate 0.5 -acceptanceRatioBreakValue 0.0001

# Visualize results
# OpenCV_CLI_Tools/opencv_visualisation --image=Metin2-Bot/classifier/sample_export_1608646494/pos_resized=True_1608567101.jpg --model=Metin2-Bot/classifier/cascade/cascade.xml --data=Metin2-Bot/classifier/visu_output_2020_12_22/


