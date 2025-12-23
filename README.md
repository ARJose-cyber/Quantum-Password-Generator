# ⚛️ Quantum-Safe Password Generator

A web-based application that leverages **true quantum randomness** to generate secure passwords. Unlike classical pseudo-random number generators (PRNGs), this tool uses the inherent unpredictability of qubit superposition on actual IBM Quantum hardware.

## 🚀 How it Works
1. **Quantum Superposition:** The app creates a quantum circuit with a single qubit.
2. **Hadamard Gate:** We apply an $H$ gate to put the qubit into a state of 50/50 superposition ($|0\rangle$ and $|1\rangle$).
3. **Measurement:** Measuring the qubit collapses the state, yielding a truly random bit.
4. **Entropy Harvesting:** These bits are used as the entropy source to build a high-complexity password.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Quantum Framework:** [Qiskit](https://www.ibm.com/quantum/qiskit)
- **Frontend:** [Streamlit](https://streamlit.io/)
- **Hardware:** IBM Quantum Platform (via Qiskit Runtime)

## ⚙️ Setup & Installation

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/quantum-password-gen.git](https://github.com/YOUR_USERNAME/quantum-password-gen.git)
   cd quantum-password-gen
