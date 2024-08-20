import matplotlib.pyplot as plt
import numpy as np

# Mac M2 Max
num_cores = 8
flops_per_core_per_cycle = 6
clock_speed_hz = 3.7 * 1e9
memory_bandwidth_gb_s = 400  # in GB/s
memory_bandwidth_bytes_s = memory_bandwidth_gb_s * 1e9  # in bytes/s

# Calculate Peak Computational Performance
peak_flops = num_cores * flops_per_core_per_cycle * clock_speed_hz  # in FLOPS
peak_flops_gflops = peak_flops / 1e9  # in GFLOPS

# Define computational intensity (FLOPs per byte) range for x-axis
intensity = np.logspace(-3, 1, 100)  # from 0.001 to 10

compute_bound = peak_flops_gflops * np.ones_like(intensity)  # Horizontal line
memory_bound = memory_bandwidth_gb_s * intensity   # Diagonal line

# Plotting
plt.figure(figsize=(10, 6))
plt.loglog(intensity, np.minimum(compute_bound, memory_bound), label="Roofline")
plt.axhline(y=peak_flops_gflops, color='r', linestyle='--', label=f"Peak Performance: {peak_flops_gflops:.0f} GFLOPS")

plt.title("Roofline Performance Model for M2 Max")
plt.xlabel("Computational Intensity (FLOPs/Byte)")
plt.ylabel("Performance (GFLOPS)")
plt.xlim([0.001, 10])
plt.xticks([0.001, 0.01, 0.1, 1, 10], [0.001, 0.01, 0.1, 1, 10])
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()
