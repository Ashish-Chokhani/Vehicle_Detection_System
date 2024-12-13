import numpy as np

class KalmanFilter:
    def __init__(self, dt, std_acc, x_std_meas, y_std_meas):

        self.dt = dt

        self.x = np.zeros((4, 1))

        self.A = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.B = np.array([
            [(dt**2) / 2, 0],
            [0, (dt**2) / 2],
            [dt, 0],
            [0, dt]
        ])

        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])

        self.Q = np.array([
            [(dt**4) / 4, 0, (dt**3) / 2, 0],
            [0, (dt**4) / 4, 0, (dt**3) / 2],
            [(dt**3) / 2, 0, dt**2, 0],
            [0, (dt**3) / 2, 0, dt**2]
        ]) * std_acc**2

        self.R = np.array([
            [x_std_meas**2, 0],
            [0, y_std_meas**2]
        ])

        self.P = np.eye(4)

    def predict(self, u=np.zeros((2, 1))):
        self.x = np.dot(self.A, self.x) + np.dot(self.B, u)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x[:2]

    def update(self, z):
        y = z - np.dot(self.H, self.x) 
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R  
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S)) 

        self.x += np.dot(K, y)
        self.P = np.dot(np.eye(4) - np.dot(K, self.H), self.P)
        return self.x[:2]
