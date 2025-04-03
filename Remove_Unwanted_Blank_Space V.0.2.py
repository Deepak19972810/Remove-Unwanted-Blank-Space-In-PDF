from PIL import Image
import numpy as np
from PyPDF2 import PdfMerger
import shutil
import os
from pdf2image import convert_from_path

# # Ensure the output directory exists
output_folder = os.path.join(os.getcwd(), "Tracking_ID_folder")
shutil.rmtree(output_folder)
os.makedirs(output_folder, exist_ok=True)

input_folder = os.path.join(os.getcwd(), "extracted_images")
shutil.rmtree(input_folder)
os.makedirs(input_folder, exist_ok=True)

def crop_and_convert_to_pdf(image_path, output_pdf_path):
    """Crops blank space at the bottom and converts the image to a PDF."""
    image = Image.open(image_path)
    gray_image = image.convert("L")  # Convert to grayscale
    image_array = np.array(gray_image)

    # Find the bottom-most non-white pixel (threshold 250 to detect content)
    non_white_pixels = np.where(image_array < 250)
    max_y = max(non_white_pixels[0]) if len(non_white_pixels[0]) > 0 else image.height

    # Crop the image to remove blank bottom space
    cropped_image = image.crop((0, 0, image.width, max_y + 10))  # Adding small margin

    # **Reduce Image Size Before PDF Conversion**
    cropped_image = cropped_image.resize((int(cropped_image.width * 0.8), int(cropped_image.height * 0.8)), Image.LANCZOS)

    # Convert to PDF and save
    cropped_image.convert("RGB").save(output_pdf_path, quality=50, optimize=True)
    print(f"PDF saved: {output_pdf_path}")

a = 0

pdffile = input("Enter The Input PDF File Name: ")
# Iterate through all PDFs in the current directory
# for item in os.listdir("."):
#     if item.endswith(".pdf"):
#         # Convert PDF pages to images
#         images = convert_from_path(item)
#
#         for page_num, img in enumerate(images):
#             a += 1
#             image_filename = os.path.join(input_folder, f"p{str(a)}.png")
#             img.save(image_filename, "PNG")

images = convert_from_path(f"{pdffile}.pdf")

for page_num, img in enumerate(images):
    a += 1
    image_filename = os.path.join(input_folder, f"p{str(a)}.JPEG")
    img.save(image_filename, "JPEG", quality=50)

# Process images
m = 1
for item in os.listdir(input_folder):
    if item.endswith(".JPEG"):
        input_image_path = os.path.join(input_folder, item)  # Full path to the image
        output_pdf = f"cropped_output_{m}.pdf"
        pdf_path = os.path.join(output_folder, output_pdf)
        crop_and_convert_to_pdf(input_image_path, pdf_path)
        m += 1

# Get a list of all PDFs in the directory
pdf_files = [f for f in os.listdir(output_folder) if f.endswith('.pdf')]

# Create a PdfMerger object
merger = PdfMerger()

# Append each PDF file from the directory
for pdf in pdf_files:
    merger.append(os.path.join(output_folder, pdf))

# Write the combined PDF to a file
with open(f'{pdffile}_output.pdf', 'wb') as output_pdf:
    merger.write(output_pdf)

# Close the merger
merger.close()
