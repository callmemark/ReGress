def create_menu_btn(tk_arg, ttk_arg, frame_parent_arg, stringvar_arg, menu_value_arg, text_arg = "Menu Button Name", bg_arg = "#292941", fg_arg = "#b0b0b0",):
    
    
    fit_intcept_param_label_menutbn = ttk_arg.Menubutton(
        frame_parent_arg, 
        text = text_arg)
    fit_intcept_param_menu = tk_arg.Menu(fit_intcept_param_label_menutbn, tearoff=0)

    # create options for menu
    for val in menu_value_arg:
        fit_intcept_param_menu.add_radiobutton(
            label = val,
            value = val,
            background = bg_arg,
            foreground = fg_arg,
            variable = stringvar_arg,
            command = lambda: fit_intcept_param_label_menutbn.configure(text = stringvar_arg.get())
            )

    ret_val = {
        "MenuButton" : fit_intcept_param_label_menutbn,
        "RadioButton" : fit_intcept_param_menu
        }

    return ret_val





#height width
def create_multi_result_panel(ttk_arg, tk_arg, orientation_arg, parent_root_frame, height_arg, width_arg, text_fill, bg_arg = "#424242", fg_arg = "#b0b0b0"):
    # the main frame thats hold children frame
    parent_panel = ttk_arg.PanedWindow(
        parent_root_frame, 
        height = height_arg, 
        width = width_arg)

  
    # display the plot of the multiple linear regression
    plotting_panel = ttk_arg.PanedWindow(
        parent_panel, orient = orientation_arg,
        width = width_arg,
        height = int(height_arg / 1.6), 
        )

    parent_panel.add(plotting_panel)

    
    # display the statistical result of the regression
    text_result_panel = ttk_arg.PanedWindow(
        parent_panel, orient = orientation_arg, 
        height = 60, 
        width = width_arg)

    parent_panel.add(text_result_panel)


    # create text widgets where text ouput will be displayed
    text_output_display = tk_arg.Text(
        text_result_panel, 
        background = bg_arg, 
        foreground = fg_arg)

    text_output_display.pack(fill = text_fill)


    frames = {
        "parent_panel" : parent_panel, # no parent must be parented to a panel or frame
        "plotting_panel" : plotting_panel, # parented to "parent_panel"
        "text_output_panel" : text_result_panel, # parented to "parent_panel"
        "text_output_display" : text_output_display # parented to "parent_panel"
        }

    return frames



def create_basic_label_menu_options(tk_arg, ttk_arg, style_arg, frame_parent_arg, label_txt_label, btn_text_label, menu_value_arg):
    root_frame = ttk_arg.Frame(
        frame_parent_arg,
        style = style_arg
        )

    menu_section_label = ttk_arg.Label(
        root_frame,
        text = label_txt_label
    )

    menu_strvar = tk_arg.StringVar()
    new_menubtn = create_menu_btn(
        tk_arg = tk_arg, 
        ttk_arg = ttk_arg,
        frame_parent_arg = root_frame, 
        text_arg = btn_text_label,
        stringvar_arg = menu_strvar, 
        menu_value_arg = menu_value_arg
        )

    menubtn = new_menubtn["MenuButton"]
    menubtn["menu"] = new_menubtn["RadioButton"]

    menu_section_label.pack(side = "top", fill = "x", pady = 2, padx = 2)
    menubtn.pack(side = "left", fill = "x", pady = 2, padx = 2)
    

    frames = {
        "root_frame" : root_frame,
        "str_var" : menu_strvar
        }

    return frames


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