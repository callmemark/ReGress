from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
import pandas as pd

import seaborn as sns
import numpy as np
        
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import linear_model

import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from pyprocessmacro import Process



class MMREG_PROC():
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
    



class LOGISTIC_REG():
    def __init__(self, df_arg, df_headers_arg, x_vars, y_var):
        self.df = df_arg
        self.df_headers = df_headers_arg
        self.X = df_headers[list(x_vars)]
        self.y = df_headers[y_var]

    def get_logistic_regression_result():
        # cretae instance of logistic regressin
        self.logistic_reg_model = LogisticRegression(solver='liblinear', random_state=0).fit(self.X, self.y)
        self.logistic_reg_model.intercept_
        self.logistic_reg_model.coef_
        self.logistic_reg_model.predict_proba(self.X)
        self.model.predict(self.X)



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



class NormalizationMethods():
    def __init__(self):
        pass

    def max_abs_scaling(self, df, column_name_arg):
        df = df.copy()
        for column in column_name_arg:
            df[column] = df[column] / df[column].abs().max()

        return df

    def min_max_scaling(self, df, column_name_arg):
        df = df.copy()

        for column in column_name_arg:
            df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min()) 

        return df
    
    def z_score_scaling(self, df, column_name_arg):
        df = df.copy()

        for column in column_name_arg:  
            df[column] = (df[column] - df[column].mean()) / df[column].std()    

        return df


def get_normalized_df(method_arg, df_arg, column_applied_arg):
    init_NM = NormalizationMethods()

    if method_arg == "max abs scaling":
        return init_NM.max_abs_scaling(df_arg, column_applied_arg)
    elif method_arg == "min max scaling":
        return init_NM.min_max_scaling(df_arg, column_applied_arg)
    elif method_arg == "z-score scaling":
        return init_NM.z_score_scaling(df_arg, column_applied_arg)



class DFOperation():
    def __init__(self):
        pass

    def drop_col(self, df_arg, cols_arg):
        new_df = df_arg
        for col in cols_arg:
            new_df = new_df.drop(col, axis = 1)

        return new_df
    

def get_df_info(inf_to_get_arg, df_arg):
    if inf_to_get_arg == "Shape":
        return ("Data frame Shape: " , df_arg.shape, " \n ")
    elif inf_to_get_arg == "Index":
        return ("Data frame Index: ", df_arg.index, " \n ")
    elif inf_to_get_arg == "Columns":
        return ("Data frame Columns", df_arg.columns, " \n ")
    elif inf_to_get_arg == "Info":
        return ("Data frame Columns: ", df_arg.info(), " \n ")
    elif inf_to_get_arg == "Count":
        return ("Data frame Count: ", df_arg.count(), " \n ")
    elif inf_to_get_arg == "" or inf_to_get_arg == None:
        return "Please selcted information to show"


def get_df_summary(summary_to_get, df_arg):
    if summary_to_get == "Sum":
        return ("Data frame Sum: " , df_arg.sum(), " \n ")

    elif summary_to_get == "CumSum":
        return ("Data frame CumSum: ", df_arg.cumsum(), " \n ")

    elif summary_to_get == "Min":
        return ("Data frame Min: ", df_arg.min(), " \n ")

    elif summary_to_get == "Max":
        return ("Data frame Max: ", df_arg.max(), " \n ")

    elif summary_to_get == "MaxIndex":
        return ("Data frame MaxIndex: ", df_arg.idxmin(), " \n ")

    elif summary_to_get == "MinIndex":
        return ("Data frame MinIndex: ", df_arg.idxmax(), " \n ")

    elif summary_to_get == "Describe":
        return ("Data frame Describe: ", df_arg.describe(), " \n ")

    elif summary_to_get == "Mean":
        return ("Data frame Mean: ", df_arg.mean(), " \n ")

    elif summary_to_get == "Median":
        return ("Data frame Median: ", df_arg.median(), " \n ")