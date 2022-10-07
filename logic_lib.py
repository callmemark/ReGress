from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
import pandas as pd

import seaborn as sns
import numpy as np
        
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import linear_model

import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from pyprocessmacro import Process


class MMREG_PROC():
    def __init__(self, df_arg, df_headers, x_vars, y_var):
        self.df = df_arg
        self.y_sample = self.df[y_var]
        
        to_drop = []
        for val in df_headers:
            if not(val in x_vars):
                to_drop.append(val)

        self.x_sample = self.df.drop(to_drop, axis = 1)
        
    
    def get_mmreg_prediction_plot(self):
        self.lr_model = LinearRegression()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.x_sample, self.y_sample, test_size = 0.3, random_state = 0)
        self.lr_model.fit(self.X_train, self.y_train)
        self.y_pred = self.lr_model.predict(self.X_train)
    
        return [self.y_train, self.y_pred]

    def get_stat_result(self):
        _x = sm.add_constant(self.x_sample)
        model = sm.OLS(self.y_sample, _x).fit()
        predictions = model.predict(_x) 
        reg_ressult = model.summary()

        return reg_ressult

    def debug_print(self):
        print("Selected X = ", self.x_sample, " \n ", "Selected Y = ", self.y_sample)




class MMREG_PROCS():
  def __init__(self, main_df_arg, x_axis_drop = [], y_axis = str, drop_axis = 1, title_arg = "Data Analysis"):
    self.main_df = main_df_arg

    if len(x_axis_drop) == 0:
        raise Exception("Error : Empty x_axis parameter and x_axis_drop parameter")
    elif len(x_axis_drop) != 0:
      self.x_sample = main_df_arg.drop(x_axis_drop, axis = drop_axis)


    self.y_sample = main_df_arg[y_axis]
    self.proc_title = title_arg
   

  def get_init_val(self):
    print("X sample: ", self.x_sample)
    print("Y sample: ", self.y_sample)
  

  def standard_proc(self, _show_plot_arg = True):
    self.scikit_train_proc(show_plot_arg = _show_plot_arg)
    self.disp_res_header()
    self.scikit_proc()
    self.statmod_proc()

  
  def disp_res_header(self):
    print(("===" * 26), "'\n")
    print(self.proc_title.center(26, "="))


  def calc_pct(self):
    x_axis_pct_chage = pd.DataFrame(self.x_sample).pct_change()
    y_axis_pct_chage = pd.DataFrame(self.y_sample).pct_change()

    print(("===" * 26), "'\n")
    print("PCT: \n", x_axis_pct_chage, y_axis_pct_chage)
    print(("===" * 26), "'\n")
    return [x_axis_pct_chage, y_axis_pct_chage]


  def scikit_train_proc(self, test_size_arg = 0.3, random_state_arg = 0, show_plot_arg = True):
    self.lr_model = LinearRegression()
    self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.x_sample, self.y_sample, test_size = test_size_arg, random_state = random_state_arg)
    self.lr_model.fit(self.X_train, self.y_train)
    self.y_pred = self.lr_model.predict(self.X_train)
    
    if show_plot_arg:
      plt.scatter(self.y_train, self.y_pred, color = "black")
      sns.regplot(x = self.y_train, y = self.y_pred , ci=None, color ='orange')

      plt.style.use('seaborn-pastel')
      plt.ylabel("Factors")
      plt.xlabel("N.Time Temp")
      plt.title(self.proc_title)

      plt.show()
    
    return [self.y_train, self.y_pred]


  def scikit_proc(self):
    regr = linear_model.LinearRegression()
    fitted_model = regr.fit(self.x_sample, self.y_sample)
    print(("===" * 26), "'\n")
    print("SCIKIT LEARN RESULT: ")
    print("Intercept: ", fitted_model.intercept_)
    print('Coefficients: ', fitted_model.coef_)
    print()
    print(("===" * 26), "'\n")

    return fitted_model


  def statmod_proc(self):
    _x = sm.add_constant(self.x_sample)
 
    model = sm.OLS(self.y_sample, _x).fit()
    predictions = model.predict(_x) 
    
    reg_ressult = model.summary()
    print(reg_ressult)

    return reg_ressult
  

  def vif(self, print_output = True):
    _result = [variance_inflation_factor(self.x_sample.values, i) for i in range(len(self.x_sample.columns))]
    return _result
  

  def mod_reg(self, independent_var, dependent_var, mediator_variable = []):
    p = Process(
        data = self.main_df, 
        model = 4, x = independent_var, 
        y = dependent_var, 
        m = mediator_variable)
    
    p.summary()

    return p



class FileSys():
    def __init__(self):
        pass

    def open_dataset_by_file(self, row_skip):
        f_type = (
            ('csv files', '*.csv'),
            ('excel files', '*.xlx')
        )

        # This variable will hold the system file path of the dataset
        file_selected = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=f_type
        )

        if row_skip != '':
            row_skip_val = int(float(row_skip))
        elif row_skip == '':
            row_skip_val = 0

        if file_selected != None or file_selected != "":
            try:
                try:
                    _df = pd.read_csv(file_selected, skiprows = row_skip_val)
                except:
                    _df = pd.read_excel(file_selected, skiprows = row_skip_val)

                return _df

                showinfo(
                    title ='Status',
                    message = "File opened sucesfully"
                )
            except:
                showinfo(
                    title ='Status',
                    message = "Failed to open file"
                )
