from PIL import Image
import os
import csv

# Set the path to the directory containing the input images
# input_dir = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie" \
#             "\\had\\potholeDetectionTest\\photos\\fotky test CSV"

input_dir = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie" \
             "\\had\\potholeDetectionTest\\photos\\fotky train CSV"

# Set the path to the directory where you want to save the output images and annotations
# output_dir = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie" \
#              "\\had\\potholeDetectionTest\\photos\\72x72 test\\pothole"

output_dir = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie" \
              "\\had\\potholeDetectionTest\\photos\\72x72 train\\pothole"

# Set the path to the annotations file
# annotations_file = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie" \
#                    "\\had\\potholeDetectionTest\\photos\\fotky test CSV\\_annotations.csv"

annotations_file = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie" \
                    "\\had\\potholeDetectionTest\\photos\\fotky train CSV\\_annotations.csv"

# Load the annotations
annotations = []
with open(annotations_file, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        annotations.append(row)

# Create the output CSV file
output_file = os.path.join(output_dir, "annotations_output.csv")
with open(output_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=annotations[0].keys())
    writer.writeheader()

    # Loop through each file in the input directory
    for filename in os.listdir(input_dir):
        # Check if the file is an image
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # Open the input image
            input_image = Image.open(os.path.join(input_dir, filename))

            # Resize the image to 72x72
            output_image = input_image.resize((72, 72))

            # Load the annotations for the input image
            annotation = next((ann for ann in annotations if ann["filename"] == filename), None)

            # Scale the annotations proportionally to the new image size
            if annotation is not None:
                x1 = int(int(annotation["xmin"]) * 72 / int(annotation["width"]))
                y1 = int(int(annotation["ymin"]) * 72 / int(annotation["height"]))
                x2 = int(int(annotation["xmax"]) * 72 / int(annotation["width"]))
                y2 = int(int(annotation["ymax"]) * 72 / int(annotation["height"]))

                # Save the annotations for the output image
                scaled_annotations = {
                    "filename": filename,
                    "width": "72",
                    "height": "72",
                    "class": annotation["class"],
                    "xmin": str(x1),
                    "ymin": str(y1),
                    "xmax": str(x2),
                    "ymax": str(y2)
                }
                writer.writerow(scaled_annotations)

            # Save the output image
            output_image.save(os.path.join(output_dir, filename))

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
