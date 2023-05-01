from PIL import Image
import os
import csv

# Set the path to the directory containing the input images
input_dir = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie" \
            "\\had\\potholeDetectionTest\\photos\\fotky train CSV"

# Set the path to the directory where you want to save the output images and annotations
output_dir = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie\\" \
             "had\\potholeDetectionTest\\photos\\56x56 train\\pothole"

# Set the path to the annotations file
annotations_file = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie" \
            "\\had\\potholeDetectionTest\\photos\\fotky train CSV\\_annotations.csv"

# Loop through each file in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is an image
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # Open the input image
        input_image = Image.open(os.path.join(input_dir, filename))

        # Resize the image to 28x28
        output_image = input_image.resize((28, 28))

        # Load the annotations for the input image
        annotations = []
        with open(annotations_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == filename:
                    annotations.append(row[1:]) # Append the annotations (excluding the filename)

        # Scale the annotations proportionally to the new image size
        scaled_annotations = []
        for annotation in annotations:
            coords = [int(coord) if coord.isdigit() else coord for coord in annotation]
            if len(coords) != 4:
                continue  # Skip this annotation if it doesn't have 4 coordinates
            x1, y1, x2, y2 = coords
            x1 = int(x1 * 56 / input_image.size[0])
            y1 = int(y1 * 56 / input_image.size[1])
            x2 = int(x2 * 56 / input_image.size[0])
            y2 = int(y2 * 56 / input_image.size[1])
            scaled_annotations.append((x1, y1, x2, y2))

        # Save the output image
        output_image.save(os.path.join(output_dir, filename))

        # Save the annotations for the output image
        with open(os.path.join(output_dir, filename + ".csv"), "w") as f:
            writer = csv.writer(f)
            for annotation in scaled_annotations:
                writer.writerow(annotation)
    # Check if the file is a text file
    elif filename.endswith(".txt"):
        # Open the input text file
        with open(os.path.join(input_dir, filename), "r") as f:
            text = f.read()

        # Create a new output text file
        with open(os.path.join(output_dir, filename), "w") as f:
            # Write the text in uppercase to the output file
            f.write(text.upper())

    else:
        # File is not an image or a text file, skip it
        continue