# Mathematical Model

The state is $[m,U,T_s,n_{CO_2},Q_v]$. Air temperature follows
$T=U/(mc_v)$, pressure follows $P=mR_{air}T/V$, density is $m/V$, and
CO₂ ppm is $10^6 n_{CO_2}/(m/M_{air})$. Nonphysical denominators and states
are rejected.

## Balances

$$
\dot m=\dot m_{in}-\dot m_{out}
$$

$$
\dot U=\dot Q_p+\dot Q_t+\dot Q_e+H(T_s-T)
+\dot m_{in}c_pT_o-\dot m_{out}c_pT
$$

$$
\dot T_s=[H(T-T_s)+UA(T_o-T_s)]/C_s
$$

$$
\dot n_{CO_2}=y_o\dot m_{in}/M_{air}
-y_i\dot m_{out}/M_{air}+N_pg_{CO_2}
$$

$$
\dot Q_v=(Q_{target}-Q_v)/\tau_v
$$

The structure/air heat term appears once in each subsystem with opposite sign.
Passenger CO₂ volume is converted at 298.15 K by
$\dot n=P\dot V/(R_uT)$.

## Air exchange and pressure

$$
Q_l=C_l\,sign(\Delta P)\sqrt{|\Delta P|}
$$

Positive leakage is outward. Mechanical supply and exhaust use equal volume
flows; piston exchange is bidirectional. Inflow mass uses outdoor density and
outflow mass uses indoor density, so equal volume flow need not mean equal mass
flow. The leakage law is a low-order approximation, not a pressure network.

The demand controller clips base plus positive temperature and CO₂ demands
between available limits. V2 equations are newly formulated after the 2024
competition.
