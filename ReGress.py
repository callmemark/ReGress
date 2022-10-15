#from asyncio.windows_events import NULL
#from doctest import master
#from re import T
#from turtle import width

import pandas as pd
from pandastable import Table, config

import logic_lib as lgb
import ReGress_methods as RgM

import tkinter as tk
from tkinter import LEFT, VERTICAL, LabelFrame, ttk
from tkinter import X, TOP, LEFT, RIGHT, BOTTOM, W, HORIZONTAL, VERTICAL, BOTH, FLAT, BOTTOM
from tkinter.filedialog import asksaveasfile


import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter.messagebox import showinfo

#import numpy as np
import seaborn as sns
from ttkthemes import ThemedTk


from idlelib.tooltip import Hovertip


class ReGress():
    def __init__(self, application):
        self.app = application
        self.app.geometry("1000x600")
        
        self.main_ui_height = 600
        self.main_ui_width = 1000

        self.tool_menu_frame_width = 240

        # dataset variables
        self.dataset = None
        self.dataset_baackup_copy = None
        self.df_headers = []

        
        # handles the visibility state of the side menu panel
        self.mpannel_vsblty_state = {
            "df_editor_frame" : False,
            "mmreg_frame" : False,
            "corl_matrix_frame" : False,
            "logistic_reg_frame" : False
            }
        
        # MMREG VARIABLES ##
        self.reg_x_axis = []
        self.reg_y_axis = None


        ##  Styling varibales  ##
        self.font_color_white = "#e4e1f7"
        self.main_accent_color = "#212121"
        self.secondary_accent_color = "#4b4b4b"

        sns.set(rc={'axes.facecolor':'#292941', 'figure.facecolor':'#292941'})


        ## override customize styles ##
        # button overide styles for button instance 
        btn_theme_style = ttk.Style()
        btn_theme_style.configure(
            "TButton",
            font=('Arial', 10),
            borderwidth = 0,
            relief = FLAT,
            highlightthickness = 0,
            pady = 4,
            padx = 4,
            ipady = 10,
            foreground = self.font_color_white,
            background = self.secondary_accent_color
            )

        menubtn_theme_style = ttk.Style()
        menubtn_theme_style.configure(
            "TMenubutton",
            font=('Arial', 10),
            borderwidth = 0,
            relief = FLAT,
            highlightthickness = 0,
            pady = 10,
            padx = 7,
            foreground = self.font_color_white,
            background = self.main_accent_color
            )

        radiobtn_theme_style = ttk.Style()
        radiobtn_theme_style.configure(
            "TRadiobutton",
            borderwidth = 0
            )
        
        label_theme_style = ttk.Style()
        label_theme_style.configure(
            "TLabel",
            font=('Arial', 10),
            foreground = self.font_color_white,
            background = self.main_accent_color
            )


        # Styling for variable selection frame
        ttk.Style().configure(
            "nav_tool.TLabelframe",
            background = self.main_accent_color,
            borderwidth = 4
            )
        ttk.Style().configure(
            "nav_tool.TLabelframe.Label",
            background = self.main_accent_color
            )

        ttk.Style().configure(
            "TEntry",
            background = "#595959",
            )


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

        tool_lframe_custom_theme = ttk.Style()
        tool_lframe_custom_theme.configure(
            'tool_lframe.TFrame',
            relief = 'solid',
            background = self.secondary_accent_color,
            bordercolor = self.secondary_accent_color
            )
        

    def init_app(self):
        self.init_tool_nav_frame()
        self.init_main_activity_panel()

        self.init_result_panel()
        self.init_tool_menu_panel()

        self.inti_dataframe_editor_tool_menu_frame()
        self.init_dataframe_editor_result_frame()

        self.MMREG_result_frame()
        self.init_MMREG_tool_menu_frame()

        self.init_correlation_matrix_tool_menu_frame()
        self.init_correlation_matrix_result_frame()

        self.init_logistic_reg_tool_menu_frame()
        self.init_logistic_reg_result_frame()


        

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
        Hovertip(file_manage_tab_btn,'Dataframe editor tab', hover_delay=500)
        
        # create a button in top navigation panel for multitple linear regression options
        mmreg_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "MMLINREG", 
            style = "nav_tool.TButton",
            command = lambda: self.update_side_menu_view("mmreg_frame"))
        Hovertip(mmreg_tab_btn,'(Multiple) Linear Regression Analysis tab', hover_delay=500)
        
        # create a button in top navigation panel for creating a matrix relationship options
        matrix_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "CMATRIX", 
            style = "nav_tool.TButton",
            command = lambda: self.update_side_menu_view("corl_matrix_frame"))
        Hovertip(matrix_tab_btn,'Correlational Matrix Analysis tab', hover_delay=500)
        
        # create a button in top navigation panel for mediator regression
        med_reg_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "LOGIREG", 
            style = "nav_tool.TButton",
            command = lambda: self.update_side_menu_view("logistic_reg_frame"))
        Hovertip(med_reg_tab_btn,'Logisitc Regression Analysis tab', hover_delay=500)

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
            height = 150,
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
            style = "nav_tool.TLabelframe",
            labelwidget = variable_selection_frame_label
            )

        # Frame for x variable selection
        x_var_selection_frame_label = ttk.Label(text = "Values") #style = "lfram_label_widg_dark.TLabel"
        x_var_selection_frame =  ttk.LabelFrame(
            self.variable_selection_frame,
            labelwidget = x_var_selection_frame_label,
            style = "nav_tool.TLabelframe.Label"
            )


        # Create a menu button listing all the variables in the dataframe
        selected_var = tk.StringVar()

        new_x_axis_col_slctn_menu_btn = RgM.create_menu_btn(
            tk_arg = tk, 
            ttk_arg = ttk,
            frame_parent_arg = x_var_selection_frame, 
            text_arg = "Variables",
            stringvar_arg = selected_var, 
            menu_value_arg = self.df_headers
            )

        x_axis_col_slctn_btn = new_x_axis_col_slctn_menu_btn["MenuButton"]
        x_axis_col_slctn_btn["menu"] = new_x_axis_col_slctn_menu_btn["RadioButton"]



        # button assigning varible to the x axis
        assign_col_btn = ttk.Button(
            x_var_selection_frame, 
            text = "Add to operation list", 
            command = lambda: self.update_mmreg_xaxis(add = True, axis = "X", val = selected_var.get())
            )

        # button to unaassigning varible to the x axis
        unassign_col_btn = ttk.Button(
            x_var_selection_frame, 
            text = "Remove in operation list", 
            command = lambda: self.update_mmreg_xaxis(add = False, axis = "X", val = selected_var.get())
            )

        # button to set y varibale value
        assign_y_axis_btn = ttk.Button(
            x_var_selection_frame,
            text = "Use Y axis",
            command = lambda: self.update_mmreg_xaxis(add = True, axis = "Y", val = selected_var.get())
            )
            
        # create frame to display selected variables in x axis
        xaxis_var_disp_frame_label = ttk.Label(text = "(X) Operation Vars")
        self.xaxis_var_disp_frame = ttk.LabelFrame(
            self.variable_selection_frame,
            labelwidget = xaxis_var_disp_frame_label,
            style = "nav_tool.TLabelframe.Label"
            )

        # create frame to display selected variables in y axis
        yaxis_var_disp_frame_label = ttk.Label(text = "Y Axis")
        self.yaxis_var_disp_frame = ttk.LabelFrame(
            self.variable_selection_frame, 
            labelwidget = yaxis_var_disp_frame_label,
            style = "nav_tool.TLabelframe.Label"
            )

        # x_var_selection_frame Grid layout
        x_axis_col_slctn_btn.grid(row = 0, column = 0, sticky = "nsew",  pady = 1, padx = 1)
        assign_col_btn.grid(row = 1, column = 0, sticky = "nsew", pady = 1, padx = 1)
        unassign_col_btn.grid(row = 2, column = 0, sticky = "nsew", pady = 1, padx = 1)
        assign_y_axis_btn.grid(row = 3, column = 0,  sticky = "nsew", pady = 5, padx = 1)

        ## grid system variable_selection_frame ##

        self.variable_selection_frame.columnconfigure(1, weight=1)
        x_var_selection_frame.grid(row = 0, column = 0, sticky = "ns", pady = 2)
        self.xaxis_var_disp_frame.grid(row = 0, column = 1, sticky = "ns", pady = 2)
        self.yaxis_var_disp_frame.grid(row = 0, column = 2, sticky = "ns", pady = 2)

         


    def init_result_panel(self):
        # Result panle viewport is the viewport where the results of operation (i.e Tables, Plot, Stat result ) are displayed
        self.result_panel = ttk.PanedWindow(
            self.app, orient = HORIZONTAL, 
            height = self.main_ui_height, 
            width = self.main_ui_width - self.tool_menu_frame_width)

        # mact | main activity window
        self.mact_panel.add(self.result_panel)



    def inti_dataframe_editor_tool_menu_frame(self):
        # This method handles UI for Dataframe manipulation
        # create a button in top navigation panel to select dataset file

        self.df_editing_tool_menu_frame = ttk.Frame(
            self.tool_submenu_config_panel, 
            height = self.main_ui_height, 
            width = self.tool_menu_frame_width)



        # create a basic widget group of confirmation button, Menu button and -
        # a lable for selecting normalization functions
        new_normalization_func_menu = RgM.create_basic_label_menu_options(
            tk_arg = tk, 
            ttk_arg = ttk, 
            style_arg = 'tool_lframe.TFrame', 
            frame_parent_arg = self.df_editing_tool_menu_frame, 
            label_txt_label = "Normalization Methods", 
            btn_text_label = "Not Normalized", 
            menu_value_arg = ["max abs scaling", "min max scaling", "z-score scaling"]
            )
        normalization_func_menu_frame = new_normalization_func_menu["root_frame"]
        max_abs_normalize_strvar = new_normalization_func_menu["str_var"]

        apply_normalize_btn = ttk.Button(
            normalization_func_menu_frame, 
            text = "Apply Normalize",
            command = lambda: self.update_dataframe_editor_result_frame(
                lgb.get_normalized_df(
                    max_abs_normalize_strvar.get(),
                    self.dataset_baackup_copy,
                    self.reg_x_axis,
                    )
                )
        )

        # create button to remove columns selected in operation list
        drop_col_btn = ttk.Button(
            self.df_editing_tool_menu_frame,
            text = "Drop Selected Columns",
            command = lambda: self.update_dataframe_editor_result_frame(
                lgb.DFOperation().drop_col(self.dataset, self.reg_x_axis)
                )
            )


        # create button to refresh the dataset when the table was edited manually
        refresh_data_frame_btn = ttk.Button(
            self.df_editing_tool_menu_frame,
            text = "Refresh Changes",
            command = lambda: self.update_variable_selection_frame()
            )


        # create a basic menu for showing basic information
        new_show_df_info_menu = RgM.create_basic_label_menu_options(
            tk_arg = tk, 
            ttk_arg = ttk, 
            style_arg = 'tool_lframe.TFrame', 
            frame_parent_arg = self.df_editing_tool_menu_frame, 
            label_txt_label = "Show Basic Information", 
            btn_text_label = "None Selected", 
            menu_value_arg = ["Shape", "Index", "Columns", "Info", "Count"]
            )

        show_df_info_menu_frame = new_show_df_info_menu["root_frame"]
        show_df_info_menu_strvar = new_show_df_info_menu["str_var"]

        confirm_show_df_info_btn = ttk.Button(
            show_df_info_menu_frame, 
            text = "Show Information",
            command = lambda: self.df_table_text_space.insert("1.0", lgb.get_df_info(show_df_info_menu_strvar.get(), self.dataset))
            )


        # create a basic menu for showing df summary
        new_show_df_summary_menu = RgM.create_basic_label_menu_options(
            tk_arg = tk, 
            ttk_arg = ttk, 
            style_arg = 'tool_lframe.TFrame', 
            frame_parent_arg = self.df_editing_tool_menu_frame, 
            label_txt_label = "Show Summary", 
            btn_text_label = "None Selected", 
            menu_value_arg = ["Sum", "CumSum", "Min", "Max", "Describe", "Mean", "Median"]
            )

        show_df_summary_menu_frame = new_show_df_summary_menu["root_frame"]
        show_df_summary_menu_strvar = new_show_df_summary_menu["str_var"]

        confirm_show_df_summary_btn = ttk.Button(
            show_df_summary_menu_frame, 
            text = "Show Summary",
            command = lambda: self.df_table_text_space.insert("1.0", lgb.get_df_summary(show_df_summary_menu_strvar.get(), self.dataset))
            )


        # create a basic menu for sorting and Ranking
        new_sort_rank_df_menu = RgM.create_basic_label_menu_options(
            tk_arg = tk, 
            ttk_arg = ttk, 
            style_arg = 'tool_lframe.TFrame', 
            frame_parent_arg = self.df_editing_tool_menu_frame, 
            label_txt_label = "Sort & Rank", 
            btn_text_label = "None Selected", 
            menu_value_arg = ["Sort Index", "Rank"]
            )

        sort_rank_df_menu_frame = new_sort_rank_df_menu["root_frame"]
        sort_rank_df_menu_strvar = new_sort_rank_df_menu["str_var"]

        confirm_sort_rank_df_btn = ttk.Button(
            sort_rank_df_menu_frame, 
            text = "Confirm",
            command = lambda: self.update_dataframe_editor_result_frame(
                    lgb.sort_rank_df(sort_rank_df_menu_strvar.get(), self.dataset)
                )
            )



        normalization_func_menu_frame.pack(fill = X, pady = 2)
        apply_normalize_btn.pack(side = RIGHT, fill = X, padx = 2)

        show_df_info_menu_frame.pack(fill = X, pady = 2)
        confirm_show_df_info_btn.pack(side = RIGHT, fill = X, padx = 2)

        show_df_summary_menu_frame.pack(fill = X, pady = 2)
        confirm_show_df_summary_btn.pack(side = RIGHT, fill = X, padx = 2)

        sort_rank_df_menu_frame.pack(fill = X, pady = 2)
        confirm_sort_rank_df_btn.pack(side = RIGHT, fill = X, padx = 2)

        drop_col_btn.pack(fill = X, pady = 2)
        refresh_data_frame_btn.pack(side = BOTTOM, fill = X, pady = 7)
      


    def init_dataframe_editor_result_frame(self):
        # crete the Result viewport fot the data frame table

        new_df_table_result_frame = RgM.create_multi_result_panel(
            ttk_arg = ttk, 
            tk_arg = tk, 
            orientation_arg = HORIZONTAL,
            parent_root_frame = self.result_panel, 
            height_arg = self.main_ui_height, 
            width_arg = self.tool_menu_frame_width,
            text_fill = BOTH
            )

        self.df_table_result_panel = new_df_table_result_frame["parent_panel"]
        self.df_table_plotting_panel = new_df_table_result_frame["plotting_panel"]
        self.df_table_text_panel = new_df_table_result_frame["text_output_panel"]
        self.df_table_text_space = new_df_table_result_frame["text_output_display"]



    def update_variable_selection_frame(self):
        # update the variable sectection frame
        # change frame to dataframe editinga frame
        self.update_side_menu_view("df_editor_frame")
        self.reg_x_axis.clear()

        # get the dataframe displayed in the table
        update_df = self.pt.model.df

        # update list of dataframe headers
        self.df_headers = tuple(update_df.columns)

        # set new dataframe
        self.dataset = update_df

        # remove the variable select frame re initizlize and display again
        self.tool_menu_varselect_panel.remove(self.variable_selection_frame)
        self.init_var_selection_submenu_frame()
        self.tool_menu_varselect_panel.add(self.variable_selection_frame)


        
    def update_dataframe_editor_result_frame(self, df):
        # ouput the tabulated display of the dataframe
        self.dataset = df
        
        self.pt = Table(self.df_table_plotting_panel, dataframe=df, showtoolbar=False, showstatusbar=True)
        options = {'colheadercolor':'black','floatprecision': 5}
        config.apply_options(options, self.pt)
       

        self.pt.show()
        
        self.update_variable_selection_frame()
        


    def open_dataset(self, row_skip):
        data_return = lgb.FileSys().open_dataset_by_file(row_skip)

        if type(data_return) != type(None):
            # if opening new file reset user selected variable
            self.reg_x_axis.clear()

            # set the opened dataset to a variable
            self.dataset = data_return

            # create a copy of the dataset
            self.dataset_baackup_copy = data_return

            # get the headers and convert to tuple then store in variable
            # this headers will be used for selecting in variable selection menu
            self.df_headers = tuple(self.dataset.columns)
            
            # update the table
            self.update_dataframe_editor_result_frame(self.dataset)

            self.update_variable_selection_frame()
            
 

    def init_MMREG_tool_menu_frame(self):
        # create the main frame or a root frame of the tool menu for multiple linear regresssion
        mmreg_frame_label = ttk.Label(text="Multiple Linear Regression")
        self.mmreg_tool_menu_submenu_frame = ttk.Labelframe(
            self.tool_submenu_config_panel,
            labelwidget = mmreg_frame_label,
            padding = 1,
            height = self.main_ui_height,
            width = self.tool_menu_frame_width,
            #style = 'tool_lframe.TLabelframe'
            )

        # fit intercept parameter UI frame
        # create menu button for selecting MMREG fit intercetp parameter
        fit_intcept_param_frame = ttk.Frame(
            self.mmreg_tool_menu_submenu_frame,
            style = 'tool_lframe.TFrame'
            )

        fit_intcept_param_label = ttk.Label(
            fit_intcept_param_frame,
            text = "Fit Intercept")

        
        fit_intcept_param_label_strvar = tk.StringVar()
        new_fit_intcept_menubtn = RgM.create_menu_btn(
            tk_arg = tk, 
            ttk_arg = ttk,
            frame_parent_arg = fit_intcept_param_frame, 
            text_arg = "Default Val: True",
            stringvar_arg = fit_intcept_param_label_strvar, 
            menu_value_arg = ["True", "False"]
            )

        fit_intcept_param_label_menutbn = new_fit_intcept_menubtn["MenuButton"]
        fit_intcept_param_label_menutbn["menu"] = new_fit_intcept_menubtn["RadioButton"]

        # positive parameter UI frame
        # create menu button for selecting MMREG normalize parameter
        positive_coef_mmreg_param_frame = ttk.Frame(
            self.mmreg_tool_menu_submenu_frame,
            style = 'tool_lframe.TFrame'
            )

        positive_coef_mmreg_param_label = ttk.Label(
            positive_coef_mmreg_param_frame,
            text = "Force Positive Coef")

         
        positive_coef_mmreg_param_strvar = tk.StringVar()
        new_positive_coef_mmreg_param_menubtn = RgM.create_menu_btn(tk_arg = tk, 
            ttk_arg = ttk,
            frame_parent_arg = positive_coef_mmreg_param_frame, 
            text_arg = "Default Val: False",
            stringvar_arg = positive_coef_mmreg_param_strvar, 
            menu_value_arg = ["True", "False"]
            )


        positive_coef_mmreg_param_menubtn = new_positive_coef_mmreg_param_menubtn["MenuButton"]
        positive_coef_mmreg_param_menubtn["menu"] = new_positive_coef_mmreg_param_menubtn["RadioButton"]


        # positive parameter UI frame
        # create entry widget for selecting MMREG njob parameter
        njob_mmreg_param_frame = ttk.Frame(
            self.mmreg_tool_menu_submenu_frame,
            style = 'tool_lframe.TFrame'
            )

        njob_mmreg_param_label = ttk.Label(
            njob_mmreg_param_frame,
            text = "Number of Jobs")

        njob_param_inp_strvar = tk.StringVar()
        njob_param_entry = ttk.Entry(njob_mmreg_param_frame, textvariable = njob_param_inp_strvar)


        # positive parameter UI frame
        # create menu button for selecting MMREG normalize parameter
        stat_output_mmreg_param_frame = ttk.Frame(
            self.mmreg_tool_menu_submenu_frame,
            style = 'tool_lframe.TFrame'
            )

        stat_output_mmreg_param_label = ttk.Label(
            stat_output_mmreg_param_frame,
            text = "Stats Result Output")

         
        stat_output_mmreg_param_strvar = tk.StringVar()
        new_stat_output_mmreg_param_menubtn = RgM.create_menu_btn(tk_arg = tk, 
            ttk_arg = ttk,
            frame_parent_arg = stat_output_mmreg_param_frame, 
            text_arg = "Default Val: StatModel",
            stringvar_arg = stat_output_mmreg_param_strvar, 
            menu_value_arg = ["StatModel", "ScikiLearn"]
            )

        stat_output_mmreg_param_menubtn = new_stat_output_mmreg_param_menubtn["MenuButton"]
        stat_output_mmreg_param_menubtn["menu"] = new_stat_output_mmreg_param_menubtn["RadioButton"]


        # Button that update the Multiple linear regression plot and stat result
        diplay_plot_btn = ttk.Button(
            self.mmreg_tool_menu_submenu_frame, 
            text = "Refresh Plot Output", 
            command = lambda: self.MMREG_update_result_output_plot(
                fit_intercept_param = fit_intcept_param_label_strvar.get(),
                positive_coef_param = positive_coef_mmreg_param_strvar.get(),
                njob_param = njob_param_inp_strvar.get(),
                stat_ouput_source = stat_output_mmreg_param_strvar.get()
                ))


        # fit_intcept_param_frame layout
        fit_intcept_param_label.pack(side = LEFT, fill = X, pady = 2)
        fit_intcept_param_label_menutbn.pack(side = RIGHT, fill = X, pady = 2)

        # normalize parame frame layout
        positive_coef_mmreg_param_label.pack(side = LEFT, fill = X, pady = 2)
        positive_coef_mmreg_param_menubtn.pack(side = RIGHT, fill = X, pady = 2)

        # njob param frame layout
        njob_mmreg_param_label.pack(side = LEFT, fill = X, pady = 2)
        njob_param_entry.pack(side = RIGHT, fill = X, pady = 2)

        # stat model frame layout
        stat_output_mmreg_param_label.pack(side = LEFT, fill = X, pady = 2)
        stat_output_mmreg_param_menubtn.pack(side = RIGHT, fill = X, pady = 2)

        # mmreg_tool_menu_submenu_frame grid layout
        fit_intcept_param_frame.pack(fill = X, padx = 5, pady = 1)
        positive_coef_mmreg_param_frame.pack(fill = X, padx = 5, pady = 1)
        njob_mmreg_param_frame.pack(fill = X, padx = 5, pady = 1)
        stat_output_mmreg_param_frame.pack(fill = X, padx = 5, pady = 1)
        diplay_plot_btn.pack(fill = X, padx = 5, pady = 15)
        


    def MMREG_result_frame(self):
        ## Multiple Linear regression result frame ##
        new_mmreg_result_multiPanels = RgM.create_multi_result_panel(
            ttk_arg = ttk, 
            tk_arg = tk, 
            orientation_arg = HORIZONTAL,
            parent_root_frame = self.result_panel, 
            height_arg = self.main_ui_height, 
            width_arg = self.tool_menu_frame_width,
            text_fill = BOTH
            )

        self.mmreg_result_panel = new_mmreg_result_multiPanels["parent_panel"]
        self.mmreg_res_plot_panel = new_mmreg_result_multiPanels["plotting_panel"]
        self.mmreg_res_text_panel = new_mmreg_result_multiPanels["text_output_panel"]
        self.MMREG_stat_res_text_space = new_mmreg_result_multiPanels["text_output_display"]
        


    def MMREG_update_result_output_plot(self, fit_intercept_param, positive_coef_param, njob_param, stat_ouput_source):
        # check variable valur
        if stat_ouput_source ==  "":
            stat_ouput_source = "StatModel"

        if fit_intercept_param == None or fit_intercept_param == "":
            fit_intercept_param = True

        if positive_coef_param == None or positive_coef_param == "":
            positive_coef_param = False

        if njob_param != None:
            if njob_param == '':
                njob_param = None

            try:
                njob_param = int(njob_param) 
            except:
                njob_param = None


        # initialize REGPROC Class
        REG_CLASS = lgb.MMREG_PROC(
            df_arg = self.dataset, 
            df_headers = self.df_headers, 
            x_vars = self.reg_x_axis, 
            y_var = self.reg_y_axis)

        # create figure for the plot
        for widget in self.mmreg_res_plot_panel.winfo_children():
            widget.destroy()

        mmreg_output_axis = REG_CLASS.get_mmreg_prediction_plot(
            fit_intercept_arg = fit_intercept_param,
            positive_coef_arg = positive_coef_param,
            njob_arg = njob_param
            )

        x_axis = mmreg_output_axis[0]
        y_axis = mmreg_output_axis[1]

        #plt.style.use("dark_background")
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


        self.MMREG_stat_res_text_space['state'] = 'normal'
        self.MMREG_stat_res_text_space.delete("1.0","end")

        if stat_ouput_source ==  "StatModel":
            stat_res = REG_CLASS.get_mmreg_stat_result()
        elif stat_ouput_source == "ScikiLearn":
            stat_res = REG_CLASS.get_sklearn_mmreg_result()

        self.MMREG_stat_res_text_space.insert("1.0", stat_res)
        self.MMREG_stat_res_text_space['state'] = 'disabled'
        


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
            if add and not(val in self.reg_x_axis) and val != "":
                self.reg_x_axis.append(val)
            
            elif not add and val in self.reg_x_axis and val != "":
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


    def init_correlation_matrix_tool_menu_frame(self):
        corl_matrix_frame_label = ttk.Label(text="Correlation Matix")
        self.corl_matrix_menu_submenu_frame = ttk.Labelframe(
            self.tool_submenu_config_panel,
            labelwidget = corl_matrix_frame_label,
            padding = 1,
            height = self.main_ui_height,
            width = self.tool_menu_frame_width,
            #style = 'tool_lframe.TLabelframe'
            )


        refresh_corl_maatrix_plot = ttk.Button(
            self.corl_matrix_menu_submenu_frame, 
            text = "Refresh Correlation Matrix Output", 
            command = lambda: self.update_correlation_matrix_result_frame())
        
        refresh_corl_maatrix_plot.pack(fill = X)


    def init_correlation_matrix_result_frame(self):
        new_corl_matrix_result_multiPanels = RgM.create_multi_result_panel(
            ttk_arg = ttk, 
            tk_arg = tk, 
            orientation_arg = HORIZONTAL,
            parent_root_frame = self.result_panel, 
            height_arg = self.main_ui_height, 
            width_arg = self.tool_menu_frame_width,
            text_fill = BOTH
            )

        self.corl_matrix_result_panel = new_corl_matrix_result_multiPanels["parent_panel"]
        self.corl_matrix_plotting_panel = new_corl_matrix_result_multiPanels["plotting_panel"]
        self.corl_text_output_disp_widget = new_corl_matrix_result_multiPanels["text_output_display"]



    def update_correlation_matrix_result_frame(self):
        for widget in self.corl_matrix_plotting_panel.winfo_children():
            widget.destroy()


        #plt.style.use("dark_background")
        fig = Figure(figsize=(5, 4), dpi=100)
        ax1 = fig.subplots()

        corrMatrix = self.dataset[self.reg_x_axis].corr()
        sns.heatmap(corrMatrix, annot=True, ax = ax1)

        # add the plot and the tool control of matplotlib to the mmreg_res_plot_panel
        canvas = FigureCanvasTkAgg(fig, master = self.corl_matrix_plotting_panel) 
        canvas.draw()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self.corl_matrix_plotting_panel)
        toolbar.update()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

        

    def init_logistic_reg_tool_menu_frame(self):
        logistic_reg_frame_label = ttk.Label(text="Logistic Regression")
        self.logistic_reg_menu_submenu_frame = ttk.Labelframe(
            self.tool_submenu_config_panel,
            labelwidget = logistic_reg_frame_label,
            padding = 1,
            height = self.main_ui_height,
            width = self.tool_menu_frame_width,
            #style = 'tool_lframe.TLabelframe'
            )

        refresh_logistic_reg_plot = ttk.Button(
            self.logistic_reg_menu_submenu_frame, 
            text = "Refresh Logistic Regression Output", 
            command = lambda: self.update_logistic_reg_result_frame())
        
        refresh_logistic_reg_plot.pack(fill = X)
    

    def init_logistic_reg_result_frame(self):
        new_logistic_reg_result_multiPanels = RgM.create_multi_result_panel(
            ttk_arg = ttk, 
            tk_arg = tk, 
            orientation_arg = HORIZONTAL,
            parent_root_frame = self.result_panel, 
            height_arg = self.main_ui_height, 
            width_arg = self.tool_menu_frame_width,
            text_fill = BOTH
            )

        self.logistic_reg_result_panel = new_logistic_reg_result_multiPanels["parent_panel"]
        self.logistic_reg_plotting_panel = new_logistic_reg_result_multiPanels["plotting_panel"]
        self.logistic_reg_output_disp_widget = new_logistic_reg_result_multiPanels["text_output_display"]
    

    def update_logistic_reg_result_frame(self):
        for widget in self.logistic_reg_plotting_panel.winfo_children():
            widget.destroy()


        #plt.style.use("dark_background")
        fig = Figure(figsize=(5, 4), dpi=100)
        ax1 = fig.subplots()

        sns.regplot(
            x = self.dataset[self.reg_x_axis], 
            y = self.dataset[self.reg_y_axis], 
            data = self.dataset, 
            logistic = True, 
            ci = None, 
            ax = ax1)

        # add the plot and the tool control of matplotlib to the mmreg_res_plot_panel
        canvas = FigureCanvasTkAgg(fig, master = self.logistic_reg_plotting_panel) 
        canvas.draw()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self.logistic_reg_plotting_panel)
        toolbar.update()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)



    def open_variable_selection_panel(self, call_state_open = bool):
        if call_state_open:
            self.tool_menu_varselect_panel.add(self.variable_selection_frame)
        elif not call_state_open:
            self.tool_menu_varselect_panel.remove(self.variable_selection_frame)
            

    def open_dataframe_frame(self, action_state_open = bool):
        if action_state_open:
            self.mpannel_vsblty_state["df_editor_frame"] = True 
            self.result_panel.add(self.df_table_result_panel)
            self.open_variable_selection_panel(True)
            self.tool_submenu_config_panel.add(self.df_editing_tool_menu_frame)
        elif not action_state_open:
            self.mpannel_vsblty_state["df_editor_frame"] = False
            self.open_variable_selection_panel(False)
            self.result_panel.remove(self.df_table_result_panel)
            self.tool_submenu_config_panel.remove(self.df_editing_tool_menu_frame)



    def open_mmreg_frame(self, action_state_open = bool):
        if action_state_open:
            self.mpannel_vsblty_state["mmreg_frame"] = True
            self.open_variable_selection_panel(True)
            self.result_panel.add(self.mmreg_result_panel)
            self.tool_submenu_config_panel.add(self.mmreg_tool_menu_submenu_frame)
        elif not action_state_open:
            self.mpannel_vsblty_state["mmreg_frame"] = False
            self.open_variable_selection_panel(False)
            self.result_panel.remove(self.mmreg_result_panel)
            self.tool_submenu_config_panel.remove(self.mmreg_tool_menu_submenu_frame)


    def open_corl_matrix_frame(self, action_state_open = bool):
        if action_state_open:
            self.mpannel_vsblty_state["corl_matrix_frame"] = True
            self.open_variable_selection_panel(True)
            self.result_panel.add(self.corl_matrix_result_panel)
            self.tool_submenu_config_panel.add(self.corl_matrix_menu_submenu_frame)
        elif not action_state_open:
            self.mpannel_vsblty_state["corl_matrix_frame"] = False
            self.open_variable_selection_panel(False)
            self.result_panel.remove(self.corl_matrix_result_panel)
            self.tool_submenu_config_panel.remove(self.corl_matrix_menu_submenu_frame)


    def open_logistic_reg_frame(self, action_state_open = bool):
        if action_state_open:
            self.mpannel_vsblty_state["logistic_reg_frame"] = True
            self.open_variable_selection_panel(True)
            self.result_panel.add(self.logistic_reg_result_panel)
            self.tool_submenu_config_panel.add(self.logistic_reg_menu_submenu_frame)
        elif not action_state_open:
            self.mpannel_vsblty_state["logistic_reg_frame"] = False
            self.open_variable_selection_panel(False)
            self.result_panel.remove(self.logistic_reg_result_panel)
            self.tool_submenu_config_panel.remove(self.logistic_reg_menu_submenu_frame)

    


    def update_side_menu_view(self, btn_click_arg):
        # This funtion handles what to hide and shown  in side menu frame
        # This function is called by nav button in head selection panel
        # btn_click_arg is a string to determine what frame shoud be shown
        if type(self.dataset) == type(None):
            showinfo(
                title ='Error',
                message = "Choose a dataset first"
                )

        elif type(self.dataset) != type(None):
            # get the keys of the frame state
            frames_key = self.mpannel_vsblty_state.keys()

            # loop through the dictionary for open frame and hide it
            # remove all frame / widgets related to the frame that is not visible
            for frame in frames_key:
                if frame == "df_editor_frame" and self.mpannel_vsblty_state[frame] == True and btn_click_arg != "df_editor_frame":
                    self.open_dataframe_frame(False)
                
                if frame == "mmreg_frame" and self.mpannel_vsblty_state[frame] == True and btn_click_arg != "mmreg_frame":
                    self.open_mmreg_frame(False)

                if frame == "corl_matrix_frame" and self.mpannel_vsblty_state[frame] == True and btn_click_arg != "corl_matrix_frame":
                    self.open_corl_matrix_frame(False)
            
                if frame == "logistic_reg_frame" and self.mpannel_vsblty_state[frame] == True and btn_click_arg != "logistic_reg_frame":
                    self.open_logistic_reg_frame(False)


            # handle if frame is shown already, if not Show
            if btn_click_arg == "df_editor_frame" and self.mpannel_vsblty_state["df_editor_frame"] == False:
                self.open_dataframe_frame(True)

            elif btn_click_arg == "mmreg_frame" and self.mpannel_vsblty_state["mmreg_frame"] == False:
                self.open_mmreg_frame(True)

            elif btn_click_arg == "corl_matrix_frame" and self.mpannel_vsblty_state["corl_matrix_frame"] == False:
                self.open_corl_matrix_frame(True)

            elif btn_click_arg == "logistic_reg_frame" and self.mpannel_vsblty_state["logistic_reg_frame"] == False:
                self.open_logistic_reg_frame(True)


            
def main():
    app = ThemedTk(theme="black")
    app_UI = ReGress(app)
    app_UI.init_app()
    app.mainloop()


if __name__ == "__main__":
    main()