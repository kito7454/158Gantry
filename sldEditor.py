import xml.etree.ElementTree as ET

def open_xml_file(file_path):
    """
    Open an XML file and return the root element.

    Args:
        file_path (str): Path to the XML file.

    Returns:
        ET.Element: The root element of the XML file.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def insert_rectangle(root, new_uid, new_x, new_y, new_width, new_height):
    """
    Insert a new RectangleElement into the XML file.

    Args:
        root (ET.Element): The root element of the XML file.
        new_uid (str): The UID of the new RectangleElement.
        new_x (float): The X coordinate of the center of the new RectangleElement.
        new_y (float): The Y coordinate of the center of the new RectangleElement.
        new_width (float): The width of the new RectangleElement.
        new_height (float): The height of the new RectangleElement.
    """
    # Find the ChildElements
    child_elements = root.find('.//ChildElements')

    if child_elements is None:
        print("ChildElements not found")
        return

    # Create a new RectangleElement
    new_rectangle = ET.SubElement(child_elements, 'RectangleElement')

    # Create UID
    uid = ET.SubElement(new_rectangle, 'UID')
    uid.set('Value', new_uid)

    # Create Label
    label = ET.SubElement(new_rectangle, 'Label')
    label.set('Value', 'Rectangle')

    # Create Area
    area = ET.SubElement(new_rectangle, 'Area')
    area.set('Value', 'True')

    # Create GraphicResolution
    graphic_resolution = ET.SubElement(new_rectangle, 'GraphicResolution')
    graphic_resolution.set('Value', '0.02')

    # Create Box
    box = ET.SubElement(new_rectangle, 'Box')

    # Create Center
    center = ET.SubElement(box, 'Center')
    center.set('X', str(new_x))
    center.set('Y', str(new_y))

    # Create Width
    width = ET.SubElement(box, 'Width')
    width.set('Value', str(new_width))

    # Create Height
    height = ET.SubElement(box, 'Height')
    height.set('Value', str(new_height))

    # Save the changes to the XML file
    tree = ET.ElementTree(root)
    tree.write(r"C:\ProgramData\Scanlab\SLLaserDesk\output.sld")

# Example usage:
root = open_xml_file(r"C:\ProgramData\Scanlab\SLLaserDesk\50x50tiles.sld")

for i in range(8):
    for j in range(8):
        x_loc = -24 + 2.5 + 6 * i
        y_loc = -24 + 2.5 + 6 * j
        insert_rectangle(root, 'G#32', x_loc, y_loc, 5, 5)



# import io
#
# def open_and_decode_file(file_path, encoding):
#     try:
#         # Open the file in binary mode
#         with open(file_path, 'rb') as binary_file:
#             # Create a TextIOWrapper object with the binary file and encoding
#             text_wrapper = open(file_path, 'r', encoding=encoding)
#             # Read the contents of the file
#             contents = text_wrapper.read()
#             return contents
#     except FileNotFoundError:
#         print(f"File not found: {file_path}")
#         return None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
#
# # Example usage:
# file_path = r"C:\ProgramData\Scanlab\SLLaserDesk\50x50tiles.sld"  # replace with your file path
#
# data  = open(file_path, 'rb').read()
# decoded_string = data.decode('utf-16le')
#
