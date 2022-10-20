class CombWidgets(): 
    def __init__(self, tk_arg, ttk_arg, hover_tip_arg):
        self.tk = tk_arg
        self.ttk = ttk_arg
        self.hover_tip = hover_tip_arg

        
        

        self.window_and_textspace_style = {
            "panned_window_bg" : "#424242",
            "textspace_bg" : "#424242",
            "textspace_text_color" : "#b0b0b0"
            }


        self.menu_selection_style = {
            "selection_bg" : "#212121",
            "selection_text_color" : "#b0b0b0"
            }


    def create_menu_btn(self, frame_parent_arg, menu_value_arg, mbtn_text_display = "Select", hover_text = None, hover_delay_arg = 500):
        # create a basi menu button frame, This is to shorten the creation of the widget for readability

        # frame_parent_arg : where the menu button will be added or packed
        # stringvar_arg : Holds the value of selected variable >> DEPRECATED <<
        # menu_value_arg : The choices available to when the menu button is created
        # mbtn_text_display : The text dislayed in the menu button

        # create string variable that will hold the selected value in the menu widget
        # Create the menu button widget
        # add the tk menu and use for loop to assign new values into the menu
        # return dictionary, The string variable, the menu button

        string_var = self.tk.StringVar()
        
        menu_btn = self.ttk.Menubutton(
            frame_parent_arg, 
            text = mbtn_text_display
            )

        if hover_text != None: self.hover_tip(menu_btn, hover_text, hover_delay = hover_delay_arg)

        menu = self.tk.Menu(
            menu_btn, 
            tearoff=0
            )

        # create options for menu
        for val in menu_value_arg:
            menu.add_radiobutton(
                label = val,
                value = val,
                background = self.menu_selection_style["selection_bg"],
                foreground = self.menu_selection_style["selection_text_color"],
                variable = string_var,
                command = lambda: menu_btn.configure(text = string_var.get())
                )

        menu_btn["menu"] = menu

        widgets = {
            "string_var" : string_var,
            "menu_button" : menu_btn
            }

        return widgets



    def create_basic_label_menu_options(self, style_arg, frame_parent_arg, label_txt_label, btn_text_label, menu_value_arg):
        # Create a widget of a tkinter label and a tkinter menu widget stored in their own frame

        # tk_arg : Tkinter tk - Removed
        # ttk_arg : Tkinter ttk - Removed
        # style_arg : custom styling NEED TO ADD IN INITALIZATION METHOD
        # frame_parent_arg : the parent frame where the root frame will be put
        # label_txt_label : The label widget text
        # btn_text_label : Menu widget text
        # menu_value_arg : the available selections in the menu widgets


        # Create a root frame
        # Create a label widget
        # Create a menu widget
        # pack the label widget and the menu widget in the root framw
        # return a dictionary of containing the root frame and the string variable

        root_frame = self.ttk.Frame(
            frame_parent_arg,
            style = style_arg
            )

        menu_section_label = self.ttk.Label(
            root_frame,
            text = label_txt_label
        )

        new_menubtn = self.create_menu_btn(
            frame_parent_arg = root_frame, 
            mbtn_text_display = btn_text_label,
            menu_value_arg = menu_value_arg
            )

        menu_strvar = new_menubtn["string_var"]
        menu_btn = new_menubtn["menu_button"]



        menu_section_label.pack(side = "top", fill = "x", pady = 2, padx = 2, ipady = 5)
        menu_btn.pack(side = "left", fill = "x", pady = 2, padx = 2)
    
        widgets = {
            "root_frame" : root_frame,
            "str_var" : menu_strvar
            }

        return widgets


    # Deprecated create_multi_result_panel
    def create_window_and_textspace_panel(self, parent_root_frame, height_arg, width_arg):
       # this function creates a tkinter panedwindow widget and tkinter text widget

       # orientation_arg : paned window orientation - Removed
       # parent_root_frame : the parent frame where the root frame will be padded or packed
       # height_arg : height of the wpanned window widget
       # width_arg : width of the wpanned window widget
       # text_fill : Direction where text will adjust to fill the are - Removed


       # Create the root panel
       # create and stack 2 empty panned window pannel
       # add the 2 panned window pannel to the root panel
       # create a tkinter text panel and pack it to the 2nd panned window panel located at the bottom
       # return value of the root panel, empty pannedwindow, the text panned window, and the text widget

       # the main frame thats hold children frame
        parent_panel = self.ttk.PanedWindow(
            parent_root_frame, 
            height = height_arg, 
            width = width_arg)

  
        # display the plot of the multiple linear regression
        #plotting_panel
        empty_panel = self.ttk.PanedWindow(
            parent_panel, 
            orient = "horizontal",
            width = width_arg,
            height = int(height_arg / 1.6), 
            )

        parent_panel.add(empty_panel)

    
        # display the statistical result of the regression
        text_result_panel = self.ttk.PanedWindow(
            parent_panel, orient = "horizontal", 
            height = 60, 
            width = width_arg)

        parent_panel.add(text_result_panel)


        # create text widgets where text ouput will be displayed
        text_output_display = self.tk.Text(
            text_result_panel, 
            background = self.window_and_textspace_style["textspace_bg"], 
            foreground = self.window_and_textspace_style["textspace_text_color"])

        text_output_display.pack(fill = "both")


        widgets = {
            "parent_panel" : parent_panel,
            "empty_panel" : empty_panel, 
            "text_output_panel" : text_result_panel, 
            "text_output_display" : text_output_display 
            }

        return widgets



    def create_labeled_text_entry(self, root_frame, frame_text_label, hover_text = None, hover_delay_arg = 500):
        self.ttk.Style().configure(
            "labeled_text_entry.TLabelframe",
            borderwidth = 4,
            background = "#212121"
            )
        
        frame_label = self.ttk.Label(text = frame_text_label)

        parent_frame = self.ttk.LabelFrame(
            root_frame,
            labelwidget = frame_label,
            style = "labeled_text_entry.TLabelframe"
            )
        
        text_entry_strvar = self.tk.StringVar()
        text_entry = self.ttk.Entry(parent_frame, textvariable = text_entry_strvar)

        if hover_text != None: self.hover_tip(text_entry, hover_text, hover_delay = hover_delay_arg)

        text_entry.pack(fill = "x", padx = 5, pady = 1, ipady = 5)

        widgets = {
            "string_var" : text_entry_strvar,
            "text_entry" : text_entry,
            "parent_frame" : parent_frame,
            "frame_label" : frame_label
            }

        return widgets


    def create_labeledmenu_menu(self, root_frame, menu_value_arg, menu_text_label, label_text_label):
        self.ttk.Style().configure(
            "labeledmenu.TFrame",
            background = "#212121"
            )

        parent_frame = self.ttk.Frame(
            root_frame,
            style = "labeledmenu.TFrame"
            )

        text_label = self.ttk.Label(
            parent_frame,
            text = label_text_label)

        
        new_menu_widget = self.create_menu_btn(
            frame_parent_arg = parent_frame, 
            mbtn_text_display = menu_text_label,
            menu_value_arg = menu_value_arg
        )

        menu_btn = new_menu_widget["menu_button"]
        menu_btn_string_var = new_menu_widget["string_var"]

        text_label.pack(side = "left", fill = "x", pady = 2, padx = 4, ipady = 5)
        menu_btn.pack(side = "right", fill = "x", pady = 2, padx = 4)

        widgets = {
            "parent_frame" : parent_frame,
            "string_var" : menu_btn_string_var
            }

        return widgets

    
    def create_labeledentry_menu(self, root_frame, label_text_label):
        self.ttk.Style().configure(
            "labeledentry.TFrame",
            background = "#212121"
            )

        parent_frame = self.ttk.Frame(
            root_frame,
            style = "labeledentry.TFrame"
            )

        menu_label = self.ttk.Label(
            parent_frame,
            text = label_text_label)

        menu_label_string_var = self.tk.StringVar()
        menu_entry = self.ttk.Entry(parent_frame, textvariable = menu_label_string_var)

        menu_label.pack(side = "left", fill = "x", pady = 2, padx = 4, ipady = 5)
        menu_entry.pack(side = "right", fill = "x", pady = 2, padx = 4, ipady = 5)

        widgets = {
            "parent_frame" : parent_frame,
            "string_var" : menu_label_string_var
            }

        return widgets



class UndoRedoSys():
    def __init__(self, main_df, saving_steps = 5):
        self.undo_steps = []
        self.redo_steps = []

    def update_undo_redo_sys(self, ):
        pass

    def undo_action(self):
        pass

    def redo_action(self):
        pass