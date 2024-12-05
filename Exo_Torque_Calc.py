import numpy as np

# Constants
g = 9.81  # Gravitational acceleration (m/s^2)
m_person = 80  # Person's mass (kg)
l1 = 0.4  # Thigh length (m)
l2 = 0.4  # Lower leg length (m)

# Masses
m_h1 = 0.1 * m_person  # Thigh mass of person (kg)
m_h2 = 0.06 * m_person  # Lower leg mass of person (kg)
m_e1 = 2  # Exoskeleton thigh mass (kg)
m_e2 = 1.5  # Exoskeleton lower leg mass (kg)

# Calculate moments of inertia for thigh (I1) and lower leg (I2)
m1_total = m_h1 + m_e1  # Total mass of thigh segment (kg)
m2_total = m_h2 + m_e2  # Total mass of lower leg segment (kg)

I1 = (1/3) * m1_total * l1**2  # Moment of inertia for thigh segment (kg·m²)
I2 = (1/3) * m2_total * l2**2  # Moment of inertia for lower leg segment (kg·m²)

print(f"Moment of inertia of the thigh (I1): {I1:.4f} kg·m²")
print(f"Moment of inertia of the lower leg (I2): {I2:.4f} kg·m²")

# Joint angles (in radians)
q1 = np.radians(30)  # Convert 30 degrees to radians
q2 = np.radians(45)  # Convert 45 degrees to radians

# Joint velocities (rad/s)
q_dot = np.array([0.5, 0.5])  # [q1_dot, q2_dot]

# Joint accelerations (rad/s^2)
q_ddot = np.array([0.1, 0.1])  # [q1_ddot, q2_ddot]

# Inertia matrix A(q)
a11 = (m_h1 + m_e1) * l1**2 + (m_h2 + m_e2) * (l1**2 + l2**2 + 2 * l1 * l2 * np.cos(q2)) + I1+I2
a12 = (m_h2 + m_e2) * (l2**2 + l1 * l2 * np.cos(q2)) + I2
a22 = (m_h2 + m_e2) * l2**2 + I2
a21 = m2_total*(l2**2+l1*l2*np.cos(q2))+I2
A = np.array([[a11, a12], [a21, a22]])

# Coriolis and Centrifugal matrix B(q, q_dot)
b12 = -(m_h2 + m_e2) * l1 * l2 * np.sin(q2) * q_dot[1]
b21 = (m_h2 + m_e2) * l1 * l2 * np.sin(q2) * q_dot[0]
b11 = -m2_total*(l1*l3*np.sin(q2))*q_dot[1]
B = np.array([[b11, b12], [b21, 0]])

# Gravity vector C(q)
g1 = ((m_h1 + m_e1)*l1 + m2_total*l2)*g*np.sin(q1)+ (m_h2 + m_e2) * l2 * g * np.sin(q1+q2)
g2 = (m_h2 + m_e2) * l2 * g * np.sin(q1 + q2)
C = np.array([g1, g2])

# Friction vector Psi_M(q_dot)
Be1, Be2 = 0.1, 0.1  # Friction coefficients (N.m.s/rad)
alpha, beta = 0.1, 0.1  # Static friction (N.m)
Psi_M = np.array([Be1 * q_dot[0] + alpha * np.sign(q_dot[0]), Be2 * q_dot[1] + beta * np.sign(q_dot[1])])

# Calculate torques
tau_A = A @ q_ddot  # Inertia-related torques
tau_B = B @ q_dot   # Coriolis and centrifugal-related torques
tau = tau_A + tau_B + C + Psi_M  # Total torque

# Output the results
print(f"Necessary torques (N·m):\nτ1 = {tau[0]:.2f} N·m\nτ2 = {tau[1]:.2f} N·m")
