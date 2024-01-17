from PIL import Image
import pytesseract

# Set the path to the Tesseract executable (replace with your path)
pytesseract.pytesseract.tesseract_cmd = 'datas/report_temp/tesseract/tesseract.exe'

def image_to_html(image_path):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image)

    # Split the extracted text into lines
    lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]

    # Generate HTML table code
    html_table = '<table border="1">\n'
    for line in lines:
        # Split each line into columns
        columns = line.split()
        # Create HTML table row
        html_table += '\t<tr>\n'
        for col in columns:
            # Create HTML table cell
            html_table += f'\t\t<td>{col}</td>\n'
        html_table += '\t</tr>\n'
    html_table += '</table>'

    return html_table

# Replace 'path/to/your/image.png' with the path to your image file
image_path = 'datas/report_temp/11.jpg'
html_code = image_to_html(image_path)

# Save the HTML code to a file or print it
with open('datas/report_temp/output.html', 'w') as file:
    file.write(html_code)

print("Conversion complete. Check 'output.html' for the HTML code.")
