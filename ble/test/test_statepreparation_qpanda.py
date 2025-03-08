import numpy as np
from pyqpanda import *
from ble.qpanda import statepreparation


def test_real_state(n, epsilon):
    """
     Tests the preparation of a random real-valued quantum state using compressed state preparation.

    Args:
        n (int): The number of qubits used to represent the state. The state will have 2^n amplitudes.
        epsilon (float): The threshold for filtering out small rotation angles during the compressed
            state preparation process. This parameter controls the trade-off between circuit complexity
            and accuracy.

    Returns:
        None: The function prints the constructed quantum circuit, the prepared state, the original
            state, and the Frobenius norm of their difference.
    """
    state = np.random.randn(2 ** n)
    state = state / np.linalg.norm(state)

    num_qubits = n
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(num_qubits)
    cbits = machine.cAlloc_many(num_qubits)

    circuit = statepreparation.compressed_state_preparation(state, qubits, is_real=True, epsilon=epsilon)
    print(circuit)

    unitary = get_unitary(circuit)
    unitary = np.array(unitary).reshape(2 ** num_qubits, 2 ** num_qubits)
    res_state = statepreparation.get_prepared_state(unitary)

    print('The prepared state (s):')
    print(res_state)
    print('')
    print('The state to be prepared (s0):')
    print(state)
    print('')
    print('||s - s0||_F:')
    print(np.linalg.norm(res_state - state))


def test_complex_state(n, epsilon):
    """
     Tests the preparation of a random complex-valued quantum state using compressed state preparation.

    Args:
        n (int): The number of qubits used to represent the state. The state will have 2^n amplitudes.
        epsilon (float): The threshold for filtering out small rotation angles during the compressed
            state preparation process. This parameter controls the trade-off between circuit complexity
            and accuracy.

    Returns:
        None: The function prints the constructed quantum circuit, the prepared state, the original
            state, and the Frobenius norm of their difference.
    """
    state = np.random.randn(2 ** n) + 1j * np.random.randn(2 ** n)
    state = state / np.linalg.norm(state)

    num_qubits = n
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(num_qubits)
    cbits = machine.cAlloc_many(num_qubits)

    circuit = statepreparation.compressed_state_preparation(state, qubits, epsilon=epsilon)
    print(circuit)

    unitary = get_unitary(circuit)
    unitary = np.array(unitary).reshape(2 ** num_qubits, 2 ** num_qubits)
    res_state = statepreparation.get_prepared_state(unitary)

    print('The prepared state (s):')
    print(res_state)
    print('')
    print('The state to be prepared (s0):')
    print(state)
    print('')
    print('||s - s0||_F:')
    print(np.linalg.norm(res_state - state))


if __name__ == '__main__':
    n = 3
    epsilon = 0

    print('--------Real state preparation--------')
    test_real_state(n, epsilon)
    print('')
    print('--------Complex state preparation--------')
    test_complex_state(n, epsilon)