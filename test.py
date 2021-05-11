import numpy as np
import matplotlib.pyplot as plt

n= 6

m1 = (0.10,0.12,0.10,0.11,0.14,0.10)
m2=(0.21,0.21,0.20,0.22,0.20,0.21)
m3=(0.29,0.27,0.28,0.24,0.23,0.23)
m4=(0.41,0.39,0.35,0.37,0.41,0.40)
x=[1,2,3,4,5,6]

fig, ax = plt.subplots()

index = np.arange(n)
bar_width = 0.2

opacity = 0.4
error_config = {'ecolor': '0.3'}
r1 = ax.bar(index, m1, bar_width,
                 alpha=opacity,
                 color='b',

                 error_kw=error_config)

r2 = ax.bar(index + bar_width, m2, bar_width,
                 alpha=opacity,
                 color='r',

                 error_kw=error_config)

r3 = ax.bar(index + bar_width+ bar_width, m3, bar_width,
                 alpha=opacity,
                 color='y',
                 error_kw=error_config)
r4 = ax.bar(index + bar_width+ bar_width+ bar_width, m4, bar_width,
                 alpha=opacity,
                 color='c',
                 error_kw=error_config)                 
plt.xlabel('D')
plt.ylabel('Anz')
plt.title('Th')

f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')

ax1.bar(x,m1, 0.2)
ax2.bar(x,m2, 0.2)
ax3.plot(x,m3)
ax4.plot(x,m4)

plt.tight_layout()
plt.show()