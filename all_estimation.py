import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

tmp_list = [11810, 16631, 16990, 16447, 15232, 18261, 14723, 17619, 17100, 19138, 17748, 14416, 13179, 18794, 19298,
            17875, 19597, 18657, 19538, 15164, 12772, 18327, 15907, 10070, 15048, 10810, 14336]

fig, ax = plt.subplots()
poly = PolynomialFeatures(degree=3, include_bias=False)
poly_reg_model = LinearRegression()

for fn in tmp_list:
    for i in range(2, 3):
        file_name = str(fn) + '/' + 'task' + str(i) + '.pickle'
        try:
            rfile = open(file_name, 'rb')
            rdata = pickle.load(rfile)


            x_val1 = [x[0] / rdata.p_f[-1][0] for x in rdata.p_f]
            y_val1 = [x[1] for x in rdata.p_f]
            x_val2 = [x[0] / rdata.p_f[-1][0] for x in rdata.p_e]
            y_val2 = [x[1] for x in rdata.p_e]
            # ax.plot(x_val1, y_val1, linewidth=3)


            xarr = np.array(x_val1)
            yarr = np.array(y_val1)

            xpoly = poly.fit_transform(xarr.reshape(-1, 1))
            poly_reg_model.fit(xpoly, yarr)
            y_predicted = poly_reg_model.predict(xpoly)
            plt.plot(xarr, y_predicted, color='green')
        except:
            pass


ax.set_xlabel('time (s)', fontsize=16)
ax.set_ylabel(r'$p_e, p_f$', fontsize=20)
lgd = ax.legend([r'$p_f$', r'$p_e$'], fontsize=15, loc='upper left', frameon=False,
                bbox_to_anchor=(0.25, 1), ncol=2)
ax.set_title(r'Bayes estimate of $p_e$ and $p_f$', fontsize=16)
ax.set_ylim([0, 1.19])
ax.set_xlim([0, round(x_val1[-1] + 0.1)])
ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)
plt.show()