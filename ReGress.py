# Copyright @ 2022 
# Licensed under GNU General Public License v3.0
# 
# Author: Mark John Velmonte
# 
# This is the main GUI program of the ReGress Software
# It handles different frames and widgets it handles frame switching and other GUI application


from textwrap import fill
import pandas as pd
from pandastable import Table, config

import logic_lib as lgb
import ReGress_methods as RgM

import tkinter as tk
from tkinter import LEFT, VERTICAL, LabelFrame, ttk
from tkinter import X, Y, TOP, LEFT, RIGHT, BOTTOM, W, HORIZONTAL, VERTICAL, BOTH, FLAT, BOTTOM
from tkinter.filedialog import asksaveasfile


import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter.messagebox import showinfo

#import numpy as np
import seaborn as sns
from ttkthemes import ThemedTk

from idlelib.tooltip import Hovertip

from time import sleep

class ReGress():
    def __init__(self, application):
        self.app = application
        self.app.geometry("1000x600")
        self.set_to_full_screen = False
        
        self.main_ui_height = 400#600
        self.main_ui_width = 1000

        self.tool_menu_frame_width = 240

        # dataset variables
        self.dataset = None
        self.dataset_backup_copy = None
        self.df_headers = []

        # intialize custom library of grouped widgets for ease of adding menus and other GUI elements
        self.grouped_widgets = RgM.CombWidgets(tk_arg = tk, ttk_arg = ttk, hover_tip_arg = Hovertip)
        

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
        self.font_color_white = "#bababa"
        self.font_darker_white = "#878787"
        self.main_accent_color = "#212121"
        self.secondary_accent_color = "#4b4b4b"
        self.important_color = "#ffc400"

        self.orange_theme_color = "#fcba03"
        self.redorange_theme_color = "#fc4c00"


        self.SEABORN_PLOT_THEMES = ["App Default", "darkgrid", "whitegrid", "dark", "white", "ticks"]

        # plot styling
        sns.set(rc={
            'axes.facecolor':'#171717', 
            'figure.facecolor':'#171717',
            'grid.linewidth' : 0.2,
            'grid.color' : "#6e6e6e",
            'axes.spines.top' : False,
            'axes.spines.right' : False,
            'xtick.color' : self.font_color_white,
            'ytick.color' : self.font_color_white,
            'axes.titlecolor' : self.font_color_white,
            'axes.labelcolor' : self.font_color_white,
            })
        sns.set_palette("pastel")


        ## override customize styles ##
        # button overide styles for button instance 
        self.btn_height = 4
        self.tool_menu_pady = 1
        self.tool_menu_padx = 1


        btn_theme_style = ttk.Style()
        btn_theme_style.map("TButton",
            foreground=[
                ('!active', self.font_color_white),
                ('pressed', self.font_color_white), 
                ('active', self.font_color_white)],
            background=[ 
                ('!active', self.main_accent_color),
                ('pressed', self.main_accent_color), 
                ('active', self.secondary_accent_color)]
          )
        btn_theme_style.configure(
            "TButton",
            font=('Roboto', 10),
            borderwidth = 0,
            relief = FLAT,
            highlightthickness = 0,
            pady = self.tool_menu_pady,
            padx = 4
            )
        
        orange_them_btn = ttk.Style()
        orange_them_btn.map("orange_btntheme.TButton",
            foreground=[
                ('!active', self.main_accent_color),
                ('pressed', self.main_accent_color), 
                ('active', self.main_accent_color)],
            background=[ 
                ('!active', self.orange_theme_color),
                ('pressed', self.orange_theme_color), 
                ('active', self.orange_theme_color)]
          )

        redorange_them_btn = ttk.Style()
        redorange_them_btn.map("redorange_btntheme.TButton",
            foreground=[
                ('!active', self.main_accent_color),
                ('pressed', self.main_accent_color), 
                ('active', self.main_accent_color)],
            background=[ 
                ('!active', self.redorange_theme_color),
                ('pressed', self.redorange_theme_color), 
                ('active', self.redorange_theme_color)]
          )



        importtant_btn_style = ttk.Style()
        importtant_btn_style.map("important.TButton",
            foreground=[('!active', 'black'),('pressed', self.font_color_white), ('active', self.font_color_white)],
            background=[ ('!active','grey75'),('pressed', self.main_accent_color), ('active', self.main_accent_color)]
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
        nav_tool_btn_style.map("nav_tool.TButton",
            foreground=[
                ('!active', self.font_darker_white),
                ('pressed', self.important_color), 
                ('active', self.important_color)],
            background=[ 
                ('!active', self.main_accent_color),
                ('pressed', self.main_accent_color), 
                ('active', self.main_accent_color)]
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
    

    def setSeabornPlotSysDefault(self):
        # plot styling
        sns.set(rc={
            'axes.facecolor':'#171717', 
            'figure.facecolor':'#171717',
            'grid.linewidth' : 0.2,
            'grid.color' : "#6e6e6e",
            'axes.spines.top' : False,
            'axes.spines.right' : False,
            'xtick.color' : self.font_color_white,
            'ytick.color' : self.font_color_white,
            'axes.titlecolor' : self.font_color_white,
            'axes.labelcolor' : self.font_color_white,
            })

        sns.set_palette("pastel")


    def InitApp(self):
        self.InitToolNavFrame()
        self.InitMainActivityPanel()
        self.InitBottomNotifPanelFrame()

        self.initResultPanel()
        self.initSideBarPanel()

        self.InitDataFrameEditorMenuFrame()
        self.InitDataFrameEditorResultPanel()

        self.InitMMREGResultFrame()
        self.InitMMREGToolMenuFrame()

        self.InitCorellationMatrixToolMenuFrame()
        self.InitCorrelationMatrixResultFrame()

        self.InitLogisticRegToolMenuFrame()
        self.InitLogisticRegResultFrame()


        
    def InitToolNavFrame(self):
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
            command = lambda: self.OpenDataset(row_skip_inp_val.get()))

        window_screen_full_screen_toggle_btn = ttk.Button(
            head_nav_frame,
            text = "Screen Toggle",
            style = "nav_tool.TButton",
            command = lambda: self.ToggleScreenFrameSize()
            )


        tools_lbl = ttk.Label(head_nav_frame, text = "TOOLS: ", style = "nav_tool.TButton")

        # create a button in top navigation panel for multitple linear regression options
        file_manage_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "DATAFRAME", 
            style = "nav_tool.TButton",
            command = lambda: self.UpdateSideMenuDisp("df_editor_frame"))
        Hovertip(file_manage_tab_btn,'Dataframe editor tab', hover_delay=500)
        
        # create a button in top navigation panel for multitple linear regression options
        mmreg_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "MMLINREG",
            style = "nav_tool.TButton",
            command = lambda: self.UpdateSideMenuDisp("mmreg_frame"))
        Hovertip(mmreg_tab_btn,'(Multiple) Linear Regression Analysis tab', hover_delay=500)
        
        # create a button in top navigation panel for creating a matrix relationship options
        matrix_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "CMATRIX", 
            style = "nav_tool.TButton",
            command = lambda: self.UpdateSideMenuDisp("corl_matrix_frame"))
        Hovertip(matrix_tab_btn,'Correlational Matrix Analysis tab', hover_delay=500)
        
        # create a button in top navigation panel for mediator regression
        med_reg_tab_btn = ttk.Button(
            head_nav_frame, 
            text = "LOGIREG", 
            style = "nav_tool.TButton",
            command = lambda: self.UpdateSideMenuDisp("logistic_reg_frame"))
        Hovertip(med_reg_tab_btn,'Logisitc Regression Analysis tab', hover_delay=500)

        btn_padx = 0.1

        skipind_lbl.grid(row = 0, column = 0,  sticky = W, padx = btn_padx)
        skip_ind_entry.grid(row = 0, column = 1,  sticky = W, padx = btn_padx)
        select_data_set_btn.grid(row = 0, column = 2,  sticky = W, padx = btn_padx)
        window_screen_full_screen_toggle_btn.grid(row = 0, column = 3, sticky = W, padx = btn_padx)

        tools_lbl.grid(row = 1, column = 0,  sticky = W, padx = btn_padx)
        file_manage_tab_btn.grid(row = 1, column = 1,  sticky = W, padx = btn_padx)
        mmreg_tab_btn.grid(row = 1, column = 2,  sticky = W, padx = btn_padx)
        matrix_tab_btn.grid(row = 1, column = 3,  sticky = W, padx = btn_padx)
        med_reg_tab_btn.grid(row = 1, column = 4,  sticky = W, padx = btn_padx)
        


    def ToggleScreenFrameSize(self):
        if self.set_to_full_screen == False:
            self.app.attributes('-fullscreen', True) 
            self.set_to_full_screen = True
        elif self.set_to_full_screen == True:
            self.app.attributes('-fullscreen', False)
            self.set_to_full_screen = False


      
    def InitMainActivityPanel(self):
        self.mact_panel = ttk.PanedWindow(
            self.app, orient = HORIZONTAL, 
            height = self.main_ui_height, 
            width = self.main_ui_width)

        self.mact_panel.pack(fill = BOTH, expand = True)



    def InitBottomNotifPanelFrame(self):
        # bottom panel where warning or error will be displayed
        botton_notif_panel_frame = ttk.Frame(self.app, height = 70, width = self.main_ui_width, style = "header.TFrame") 
        botton_notif_panel_frame.pack(side = BOTTOM, fill = X)

        notif_label = ttk.Label(botton_notif_panel_frame, text = "Notifiaction alert panel")
        notif_label.grid(row = 1, column = 1, pady = 7)

        self.notif_panel_update_manager = RgM.AppNotifHandle(notif_label, ttk)
        self.notif_panel_update_manager.create_bnotif("N", "Application Started : Please select dataset to start operations")


       
    def initSideBarPanel(self):
        # side_bar_parent_panel holds different panel where tools are used to manipulate the results -
        #   shown in the result panel
        self.side_bar_panel = ttk.PanedWindow(
            self.mact_panel, 
            orient = HORIZONTAL,
            height = self.main_ui_height,
            width = self.tool_menu_frame_width
            )

        self.mact_panel.add(self.side_bar_panel)
        self.initSubpanelParentPanel()


    def initSubpanelParentPanel(self):
        ## Initialize the subpanels inside the side panel ##

        # handles submenus widgets and panels
        # side_bar_subpanel_parent_panel holds 2 subpanel the upper panel where variable selection are handles
        #   and on bottom pannel where data operation are handled.
        self.side_bar_subpanel_parent_panel = ttk.PanedWindow(
            self.side_bar_panel,
            width = self.tool_menu_frame_width
            )

        # tool_menu_varselect_panel Handles var selection
        self.tool_menu_varselect_panel = ttk.PanedWindow(
            self.side_bar_subpanel_parent_panel,
            orient = HORIZONTAL,
            height = 150,
            width = self.tool_menu_frame_width
            )

        # tool_submenu_config_panel 
        self.tool_submenu_config_panel = ttk.PanedWindow(
            self.side_bar_subpanel_parent_panel,
            orient = HORIZONTAL,
            width = self.tool_menu_frame_width
            )


        self.variable_selection_canvas = tk.Canvas(self.tool_menu_varselect_panel, background = self.main_accent_color)
        self.tool_menu_canvas = tk.Canvas(self.tool_submenu_config_panel, background = self.main_accent_color)
        

        # create scrollbar df_editor_tool_menu_scroll_bar
        self.tool_menu_scroll_bar = ttk.Scrollbar(self.tool_submenu_config_panel,
                                     command = self.tool_menu_canvas.yview,
                                     orient = "vertical"
                                     )
        
        self.var_selectn_panel_scroll_bar = ttk.Scrollbar(self.tool_menu_varselect_panel,
                                                          command = self.variable_selection_canvas.yview,
                                                          orient = "vertical"
                                                          )


        self.tool_menu_scroll_bar.pack(side = RIGHT, fill = Y )
        self.var_selectn_panel_scroll_bar.pack(side = RIGHT, fill = Y )

        self.InitVarSelectSubMenuFrame()

        self.side_bar_subpanel_parent_panel.pack(fill = BOTH)
        self.side_bar_subpanel_parent_panel.add(self.tool_menu_varselect_panel)
        self.side_bar_subpanel_parent_panel.add(self.tool_submenu_config_panel)

        self.tool_menu_varselect_panel.add(self.variable_selection_canvas)
        self.tool_submenu_config_panel.add(self.tool_menu_canvas)

        self.side_bar_panel.add(self.side_bar_subpanel_parent_panel)


        
    def InitVarSelectSubMenuFrame(self):
        # handles UI for selecting variables for x and y axis for plotting and regression analysis
        # creat frame that will parent all widgets related to setting the x and y axis variable
           
        self.variable_selection_frame = ttk.Frame(
                self.variable_selection_canvas,
                width = self.tool_menu_frame_width
            )
        
        # contains widgets related to electing operation / x axis variable
        operation_var_container_panel = ttk.Frame(
                self.variable_selection_frame,
                width = self.tool_menu_frame_width
            )

        # contains widgets related to selecting key varible or y axis variable
        key_var_container_panel = ttk.Frame(
                self.variable_selection_frame,
                width = self.tool_menu_frame_width
            )


        extra_option_container_panel = ttk.Frame(
                self.variable_selection_frame,
                width = self.tool_menu_frame_width
            )
        


        # Create a menu button listing all the variables in the dataframe
        new_x_axis_col_slctn_menu_btn = self.grouped_widgets.create_menu_btn(
            frame_parent_arg = operation_var_container_panel, 
            mbtn_text_display = "Variables",
            menu_value_arg = self.df_headers
            )

        selected_var = new_x_axis_col_slctn_menu_btn["string_var"]
        x_axis_col_slctn_btn = new_x_axis_col_slctn_menu_btn["menu_button"]

        
        


        # button assigning varible to the x axis
        assign_col_btn = ttk.Button(
            operation_var_container_panel, 
            text = "Add to operation list",
            style = "orange_btntheme.TButton",
            command = lambda: self.UpdateVarSelectionList(add = True, axis = "X", val = selected_var.get())
            )

        # button to unaassigning varible to the x axis
        unassign_col_btn = ttk.Button(
            operation_var_container_panel, 
            text = "Remove in operation list",
            style = "redorange_btntheme.TButton",
            command = lambda: self.UpdateVarSelectionList(add = False, axis = "X", val = selected_var.get())
            )

        x_axis_selected_list_label = ttk.Label(
            operation_var_container_panel,
            text = "X-Axis / Operation variable: "
            )

        # create frame to display selected variables in x axis
        self.xaxis_var_disp_frame = ttk.Frame(
            operation_var_container_panel,
            style = "nav_tool.TLabelframe.Label"
            )

        # Drop down menu to select variables
        new_y_axis_col_slctn_menu_btn = self.grouped_widgets.create_menu_btn(
            frame_parent_arg = key_var_container_panel, 
            mbtn_text_display = "Variables",
            menu_value_arg = self.df_headers
            )

        selected_yaxis_var = new_y_axis_col_slctn_menu_btn["string_var"]
        y_axis_col_slctn_btn = new_y_axis_col_slctn_menu_btn["menu_button"]

        # button to set y varibale value
        assign_y_axis_btn = ttk.Button(
            key_var_container_panel,
            text = "Use Y axis",
            style = "orange_btntheme.TButton",
            command = lambda: self.UpdateVarSelectionList(add = True, axis = "Y", val = selected_yaxis_var.get())
            )
        
        y_axis_selected_var_list_label = ttk.Label(
            key_var_container_panel, 
            text = "Y-Axis / Primary key: "
            )

        # create frame to display selected variables in y axis
        self.yaxis_var_disp_frame = ttk.Frame(
            key_var_container_panel, 
            style = "nav_tool.TLabelframe.Label"
            )


        # create menu to slice dataset from and to the selected value
        new_df_row_slice_selection_menu = self.grouped_widgets.create_compared_entries_menu(
            root_frame = extra_option_container_panel,
            frame_text_label = "Select Only rows",
            val1_label_text_arg = "From",
            val2_label_text_arg = "To"
            )

        df_row_slice_selection_frame = new_df_row_slice_selection_menu["parent_frame"]
        self.df_row_slice_selection_string_var_01 = new_df_row_slice_selection_menu["string_var_01"]
        self.df_row_slice_selection_string_var_02 = new_df_row_slice_selection_menu["string_var_02"]


        # packed layout
        operation_var_container_panel.pack(fill = X, padx = 5, pady = 5)
        key_var_container_panel.pack(fill = X, padx = 5, pady = 5)
        extra_option_container_panel.pack(fill = X, padx = 5, pady = 5)

        x_axis_col_slctn_btn.pack(fill = X, pady = self.tool_menu_pady)
        assign_col_btn.pack(fill = X, pady = self.tool_menu_pady)
        unassign_col_btn.pack(fill = X, pady = self.tool_menu_pady)
        x_axis_selected_list_label.pack(fill = X, pady = self.tool_menu_pady)
        self.xaxis_var_disp_frame.pack(fill = X, pady = self.tool_menu_pady)

        y_axis_col_slctn_btn.pack(fill = X, pady = self.tool_menu_pady)
        assign_y_axis_btn.pack(fill = X, pady = self.tool_menu_pady)
        y_axis_selected_var_list_label.pack(fill = X, pady = self.tool_menu_pady)
        self.yaxis_var_disp_frame.pack(fill = X, pady = self.tool_menu_pady)

        df_row_slice_selection_frame.pack(fill = X, pady = self.tool_menu_pady)



    def UpdateVarSelectionList(self, add = True, axis = "X", val = ""):
        self.OpenVariableSelectionPanel(False)
        if axis == "X":
            if add and not(val in self.reg_x_axis) and val != "":
                self.reg_x_axis.append(val)
            
            elif not add and val in self.reg_x_axis and val != "":
                self.reg_x_axis.remove(val)

            self.RefreshXVarSelectionList(self.df_headers)

        elif axis == "Y":
            self.reg_y_axis = val
            self.RefreshYVarSelectionList(self.df_headers)
        
        var_select_panel = self.variable_selection_frame.winfo_height()

        self.OpenVariableSelectionPanel(True)
        self.initSideBarPanelWidth()
        
        

    def RefreshXVarSelectionList(self, df_headers_list_arg):
        # Remove all the widgets in the sidplay frame to prevent widgets with same text value
        for widget in self.xaxis_var_disp_frame.winfo_children():
            widget.destroy()

        # check if the value in selected x_variables or operation variable is in the new updated dataset
        for old_head_val in self.reg_x_axis:
            if not(old_head_val in df_headers_list_arg):
                self.reg_x_axis.remove(old_head_val)

        # iterate through list reg_x_axis where x axis variable are stored and call 
        # function AddValueToVarList to add new label displaying varibale names in the frame
        for val in self.reg_x_axis:
            self.AddValueToVarList(val, "X")

 
    def RefreshYVarSelectionList(self, df_header_list_arg):
        for widget in self.yaxis_var_disp_frame.winfo_children():
                widget.destroy()

        if self.reg_y_axis in df_header_list_arg:
            self.AddValueToVarList(self.reg_y_axis, "Y")



    def AddValueToVarList(self, text_param, axis):
        # add new label widgets 
        if axis == "X":
            if not(text_param == '') or not(text_param == None):
                new_label = ttk.Label(self.xaxis_var_disp_frame, text = text_param)
                new_label.pack(fill = X)
        elif axis == "Y":
            if not(text_param == '') or not(text_param == None):
                new_label = ttk.Label(self.yaxis_var_disp_frame, text = text_param)
                new_label.pack(fill = X)



    def initResultPanel(self):
        # Result panle viewport is the viewport where the results of operation (i.e Tables, Plot, Stat result ) are displayed
        self.result_panel = ttk.PanedWindow(
            self.app, orient = HORIZONTAL, 
            height = self.main_ui_height, 
            width = self.main_ui_width - self.tool_menu_frame_width)

        # mact | main activity window
        self.mact_panel.add(self.result_panel)



    def InitDataFrameEditorMenuFrame(self):
        # This method handles UI for Dataframe manipulation
        self.df_editing_tool_menu_frame = ttk.Frame(
            self.tool_menu_canvas,
            height = self.main_ui_height, 
            width = self.tool_menu_frame_width
            )


        # create a basic widget group of confirmation button, Menu button and -
        # a lable for selecting normalization functions
        new_normalization_func_menu = self.grouped_widgets.create_basic_label_menu_options(
            style_arg = 'tool_lframe.TFrame', 
            frame_parent_arg = self.df_editing_tool_menu_frame,
            label_txt_label = "Normalization Methods", 
            btn_text_label = "Not Normalized", 
            menu_value_arg = ["Not Normalized", "max abs scaling", "min max scaling", "z-score scaling"]
            )
        normalization_func_menu_frame = new_normalization_func_menu["root_frame"]
        max_abs_normalize_strvar = new_normalization_func_menu["str_var"]

        apply_normalize_btn = ttk.Button(
            normalization_func_menu_frame, 
            text = "Apply Normalize",
            command = lambda: self.UpdateDataFrameEditorResultFrame(
                lgb.get_normalized_df(
                    max_abs_normalize_strvar.get(),
                    self.dataset,
                    self.reg_x_axis,
                    )
                )
        )

        # create button to remove columns selected in operation list
        drop_col_btn = ttk.Button(
            self.df_editing_tool_menu_frame,
            text = "Drop Selected Columns",
            command = lambda: self.UpdateDataFrameEditorResultFrame(
                lgb.DFOperation().drop_col(self.dataset, self.reg_x_axis)
                )
            )



        # create a basic menu for showing basic information
        new_show_df_info_menu = self.grouped_widgets.create_basic_label_menu_options(
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
        new_show_df_summary_menu = self.grouped_widgets.create_basic_label_menu_options(
            style_arg = 'tool_lframe.TFrame', 
            frame_parent_arg = self.df_editing_tool_menu_frame, 
            label_txt_label = "Show Summary", 
            btn_text_label = "None Selected", 
            menu_value_arg = ["None Selected", "Sum", "CumSum", "Min", "Max", "Describe", "Mean", "Median"]
            )

        show_df_summary_menu_frame = new_show_df_summary_menu["root_frame"]
        show_df_summary_menu_strvar = new_show_df_summary_menu["str_var"]

        confirm_show_df_summary_btn = ttk.Button(
            show_df_summary_menu_frame, 
            text = "Show Summary",
            command = lambda: self.df_table_text_space.insert("1.0", lgb.get_df_summary(show_df_summary_menu_strvar.get(), self.dataset))
            )


        # create a basic menu for sorting and Ranking
        new_sort_rank_df_menu = self.grouped_widgets.create_basic_label_menu_options(
            style_arg = 'tool_lframe.TFrame', 
            frame_parent_arg = self.df_editing_tool_menu_frame, 
            label_txt_label = "Sort & Rank", 
            btn_text_label = "None Selected", 
            menu_value_arg = ["None Selected", "Sort Index", "Rank"]
            )

        sort_rank_df_menu_frame = new_sort_rank_df_menu["root_frame"]
        sort_rank_df_menu_strvar = new_sort_rank_df_menu["str_var"]

        confirm_sort_rank_df_btn = ttk.Button(
            sort_rank_df_menu_frame, 
            text = "Confirm",
            command = lambda: self.UpdateDataFrameEditorResultFrame(
                    lgb.sort_rank_df(sort_rank_df_menu_strvar.get(), self.dataset)
                )
            )


        # create a button to fill cell with value Nan or have no value
        fill_df_nanval_btn = ttk.Button(
            self.df_editing_tool_menu_frame,
            text = "Fill Nan value with 0",
            command = lambda: self.UpdateDataFrameEditorResultFrame(
                self.dataset.fillna(0)
                )
            )


        # create a button to reset dataset back to original file
        restore_orig_df_btn = ttk.Button(
            self.df_editing_tool_menu_frame,
            text = "Restore Original Dataset",
            style = "orange_btntheme.TButton",
            command = lambda: self.UpdateDataFrameEditorResultFrame(
                self.dataset_backup_copy
                )
            )


        # create button to refresh the dataset when the table was edited manually
        refresh_data_frame_btn = ttk.Button(
            self.df_editing_tool_menu_frame,
            text = "Refresh Changes",
            style = "orange_btntheme.TButton",
            command = lambda: self.UpdateVarSelectionFrame()
            )


        normalization_func_menu_frame.pack(fill = X, pady = self.tool_menu_pady)
        apply_normalize_btn.pack(side = RIGHT, fill = X, padx = self.tool_menu_padx)

        show_df_info_menu_frame.pack(fill = X, pady = self.tool_menu_pady)
        confirm_show_df_info_btn.pack(side = RIGHT, fill = X, padx = self.tool_menu_padx)

        show_df_summary_menu_frame.pack(fill = X, pady = self.tool_menu_pady)
        confirm_show_df_summary_btn.pack(side = RIGHT, fill = X, padx = self.tool_menu_padx)

        sort_rank_df_menu_frame.pack(fill = X, pady = self.tool_menu_pady)
        confirm_sort_rank_df_btn.pack(side = RIGHT, fill = X, padx = self.tool_menu_padx)

        fill_df_nanval_btn.pack(fill = X, pady = self.tool_menu_pady, ipady = self.btn_height)

        drop_col_btn.pack(fill = X, pady = self.tool_menu_pady, ipady = self.btn_height)

        restore_orig_df_btn.pack(side = BOTTOM, fill = X, pady = self.tool_menu_pady, ipady = self.btn_height)
        refresh_data_frame_btn.pack(side = BOTTOM, fill = X, pady = self.tool_menu_pady, ipady = 4)
      

    # function name deprecated from updateToolMenuFrameWidth to oneventScrollUpdateMenuPanelWidth
    def oneventScrollUpdateMenuPanelWidth(self, event):
        # Update dataframe_editor_tool_menu_frame width when the paned window changes
        btns_to_slidebar_margin = 20
        new_width = event.width
        self.tool_menu_canvas.itemconfig(self.canvas_frame, width = new_width - btns_to_slidebar_margin)

    # function name deprecated from updateVarSelectPanelWidth to oneventScrollUpdateVarSelectPanelWidth
    def oneventScrollUpdateVarSelectPanelWidth(self, event):
        btns_to_slidebar_margin = 20
        new_width = event.width
        self.variable_selection_canvas.itemconfig(self.varselect_canvas_frame, width = new_width - btns_to_slidebar_margin)
    

    def initSideBarPanelWidth(self):
        sidebar_width = self.side_bar_panel.winfo_width()
        self.tool_menu_canvas.itemconfig(self.canvas_frame, width = sidebar_width)
        self.variable_selection_canvas.itemconfig(self.varselect_canvas_frame, width = sidebar_width)



    def InitDataFrameEditorResultPanel(self):
        # crete the Result viewport fot the data frame table

        new_df_table_result_frame = self.grouped_widgets.create_window_and_textspace_panel(
            parent_root_frame = self.result_panel, 
            height_arg = self.main_ui_height, 
            width_arg = self.tool_menu_frame_width
            )

        self.df_table_result_panel = new_df_table_result_frame["parent_panel"]
        self.df_table_plotting_panel = new_df_table_result_frame["empty_panel"]
        self.df_table_text_panel = new_df_table_result_frame["text_output_panel"]
        self.df_table_text_space = new_df_table_result_frame["text_output_display"]



    def UpdateVarSelectionFrame(self):
        # update the variable sectection frame
        # change frame to dataframe editinga frame
        

        # get the dataframe displayed in the table
        update_df = self.pt.model.df

        # set new dataframe
        self.dataset = update_df

        # update list of dataframe headers
        self.df_headers = tuple(update_df.columns)


        # remove the variable select frame re initizlize and display again

        self.InitVarSelectSubMenuFrame()
        

        self.RefreshXVarSelectionList(update_df.columns)
        self.RefreshYVarSelectionList(update_df.columns)

        self.OpenVariableSelectionPanel(True)
        self.UpdateSideMenuDisp("df_editor_frame")


 
    def UpdateDataFrameEditorResultFrame(self, df):
        # ouput the tabulated display of the dataframe
        self.dataset = df
        
        self.pt = Table(self.df_table_plotting_panel, dataframe=df, showtoolbar=False, showstatusbar=True)
        options = {'colheadercolor':'black','floatprecision': 5}
        config.apply_options(options, self.pt)
       
        self.pt.show()
        
        self.UpdateVarSelectionFrame()
        

 
    def OpenDataset(self, row_skip):
        data_return = lgb.FileSys().open_dataset_by_file(row_skip)

        if type(data_return) != type(None):
            # if opening new file reset user selected variable
            self.reg_x_axis.clear()
            # set the opened dataset to a variable
            self.dataset = data_return
            # create a copy of the dataset
            self.dataset_backup_copy = data_return.copy()
            # get the headers and convert to tuple then store in variable
            # this headers will be used for selecting in variable selection menu
            self.df_headers = tuple(self.dataset.columns)
            
            # update the table
            self.UpdateDataFrameEditorResultFrame(self.dataset)
            self.UpdateVarSelectionFrame()
            self.notif_panel_update_manager.create_bnotif("N", "File opened succesfully")



        elif type(data_return) == type(None):
            self.notif_panel_update_manager.create_bnotif("W", "No file selected")
            
 
 
    def InitMMREGToolMenuFrame(self):
        # create the main frame or a root frame of the tool menu for multiple linear regresssion
        self.mmreg_tool_menu_submenu_frame = ttk.Frame(
            self.tool_menu_canvas,
            padding = 1,
            height = self.main_ui_height,
            width = self.tool_menu_frame_width,
            #style = 'tool_lframe.TLabelframe'
            )

        # create menu button for selecting MMREG fit intercetp parameter
        new_fit_intcept_param_menu_widgets = self.grouped_widgets.create_labeledmenu_menu(
            root_frame = self.mmreg_tool_menu_submenu_frame,
            menu_value_arg = ["True", "False"],
            menu_text_label = "Default Val: True",
            label_text_label = "Fit Intercept"
            ) 

        fit_intcept_param_parent_frame = new_fit_intcept_param_menu_widgets["parent_frame"]
        fit_intcept_param_strvar = new_fit_intcept_param_menu_widgets["string_var"]


        # create menu button for forcing coef to be positive
        new_positive_coef_mmreg_param_menu_widgets = self.grouped_widgets.create_labeledmenu_menu(
            root_frame = self.mmreg_tool_menu_submenu_frame,
            menu_value_arg = ["True", "False"],
            menu_text_label = "Default Val: False",
            label_text_label = "Force Positive Coef"
            )  

        positive_coef_mmreg_param_parent_frame = new_positive_coef_mmreg_param_menu_widgets["parent_frame"]
        positive_coef_mmreg_param_strvar = new_positive_coef_mmreg_param_menu_widgets["string_var"]


        # create entry widget for selecting MMREG njob parameter
        new_njob_mmreg_param_menu = self.grouped_widgets.create_labeledentry_menu(
            root_frame = self.mmreg_tool_menu_submenu_frame, 
            label_text_label = "Number of Jobs"
            )

        njob_param_strvar = new_njob_mmreg_param_menu["string_var"]
        njob_param_frame = new_njob_mmreg_param_menu["parent_frame"]


        # create menu button for selecting MMREG normalize parameter
        new_mmreg_normalize_func_menu_widgets = self.grouped_widgets.create_labeledmenu_menu(
            root_frame = self.mmreg_tool_menu_submenu_frame,
            menu_value_arg = ["StatModel", "ScikiLearn"],
            menu_text_label = "Default Val: StatModel",
            label_text_label = "Stats Result Output"
            )  

        stat_output_mmreg_param_parent_frame = new_mmreg_normalize_func_menu_widgets["parent_frame"]
        stat_output_mmreg_param_strvar = new_mmreg_normalize_func_menu_widgets["string_var"]


        ## PLOTTING MWNE OPTIONS ##
        # create a menu for entering plot title
        new_mmreg_plot_title_menu = self.grouped_widgets.create_labeled_text_entry(
            root_frame = self.mmreg_tool_menu_submenu_frame,
            frame_text_label = "Plot Title",
            hover_text = "Add title to the plot"
            )

        mmreg_plot_title_entry_frame = new_mmreg_plot_title_menu["parent_frame"]
        mmreg_plot_title_string_var = new_mmreg_plot_title_menu["string_var"]

        # create a menu for entering plot x label
        new_mmreg_plot_xlabel_menu = self.grouped_widgets.create_labeled_text_entry(
            root_frame = self.mmreg_tool_menu_submenu_frame,
            frame_text_label = "X axis Label",
            hover_text = "Add title to the X axis"
            )

        mmreg_plot_xlabel_entry_frame = new_mmreg_plot_xlabel_menu["parent_frame"]
        mmreg_plot_xlabel_string_var = new_mmreg_plot_xlabel_menu["string_var"]

        # create a menu for entering plot y label
        new_mmreg_plot_ylabel_menu = self.grouped_widgets.create_labeled_text_entry(
            root_frame = self.mmreg_tool_menu_submenu_frame,
            frame_text_label = "Y axis Label",
            hover_text = "Add title to the Y axis"
            )

        mmreg_plot_ylabel_entry_frame = new_mmreg_plot_ylabel_menu["parent_frame"]
        mmreg_plot_ylabel_string_var = new_mmreg_plot_ylabel_menu["string_var"]


        # Button that update the Multiple linear regression plot and stat result
        diplay_plot_btn = ttk.Button(
            self.mmreg_tool_menu_submenu_frame, 
            text = "Refresh Plot Output", 
            style = "orange_btntheme.TButton",
            command = lambda: self.MMREGUpdateResultOutputPlot(
                fit_intercept_param = fit_intcept_param_strvar.get(),
                positive_coef_param = positive_coef_mmreg_param_strvar.get(),
                njob_param = njob_param_strvar.get(),
                stat_ouput_source = stat_output_mmreg_param_strvar.get(),
                plot_title = mmreg_plot_title_string_var.get(),
                plot_xaxis_label = mmreg_plot_xlabel_string_var.get(),
                plot_yaxis_label = mmreg_plot_ylabel_string_var.get()
                ))


        # mmreg_tool_menu_submenu_frame grid layout
        fit_intcept_param_parent_frame.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady)
        njob_param_frame.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady)
        stat_output_mmreg_param_parent_frame.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady)
        positive_coef_mmreg_param_parent_frame.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady)

        mmreg_plot_title_entry_frame.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady)
        mmreg_plot_xlabel_entry_frame.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady)
        mmreg_plot_ylabel_entry_frame.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady)

        diplay_plot_btn.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady, ipady = self.btn_height)
        


    def InitMMREGResultFrame(self):
        ## Multiple Linear regression result frame ##
        new_mmreg_result_multiPanels = self.grouped_widgets.create_window_and_textspace_panel(
            parent_root_frame = self.result_panel, 
            height_arg = self.main_ui_height, 
            width_arg = self.tool_menu_frame_width
            )

        self.mmreg_result_panel = new_mmreg_result_multiPanels["parent_panel"]
        self.mmreg_res_plot_panel = new_mmreg_result_multiPanels["empty_panel"]
        self.mmreg_res_text_panel = new_mmreg_result_multiPanels["text_output_panel"]
        self.MMREG_stat_res_text_space = new_mmreg_result_multiPanels["text_output_display"]
        


    def MMREGUpdateResultOutputPlot(self, fit_intercept_param, positive_coef_param, njob_param, stat_ouput_source, plot_title, plot_xaxis_label, plot_yaxis_label):
        # check variable valur
        self.setSeabornPlotSysDefault()
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
            njob_arg = njob_param,
            slice_index_from = self.df_row_slice_selection_string_var_01.get(),
            slice_index_to = self.df_row_slice_selection_string_var_02.get()
            )


        x_axis = mmreg_output_axis[0]
        y_axis = mmreg_output_axis[1]

        fig = Figure(figsize=(5, 4), dpi=100)
        ax1 = fig.subplots()

        
        # plot the value
        sns.regplot(
            x = x_axis, 
            y = y_axis , 
            ci=None, 
            ax = ax1
            ).set(
                xlabel = plot_xaxis_label, 
                ylabel = plot_yaxis_label, 
                title = plot_title
                )

        # add the plot and the tool control of matplotlib to the mmreg_res_plot_panel
        canvas = FigureCanvasTkAgg(fig, master = self.mmreg_res_plot_panel) 
        canvas.draw()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self.mmreg_res_plot_panel)
        toolbar.config(background="#212121")
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

        self.notif_panel_update_manager.create_bnotif("N", "Multiple Linear Regression Plot refreshed")
        

   
    def InitCorellationMatrixToolMenuFrame(self):
        self.corl_matrix_menu_submenu_frame = ttk.Frame(
            self.tool_menu_canvas,
            height = self.main_ui_height,
            width = self.tool_menu_frame_width
            )


        corlmatrix_plot_title_menu = self.grouped_widgets.create_labeled_text_entry(
            root_frame = self.corl_matrix_menu_submenu_frame,
            frame_text_label = "Plot Title",
            hover_text = "Add title text to  plot"
            )

        corlmatrix_plot_input_frame = corlmatrix_plot_title_menu["parent_frame"]
        corlmatrix_plot_input_string_var = corlmatrix_plot_title_menu["string_var"]


        refresh_corl_maatrix_plot = ttk.Button(
            self.corl_matrix_menu_submenu_frame, 
            text = "Refresh Correlation Matrix Output",
            style = "orange_btntheme.TButton",
            command = lambda: self.UpdateCorrelationMatrixResultFrame(corlmatrix_plot_input_string_var.get()))
        

        corlmatrix_plot_input_frame.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady, ipady = self.btn_height)
        refresh_corl_maatrix_plot.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady, ipady = self.btn_height)


   
    def InitCorrelationMatrixResultFrame(self):
        new_corl_matrix_result_multiPanels = self.grouped_widgets.create_window_and_textspace_panel(
            parent_root_frame = self.result_panel, 
            height_arg = self.main_ui_height, 
            width_arg = self.tool_menu_frame_width
            )

        self.corl_matrix_result_panel = new_corl_matrix_result_multiPanels["parent_panel"]
        self.corl_matrix_plotting_panel = new_corl_matrix_result_multiPanels["empty_panel"]
        self.corl_text_output_disp_widget = new_corl_matrix_result_multiPanels["text_output_display"]


 
    def UpdateCorrelationMatrixResultFrame(self, plot_title = ""):
        self.setSeabornPlotSysDefault()
        for widget in self.corl_matrix_plotting_panel.winfo_children():
            widget.destroy()


        #plt.style.use("dark_background")
        fig = Figure(figsize=(5, 4), dpi=100)
        ax1 = fig.subplots()

        corrMatrix = self.dataset[self.reg_x_axis].corr()
        sns.heatmap(corrMatrix, annot=True, ax = ax1).set(title = plot_title)

        # add the plot and the tool control of matplotlib to the mmreg_res_plot_panel
        canvas = FigureCanvasTkAgg(fig, master = self.corl_matrix_plotting_panel) 
        canvas.draw()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self.corl_matrix_plotting_panel)
        toolbar.update()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

        
 
    def InitLogisticRegToolMenuFrame(self):
        self.logistic_reg_menu_submenu_frame = ttk.Frame(
                self.tool_menu_canvas,
                padding = 1,
                height = self.main_ui_height,
                width = self.tool_menu_frame_width
            )


        plot_themes_menu = self.grouped_widgets.create_menu_btn(
            frame_parent_arg = self.logistic_reg_menu_submenu_frame, 
            mbtn_text_display = "Variables",
            menu_value_arg = self.SEABORN_PLOT_THEMES
            )

        plot_theme_mnu_btn = plot_themes_menu["menu_button"]
        plot_theme_string_var = plot_themes_menu["string_var"]


        logreg_plot_title_menu = self.grouped_widgets.create_labeled_text_entry(
                root_frame = self.logistic_reg_menu_submenu_frame,
                frame_text_label = "Plot Title",
                hover_text = "Add title text to  plot"
            )

        logreg_plot_title_frame = logreg_plot_title_menu["parent_frame"]
        logreg_plot_title_string_var = logreg_plot_title_menu["string_var"]



        refresh_logistic_reg_plot = ttk.Button(
                self.logistic_reg_menu_submenu_frame, 
                text = "Refresh Logistic Regression Output",
                style = "orange_btntheme.TButton",
                command = lambda: self.UpdateLogisticRegResultFrame(plot_theme_string_var.get(), logreg_plot_title_string_var.get())
            )
        

        plot_theme_mnu_btn.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady, ipady = self.btn_height)
        logreg_plot_title_frame.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady, ipady = self.btn_height)
        refresh_logistic_reg_plot.pack(fill = X, padx = self.tool_menu_padx, pady = self.tool_menu_pady, ipady = self.btn_height)
        


  
    def InitLogisticRegResultFrame(self):
        new_logistic_reg_result_multiPanels = self.grouped_widgets.create_window_and_textspace_panel(
            parent_root_frame = self.result_panel, 
            height_arg = self.main_ui_height, 
            width_arg = self.tool_menu_frame_width
            )

        self.logistic_reg_result_panel = new_logistic_reg_result_multiPanels["parent_panel"]
        self.logistic_reg_plotting_panel = new_logistic_reg_result_multiPanels["empty_panel"]
        self.logistic_reg_output_disp_widget = new_logistic_reg_result_multiPanels["text_output_display"]
    


    def UpdateLogisticRegResultFrame(self, plot_theme, plot_title = ""):
        for widget in self.logistic_reg_plotting_panel.winfo_children():
            widget.destroy()

        if plot_theme in self.SEABORN_PLOT_THEMES:
            if plot_theme == "App Default":
                self.setSeabornPlotSysDefault()
            elif plot_theme != "App Default":
                sns.set_style(plot_theme)

        #plt.style.use("dark_background")
        fig = Figure(figsize=(5, 4), dpi=100)
        ax1 = fig.subplots()

        sns.regplot(
            x = self.dataset[self.reg_x_axis[0]], 
            y = self.dataset[self.reg_y_axis], 
            data = self.dataset, 
            logistic = True, 
            ci = None, 
            ax = ax1).set(title = plot_title)

        print("Logistic regression x var: ", self.reg_x_axis[0])

        # add the plot and the tool control of matplotlib to the logistic_reg_plotting_panel
        canvas = FigureCanvasTkAgg(fig, master = self.logistic_reg_plotting_panel) 
        canvas.draw()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self.logistic_reg_plotting_panel)
        toolbar.update()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)



    def OpenVariableSelectionPanel(self, call_state_open = bool):
        if call_state_open == True:
            self.varselect_canvas_frame = self.variable_selection_canvas.create_window(0, 0, anchor = "nw", window = self.variable_selection_frame)

            self.variable_selection_canvas.update_idletasks()
            self.variable_selection_canvas.configure(scrollregion = self.variable_selection_canvas.bbox("all"),
                                                    yscrollcommand = self.var_selectn_panel_scroll_bar.set)
            self.variable_selection_canvas.bind("<Configure>", self.oneventScrollUpdateVarSelectPanelWidth)
        elif call_state_open == False:
            self.variable_selection_canvas.delete("all")


    def OpenDataFrameEditorFrame(self, action_state_open = bool):
        #self.df_editing_tool_menu_canva
        if action_state_open:
            self.mpannel_vsblty_state["df_editor_frame"] = True 
            self.result_panel.add(self.df_table_result_panel)
            self.OpenVariableSelectionPanel(True)
            self.canvas_frame = self.tool_menu_canvas.create_window(0, 0, anchor = "nw", window = self.df_editing_tool_menu_frame)
        elif not action_state_open:
            self.mpannel_vsblty_state["df_editor_frame"] = False
            self.OpenVariableSelectionPanel(False)
            self.result_panel.remove(self.df_table_result_panel)
            self.tool_menu_canvas.delete("all")
            

            
    def OpenMMREGFrame(self, action_state_open = bool):
        if action_state_open:
            self.mpannel_vsblty_state["mmreg_frame"] = True
            self.OpenVariableSelectionPanel(True)
            self.result_panel.add(self.mmreg_result_panel)
            self.canvas_frame = self.tool_menu_canvas.create_window(0, 0, anchor = "nw", window = self.mmreg_tool_menu_submenu_frame)
        elif not action_state_open:
            self.mpannel_vsblty_state["mmreg_frame"] = False
            self.OpenVariableSelectionPanel(False)
            self.result_panel.remove(self.mmreg_result_panel)
            self.tool_menu_canvas.delete("all")



    def OpenCorrelMatrixFrame(self, action_state_open = bool):
        if action_state_open:
            self.mpannel_vsblty_state["corl_matrix_frame"] = True
            self.OpenVariableSelectionPanel(True)
            self.result_panel.add(self.corl_matrix_result_panel)
            self.canvas_frame = self.tool_menu_canvas.create_window(0, 0, anchor = "nw", window = self.corl_matrix_menu_submenu_frame)
        elif not action_state_open:
            self.mpannel_vsblty_state["corl_matrix_frame"] = False
            self.OpenVariableSelectionPanel(False)
            self.result_panel.remove(self.corl_matrix_result_panel)
            self.tool_menu_canvas.delete("all")


      
    def OpenLogisticRegFrame(self, action_state_open = bool):
        if action_state_open:
            self.mpannel_vsblty_state["logistic_reg_frame"] = True
            self.OpenVariableSelectionPanel(True)
            self.result_panel.add(self.logistic_reg_result_panel)
            self.canvas_frame = self.tool_menu_canvas.create_window(0, 0, anchor = "nw", window = self.logistic_reg_menu_submenu_frame)
        elif not action_state_open:
            self.mpannel_vsblty_state["logistic_reg_frame"] = False
            self.OpenVariableSelectionPanel(False)
            self.result_panel.remove(self.logistic_reg_result_panel)
            self.tool_menu_canvas.delete("all")

    
    def UpdateSideMenuDisp(self, btn_click_arg):
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
                    self.OpenDataFrameEditorFrame(False)
                
                if frame == "mmreg_frame" and self.mpannel_vsblty_state[frame] == True and btn_click_arg != "mmreg_frame":
                    self.OpenMMREGFrame(False)

                if frame == "corl_matrix_frame" and self.mpannel_vsblty_state[frame] == True and btn_click_arg != "corl_matrix_frame":
                    self.OpenCorrelMatrixFrame(False)
            
                if frame == "logistic_reg_frame" and self.mpannel_vsblty_state[frame] == True and btn_click_arg != "logistic_reg_frame":
                    self.OpenLogisticRegFrame(False)


            # handle if frame is shown already, if not Show
            if btn_click_arg == "df_editor_frame" and self.mpannel_vsblty_state["df_editor_frame"] == False:
                self.OpenDataFrameEditorFrame(True)

            elif btn_click_arg == "mmreg_frame" and self.mpannel_vsblty_state["mmreg_frame"] == False:
                self.OpenMMREGFrame(True)

            elif btn_click_arg == "corl_matrix_frame" and self.mpannel_vsblty_state["corl_matrix_frame"] == False:
                self.OpenCorrelMatrixFrame(True)

            elif btn_click_arg == "logistic_reg_frame" and self.mpannel_vsblty_state["logistic_reg_frame"] == False:
                self.OpenLogisticRegFrame(True)


            self.tool_menu_canvas.update_idletasks()
            self.tool_menu_canvas.configure(scrollregion = self.tool_menu_canvas.bbox("all"),
                                                    yscrollcommand = self.tool_menu_scroll_bar.set)
            self.tool_menu_canvas.bind('<Configure>', self.oneventScrollUpdateMenuPanelWidth)

            self.variable_selection_canvas.update_idletasks()
            self.variable_selection_canvas.configure(scrollregion = self.variable_selection_canvas.bbox("all"),
                                                    yscrollcommand = self.var_selectn_panel_scroll_bar.set)
            self.variable_selection_canvas.bind("<Configure>", self.oneventScrollUpdateVarSelectPanelWidth)
            
        self.initSideBarPanelWidth()
                
            
def Main():
    app = ThemedTk(theme="black")
    app_UI = ReGress(app)
    app_UI.InitApp()
    app.mainloop()


if __name__ == "__main__":
    Main()