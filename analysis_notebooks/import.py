import struct
import matplotlib.pyplot as plt
with open("./final_log_12mhz", "rb") as file:
	data = file.read(8000000)


num_floats = len(data) // 4
floats = struct.unpack(f'<{num_floats}f', data)

plt.figure()
plt.plot(floats)

plt.show()
