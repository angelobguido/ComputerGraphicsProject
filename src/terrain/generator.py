import numpy as np
import matplotlib.pyplot as plt

terrain_max = 50

range = np.array([[0,terrain_max],[0,terrain_max]])

mean1 = [0, 0]
cov1 = [[100, 0], [0, 100]]

mean2 = [50, 50]  # Adjust the means as desired
cov2 = [[10, 0], [0, 10]]  # Adjust the covariance matrix as desired

samples1 = np.random.multivariate_normal(mean1, cov1, 2500)

samples2 = np.random.multivariate_normal(mean2, cov2, 2500)

samples = np.concatenate((samples1, samples2))

x, y = samples.T

hist = (np.histogram2d(x, y, bins=terrain_max, range=range)[0]).astype(np.int64)

np.savetxt("test.txt", hist, "%d")