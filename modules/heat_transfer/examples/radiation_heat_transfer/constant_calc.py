from __future__ import annotations

import argparse

import numpy as np

from numpy.polynomial.legendre import leggauss



def _cos_theta2_from_mu(mu: np.ndarray, n1: float, n2: float):

    mu = np.clip(mu, 0.0, 1.0)

    sin_theta1 = np.sqrt(np.maximum(0.0, 1.0 - mu**2))

    sin_theta2 = (n1 / n2) * sin_theta1

    tir_mask = sin_theta2 > 1.0

    cos_theta2 = np.zeros_like(mu)

    valid = ~tir_mask

    cos_theta2[valid] = np.sqrt(np.maximum(0.0, 1.0 - sin_theta2[valid] ** 2))

    return cos_theta2, tir_mask



def fresnel_rho(mu: np.ndarray | float, n1: float, n2: float) -> np.ndarray:

    mu_arr = np.asarray(mu, dtype=float)

    cos1 = np.clip(mu_arr, 0.0, 1.0)

    cos2, tir_mask = _cos_theta2_from_mu(cos1, n1, n2)

    with np.errstate(divide="ignore", invalid="ignore"):

        Rs = ((n1 * cos1 - n2 * cos2) / (n1 * cos1 + n2 * cos2)) ** 2

        Rp = ((n1 * cos2 - n2 * cos1) / (n1 * cos2 + n2 * cos1)) ** 2

    rho = 0.5 * (Rs + Rp)

    if np.any(tir_mask):

        rho = np.where(tir_mask, 1.0, rho)

    return np.nan_to_num(rho, nan=1.0)



def rho_minus(mu: np.ndarray | float, n1: float, n2: float) -> np.ndarray:

    return fresnel_rho(mu, n2, n1)



def hemispheric_alpha(n1: float, n2: float, N: int = 400) -> float:

    if N < 32:

        N = 32

    x, w = leggauss(N)

    mu = 0.5 * (x + 1.0)

    weights = 0.5 * w

    rho_vals = fresnel_rho(mu, n1, n2)

    integral = np.sum(weights * (mu * (1.0 - rho_vals)))

    return float(2.0 * n1 * integral)



def P1(mu): return mu

def P2(mu): return 0.5 * (3.0 * mu**2 - 1.0)

def P3(mu): return 0.5 * (5.0 * mu**3 - 3.0 * mu)



def r_integrals(n1: float, n2: float, N: int = 800):

    if N < 64:

        N = 64

    x, w = leggauss(N)

    mu = 0.5 * (x + 1.0)

    weights = 0.5 * w

    rmin = rho_minus(mu, n1, n2)

    r1 = float(np.sum(weights * (mu * rmin)))

    r2 = float(np.sum(weights * (mu**2 * rmin)))

    r3 = float(np.sum(weights * (mu**3 * rmin)))

    r4 = float(np.sum(weights * (mu * P3(mu) * rmin)))

    r5 = float(np.sum(weights * (P3(mu) * rmin)))

    r6 = float(np.sum(weights * (P2(mu) * P3(mu) * rmin)))

    r7 = float(np.sum(weights * (P3(mu) * P3(mu) * rmin)))

    return r1, r2, r3, r4, r5, r6, r7



def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--n1", type=float, required=True)

    parser.add_argument("--n2", type=float, required=True)

    parser.add_argument("--N", type=int, default=400)

    parser.add_argument("--save-plot", action="store_true")

    args = parser.parse_args()

    a = hemispheric_alpha(args.n1, args.n2, N=args.N)

    print(f"alpha = {a:.12g}")

    r1, r2, r3, r4, r5, r6, r7 = r_integrals(args.n1, args.n2, N=max(2*args.N, 800))
    # r1 = 0.0
    # r2 = 0.0
    # r3 = 0.0
    # r4 = 0.0
    # r5 = 0.0
    # r6 = 0.0
    # r7 = 0.0

    A1 = (1 - 2*r1)/4
    A2 = (1 - 8*r3)*5/16
    A3 = (1 + 3*r2)/6
    A4 = ((1 + 3*r2)/3 + 3*r4/2) #*2/3

    B1 = -(1 + 8*r5)/16
    B2 = (1 - 8*r6)*5/16
    B3 = 3*r4/6
    B4 = r4 + 3/14*(1+7*r7)

    w0 = 7/36*np.sqrt(6/5)
    gamma1 = 5/7*(1 - 3*np.sqrt(6/5))
    gamma2 = 5/7*(1 + 3*np.sqrt(6/5))

    C1 = w0*(gamma2*A1 - A2)
    C2 = w0*(A2 - gamma1*A1)
    C3 = w0*(gamma2*A3 - A4)
    C4 = w0*(A4 - gamma1*A3)

    D1 = w0*(gamma2*B1 - B2)
    D2 = w0*(B2 - gamma1*B1)
    D3 = w0*(gamma2*B3 - B4)
    D4 = w0*(B4 - gamma1*B3)

    D = C3*D4 - D3*C4
    rho1 = (1-2*r1) * np.pi
    rho3 = -(1/4 + 2*r5) * np.pi

    alpha1 = (C1*D4 - D1*C4)/D
    alpha2 = (C3*D2 - C2*D3)/D
    beta1 = (C3*D1 - D3*C1)/D
    beta2 = (C2*D4 - D2*C4)/D
    eta1 = (D4*rho1 - C4*rho3)/D
    eta2 = (C3*rho3 - D3*rho1)/D

    alpha11 = 5/96*(34+11*np.sqrt(6/5))
    alpha22 = 5/96*(34-11*np.sqrt(6/5))
    beta11 = 5/96*(2-np.sqrt(6/5))
    beta22 = 5/96*(2+np.sqrt(6/5))
    eta11 = 5*np.pi/2*(3+np.sqrt(6/5))
    eta22 = 5*np.pi/2*(3-np.sqrt(6/5))

    print(f"alpha1 = {alpha1:.12g} | {alpha11:.12g}")
    print(f"alpha2 = {alpha2:.12g} | {alpha22:.12g}")
    print(f"beta1 = {beta1:.12g} | {beta11:.12g}")
    print(f"beta2 = {beta2:.12g} | {beta22:.12g}")
    print(f"eta1 = {eta1:.12g} | {eta11:.12g}")
    print(f"eta2 = {eta2:.12g} | {eta22:.12g}")

    if args.save-plot:

        import matplotlib.pyplot as plt

        mu_plot = np.linspace(0.0, 1.0, 2001)

        rho_in = fresnel_rho(mu_plot, args.n1, args.n2)

        rho_out = rho_minus(mu_plot, args.n1, args.n2)

        import matplotlib.pyplot as plt

        plt.figure()

        plt.plot(mu_plot, rho_in, label="rho(mu) n1→n2")

        plt.plot(mu_plot, rho_out, label="rho(-mu) n2→n1", linestyle="--")

        plt.xlabel("mu")

        plt.ylabel("rho")

        plt.legend()

        plt.grid(True, which="both", alpha=0.3)

        plt.tight_layout()

        plt.savefig("rho_mu_both.png", dpi=200)

        print("Saved rho_mu_both.png")



if __name__ == "__main__":

    main()

# import numpy as np
# from scipy.integrate import quad
# import matplotlib.pyplot as plt

# def const_internal(n1, n2):
#     muc = np.sqrt(1 - (n2/n1)**2)
    
#     def rho_internal(mu):
#         if abs(mu) < abs(muc):
#             return 1.0
        
#         sin1 = np.sqrt(1.0 - mu**2)
#         sin2 = (n1/n2) * sin1
#         mu2 = np.sqrt(1.0 - sin2 **2)

#         # Rs = ((n1*mu - n2*mu2)/(n1*mu2 + n2*mu)) ** 2
#         # Rp = ((n1*mu2 - n2*mu)/(n1*mu2 + n2*mu)) ** 2

#         # return 0.5*(Rs+Rp)
#         prefix = 0.5 * ((n1*mu-n2*mu2)/(n1*mu + n2*mu2))**2
#         parse = 1 + ((n2*mu*mu2-n1*(1-mu*mu))/(n2*mu*mu2+n1*(1-mu*mu)))**2

#         return prefix * parse
    
#     def P2(mu):
#         return (3/2*mu**2 - 1/2)
    
#     def P3(mu):
#         return (5/2*mu**3 - 3/2*mu)
    
#     alpha_integrand = lambda mu : 1.0 - rho_internal(mu)
#     alpha_I, _ = quad(alpha_integrand, 0.0,1.0)
#     alpha_calc = 2.0 * n1 * alpha_I

#     r1_integrand = lambda mu : mu * rho_internal(mu)
#     r1, _ = quad(r1_integrand, 0.0, 1.0)

#     r2_integrand = lambda mu : mu**2 * rho_internal(mu)
#     r2, _ = quad(r2_integrand, 0.0, 1.0)

#     r3_integrand = lambda mu : mu**3 * rho_internal(mu)
#     r3, _ = quad(r3_integrand, 0.0, 1.0)

#     r4_integand = lambda mu : mu * P3(mu) * rho_internal(mu)
#     r4, _ = quad(r4_integand, 0.0, 1.0)

#     r5_integrand = lambda mu: P3(mu) * rho_internal(mu)
#     r5, _ = quad(r5_integrand, 0.0, 1.0)

#     r6_integrand = lambda mu: P2(mu) * P3(mu) * rho_internal(mu)
#     r6, _ = quad(r6_integrand, 0.0, 1.0)

#     r7_integrand = lambda mu: P3(mu) * P3(mu) * rho_internal(mu)
#     r7, _ = quad(r7_integrand, 0.0, 1.0)

#     # r1 = 0.0
#     # r2 = 0.0
#     # r3 = 0.0
#     # r4 = 0.0
#     # r5 = 0.0
#     # r6 = 0.0
#     # r7 = 0.0

#     rho1 = (1 - 2*r1)*np.pi
#     rho3 = -(1/4 + 2*r5)*np.pi

#     gamma1 = 5/7*(1 - 3*np.sqrt(6/5))
#     gamma2 = 5/7*(1 + 3*np.sqrt(6/5))

#     w0 = 1/(gamma2 - gamma1)

#     A1 = (1-2*r1)/4
#     A2 = (1-8*r3)*5/16
#     A3 = (1+3*r2)/6
#     A4 = ((1+3*r2)/3 + (3*r4/2))  *2/3

#     # print("A1-4")
#     # print(A1, A2, A3, A4)

#     B1 = -(1+8*r5)/16
#     B2 = (1-8*r6)*5/16
#     B3 = 3*r4/6
#     B4 = r4 + 3/14*(1+7*r7)

#     # print("B1-4")
#     # print(B1, B2, B3, B4)
    
#     C1 = w0 * (gamma2*A1 - A2)
#     C2 = w0 * (A2 - gamma1*A1)
#     C3 = w0 * (gamma2*A3 - A4)
#     C4 = w0 * (A4 - gamma1*A3)

#     # print(C1, C2, C3, C4)

#     D1 = w0 * (gamma2*B1 - B2)
#     D2 = w0 * (B2 - gamma1*B1)
#     D3 = w0 * (gamma2*B3 - B4)
#     D4 = w0 * (B4 - gamma1*B3)

#     # print(D1, D2, D3, D4)

#     D = C3*D4 - D3*C4
#     # print(f"given {np.sqrt(6/5)/144}, got {D} : {C3} * {D4} - {D3} * {C4}")

#     alpha1 = (C1*D4 - D1*C4) / D
#     alpha2 = (C3*D2 - C2*D3) / D
#     beta1 = (C3*D1 - D3*C1) / D
#     beta2 = (C2*D4 - D2*C4) / D
#     eta1 = (D4*rho1 - C4*rho3) / D
#     eta2 = (C3*rho3 - D3*rho1) / D

#     return alpha_calc, alpha1, alpha2, beta1, beta2, eta1, eta2


# def main():
#     n1 = 1.0
#     n2 = 1.46

#     alpha_calc, alpha1, alpha2, beta1, beta2, eta1, eta2 = const_internal(n1, n2)

#     print(f"n1 = {n1}, n2 = {n2}")
#     print(f"alpha_calc: {alpha_calc:.6f}")
#     print(f"alpha1: {alpha1:.6f}")
#     print(f"alpha2: {alpha2:.6f}")
#     print(f"beta1: {beta1:.6f}")
#     print(f"beta2: {beta2:.6f}")
#     print(f"eta1: {eta1:.6f}")
#     print(f"eta2: {eta2:.6f}")

# if __name__ == "__main__":
#     main()
