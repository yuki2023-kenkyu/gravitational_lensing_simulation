import numpy as np
from scipy.integrate import solve_ivp

def schwarzschild_geodesic(Rs, initial_conditions, t_span):
    def equations(t, w):
        r, theta, phi, pr, ptheta, pphi = w
        drdt = pr
        dthetadt = ptheta
        dphidt = pphi
        dprdt = -Rs/(2*r**2) * pr**2 + r*ptheta**2 + r*np.sin(theta)**2 * pphi**2 - Rs/(2*r**2)
        dpthetadt = -2/r * pr*ptheta + np.sin(theta)*np.cos(theta) * pphi**2
        dpphidt = 0
        return [drdt, dthetadt, dphidt, dprdt, dpthetadt, dpphidt]

    sol = solve_ivp(equations, t_span, initial_conditions, method='RK45', dense_output=True)
    return sol

def kerr_geodesic(Rs, a, initial_conditions, t_span):
    def equations(t, w):
        r, theta, phi, pr, ptheta, pphi = w
        delta = r**2 - Rs*r + a**2
        drdt = pr
        dthetadt = ptheta
        dphidt = pphi
        dprdt = -Rs/(2*r**2) * pr**2 + r*ptheta**2 + r*np.sin(theta)**2 * pphi**2 - Rs/(2*r**2) + 2*a*pphi/r
        dpthetadt = -2/r * pr*ptheta + np.sin(theta)*np.cos(theta) * pphi**2
        dpphidt = 0
        return [drdt, dthetadt, dphidt, dprdt, dpthetadt, dpphidt]

    sol = solve_ivp(equations, t_span, initial_conditions, method='RK45', dense_output=True)
    return sol
