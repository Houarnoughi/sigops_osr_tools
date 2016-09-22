#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt
from pyearth import Earth
import sys
from sklearn.linear_model import LinearRegression
import numpy as np

# Import all regression precission metrics
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, median_absolute_error, r2_score
from sklearn.cross_validation import train_test_split

# Regression linear for CPU
# This regression takes a csv CPU stats file and use a linear regression
# using default scikit model   
def get_cpu_model_classic(cpu_stats_csv):
	
	# Get the data frame
	df = pd.read_csv(cpu_stats_csv,sep=';')
	
	# Drop the target feature (i.e. CPU load)
	X = df.drop('ssd_tot_cpu', axis=1).drop('hdd_tot_cpu', axis=1).drop('ssd_iops', axis=1)
	
	# Split data to training and validation data sets
	x_train_h, x_val_h, y_train_h, y_val_h = train_test_split(X, 
														df['hdd_tot_cpu'], 
														test_size = 0.33, 
														random_state = 5)
	x_train_s, x_val_s, y_train_s, y_val_s = train_test_split(X, 
														df['ssd_tot_cpu'], 
														test_size = 0.33, 
														random_state = 5)
	
	# Calculate the linear regression using the training data set
	lm_h = LinearRegression().fit(x_train_h, y_train_h)
	lm_s = LinearRegression().fit(x_train_s, y_train_s)
	
	# Le coefficient Intercept est la valeur de l'origine (X=0)
	print 'HDD Trainng Data Set: estimated intercept coefficient', lm_h.intercept_
	print 'HDD Trainng Data Set: number of coefficient', len(lm_h.coef_)
	print 'SSD Trainng Data Set: estimated intercept coefficient', lm_s.intercept_
	print 'SSD Trainng Data Set: number of coefficient', len(lm_s.coef_)
	estim_pd_h = pd.DataFrame(zip(x_train_h.columns, lm_h.coef_), 
	columns = ['features', 'estimatedCoefficient'])
	estim_pd_s = pd.DataFrame(zip(x_train_s.columns, lm_s.coef_), 
	columns = ['features', 'estimatedCoefficient'])
	print '##### HDD Coeff & Features #######'
	print estim_pd_h
	print '##### SSD Coeff & Features #######'
	print estim_pd_s
	
	# All regression precision metrics (Training vs Validation)
	
	# Training Data Set stats
	tr_evs_cpu = explained_variance_score(y_train_h,lm_h.predict(x_train_h))
	tr_mae_cpu = mean_absolute_error(y_train_h,lm_h.predict(x_train_h))
	tr_mde_cpu = median_absolute_error(y_train_h,lm_h.predict(x_train_h))
	tr_mse_cpu = mean_squared_error(y_train_h,lm_h.predict(x_train_h))
	tr_r_2_cpu = r2_score(y_train_h,lm_h.predict(x_train_h))
	
	# Training Data Set stats
	val_evs_cpu = explained_variance_score(y_val_h,lm_h.predict(x_val_h))
	val_mae_cpu = mean_absolute_error(y_val_h,lm_h.predict(x_val_h))
	val_mde_cpu = median_absolute_error(y_val_h,lm_h.predict(x_val_h))
	val_mse_cpu = mean_squared_error(y_val_h,lm_h.predict(x_val_h))
	val_r_2_cpu = r2_score(y_val_h,lm_h.predict(x_val_h))
	
	############################### Print Stats
	print '#################### scikit Regression model ###############'
	print 'Training: Explained Variance Score of the CPU model:', tr_evs_cpu
	print 'Validation: Explained Variance Score of the CPU model:', val_evs_cpu
	print 'Training: Mean Absolute Error of the CPU model:', tr_mae_cpu
	print 'Validation: Mean Absolute Error of the CPU model:', val_mae_cpu
	print 'Training: Median Absolute Error of the CPU model:', tr_mde_cpu
	print 'Validation: Median Absolute Error of the CPU model:', val_mde_cpu
	print 'Training: Mean Squared Error of the CPU model:', tr_mse_cpu
	print 'Validation: Mean Squared Error of the CPU model:', val_mse_cpu
	print 'Training: R2 score of the CPU model:', tr_r_2_cpu
	print 'Validation: R2 score of the CPU model:', val_r_2_cpu

# Regression linear for CPU using MARS
def get_cpu_model_mars(cpu_stats_csv):
	
	# Get the data frame
	df = pd.read_csv(cpu_stats_csv,sep=';')
	
	# Drop the target feature (ssd_tot_cpu, hdd_tot_cpu)
	X = df.drop('ssd_tot_cpu', axis=1).drop('hdd_tot_cpu', axis=1)
	
	# Split data to training and validation data sets
	x_train_h, x_val_h, y_train_h, y_val_h = train_test_split(X, 
														df['hdd_tot_cpu'], 
														test_size = 0.33, 
														random_state = 5)
	x_train_s, x_val_s, y_train_s, y_val_s = train_test_split(X, 
														df['ssd_tot_cpu'], 
														test_size = 0.33, 
														random_state = 5)
	# Print Earth model
	mdl_h = Earth().fit(x_train_h, y_train_h)
	mdl_s = Earth().fit(x_train_s, y_train_s)
	
	print mdl_h.summary()
	print mdl_s.summary()
	#~ print 'Basis: ', model.basis_
	#~ print 'Coeff:', model.coef_
	
	# All regression precision metrics (Training vs Validation)
	
	# Training Data Set stats
	#~ tr_evs_cpu = explained_variance_score(y_train,model.predict(x_train))
	#~ tr_mae_cpu = mean_absolute_error(y_train,model.predict(x_train))
	#~ tr_mde_cpu = median_absolute_error(y_train,model.predict(x_train))
	#~ tr_mse_cpu = mean_squared_error(y_train,model.predict(x_train))
	#~ tr_r_2_cpu = r2_score(y_train,model.predict(x_train))
	
	#~ # Training Data Set stats
	#~ val_evs_cpu = explained_variance_score(y_val,model.predict(x_val))
	#~ val_mae_cpu = mean_absolute_error(y_val,model.predict(x_val))
	#~ val_mde_cpu = median_absolute_error(y_val,model.predict(x_val))
	#~ val_mse_cpu = mean_squared_error(y_val,model.predict(x_val))
	#~ val_r_2_cpu = r2_score(y_val,model.predict(x_val))
	
	#~ ############################### Print Stats
	#~ print '################ Earth MARS Regression model ###############'
	#~ print 'Training: Explained Variance Score of the CPU model:', tr_evs_cpu
	#~ print 'Validation: Explained Variance Score of the CPU model:', val_evs_cpu
	#~ print 'Training: Mean Absolute Error of the CPU model:', tr_mae_cpu
	#~ print 'Validation: Mean Absolute Error of the CPU model:', val_mae_cpu
	#~ print 'Training: Median Absolute Error of the CPU model:', tr_mde_cpu
	#~ print 'Validation: Median Absolute Error of the CPU model:', val_mde_cpu
	#~ print 'Training: Mean Squared Error of the CPU model:', tr_mse_cpu
	#~ print 'Validation: Mean Squared Error of the CPU model:', val_mse_cpu
	#~ print 'Training: R2 score of the CPU model:', tr_r_2_cpu
	#~ print 'Validation: R2 score of the CPU model:', val_r_2_cpu
	
if __name__ == "__main__":
	
	if len(sys.argv) < 2:
		print 'Usage: {0} <cpu_stats_csv>'.format(sys.argv[0])
		sys.exit(0)
	
	# Get the CPU regression model
	get_cpu_model_classic(sys.argv[1])
	
	get_cpu_model_mars(sys.argv[1])
