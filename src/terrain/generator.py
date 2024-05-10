import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

# terrain_max = 300

# range = np.array([[0,terrain_max],[0,terrain_max]])

# mean1 = [0, 0]
# cov1 = [[1000, 0], [0, 1000]]

# mean2 = [50, 50]  
# cov2 = [[100, 0], [0, 100]]  

# mean3 = [120, 120]  
# cov3 = [[500, 0], [0, 500]]  

# samples1 = np.random.multivariate_normal(mean1, cov1, 10000000)

# samples2 = np.random.multivariate_normal(mean2, cov2, 10000000)

# samples3 = np.random.multivariate_normal(mean3, cov3, 10000000)

# samples = np.concatenate((samples1, samples2, samples3))

# x, y = samples.T

# hist = (np.histogram2d(x, y, bins=terrain_max, range=range)[0])
# hist = ((hist-np.min(hist))/np.max(hist))*200+30
# hist = hist.astype(np.int32)

# np.savetxt("test.txt", hist, "%d")


noise = PerlinNoise(octaves=10, seed=1)
xpix, ypix = 100, 100
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

plt.imshow(pic, cmap='gray')
plt.show()

print(noise([1/16,4/16]))