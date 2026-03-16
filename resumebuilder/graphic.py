import tkinter as tk

def create_graphic_page():
    root = tk.Tk()
    root.title("Resume Graphic Page")
    root.geometry("600x400")

    # Example: Add a label as a placeholder for graphics
    label = tk.Label(root, text="Your Resume Graphic Will Appear Here", font=("Arial", 16))
    label.pack(pady=50)

    # You can add more widgets or use Canvas for custom graphics
    canvas = tk.Canvas(root, width=500, height=200, bg="lightgray")
    canvas.pack(pady=20)
    # Example: Draw a rectangle (placeholder for a chart or graphic)
    canvas.create_rectangle(50, 50, 450, 150, fill="skyblue")

    root.mainloop()

if __name__ == "__main__":
    create_graphic_page()