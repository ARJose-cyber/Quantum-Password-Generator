import streamlit as st
import os
import string
from dotenv import load_dotenv

# Quantum Libraries
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit_aer import Aer
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# 1. Load Environment Variables
load_dotenv()
API_KEY = os.getenv('API_Key')

# 2. Page Configuration
st.set_page_config(page_title="Quantum Pass", page_icon="⚛️", layout="centered")
st.title("⚛️ Quantum-Safe Password Generator")
st.markdown("""
This app generates passwords using **True Randomness** from quantum superposition.
Standard computers use math to 'guess' random numbers; Quantum computers use physics.
""")

# 3. Sidebar Settings
st.sidebar.header("Settings")
mode = st.sidebar.radio("Backend Source:", ["Local Simulator (Fast)", "IBM Quantum (Real Hardware)"])
pass_length = st.sidebar.slider("Password Length", 8, 32, 16)

def generate_quantum_bits(bit_length, use_hardware):
    # Create the base circuit: 1 qubit, 1 measurement
    qc = QuantumCircuit(1)
    qc.h(0)  # Put qubit in superposition (50/50 chance of 0 or 1)
    qc.measure_all()
    
    try:
        if use_hardware:
            if not API_KEY:
                st.error("API Key not found in .env file!")
                return None
            
            # Connect to IBM
            service = QiskitRuntimeService(channel="ibm_quantum_platform", token=API_KEY)
            backend = service.least_busy(simulator=False, operational=True)
            st.info(f"Connected to: {backend.name}. Sending job to queue...")
            
            # ISA Transpilation (Mandatory for modern IBM hardware)
            pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
            isa_circuit = pm.run(qc)
            
            # Run Job
            sampler = SamplerV2(backend)
            job = sampler.run([isa_circuit], shots=bit_length)
        else:
            # Use Local Simulator
            backend = Aer.get_backend('qasm_simulator')
            sampler = SamplerV2(backend)
            job = sampler.run([qc], shots=bit_length)
            
        # Get Results
        result = job.result()
        pub_result = result[0]
        bitstrings = pub_result.data.meas.get_bitstrings()
        return "".join(bitstrings)

    except Exception as e:
        st.error(f"Quantum Error: {e}")
        return None

# 4. Main UI Logic
if st.button("Generate Secure Password"):
    with st.spinner("Harvesting Quantum Entropy..."):
        # We fetch 8 bits per character to ensure high entropy
        raw_bits = generate_quantum_bits(pass_length * 8, mode == "IBM Quantum (Real Hardware)")
        
        if raw_bits:
            # Character set for the password
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ""
            
            # Convert 8-bit chunks into characters
            for i in range(0, len(raw_bits), 8):
                byte = raw_bits[i:i+8]
                index = int(byte, 2) % len(chars)
                password += chars[index]
            
            st.success("Generation Complete!")
            st.subheader("Your New Password:")
            st.code(password)
            
            # Visual Feedback
            with st.expander("See Raw Quantum Data"):
                st.write(f"**Backend used:** {mode}")
                st.write(f"**Raw Bits Collected:** {raw_bits[:64]}...")
                st.write(f"**Entropy source:** Hadamard Gate ($H$) on Qubit 0")

