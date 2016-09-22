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
def get_cpu_model_classic(all_cpu_stats_csv):
	
	# Get the data frame
	df = pd.read_csv(all_cpu_stats_csv,sep=';')
	
	# Drop the target feature (i.e. CPU load)
	X = df.drop('cpu', axis=1)
	
	# Split data to training and validation data sets
	x_train, x_val, y_train, y_val = train_test_split(X, 
														df['cpu'], 
														test_size = 0.33, 
														random_state = 5)
	
	# Calculate the linear regression using the training data set
	lm = LinearRegression().fit(x_train, y_train)
	
	# Le coefficient Intercept est la valeur de l'origine (X=0)
	print 'Trainng Data Set: estimated intercept coefficient', lm.intercept_
	print 'Trainng Data Set: number of coefficient', len(lm.coef_)
	estim_pd = pd.DataFrame(zip(x_train.columns, lm.coef_), columns = ['features', 'estimatedCoefficient'])
	print '####### scikit Regression Model ########'
	print estim_pd
	
	# All regression precision metrics (Training vs Validation)
	
	# Training Data Set stats
	tr_evs_cpu = explained_variance_score(y_train,lm.predict(x_train))
	tr_mae_cpu = mean_absolute_error(y_train,lm.predict(x_train))
	tr_mde_cpu = median_absolute_error(y_train,lm.predict(x_train))
	tr_mse_cpu = mean_squared_error(y_train,lm.predict(x_train))
	tr_r_2_cpu = r2_score(y_train,lm.predict(x_train))
	
	# Training Data Set stats
	val_evs_cpu = explained_variance_score(y_val,lm.predict(x_val))
	val_mae_cpu = mean_absolute_error(y_val,lm.predict(x_val))
	val_mde_cpu = median_absolute_error(y_val,lm.predict(x_val))
	val_mse_cpu = mean_squared_error(y_val,lm.predict(x_val))
	val_r_2_cpu = r2_score(y_val,lm.predict(x_val))
	
	############################### Print Stats
	print '===> Stats <==='
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
	print '====================================================='

# Regression linear for CPU using MARS
def get_cpu_model_mars(all_cpu_stats_csv):
	
	# Get the data frame
	df = pd.read_csv(all_cpu_stats_csv,sep=';')
	
	# Drop the target feature (ssd_tot_cpu, hdd_tot_cpu)
	X = df.drop('cpu', axis=1)
	
	# Split data to training and validation data sets
	#~ x_train, x_val, y_train, y_val = train_test_split(X, 
														#~ df['cpu'], 
														#~ test_size = 0.33, 
														#~ random_state = 5)
	# Print Earth model
	model = Earth()
	model.fit(X, df['cpu'])
	print '####### Earth Mars Regression Model ########'
	print model.summary()
	#~ print 'Basis: ', model.basis_
	#~ print 'Coeff:', model.coef_
	
	# All regression precision metrics (Training vs Validation)
	
	# Training Data Set stats
	#~ tr_evs_cpu = explained_variance_score(y_train,model.predict(x_train))
	#~ tr_mae_cpu = mean_absolute_error(y_train,model.predict(x_train))
	#~ tr_mde_cpu = median_absolute_error(y_train,model.predict(x_train))
	#~ tr_mse_cpu = mean_squared_error(y_train,model.predict(x_train))
	#~ tr_r_2_cpu = r2_score(y_train,model.predict(x_train))
	
	# Training Data Set stats
	#~ val_evs_cpu = explained_variance_score(y_val,model.predict(x_val))
	#~ val_mae_cpu = mean_absolute_error(y_val,model.predict(x_val))
	#~ val_mde_cpu = median_absolute_error(y_val,model.predict(x_val))
	#~ val_mse_cpu = mean_squared_error(y_val,model.predict(x_val))
	#~ val_r_2_cpu = r2_score(y_val,model.predict(x_val))
	
	############################### Print Stats
	#~ print '===> Stats <==='
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
