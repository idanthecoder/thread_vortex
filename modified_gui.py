import customtkinter as ctk


class ModifiedCTkScrollableFrame(ctk.CTkScrollableFrame):
    """
    A class that inherits from the CTkScrollableFrame class, and therefore behaves as a customtkinter ScrollableFrame.
    This class is, in a way, an upgraded version of the ScrollableFrame that calls a function of choice when close to the end of the screen.

    Attributes:
        func (function): A function to call when near the end of the screen.
        args (tuple): Arguments to give as parameters to the function if needed.
    """
    
    def __init__(self, master):
        """
        The constructor for ModifiedCTkScrollableFrame class.

        Args:
            master (CTk): The master window / parent of the ModifiedCTkScrollableFrame, can be a CTk window, or CTkFrame / CTkScrollableFrame.
        """
        
        super().__init__(master)
        
        self.func = None
        self.args = None
        # Bind the scrollbar's scroll event to the custom function (currently it gets more conversation but may use this for more things)
        self._scrollbar.bind("<B1-Motion>", self.on_scroll) # the left mouse button
        self._scrollbar.bind("<MouseWheel>", self.on_scroll) # the mouse wheel (if cursor on the scrollbar)
        self.bind("<MouseWheel>", self.on_scroll) # using the mouse whell (if cursor on the frame)

    def on_scroll(self, event):
        """
        The method to call when a scrolling event occurs that will check if the scrollbar is near the end of the screen and call a random function.
        """
        
        # Check if the scrollbar is near the end
        if self._scrollbar.get()[1] >= 0.95:
            self.custom_function()

    def custom_function(self):
        """
        Call a custom function.
        """
        
        #print("Scrollbar reached near the end!")
        if len(self.args) == 0:
            self.func()
        else:
            self.func(*self.args)
        
    def set_func(self, func, *args):
        """
        Set the function to run and its arguments.

        Args:
            func (function): The function to call.
        """
        
        self.func = func
        self.args = args
