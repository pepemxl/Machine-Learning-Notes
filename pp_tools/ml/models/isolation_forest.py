# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 15:53:51 2022

@author: Jose Alonzo
"""
from sklearn.datasets import load_diabetes
from sklearn import linear_model
import m2cgen as m2c

X, y = load_diabetes(return_X_y=True)

estimator = linear_model.LinearRegression()
estimator.fit(X, y)

code = m2c.export_to_python(estimator)
code_cpp = m2c.export_to_c_sharp(estimator)
code_rust = m2c.export_to_rust(estimator)
code_php = m2c.export_to_php(estimator)
code_js = m2c.export_to_javascript(estimator)


print(code)
print(code_cpp)
print(code_rust)
print(code_php)
print(code_js)