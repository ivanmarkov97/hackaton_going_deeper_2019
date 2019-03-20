# -*- coding: utf-8 -*-
"""demo_hack.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OvUX720nJwEJLBDupKOsTNf9IcFrn7ap
"""

import numpy as np
import pandas as pd

M_global = 100
V0_global = 250
alpha_global = 45

V = np.linspace(0, 270, 28)
Fa = np.array([
    0,
    14.019,
    80.836,
    240.06,
    449.91,
    686.02,
    983.03,
    1361.6,
    1804.9,
    2289.1,
    2807.5,
    3361.5,
    3961.7,
    4633.8,
    5373,
    6166.7,
    7014.9,
    7917.5,
    8874.5,
    9886,
    10952,
    12072,
    13246,
    14475,
    15757,
    17094,
    18486,
    19931
])

data_V = pd.Series(Fa, index=V)

from matplotlib import pyplot as plt
# %matplotlib inline

fig, ax = plt.subplots(figsize=(14,10))

ax.plot(data_V.index.values, data_V.values)

def f(x):
  a = 0.2739
  return a*x**2

_X = np.linspace(0, 270, 28)
_Y = f(_X)
ax.plot(_X, _Y)
plt.show()

Y = np.linspace(0, 1400, 15)
Wx = np.array([
    3.38,
    3.52,
    3.84,
    4.39,
    4.75,
    4.53,
    3.58,
    3.37,
    4.37,
    2.99,
    4.2,
    5.19,
    2.88,
    4.59,
    3.61
])

Wz = np.array([
    -1.81,
    -2.88,
    -2.60,
    -1.18,
    -1.42,
    -1.94,
    -1.73,
    -2.25,
    -2.16,
    -2.42,
    -1.97,
    -2.4,
    -1.55,
    -1.4,
    -1.13
])

data_Y = pd.DataFrame({'Wx': Wx, 'Wz': Wz, 'Y': Y})

alpha = 30
import math
#math.sin(math.pi * alpha / 180.0)

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Activation
from keras.models import Sequential

X = data_Y['Y'].values
y_wx = data_Y['Wx'].values
y_wz = data_Y['Wz'].values

X_scaler = preprocessing.StandardScaler()
X_scaled = (X_scaler.fit_transform(X.reshape(-1,1)))

model_wx = Sequential()
model_wx.add(Dense(512, input_dim=1, activation='relu'))
model_wx.add(Dropout(.1))
model_wx.add(Dense(256, activation='relu'))
model_wx.add(Dropout(.1))
model_wx.add(Dense(256, activation='relu'))
model_wx.add(Dense(1))

model_wx.compile(loss='mse', optimizer='rmsprop', metrics=["accuracy"])

model_wx.fit(X_scaled, y_wx, epochs=512, batch_size=5, verbose=0)

data_test = np.linspace(0, 1400, 101)
print(data_test.shape)
data_test_scaled = (X_scaler.fit_transform(data_test.reshape(-1,1)))

print(X_scaled.shape, data_test_scaled.shape)

predicted = model_wx.predict(data_test_scaled)
predicted = predicted.T[0]

predicted_self = model_wx.predict(X_scaled)
predicted_self = predicted_self.T[0]

plt.plot(X, y_wx)
plt.plot(data_test, predicted)

%%time
model_wz = Sequential()
model_wz.add(Dense(512, input_dim=1, activation='relu'))
model_wz.add(Dropout(.1))
model_wz.add(Dense(256, activation='relu'))
model_wz.add(Dropout(.1))
model_wz.add(Dense(256, activation='relu'))
model_wz.add(Dense(1))

model_wz.compile(loss='mse', optimizer='rmsprop', metrics=["accuracy"])

model_wz.fit(X_scaled, y_wz, epochs=512, batch_size=5, verbose=0)

data_test = np.linspace(0, 1400, 101)
print(data_test.shape)
data_test_scaled = (X_scaler.fit_transform(data_test.reshape(-1,1)))

print(X_scaled.shape, data_test_scaled.shape)

predicted = model_wz.predict(data_test_scaled)
predicted = predicted.T[0]

predicted_self = model_wx.predict(X_scaled)
predicted_self = predicted_self.T[0]

plt.plot(X, y_wz)
plt.plot(data_test, predicted)




from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'])
drop = Point(0.0, 0.0, 0.0)
place = Point(0.0, 0.0, 0.0)
#place = place._replace(x=10)

#X_scaler.transform([[195.12923069695137]])[0][0]

"""**Всегда бросать по ветру не сссать против ветра**

![alt text](https://s15.stc.all.kpcdn.net/share/i/12/10304111/inx960x640.jpg)
"""

def get_pred_wind(model, H, X_scaler):
  return model.predict([X_scaler.transform([[H]])[0][0]])[0][0]
  
def H(t, a, H0):
  return H0 - ((9.81 - a) / 2.0) * t**2

def simulate(dt, drop, M, V0, alpha):
  Sx = drop.x
  Sz = drop.z
  H0 = drop.y
  T = 0
  V_y = 0
  V_y_prev = 0
  
  #print(Sx, Sz, H0, M, V0, alpha)

  H_cur = H0
  H_prev = H0

  wx_fall = []
  wz_fall = []

  Sx_fall = [[Sx, 0]]
  Sz_fall = [[Sz, 0]]

  is_reduced = False
  
  while H_cur > 0:
    if T == 0:
      T += dt
      H_cur = H(T, 0, H0)
      V_y = (H_prev - H_cur) / dt
      #print(f'Vy == {V_y} H-prev== {H_prev}, H-cur == {H_cur}')
    else:
      T += dt
      Fa = f(V_y)
      if Fa / M >= 9.81:
        H_cur = H_cur - V_y * dt
      else:
        H_cur += H(T, Fa / M, H0) - H(T - dt, f(V_y_prev) / M, H0)
        V_y = (H_prev - H_cur) / dt
      #print(f'T=={T}, Fa == {Fa / M}, Vy == {V_y} H-prev== {H_prev}, H-cur == {H_cur}')

    Wx_pred = get_pred_wind(model_wx, H_cur, X_scaler)
    Wz_pred = get_pred_wind(model_wz, H_cur, X_scaler)
    
    Sx = Sx + (V0 - Wx_pred) * dt * math.cos(math.pi * alpha / 180.0)
    Sz = Sz + (0 + Wz_pred) * dt * math.sin(math.pi * alpha / 180.0)

    Sx_fall.append([Sx, T])
    Sz_fall.append([Sz, T])

    wx_fall.append([T, Wx_pred])
    wz_fall.append([T, Wz_pred])
    
    #print(f'V_y == {V_y}, H_prev=={H_prev}, H_cur == {H_cur}')
    H_prev = H_cur
    V_y_prev = V_y
    
    if not is_reduced and H_cur < 200:
      dt /= 2.0
      is_reduced = True
    
  #print(H_cur, Sx_fall[-1][0], Sz_fall[-1][0], T)
    
  return wx_fall, wz_fall, Sx_fall, Sz_fall

wx_fall, wz_fall, Sx_fall, Sz_fall = simulate(dt=0.1, drop=Point(0.0, 1000.0, 0.0), M=M_global, V0=V0_global, alpha=alpha_global)

fig, axes = plt.subplots(1, 2, figsize=(12 ,6))

wx_fall = np.array(wx_fall)
wz_fall = np.array(wz_fall)

axes[0].plot(wx_fall[:, 0], wx_fall[:, 1])
axes[1].plot(wz_fall[:, 0], wz_fall[:, 1])
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(12 ,6))

Sx_fall = np.array(Sx_fall)
Sz_fall = np.array(Sz_fall)

axes[0].plot(Sx_fall[:, 1], Sx_fall[:, 0])
axes[1].plot(Sz_fall[:, 1], Sz_fall[:, 0])

axes[0].set_xlabel('time')
axes[1].set_xlabel('time')
plt.show()

X_start = 0
Y_start = 1000
Z_start = 0

x_area = 3500
x_num = 13

y_area = 400
y_num = 5

z_area = 30
z_num = 5 

X_drop = np.linspace(X_start - x_area, X_start + x_area, x_num)
Y_drop = np.linspace(Y_start - y_area, Y_start + y_area, y_num)
Z_drop = np.linspace(Z_start - z_area, Z_start + z_area, z_num)

plt.scatter(*np.meshgrid(X_drop, Y_drop))
plt.show()

drops = []

for _x in X_drop:
  for _y in Y_drop:
    for _z in Z_drop:
      drops.append(Point(_x, _y, _z))

min_pos = -1
min_distance = math.inf

for num, drop in enumerate(drops):
  _, _, Sx_fall, Sz_fall = simulate(dt=0.1, drop=drop, M=M_global, V0=V0_global, alpha=alpha_global)
  dist = math.sqrt((0 - Sx_fall[-1][0])**2 + (0 - Sz_fall[-1][0])**2)
  if dist < min_distance:
    min_distance = dist
    min_pos = num
    print(num, min_distance, [Sx_fall[-1][0], Sz_fall[-1][0]])

nearest_drop = drops[min_pos]
#nearest_drop

_, _, Sx_fall, Sz_fall = simulate(dt=0.1, drop=nearest_drop, M=M_global, V0=V0_global, alpha=alpha_global)
math.sqrt((0 - Sx_fall[-1][0])**2 + (0 - Sz_fall[-1][0])**2)

X_start = nearest_drop.x
Y_start = nearest_drop.y
Z_start = nearest_drop.z

x_area = x_area / (2 * x_num)
x_num = 13

y_area = y_area / (2 * y_num)
y_num = 5

z_area = z_area / (2 * z_num)
y_num = 5

X_drop = np.linspace(X_start - x_area, X_start + x_area, x_num)
Y_drop = np.linspace(Y_start - y_area, Y_start + y_area, y_num)
Z_drop = np.linspace(Z_start - z_area, Z_start + z_area, z_num)

plt.scatter(*np.meshgrid(X_drop, Y_drop))
plt.show()

drops = []

for _x in X_drop:
  for _y in Y_drop:
    for _z in Z_drop:
      drops.append(Point(_x, _y, _z))
       
#len(drops)

min_pos = -1
min_distance = math.inf

for num, drop in enumerate(drops):
  _, _, Sx_fall, Sz_fall = simulate(dt=0.1, drop=drop, M=M_global, V0=V0_global, alpha=alpha_global)
  dist = math.sqrt((0 - Sx_fall[-1][0])**2 + (0 - Sz_fall[-1][0])**2)
  if dist < min_distance:
    min_distance = dist
    print(num, min_distance, [Sx_fall[-1][0], Sz_fall[-1][0]])
  if min_distance < 3:
    break
drops[min_pos]