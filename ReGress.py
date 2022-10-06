from doctest import master
from turtle import width
import pandas as pd
from pandastable import Table, config
import logic_lib as lgb

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog as fd



class ReGress():
    def __init__(self, application):
        self.app = application
        self.app.geometry("1000x600")

        self.main_ui_height = 600
        self.main_ui_width = 1000

        self.nav_frame_width = 240

        self.dataset = None
        self.df_headers = None

        # handles the visibility state of the side menu panel
        self.mpannel_vsblty_state = {
            "fselection_frame" : False,
            "mmreg_frame" : False
            }
        
        ## MMREG VARIABLES ##
        self.mmreg_x_axis = []
        self.mmreg_y_axis = None


    def init_app(self):
        self.init_tool_nav_frame()
        self.init_main_activity_panel()
        
        self.init_result_panel()
        self.init_tool_menu_panel()

        #self.MMREG_tool_menu_frame()
        self.file_selection_tool_menu_frame()
        self.file_selection_result_frame()

        


    def init_tool_nav_frame(self):
        # create the header navigation panel
        head_nav_frame = Frame(height = 40, width = self.main_ui_width)
        head_nav_frame.pack(side=TOP,fill = X)
        
        skipind_lbl = Label(head_nav_frame, text = "skip rows: ")
        row_skip_inp_val = StringVar()
        skip_ind_entry = Entry(head_nav_frame, textvariable = row_skip_inp_val, width = 10)
        
        select_data_set_btn = Button(head_nav_frame, text = "Open", command = lambda: self.open_dataset(row_skip_inp_val.get()))
        #select_data_set_btn.pack(side=LEFT)


        tools_lbl = Label(head_nav_frame, text = "Tools ")

        # create a button in top navigation panel for multitple linear regression options
        file_manage_tab_btn = Button(head_nav_frame, text = "file sys", command = lambda: self.update_side_menu_view("fselection_frame"))
        
        # create a button in top navigation panel for multitple linear regression options
        mmreg_tab_btn = Button(head_nav_frame, text = "MMREG", command = lambda: self.update_side_menu_view("mmreg_frame"))
        
        # create a button in top navigation panel for creating a matrix relationship options
        matrix_tab_btn = Button(head_nav_frame, text = "Matrix", command = lambda: self.update_side_menu_view("matrix_btn"))
        
        # create a button in top navigation panel for mediator regression
        med_reg_tab_btn = Button(head_nav_frame, text = "MedReg", command = lambda: self.update_side_menu_view("med_reg_btn"))
       
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
        mact_viewport_style = Style().configure(
            "proc_vp.TFrame",
            background = "red"
            )
        self.mact_panel = PanedWindow(self.app, orient = HORIZONTAL, style = "proc_vp.TFrame", height = self.main_ui_height, width = self.main_ui_width)
        self.mact_panel.pack(fill = BOTH, expand = True)

    def init_tool_menu_panel(self):
        side_nav_style = Style().configure(
            "isde_nav.TFrame",
            background = "yellow"
            )
        self.tool_menu_panel = PanedWindow(self.app, orient = HORIZONTAL, style = "isde_nav.TFrame", height = self.main_ui_height, width = self.nav_frame_width)
        self.mact_panel.add(self.tool_menu_panel)
 
    def init_result_panel(self):
        proc_viewport_style = Style().configure(
            "proc_vp.TFrame",
            background = "green"
            )
        self.result_panel = PanedWindow(self.app, orient = HORIZONTAL, style = "proc_vp.TFrame", height = self.main_ui_height, width = self.main_ui_width - self.nav_frame_width)
        self.mact_panel.add(self.result_panel)


    def file_selection_tool_menu_frame(self):
        # This side selection is under the frame handles opening files
        # create a button in top navigation panel to select dataset file
        self.fselect_frame = Frame(self.tool_menu_panel, height = self.main_ui_height, width = self.nav_frame_width)
        
        stmf_title = Label(self.fselect_frame, text = "File Selection Tool")
        stmf_title.grid(row = 0, column = 0,  sticky = W, pady = 25)


    def file_selection_result_frame(self):
        self.fslctn_result_frame = Frame(self.result_panel, height = self.main_ui_height, width = self.nav_frame_width)

        
    def update_file_selection_result_frame(self, df):
        self.df_table = pt = Table(self.fslctn_result_frame, dataframe=df, showtoolbar=True, showstatusbar=True)
        pt.show()
        options = {'colheadercolor':'green','floatprecision': 5}
        config.apply_options(options, pt)

        pt.show()


    def MMREG_tool_menu_frame(self):
        self.mmreg_frame = Frame(self.tool_menu_panel, height = self.main_ui_height, width = self.nav_frame_width)
        
        mmregf_title = Label(self.mmreg_frame, text = "Multuple Linear Regression")


        menu_label = Label(self.mmreg_frame, text = "X axis variables")
        # Create a menu button listing all the variables in the dataframe
        selected_var = StringVar()
        x_axis_col_slctn_btn = Menubutton(self.mmreg_frame, text = "Headers")
        x_axis_col_slctn_menu = Menu(x_axis_col_slctn_btn,tearoff=0)

        # create options for menu
        for col_name in self.df_headers:
            x_axis_col_slctn_menu.add_radiobutton(label = col_name, value = col_name, variable = selected_var)

        x_axis_col_slctn_btn["menu"] = x_axis_col_slctn_menu
        
        assign_col_btn = Button(self.mmreg_frame, text = "Add to X-Axis", command = lambda: self.update_mmreg_xaxis(add = True, val = selected_var.get()))
        unassign_col_btn = Button(self.mmreg_frame, text = "remove to X-Axis", command = lambda: self.update_mmreg_xaxis(add = False, val = selected_var.get()))


        mmregf_title.grid(row = 0, column = 0,  sticky = W, pady = 25)
        menu_label.grid(row = 1, column = 0,  sticky = W, pady = 2)
        x_axis_col_slctn_btn.grid(row = 1, column = 1,  sticky = W, pady = 2)
        assign_col_btn.grid(row = 2, column = 0,  sticky = W, pady = 2)
        unassign_col_btn.grid(row = 2, column = 1,  sticky = W, pady = 2)


    def update_mmreg_xaxis(self, add = True, val = "str"):
        if add and not(val in self.mmreg_x_axis):
            self.mmreg_x_axis.append(val)
        elif not add and val in self.mmreg_x_axis:
            self.mmreg_x_axis.remove(val)

        print(self.mmreg_x_axis)


    def open_dataset(self, row_skip):
        self.dataset = lgb.FileSys().open_dataset_by_file(row_skip)
        self.df_headers = tuple(self.dataset.columns)
        self.update_file_selection_result_frame(self.dataset)

        self.MMREG_tool_menu_frame()


    def update_side_menu_view(self, btn_click_arg):
        # This funtion handles what to hide and shown  in side menu frame
        # This function is called by nav button in head selection panel
        # btn_click_arg is a string to determine what frame shoud be shown

        # get the keys of the frame state
        frames_key = self.mpannel_vsblty_state.keys()

        # loop through the dictionary for open frame and hide it
        
        for frame in frames_key:
            if frame == "fselection_frame" and self.mpannel_vsblty_state[frame] == True:
                self.mpannel_vsblty_state["fselection_frame"] = False
                self.tool_menu_panel.remove(self.fselect_frame)
                self.result_panel.remove(self.fslctn_result_frame)

            if frame == "mmreg_frame" and self.mpannel_vsblty_state[frame] == True:
                self.mpannel_vsblty_state["mmreg_frame"] = False
                self.tool_menu_panel.remove(self.mmreg_frame)
                self.result_panel.remove(self.fslctn_result_frame)

        # handle if frame is shown already, if not. Show
        if btn_click_arg == "fselection_frame":
            if self.mpannel_vsblty_state["fselection_frame"] == False:
                self.mpannel_vsblty_state["fselection_frame"] = True 
                self.tool_menu_panel.add(self.fselect_frame)
                self.result_panel.add(self.fslctn_result_frame)

        elif btn_click_arg == "mmreg_frame":
            if self.mpannel_vsblty_state["mmreg_frame"] == False:
                self.mpannel_vsblty_state["mmreg_frame"] = True 
                self.tool_menu_panel.add(self.mmreg_frame)
                self.result_panel.add(self.fslctn_result_frame)



def main():
    app = Tk()
    app_UI = ReGress(app)
    app_UI.init_app()
    app.mainloop()



if __name__ == "__main__":
    main()