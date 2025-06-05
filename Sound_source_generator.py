#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 16:30:40 2025

@author: elliot
"""

import numpy as np
import pandas as pd

# Define bounds for the middle region (example: central 50% of the box)
x = np.random.uniform(0.75, 2.25, 512)
y = np.random.uniform(0.5, 1.5, 512)
z = np.random.uniform(0.5, 1.5, 512)

# Convert to strings with formatting and concatenate
x_line = "x_src " + " ".join(f"{val:.6f}" for val in x)
y_line = "y_src " + " ".join(f"{val:.6f}" for val in y)
z_line = "z_src " + " ".join(f"{val:.6f}" for val in z)

# Combine all three lines
sweep_param_text = "\n".join([x_line, y_line, z_line])

# Save to file
with open("comsol_sweep_source.txt", "w") as f:
    f.write(sweep_param_text)
