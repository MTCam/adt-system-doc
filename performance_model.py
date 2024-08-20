# Generate performance model data for ADT system as implemented in mirgecom
import numpy as np

# Simulation input parameters:
N_v = 1000000  # Number of elements
p = 1  # polynomial order
type_of_elements = "simplex"
d = 3 # spatial dimension

# Platform parameters:
# Memory bandwidth (Bytes/s)
platform_memory_bw = 1e11  # 100GB/s
# FLOP rate (FLOPS/s)
platform_flop_rate = 1e11  # 100GFLOPS

# Calculated parameters
# volume DOFs per el
d_v = np.math.factorial(d+p)/(np.math.factorial(p)*np.math.factorial(d))
# facial DOFs per face
d_f = np.math.factorial(d+p-1)/(np.math.factorial(p)*np.math.factorial(d-1))
n_f = (d+1)  # number of faces per *simplex* element
N_f = N_v * n_f  # Total number of faces

# Solution projection
soln_proj_flops = N_f*d_v*(2*d_f - 1)
soln_proj_ls = N_f*(d_v*d_f + d_f + d_v)
soln_proj_ci = soln_proj_flops / soln_proj_ls

# Advection flux in volume
adv_flux_flops = d*N_v*d_v
adv_flux_ls = N_v*(d+1)*d_v
adv_flux_ci = adv_flux_flops/adv_flux_ls

# Advection numerical flux
adv_num_flux_flops = N_f*(2*d+1)*d_f
adv_num_flux_ls = N_f*(d+3)*d_f
adv_num_flux_ci = adv_num_flux_flops / adv_num_flux_ls

# Apply Inverse Mass Operator
# -- div
div_flux_vol_flops = N_v*d_v*(2*d*d_v + 1)
div_flux_vol_ls = N_v*d_v*(d*(d_v + 1) + 1)
div_flux_vol_ci = div_flux_vol_flops / div_flux_vol_ls

# -- face mass operator 
face_mass_operator_flops = N_v*(n_f*d_v*2*d_f-1)
face_mass_operator_ls = N_v*(n_f*d_f*(d_v+1) + d_v)
face_mass_operator_ci = face_mass_operator_flops / face_mass_operator_ls

# -- inverse mass operator
inv_mass_operator_flops = N_v*2*d_v*d_v
inv_mass_operator_ls = N_v*d_v*(d_v + 2)
inv_mass_operator_ci = inv_mass_operator_flops / inv_mass_operator_ls

print("Computational Intensities:\n"
      f"Soln Proj: {soln_proj_ci=}\n"
      f"Advection vol flux: {adv_flux_ci=}\n"
      f"Advection num flux: {adv_num_flux_ci=}\n"
      f"Div Flux: {div_flux_vol_ci=}\n"
      f"Face Mass Oper: {face_mass_operator_ci=}\n"
      f"Inv Mass Oper: {inv_mass_operator_ci=}\n")



