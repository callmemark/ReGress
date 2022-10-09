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



class REG_PROC():
    def __init__(self, df_arg, df_headers, x_vars, y_var):
        self.df = df_arg
        self.y_sample = self.df[y_var]
        self.x_sample = self.df[x_vars]

        self.selected_var = x_vars
        
    def get_mmreg_prediction_plot(self, fit_intercept_arg, positive_coef_arg, njob_arg):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.x_sample, self.y_sample, test_size = 0.3, random_state = 0)

        self.lr_model = LinearRegression(
            fit_intercept = fit_intercept_arg,
            positive = positive_coef_arg,
            n_jobs = njob_arg,
            copy_X = False
            )

        self.lr_model.fit(self.X_train, self.y_train)
        self.y_pred = self.lr_model.predict(self.X_train)
        
        print("fit_intercept_arg : ", fit_intercept_arg, "\n", "positive_coef_arg: ", positive_coef_arg, "\n", "njob_arg", njob_arg)

        return [self.y_train, self.y_pred]
        
    
    def get_sklearn_mmreg_result(self):
        coef_data = [] 
        coef_res = self.lr_model.coef_

        try:
            for i in range(len(self.selected_var)):
                val_arr = [self.selected_var[i], coef_res[i]]
                coef_data.append(val_arr)

            result_df = pd.DataFrame(coef_data, columns = ["Variable", "Coef"])
        except:
            result_df = "Error processing in method - get_sklearn_mmreg_result"


        return result_df


    def get_mmreg_stat_result(self):
        _x = sm.add_constant(self.x_sample)
        model = sm.OLS(self.y_sample, _x).fit()
        predictions = model.predict(_x) 
        reg_ressult = model.summary()
        
        return reg_ressult

    def debug_print(self):
        print("Selected X = ", self.x_sample, " \n ", "Selected Y = ", self.y_sample)



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

                showinfo(
                    title ='Status',
                    message = "File opened sucesfully"
                )

                return _df

            except:
                showinfo(
                    title ='Status',
                    message = "Failed to open file"
                )

                return None
