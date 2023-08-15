import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def pencil_sketch(image_path, brightness=40):
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_gray = 255 - gray_img
    blurred_img = cv2.GaussianBlur(inverted_gray, (21, 21), 0)
    inverted_blur = 255 - blurred_img
    pencil_sketch = cv2.divide(gray_img, inverted_blur, scale=256.0)
    return pencil_sketch


def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    return file_path


def sketch_image():
    input_image = select_image()
    if not input_image:
        return

    # Perform sketching
    sketch = pencil_sketch(input_image)

    # Display the sketched image in a new tkinter window
    sketch_img = Image.fromarray(sketch)
    sketch_img = ImageTk.PhotoImage(sketch_img)

    sketch_window = tk.Toplevel()
    sketch_window.title("Pencil Sketch")

    canvas = tk.Canvas(sketch_window, width=sketch.shape[1], height=sketch.shape[0])
    canvas.pack()

    canvas.create_image(0, 0, anchor=tk.NW, image=sketch_img)
    canvas.image = sketch_img

    # Create a button to save the sketched image
    save_button = tk.Button(sketch_window, text="Save Sketch", command=lambda: save_sketch(sketch, sketch_window))
    save_button.pack()

    # Create a close button to close the display box
    close_button = tk.Button(sketch_window, text="Close", command=sketch_window.destroy)
    close_button.pack()


def save_sketch(sketch, window):
    output_image = filedialog.asksaveasfilename(title="Save Sketch", defaultextension=".jpg", filetypes=[("Image Files", "*.jpg")])
    if not output_image:
        return

    # Save the sketched image
    cv2.imwrite(output_image, sketch)

    # Close the display box after saving
    window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pencil Sketch App")

    # Create a button to select an image and start sketching
    sketch_button = tk.Button(root, text="Select Image and Sketch", command=sketch_image)
    sketch_button.pack()

    # Create a button to close the application
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack()

    root.mainloop()
