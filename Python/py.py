import numpy as np
ar1 = [0.40, 0.50]
ar2 = [0.90,0.80]

c = (np.array(ar2) - np.array(ar1)) ** 2
ts = c.tobytes()
print(np.frombuffer(ts, dtype=float))