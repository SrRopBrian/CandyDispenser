import customtkinter
import os
import random
from PIL import Image
from typing import List

customtkinter.set_appearance_mode("light")  
customtkinter.set_default_color_theme("blue") 

class Empty(Exception):
    pass

class CandyDispenserApp(customtkinter.CTk):
    
    def __init__(self, capacity, max_capacity):
        super().__init__()
        self.geometry("850x550")
        self.title("Candy Dispenser")
        self.resizable(False, False)

        self._capacity = capacity
        self._max_capacity = max_capacity
        self._candy_stack: List[str] = []
        self.candy_rectangles = [] 
        self.candy_texts = []  # List to hold text IDs

        self.candy_types = ["Juicy Fruit", "Twix", "Snickers", "Kit Kat", "Gummy Bears", "Toffee crisp", 
                   "Bubble yum", "Trident", "Hubba Bubba", "Haribo"]
        self.available_candies = self.candy_types[:]
        random.shuffle(self.available_candies)

        # set background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/resources/candybg3.jpg"),
                                               size=(self.winfo_width(), self.winfo_height()))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # a textbox that displays messages on pressing the buttons
        self.message_text = customtkinter.CTkTextbox(self, width=225, height=130, corner_radius=10, bg_color="#df8ec0", fg_color="white", font=("Jokerman", 16))
        self.message_text.place(relx=0.96, rely=0.35, anchor="e")

        # buttons for the stack operations
        self.pushbtn = customtkinter.CTkButton(master=self, fg_color="#ffa500", bg_color='#df8ec0', text="Push candy", command=self.push)
        self.popbtn = customtkinter.CTkButton(master=self, fg_color="#ffa500", bg_color='#df8ec0', text="Pop candy", command=self.pop)
        self.topbtn = customtkinter.CTkButton(master=self, fg_color="#ffa500", bg_color='#df8ec0', text="Top candy", command=self.top)
        self.emptybtn = customtkinter.CTkButton(master=self, fg_color="#ffa500", bg_color='#df8ec0', text="Is it empty?", command=self.print_is_empty)
        self.lengthbtn = customtkinter.CTkButton(master=self, fg_color="#ffa500", bg_color='#df8ec0', text="Number of candy", command=self.candy_amt)

        self.pushbtn.place(relx=0.83, rely=0.56, anchor=customtkinter.CENTER)
        self.popbtn.place(relx=0.83, rely=0.62, anchor=customtkinter.CENTER)
        self.topbtn.place(relx=0.83, rely=0.68, anchor=customtkinter.CENTER)
        self.emptybtn.place(relx=0.83, rely=0.74, anchor=customtkinter.CENTER)
        self.lengthbtn.place(relx=0.83, rely=0.80, anchor=customtkinter.CENTER)

        # canvas for the candy dispenser and the spring
        self.dispenser_canvas = customtkinter.CTkCanvas(self, width=200, height=450, bg="white")
        self.dispenser_canvas.place(relx=0.53, rely=0.53, anchor="center")

        #spring itself
        self.spring_zigzag = self.dispenser_canvas.create_line(30, 70, 30, 440, fill="gray", width=2)

    # display messages in the text box
    def display_msg(self, message):
        self.message_text.delete("1.0", "end")
        self.message_text.insert("end", message + "\n")
        self.message_text.see("end")

    # update the spring size using a compression factor
    def update_spring(self):
        compression = len(self._candy_stack) / self._max_capacity
        compressed_height = 70 + (compression * 300)
                 
        # Generate zigzag coordinates for the spring
        x_left = 30
        x_right = 170
        y_top = compressed_height
        y_bottom = 440
        num_coils = 10  # Number of coils in the spring
        coil_spacing = (y_bottom - y_top) / (2 * num_coils)

        # Create zigzag pattern
        zigzag_coords = []
        for i in range(num_coils * 2 + 1):
            x = x_left if i % 2 == 0 else x_right
            y = y_top + i * coil_spacing
            zigzag_coords.append((x, y))

        # Flatten the coordinate list for the canvas line
        zigzag_coords_flat = [coord for point in zigzag_coords for coord in point]
        self.dispenser_canvas.coords(self.spring_zigzag, *zigzag_coords_flat)

        # Reposition all candy rectangles
        for i, (rect,text) in enumerate(zip(self.candy_rectangles, self.candy_texts)):
            y_top = compressed_height - ((i + 1) * 30)
            y_bottom = y_top + 30
            self.dispenser_canvas.coords(rect, 40, y_top, 160, y_bottom)

            # Update the text position to be centered on the rectangle
            self.dispenser_canvas.coords(text, 100, (y_top + y_bottom) / 2)


    # get a random candy type from the candy_types list and push it to the dispenser
    def push(self):
        
        if (self._capacity == self._max_capacity):
            self.display_msg("Candy dispenser full.")
        else:
            if not self.available_candies:
                # Reshuffle the candy list when all candy types have been used
                self.available_candies = self.candy_types[:]
                random.shuffle(self.available_candies)
        
            # Get a candy from the available list
            new_candy = self.available_candies.pop()
            self._candy_stack.append(new_candy)
            self.display_msg(f"{new_candy} added")

            #Generate random hex values for candy color
            random_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            # Calculate the Y position based on the spring's compressed height
            compression = len(self._candy_stack) / self._max_capacity
            compressed_height = 70 + (compression * 300)

            # Adjust the Y position to place the candy on top of the spring
            y_top = compressed_height - (len(self._candy_stack) * 30)
            y_bottom = y_top + 30

            candy_rect = self.dispenser_canvas.create_rectangle(40, y_top, 160, y_bottom, fill=random_color, outline="black")
            self.candy_rectangles.append(candy_rect)

            # Add text to the candy
            candy_text = self.dispenser_canvas.create_text(100, (y_top + y_bottom) / 2, text=new_candy, font=("Arial", 12), fill="black")
            self.candy_texts.append(candy_text)

            self._capacity += 1
            self.update_spring()


    def pop(self):
        if (self.is_empty()):
            self.display_msg("No candy to pop!")
            raise Empty('No candy to pop!')
    
        popped_candy = self._candy_stack.pop()
        self.display_msg(f"{popped_candy} popped")

        top_candy_rect = self.candy_rectangles.pop()  # Get the latest rectangle and remove it
        self.dispenser_canvas.delete(top_candy_rect)   # Delete the rectangle from the canvas

        top_candy_text = self.candy_texts.pop()
        self.dispenser_canvas.delete(top_candy_text)

        self._capacity -= 1
        self.update_spring()
        return popped_candy

        
    def top(self):
        if self.is_empty():
            self.display_msg("No candy at all!")
            raise Empty('No candy at all!')
        
        top_candy = self._candy_stack[-1]
        self.display_msg(f"{top_candy} is at the top")
        return(self._candy_stack[-1])

    def is_empty(self):
        return len(self._candy_stack) == 0

    def candy_amt(self):
        self.display_msg(f"{(len(self._candy_stack))}")
        return len(self._candy_stack)
    
    def print_is_empty(self):
        self.display_msg(f"{(len(self._candy_stack) == 0)}")

app = CandyDispenserApp(0,10)
app.mainloop()