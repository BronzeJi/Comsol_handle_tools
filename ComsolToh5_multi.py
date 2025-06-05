#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 23:54:11 2025

@author: elliot
"""



import h5py
import numpy as np
import pandas as pd
import glob




pathname="pathyouwish"

#df = pd.read_csv(pathname+'pressure_512_2.csv')

files=glob.glob(pathname+"comsol_data/Pressure_*.csv")


# Soundsource
positions = []
j=1

with open(pathname+"comsol_sweep_source.txt", "r") as f:
    lines = f.readlines()

# Split each line and ignore the first item (parameter name)
x_vals = list(map(float, lines[0].strip().split()[1:]))
y_vals = list(map(float, lines[1].strip().split()[1:]))
z_vals = list(map(float, lines[2].strip().split()[1:]))

# Combine into list of tuples (x, y, z)
positions = list(zip(x_vals, y_vals, z_vals))

print("Files: "+str(files))

#-----------------------------


for file in files:
    df = pd.read_csv(file)
    # Extract coordinate columns
    coordinates = df.iloc[:, :3]
    
    # Divide the rest of the columns (starting from the 4th column)
    data = df.iloc[:, 3:]
    num_blocks = data.shape[1] // 101
    
    # Split data into a list of matrices (one for each 101-column block)
    matrices = [data.iloc[:, i*101:(i+1)*101].values for i in range(num_blocks)]
    
    
    # Isolate the base filename
    base = file.split('/')[-1]
    # Extract and convert the start number
    start_num = int(base.split('_')[1].split('-')[0])
    #start_num="1" # if it start from the begining no splited file occasion
    print("Extracting from"+file+".  Start number" + str(start_num))
    
    for i in range(len(matrices)):
        
        pressures_com= matrices[i] #pressure
        dic = pressures_com[:,0] #initial impulse
        
        index=np.random.choice(matrices[1][:, 1].shape[0], size=1728, replace=False)
        
        ic_com = dic[index]
        umesh_com = coordinates.iloc[index].reset_index(drop=True)
        
        
        with h5py.File(pathname+'hdf5_data/train_'+str(j)+'.h5', 'w') as h5file:
            j=j+1
        
            #data_mesh = np.zeros((57124,3))
            data_mesh=coordinates
            #data_mesh[-1]=[1,1,1]
            
            #pressures=np.zeros((101,57124))
            pressures=pressures_com.T
            
            #soundsource=np.ones((3))
            #umesh=np.zeros((1728, 3))
            #upressures= np.zeros(1728)
            umesh=umesh_com
            upressures=ic_com
            soundsource=positions[i+int(start_num)-1]
            print("Current sound source position" + str(soundsource))
            
            time_steps = np.linspace(0, 0.05, 101, dtype=np.float32)
            ushape= np.array([12,12,12], dtype=np.float32)
            
                               
            
            
            dset_1 = h5file.create_dataset(
                name='mesh',       # dataset path/name within the file
                data=data_mesh,               # the actual array to store
                dtype='float32'
            )
            dset_2 = h5file.create_dataset(
                name='pressures',       # dataset path/name within the file
                data=pressures,               # the actual array to store
                dtype='float16'
            )
            dset_3 = h5file.create_dataset(
                name='source_position',       # dataset path/name within the file
                data=soundsource,               # the actual array to store
                dtype='float32'
            )
            dset_4 = h5file.create_dataset(
                name='umesh',       # dataset path/name within the file
                data=umesh,               # the actual array to store
                dtype='float32'
            )
            dset_5 = h5file.create_dataset(
                name='upressures',       # dataset path/name within the file
                data=upressures,               # the actual array to store
                dtype='float16'
            )
        
            
           
            dset_2.attrs['time_steps'] = time_steps
            dset_4.attrs['umesh_shape']= ushape
    print("Extracted from"+file)
        


