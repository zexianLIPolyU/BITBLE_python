from mindquantum import *
from ble.mindquantum import blockencoding
import numpy as np


def test_real_matrix(n, epsilon):
    """
    Tests the block encoding of a random real-valued matrix using compressed quantum circuit.

    Args:
        n (int): The number of qubits used to represent the matrix. The matrix will have dimensions
            2^n × 2^n.
        epsilon (float): The threshold for filtering out small rotation angles during the compressed
            quantum circuit construction. This parameter controls the trade-off between circuit
            complexity and accuracy.

    Returns:
        None: The function prints the constructed quantum circuit, the encoded matrix, the original
            matrix, and the Frobenius norm of their difference.
    """
    matrix = np.random.randn(2 ** n, 2 ** n)
    matrix = matrix / np.linalg.norm(matrix)

    qubits = list(range(2 * n))
    circuit = blockencoding.compress_qcircuit(matrix, qubits, is_real=True, epsilon=epsilon)
    print(circuit)

    unitary = circuit.matrix()
    res_matrix = blockencoding.get_encoded_matrix(unitary, n)

    print('The encoded matrix (A):')
    print(res_matrix)
    print('')
    print('The matrix to be encoded (A0):')
    print(matrix)
    print('')
    print('||A - A0||_F:')
    print(np.linalg.norm(res_matrix - matrix))


def test_complex_matrix(n, epsilon):
    """
    Tests the block encoding of a random complex-valued matrix using compressed quantum circuit.

    Args:
        n (int): The number of qubits used to represent the matrix. The matrix will have dimensions
            2^n × 2^n.
        epsilon (float): The threshold for filtering out small rotation angles during the compressed
            quantum circuit construction. This parameter controls the trade-off between circuit
            complexity and accuracy.

    Returns:
        None: The function prints the constructed quantum circuit, the encoded matrix, the original
            matrix, and the Frobenius norm of their difference.
    """
    matrix = np.random.randn(2 ** n, 2 ** n) + 1j * np.random.randn(2 ** n, 2 ** n)
    matrix = matrix / np.linalg.norm(matrix)

    qubits = list(range(2 * n))
    circuit = blockencoding.compress_qcircuit(matrix, qubits, epsilon=epsilon)
    print(circuit)

    unitary = circuit.matrix()
    res_matrix = blockencoding.get_encoded_matrix(unitary, n)

    print('The encoded matrix (A):')
    print(res_matrix)
    print('')
    print('The matrix to be encoded (A0):')
    print(matrix)
    print('')
    print('||A - A0||_F:')
    print(np.linalg.norm(res_matrix - matrix))


if __name__ == '__main__':
    n = 2
    epsilon = 0

    print('--------Real matrix--------')
    test_real_matrix(n, epsilon)
    print('')
    print('--------Complex matrix--------')
    test_complex_matrix(n, epsilon)