def create_menu_btn(tk_arg, ttk_arg, frame_parent_arg, stringvar_arg, menu_value_arg, text_arg = "Menu Button Name", bg_arg = "#212121", fg_arg = "#b0b0b0",):
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