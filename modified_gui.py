import customtkinter as ctk


class ModifiedCTkScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.func = None
        self.args = None
        # Bind the scrollbar's scroll event to the custom function (currently it gets more conversation but may use this for more things)
        self._scrollbar.bind("<B1-Motion>", self._on_scroll) # the left mouse button
        self._scrollbar.bind("<MouseWheel>", self._on_scroll) # the mouse wheel (if cursor on the scrollbar)
        self.bind("<MouseWheel>", self._on_scroll) # using the mouse whell (if cursor on the frame)

    def _on_scroll(self, event):
        # Check if the scrollbar is near the end
        if self._scrollbar.get()[1] >= 0.95:
            self._custom_function()

    def _custom_function(self):
        #print("Scrollbar reached near the end!")
        self.func(*self.args)
        
    def set_func(self, func, *args):
        self.func = func
        self.args = args
