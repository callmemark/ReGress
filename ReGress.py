from asyncio.windows_events import NULL
from doctest import master
from re import T
from turtle import width
import pandas as pd
from pandastable import Table, config
import logic_lib as lgb

import tkinter as tk
from tkinter import VERTICAL, ttk
from tkinter import X, TOP, W, HORIZONTAL, VERTICAL, BOTH, FLAT, BOTTOM

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import numpy as np
import seaborn as sns
from ttkthemes import ThemedTk



class ReGress():
    def __init__(self, application):
        self.app = application
        self.app.geometry("1000x600")

        self.main_ui_height = 600
        self.main_ui_width = 1000

        self.tool_menu_frame_width = 240


        # dataset variables
        self.dataset = None
        self.df_headers = []



        # handles the visibility state of the side menu panel
        self.mpannel_vsblty_state = {
            "df_editor_frame" : False,
            "mmreg_frame" : False
            }
        
        # MMREG VARIABLES ##
        self.reg_x_axis = []
        self.reg_y_axis = None


        ##  Styling varibales  ##
        self.font_color_white = "#b0b0b0"
        self.main_accent_color = "#212121"
        self.secondary_accent_color = "#424242"


        ## override customize styles ##
        # button overide styles for button instance 
        btn_theme_style = ttk.Style()
        btn_theme_style.configure(
            "TButton",
            font=('Arial', 10),
            borderwidth = 0,
            relief = FLAT,
            highlightthickness = 0,
            pady = 10,
            padx = 7,
            foreground = self.font_color_white
            )
        
        label_theme_style = ttk.Style()
        label_theme_style.configure(
            "TLabel",
            font=('Arial', 10),
            foreground = self.font_color_white
            )

        lframe_custom_theme = ttk.Style()
        lframe_custom_theme.configure(
            'TLabelframe',
            relief = 'solid', 
            background = self.secondary_accent_color,
            bordercolor = self.main_accent_color,
            borderwidth = 4
            )
        lframe_custom_theme.configure(
            'TLabelframe.Label',
            relief = 'solid', 
            background = self.main_accent_color,
            borderwidth = 4
            )


        ## different customize style ##
        # button style for header button
        nav_tool_btn_style = ttk.Style()
        nav_tool_btn_style.configure(
            "nav_tool.TButton",
            background = self.main_accent_color
            )
        
        nav_tool_label_style = ttk.Style()
        nav_tool_label_style.configure(
            "nav_tool.TButton",
            background = self.main_accent_color
            )

        header_frame_style = ttk.Style()
        header_frame_style.configure(
            "header.TFrame",
            background = self.main_accent_color,
            pady = 7
            )
        
        tool_lframe_custom_theme = ttk.Style()
        tool_lframe_custom_theme.configure(
            'tool_lframe.TLabelframe',
            relief = 'solid',
            background = self.main_accent_color,
            bordercolor = self.main_accent_color
            )


        

    def init_app(self):
        self.init_tool_nav_frame()
        self.init_main_activity_panel()

        
        self.init_result_panel()
        self.init_tool_menu_panel()

        self.file_selection_tool_menu_frame()
        self.file_selection_result_frame()
        self.MMREG_result_frame()


        ## initialize Submenus ##
        self.init_MMREG_tool_menu_frame()


        # run startup dataframe viewer on start as inital viewport
        #self.tool_menu_varselect_panel.add(self.df_editing_tool_menu_farame)
        #self.result_panel.add(self.df_table_result_frame)
        


    def init_tool_nav_frame(self):
        # create the header navigation panel
        # Child Widgets for this panel dont need to have own functions since chnages will be handled in this panel
        head_nav_frame = ttk.Frame(self.app, height = 40, width = self.main_ui_width, style = "header.TFrame") 
        head_nav_frame.pack(side = TOP, fill = X)
        
        skipind_lbl = ttk.Label(head_nav_frame, text = "SKIPROWS: ", style = "nav_tool.TButton")
        row_skip_inp_val = tk.StringVar()
        skip_ind_entry = ttk.Entry(head_nav_frame, textvariable = row_skip_inp_val, width = 10)
        
        select_data_set_btn = ttk.Button(
            head_nav_frame, 
            text = "Open", 
            style = "nav_tool.TButton",
            command = lambda: self.open_dataset(row_skip_inp_val.get()))


        tools_lbl = ttk.Label(head_nav_frame, text = "TOOLS: ", style = "nav_tool.TButton")

        # create a button in top navigation panel for multitple linear regression options
        file_manage_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "DATAFRAME", 
            style = "nav_tool.TButton",
            command = lambda: self.update_side_menu_view("df_editor_frame"))
        
        # create a button in top navigation panel for multitple linear regression options
        mmreg_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "MMLINREG", 
            style = "nav_tool.TButton",
            command = lambda: self.update_side_menu_view("mmreg_frame"))
        
        # create a button in top navigation panel for creating a matrix relationship options
        matrix_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "LINREG", 
            style = "nav_tool.TButton",
            command = lambda: self.update_side_menu_view("matrix_btn"))
        
        # create a button in top navigation panel for mediator regression
        med_reg_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "MEDREG", 
            style = "nav_tool.TButton",
            command = lambda: self.update_side_menu_view("med_reg_btn"))

        btn_padx = 0.1

        skipind_lbl.grid(row = 0, column = 0,  sticky = W, padx = btn_padx)
        skip_ind_entry.grid(row = 0, column = 1,  sticky = W, padx = btn_padx)
        select_data_set_btn.grid(row = 0, column = 2,  sticky = W, padx = btn_padx)

        tools_lbl.grid(row = 1, column = 0,  sticky = W, padx = btn_padx)
        file_manage_tab_btn.grid(row = 1, column = 1,  sticky = W, padx = btn_padx)
        mmreg_tab_btn.grid(row = 1, column = 2,  sticky = W, padx = btn_padx)
        matrix_tab_btn.grid(row = 1, column = 3,  sticky = W, padx = btn_padx)
        med_reg_tab_btn.grid(row = 1, column = 4,  sticky = W, padx = btn_padx)
        


    def init_main_activity_panel(self):
        self.mact_panel = ttk.PanedWindow(
            self.app, orient = HORIZONTAL, 
            height = self.main_ui_height, 
            width = self.main_ui_width)

        self.mact_panel.pack(fill = BOTH, expand = True)



    def init_tool_menu_panel(self):
        self.tool_menu_panel = ttk.PanedWindow(
            self.mact_panel, 
            orient = HORIZONTAL,
            height = self.main_ui_height,
            width = self.tool_menu_frame_width
            )

        self.mact_panel.add(self.tool_menu_panel)
        self.init_menu_submenu_panel()



    def init_menu_submenu_panel(self):
        # handles submenus widgets and panels
        self.tool_submenu_widget_panel = ttk.PanedWindow(
            self.tool_menu_panel,
            width = self.tool_menu_frame_width
            )

        # tool_menu_varselect_panel Handles var selection
        self.tool_menu_varselect_panel = ttk.PanedWindow(
            self.tool_submenu_widget_panel,
            orient = HORIZONTAL,
            height = 70,
            width = self.tool_menu_frame_width
            )

        # tool_submenu_config_panel handles the widgets for manipulating the behaviour of the regression
        self.tool_submenu_config_panel = ttk.PanedWindow(
            self.tool_submenu_widget_panel,
            orient = HORIZONTAL,
            width = self.tool_menu_frame_width
            )

        self.init_var_selection_submenu_frame()

        self.tool_submenu_widget_panel.pack(fill = BOTH)
        self.tool_submenu_widget_panel.add(self.tool_menu_varselect_panel)
        self.tool_submenu_widget_panel.add(self.tool_submenu_config_panel)
        self.tool_menu_panel.add(self.tool_submenu_widget_panel)


    def init_var_selection_submenu_frame(self):
        # handles UI for selecting variables for x and y axis for plotting and regression analysis
        # creat frame that will parent all widgets related to setting the x and y axis variable
        variable_selection_frame_label = ttk.Label(text = "Variable Selection") #style = "lfram_label_widg_dark.TLabel"
        self.variable_selection_frame = ttk.LabelFrame(
            self.tool_menu_varselect_panel,
            style = 'tool_lframe.TLabelframe',
            labelwidget = variable_selection_frame_label
            )

        # Frame for x variable selection
        x_var_selection_frame_label = ttk.Label(text = "Values") #style = "lfram_label_widg_dark.TLabel"
        x_var_selection_frame =  ttk.LabelFrame(
            self.variable_selection_frame,
            labelwidget = x_var_selection_frame_label
            )

        # Create a menu button listing all the variables in the dataframe
        selected_var = tk.StringVar()
        x_axis_col_slctn_btn = tk.Menubutton(
            x_var_selection_frame, 
            text = "Variables"
             )

        x_axis_col_slctn_menu = tk.Menu(x_axis_col_slctn_btn,tearoff=0)

        # create options for menu
        for col_name in self.df_headers:
            x_axis_col_slctn_menu.add_radiobutton(label = col_name, value = col_name, variable = selected_var)

        x_axis_col_slctn_btn["menu"] = x_axis_col_slctn_menu

        # button assigning varible to the x axis
        assign_col_btn = ttk.Button(
            x_var_selection_frame, 
            text = "Add to X-Axis", 
            command = lambda: self.update_mmreg_xaxis(add = True, axis = "X", val = selected_var.get())
            )

        # button to unaassigning varible to the x axis
        unassign_col_btn = ttk.Button(
            x_var_selection_frame, 
            text = "remove to X-Axis", 
            command = lambda: self.update_mmreg_xaxis(add = False, axis = "X", val = selected_var.get())
            )

        # button to set y varibale value
        assign_y_axis_btn = ttk.Button(
            x_var_selection_frame,
            text = "Use Y axis",
            command = lambda: self.update_mmreg_xaxis(add = True, axis = "Y", val = selected_var.get())
            )
            
        # create frame to display selected variables in x axis
        xaxis_var_disp_frame_label = ttk.Label(text = "X Axis")
        self.xaxis_var_disp_frame = ttk.LabelFrame(
            self.variable_selection_frame,
            labelwidget = xaxis_var_disp_frame_label
            )

        # create frame to display selected variables in y axis
        yaxis_var_disp_frame_label = ttk.Label(text = "Y Axis")
        self.yaxis_var_disp_frame = ttk.LabelFrame(
            self.variable_selection_frame, 
            labelwidget = yaxis_var_disp_frame_label
            )

        # x_var_selection_frame Grid layout
        x_axis_col_slctn_btn.grid(row = 0, column = 0, pady = 2)
        assign_col_btn.grid(row = 1, column = 0, pady = 2)
        unassign_col_btn.grid(row = 1, column = 1, pady = 2)
        assign_y_axis_btn.grid(row = 2, column = 0, pady = 2)

        ## grid system variable_selection_frame ##
        x_var_selection_frame.grid(row = 0, column = 0, sticky = "nsew", pady = 2)
        self.xaxis_var_disp_frame.grid(row = 0, column = 1, sticky = "nsew", pady = 2)
        self.yaxis_var_disp_frame.grid(row = 0, column = 2, sticky = "nsew", pady = 2)



    def init_result_panel(self):
        # Result panle viewport is the viewport where the results of operation (i.e Tables, Plot, Stat result ) are displayed
        self.result_panel = ttk.PanedWindow(
            self.app, orient = HORIZONTAL, 
            height = self.main_ui_height, 
            width = self.main_ui_width - self.tool_menu_frame_width)

        # mact | main activity window
        self.mact_panel.add(self.result_panel)



    def file_selection_tool_menu_frame(self):
        # This method handles UI for Dataframe manipulation
        # create a button in top navigation panel to select dataset file
        self.df_editing_tool_menu_farame = ttk.Frame(
            self.tool_menu_varselect_panel, 
            height = self.main_ui_height, 
            width = self.tool_menu_frame_width)
        
        stmf_title = ttk.Label(self.df_editing_tool_menu_farame, text = "File Selection Tool")
        stmf_title.grid(row = 0, column = 0,  sticky = W, pady = 25)



    def file_selection_result_frame(self):
        # crete the Result viewport fot the data frame table
        self.df_table_result_frame = ttk.Frame(
            self.result_panel, 
            height = self.main_ui_height, 
            width = self.tool_menu_frame_width)



    def update_file_selection_result_frame(self, df):
        # ouput the tabulated display of the dataframe
        self.df_table = pt = Table(self.df_table_result_frame, dataframe=df, showtoolbar=True, showstatusbar=True)
        pt.show()
        options = {'colheadercolor':'green','floatprecision': 5}
        config.apply_options(options, pt)

        pt.show()



    def init_MMREG_tool_menu_frame(self):
        # create the main frame or a root frame of the tool menu for multiple linear regresssion
        mmreg_frame_label = ttk.Label(text="Multiple Linear Regression")
        self.mmreg_tool_menu_submenu_frame = ttk.Labelframe(
            self.tool_submenu_config_panel,
            labelwidget = mmreg_frame_label,
            padding = 1,
            height = self.main_ui_height,
            width = self.tool_menu_frame_width,
            style = 'tool_lframe.TLabelframe'
            )

        # Button that update the Multiple linear regression plot and stat result
        diplay_plot_btn = ttk.Button(
            self.mmreg_tool_menu_submenu_frame, 
            text = "Refresh Plot Output", 
            command = lambda: self.MMREG_update_result_output_plot())

        diplay_plot_btn.pack(fill = X, padx = 5, pady = 15)
        


    def MMREG_result_frame(self):
        ## Multiple Linear regression result frame ##
        self.mmreg_result_panel = ttk.PanedWindow(
            self.result_panel, 
            height = self.main_ui_height, 
            width = self.tool_menu_frame_width)

        # display the plot of the multiple linear regression
        self.mmreg_res_plot_panel = ttk.PanedWindow(
            self.mmreg_result_panel, orient = HORIZONTAL,
            height = self.main_ui_height, 
            width = self.main_ui_width)

        self.mmreg_result_panel.add(self.mmreg_res_plot_panel)


        # display the statistical result of the regression
        self.mmreg_res_text_panel = ttk.PanedWindow(
            self.mmreg_result_panel, orient = HORIZONTAL, 
            height = self.main_ui_height, 
            width = self.main_ui_width)

        self.mmreg_result_panel.add(self.mmreg_res_text_panel)
        self.MMREG_stat_res_frame = tk.Text(self.mmreg_res_text_panel)
        self.MMREG_stat_res_frame.pack(fill = BOTH)
        


    def MMREG_update_result_output_plot(self):
        REG_CLASS = lgb.REG_PROC(self.dataset, self.df_headers, self.reg_x_axis, self.reg_y_axis)
        # create figure for the plot

        for widget in self.mmreg_res_plot_panel.winfo_children():
            widget.destroy()

        mmreg_output_axis = REG_CLASS.get_mmreg_prediction_plot()
        x_axis = mmreg_output_axis[0]
        y_axis = mmreg_output_axis[1]

        fig = Figure(figsize=(5, 4), dpi=100)
        ax1 = fig.subplots()
        #fig.add_subplot(111).scatter(x_axis, y_axis)
        sns.regplot(x = x_axis, y = y_axis , ci=None, color ='orange', ax = ax1)

        # add the plot and the tool control of matplotlib to the mmreg_res_plot_panel
        canvas = FigureCanvasTkAgg(fig, master = self.mmreg_res_plot_panel) 
        canvas.draw()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self.mmreg_res_plot_panel)
        toolbar.update()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

        self.MMREG_stat_res_frame['state'] = 'normal'
        self.MMREG_stat_res_frame.delete("1.0","end")
        stat_res = REG_CLASS.get_mmreg_stat_result()
        self.MMREG_stat_res_frame.insert("1.0", stat_res)
        self.MMREG_stat_res_frame['state'] = 'disabled'
        


    def create_new_label(self, text_param, axis):
        # add new label widgets 
        if axis == "X":
            if not(text_param == '') or not(text_param == None):
                new_label = ttk.Label(self.xaxis_var_disp_frame, text = text_param)
                new_label.pack(fill = X)
        elif axis == "Y":
            if not(text_param == '') or not(text_param == None):
                new_label = ttk.Label(self.yaxis_var_disp_frame, text = text_param)
                new_label.pack(fill = X)



    def update_mmreg_xaxis(self, add = True, axis = "X", val = "str"):
        if axis == "X":
            if add and not(val in self.reg_x_axis):
                self.reg_x_axis.append(val)
            
            elif not add and val in self.reg_x_axis:
                self.reg_x_axis.remove(val)

            # Remove all the woidgets in the sidplay frame to prevent sidgets with same text value
            for widget in self.xaxis_var_disp_frame.winfo_children():
                widget.destroy()

            # iterate through list reg_x_axis where x axis variable are stored and call 
            # function create_new_label to add new label displaying varibale names in the frame
            for val in self.reg_x_axis:
                self.create_new_label(val, axis)

        elif axis == "Y":
            for widget in self.yaxis_var_disp_frame.winfo_children():
                widget.destroy()

            self.reg_y_axis = val
            self.create_new_label(self.reg_y_axis, axis)



    def open_dataset(self, row_skip):
        self.dataset = lgb.FileSys().open_dataset_by_file(row_skip)
        self.df_headers = tuple(self.dataset.columns)
        self.update_file_selection_result_frame(self.dataset)

        self.init_var_selection_submenu_frame()


    def update_side_menu_view(self, btn_click_arg):
        # This funtion handles what to hide and shown  in side menu frame
        # This function is called by nav button in head selection panel
        # btn_click_arg is a string to determine what frame shoud be shown

        # get the keys of the frame state
        frames_key = self.mpannel_vsblty_state.keys()


        # loop through the dictionary for open frame and hide it
        # remove all frame / widgets related to the frame that is not visible
        for frame in frames_key:
            if frame == "df_editor_frame" and self.mpannel_vsblty_state[frame] == True and btn_click_arg != "df_editor_frame":
                self.mpannel_vsblty_state["df_editor_frame"] = False
                self.tool_menu_varselect_panel.remove(self.df_editing_tool_menu_farame)
                self.result_panel.remove(self.df_table_result_frame)
                

             
            if frame == "mmreg_frame" and self.mpannel_vsblty_state[frame] == True and btn_click_arg != "mmreg_frame":
                self.mpannel_vsblty_state["mmreg_frame"] = False
                self.tool_menu_varselect_panel.remove(self.variable_selection_frame)
                self.tool_submenu_config_panel.remove(self.mmreg_tool_menu_submenu_frame)
                self.result_panel.remove(self.mmreg_result_panel)

        
        # handle if frame is shown already, if not. Show
        if btn_click_arg == "df_editor_frame" and self.mpannel_vsblty_state["df_editor_frame"] == False:
                self.mpannel_vsblty_state["df_editor_frame"] = True 
                self.tool_menu_varselect_panel.add(self.df_editing_tool_menu_farame)
                self.result_panel.add(self.df_table_result_frame)

        elif btn_click_arg == "mmreg_frame" and self.mpannel_vsblty_state["mmreg_frame"] == False:
                self.mpannel_vsblty_state["mmreg_frame"] = True
                self.tool_menu_varselect_panel.add(self.variable_selection_frame)
                self.tool_submenu_config_panel.add(self.mmreg_tool_menu_submenu_frame)
                self.result_panel.add(self.mmreg_result_panel)
                

 
def main():
    #app = tk.Tk()
    app = ThemedTk(theme="black")
    app_UI = ReGress(app)
    app_UI.init_app()
    app.mainloop()


if __name__ == "__main__":
    main()