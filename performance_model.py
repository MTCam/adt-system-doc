# Generate performance model data for ADT system as implemented in mirgecom
import math

# Simulation input parameters:
N_v = 511104  # Number of elements
p = 2  # polynomial order
type_of_elements = "simplex"
d = 3 # spatial dimension

# Platform parameters:
# Memory bandwidth (Bytes/s)
platform_memory_bw = 4e11  # 400GB/s
# FLOP rate (FLOPS/s)
platform_name = "Apple M2 Max"
platform_flops_per_cycle_per_core = 6
platform_num_cores = 8
platform_clock_rate = 3.7e9  # Hz
platform_flop_rate = \
    platform_flops_per_cycle_per_core * platform_num_cores * platform_clock_rate   # FLOPS
flop_bound_limit = platform_flop_rate / platform_memory_bw

print(f"Platform name: {platform_name}\n"
      f"DP flops per cycle per core: {platform_flops_per_cycle_per_core}\n"
      f"Num cores: {platform_num_cores}\n"
      f"Clock rate (GHz): {platform_clock_rate/1e9}\n"
      f"FLOPS (GFLOPS/s): {platform_flop_rate/1e9}\n"
      f"Memory BW (GB/s): {platform_memory_bw/1e9}\n"
      f"Flop bound limit: {flop_bound_limit}")
print("==============================")

# Calculated parameters
# volume DOFs per el
d_v = math.factorial(d+p)/(math.factorial(p)*math.factorial(d))
# facial DOFs per face
d_f = math.factorial(d+p-1)/(math.factorial(p)*math.factorial(d-1))
n_f = (d+1)  # number of faces per *simplex* element
N_f = N_v * n_f  # Total number of faces

print(f"Total Number of ({p=}) Elements: {N_v}\n"
      f"Spatial dimension: {d}\n"
      f"Number of faces per element: {n_f}\n"
      f"Total number of faces: {N_f}\n"
      f"Volume DOFS: {d_v}\n"
      f"Face DOFS: {d_f}\n")
print("==================")

total_mem = 0
total_flops = 0
total_time = 0

# Solution projection
soln_proj_flops = N_f*d_v*(2*d_f - 1)
soln_proj_ls = N_f*(d_v*d_f + d_f + d_v)
soln_proj_mem = 8*soln_proj_ls
soln_proj_ci = soln_proj_flops / soln_proj_mem
total_mem = total_mem + soln_proj_mem
total_flops = total_flops + soln_proj_flops
compute_rate = platform_memory_bw
if soln_proj_ci >= flop_bound_limit:
    total_time = total_time + soln_proj_flops / platform_flop_rate
else:
    total_time = total_time + soln_proj_mem / platform_memory_bw

# Advection flux in volume
adv_flux_flops = d*N_v*d_v
adv_flux_ls = N_v*(d+1)*d_v
adv_flux_mem = 8*adv_flux_ls
adv_flux_ci = adv_flux_flops / adv_flux_mem
total_mem = total_mem + adv_flux_mem
total_flops = total_flops + adv_flux_flops
if adv_flux_ci >= flop_bound_limit:
    total_time = total_time + adv_flux_flops / platform_flop_rate
else:
    total_time = total_time + adv_flux_mem / platform_memory_bw

# Advection numerical flux
adv_num_flux_flops = N_f*(2*d+1)*d_f
adv_num_flux_ls = N_f*(d+3)*d_f
adv_num_flux_mem = 8*adv_num_flux_ls
adv_num_flux_ci = adv_num_flux_flops / adv_num_flux_mem
total_mem = total_mem + adv_num_flux_mem
total_flops = total_flops + adv_num_flux_flops
if adv_num_flux_ci >= flop_bound_limit:
    total_time = total_time + adv_num_flux_flops / platform_flop_rate
else:
    total_time = total_time + adv_num_flux_mem / platform_memory_bw

# Apply Inverse Mass Operator
# -- div (applies stiffness operator dim times and sums)
div_flux_vol_flops = N_v*d_v*(2*d*d_v + 1)
div_flux_vol_ls = N_v*d_v*(d*(d_v + 1) + 1)
div_flux_vol_mem = 8*div_flux_vol_ls
div_flux_vol_ci = div_flux_vol_flops / div_flux_vol_mem
total_mem = total_mem + div_flux_vol_mem
total_flops = total_flops + div_flux_vol_flops
if div_flux_vol_ci >= flop_bound_limit:
    total_time = total_time + div_flux_vol_flops / platform_flop_rate
else:
    total_time = total_time + div_flux_vol_mem / platform_memory_bw

# -- face mass operator
face_mass_operator_flops = N_v*(n_f*d_v*2*d_f-1)
face_mass_operator_ls = N_v*(n_f*d_f*(d_v+1) + d_v)
face_mass_operator_mem = 8*face_mass_operator_ls
face_mass_operator_ci = face_mass_operator_flops / face_mass_operator_mem
total_mem = total_mem + face_mass_operator_mem
total_flops = total_flops + face_mass_operator_flops
if face_mass_operator_ci >= flop_bound_limit:
    total_time = total_time + face_mass_operator_flops / platform_flop_rate
else:
    total_time = total_time + face_mass_operator_mem / platform_memory_bw

# -- inverse mass operator
inv_mass_operator_flops = N_v*2*d_v*d_v
inv_mass_operator_ls = N_v*d_v*(d_v + 2)
inv_mass_operator_mem = 8*inv_mass_operator_ls
inv_mass_operator_ci = inv_mass_operator_flops / inv_mass_operator_mem
total_mem = total_mem + inv_mass_operator_mem
total_flops = total_flops + inv_mass_operator_flops

if inv_mass_operator_ci >= flop_bound_limit:
    total_time = total_time + inv_mass_operator_flops / platform_flop_rate
else:
    total_time = total_time + inv_mass_operator_mem / platform_memory_bw

print("Computational Intensities (flops/byte):\n"
      f"Soln Proj: {soln_proj_ci=}\n"
      f"Advection vol flux: {adv_flux_ci=}\n"
      f"Advection num flux: {adv_num_flux_ci=}\n"
      f"Div Flux: {div_flux_vol_ci=}\n"
      f"Face Mass Oper: {face_mass_operator_ci=}\n"
      f"Inv Mass Oper: {inv_mass_operator_ci=}\n")
print("==========================")
print(f"Total GFLOPs: {total_flops/1e9}\n"
      f"Total Mem (GB): {total_mem/1e9}\n"
      f"Total Time: {total_time}\n")
print("==========================")

sysmem_coords = d * 8 * d_v * N_v
sysmem_metrics = d * d * 8 * d_v * N_v
sysmem_mass = 8 * d_v * d_v * N_v
sysmem_invmass = sysmem_mass
sysmem_facemass = 8 * d_f * d_v * N_f
sysmem_stiff = d * 8 * d_v * d_v * N_v
sysmem_elconn = 4 * N_v * d_v
sysmem_faceconn = 4 * d_f * N_f
sysmem_eladj = 4 * N_f
sysmem_soln_vol = 8*(N_v * d_v)
sysmem_soln_faces = 0 # Transient: 8*2*(N_f * d_f)
sysmem_fluxes = 0 # Transient: 8 * d * (N_v * d_v + N_f * d_f)
sysmem_normals = d * 8 * N_f * d_f
sysmem_numfluxes = 0 # Transient: 8 * (2*(N_f * d_f) + N_v * d_v)
sysmem_rhs = 0 # Transient: 8 * N_v * d_v
sysmem_vel = 0  # single scalar - not an array
sysmem_diff = 0  # single scalar
sysmem_vdm = 8 * 1 * N_v * (d_v+1) * (d_v+1)
sysmem_dmat = sysmem_vdm
sysmem_operators = \
    (sysmem_invmass + sysmem_mass + sysmem_facemass + sysmem_stiff)
sysmem_soln = sysmem_soln_vol # Transient: + sysmem_soln_faces
sysmem_total = \
    (sysmem_coords + sysmem_metrics + sysmem_elconn + sysmem_faceconn
     + sysmem_eladj + sysmem_operators + sysmem_soln + sysmem_fluxes
     + sysmem_normals + sysmem_numfluxes + sysmem_rhs + sysmem_vel + sysmem_diff)
print("Additional System Memory(GB):\n"
      f"Soln: {sysmem_soln_vol/1e9}\n"
      f"Coords: {sysmem_coords/1e9}\n"
      f"Metrics: {sysmem_metrics/1e9}\n"
      f"Mass: {sysmem_mass/1e9}\n"
      f"FaceMass: {sysmem_facemass/1e9}\n"
      f"Stiffness: {sysmem_stiff/1e9}\n"
      f"Operators: {sysmem_operators/1e9}\n"
      f"ElConn: {sysmem_elconn/1e9}\n"
      f"FaceConn: {sysmem_faceconn/1e9}\n"
      f"ElAdj: {sysmem_eladj/1e9}\n"
      "----------------------\n"
      f"Total: {sysmem_total/1e9}")



