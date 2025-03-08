"""
Block Encoding:
Let A be a complex matrix in $\mathbb{C}^{2^n × 2^n}$ and UA be a unitary in $\mathbb{C}^{2^(n+a) × 2^(n+a)}$.
UA is a block encoding of A if
UA = [[A  *]
      [*  *]]
where * denotes a matrix block yet to be determined.
For an arbitrary matrix A, its block encoding can be realized via the following circuit,
\ket{0}^{\otimes n} —/———|PREP_j|———×———|PREP_GLOBAL†|——
                             |      |
            \ket{j} —/———————▢—————×———————————————————
where PREP_j is a oracle to prepare the j-th column of A, i.e.,
$ PREP_j \ket{0}^{\otimes n} \ket{j} = (1/||A_j||_F) \sum_{i=0}^{2^n-1} A_{ij} \ket{i} \ket{j} $,
PREP_norm is a oracle to prepare a state whose j-th component is the Frobenius norm ||A_j||_F of the j-th column of A, i.e.,
$ PREP_GLOBAL \ket{0}^{\otimes n} = (1/||A||_F) \sum_{i=0}^{2^n-1} ||A_j||_F \ket{j}$,
and ||A||_F is the Frobenius norm of A.
"""
from mindquantum import *
from BITBLE.mindquantum import qgates
from BITBLE import anglecompute, tools
import numpy as np


def qcircuit(matrix, target_qubits, is_real=False, control_qubits=None, control_states=None):
    """
    Constructs a quantum circuit to block encoding a given matrix.

    Args:
        matrix (numpy.array): The input unitary matrix to be implemented.
        target_qubits (list[int] or int): The list of target qubits used to implement the matrix.
        is_real (bool, optional): Whether the matrix is real-valued. If True, only RY gates are used. Defaults to False.
        control_qubits (list[int] or int, optional): Additional control qubits for conditional application of the circuit. Defaults to None.
        control_states (list[int] or int, optional): The control states for the control qubits (0 or 1). Defaults to None.

    Returns:
        Circuit: The quantum circuit that block encodes the given matrix.
    """
    # Create a circuit object
    circuit = Circuit()

    n = int(np.log2(len(matrix)))

    # Compute rotation angles
    if is_real:
        norm_angles = anglecompute.rotation_angles_matrix(matrix, True)
    else:
        norm_angles, phase_angles = anglecompute.rotation_angles_matrix(matrix)

    # PREP_j
    circuit_PREP = Circuit()
    if not is_real:
        for col in range(2 ** n):
            qgates.qgate('RZ',
                         circuit_PREP,
                         target_qubit=target_qubits[0],
                         control_qubits=target_qubits[n: 2 * n],
                         control_states=tools.binary_list(col, n),
                         rotation_angle=phase_angles[0, col])
    for col in range(2 ** n):
        angle_index = 0
        for layer in range(n):
            for i in range(2 ** layer):
                qgates.qgate('RY',
                             circuit_PREP,
                             target_qubit=target_qubits[layer],
                             control_qubits=target_qubits[:layer] + target_qubits[n: 2 * n],
                             control_states=tools.binary_list(i, layer) + tools.binary_list(col, n),
                             rotation_angle=norm_angles[angle_index + i, col])
            angle_index += 2 ** layer
    if not is_real:
        for col in range(2 ** n):
            angle_index = 1
            for layer in range(n):
                for i in range(2 ** layer):
                    qgates.qgate('RZ',
                                 circuit_PREP,
                                 target_qubit=target_qubits[layer],
                                 control_qubits=target_qubits[:layer] + target_qubits[n: 2 * n],
                                 control_states=tools.binary_list(i, layer) + tools.binary_list(col, n),
                                 rotation_angle=phase_angles[angle_index + i, col])
                angle_index += 2 ** layer
    circuit += circuit_PREP

    # SWAP
    for qubit in range(n):
        qgates.qgate('SWAP',
                     circuit,
                     target_qubit=[target_qubits[qubit], target_qubits[n + qubit]])

    # PREP_GLOBAL ^{dagger}
    circuit_GLOBAL = Circuit()
    angle_index = 0
    for layer in range(n):
        for i in range(2 ** layer):
            qgates.qgate('RY',
                         circuit_GLOBAL,
                         target_qubit=target_qubits[layer],
                         control_qubits=target_qubits[:layer],
                         control_states=tools.binary_list(i, layer),
                         rotation_angle=-norm_angles[angle_index + i, 2 ** n])
        angle_index += 2 ** layer
    circuit_GLOBAL.reverse()
    circuit += circuit_GLOBAL

    if control_qubits is not None:
        if not isinstance(control_qubits, list):
            control_qubits = [control_qubits]
        if control_states is not None:
            control_states = [control_states]
        qubits_state0 = [control_qubits[index] for index, state in enumerate(control_states) if state == 0]
        circ = Circuit()
        for qubit in qubits_state0:
            circ += X.on(qubit)
        circ += controlled(circuit)(control_qubits)
        for qubit in qubits_state0:
            circ += X.on(qubit)
        return circ
    else:
        return circuit


def compress_qcircuit(matrix, target_qubits, is_real=False, epsilon=0, control_qubits=None, control_states=None):
    """
    Constructs a compressed quantum circuit to block encode a given matrix

    Args:
        matrix (numpy.array): The input unitary matrix to be implemented. It must be a square matrix with dimensions that are a power of 2.
        target_qubits (list[int] or int): The list of target qubits used to implement the matrix. The type of each qubit should be `pyqpanda.pyQPanda.Qubit`.
        is_real (bool, optional): Whether the matrix is real-valued. If True, only RY gates are used. Defaults to False.
        epsilon (float, optional): The threshold for filtering out small rotation angles. Defaults to 0.
        control_qubits (list[int] or int, optional): Additional control qubits for conditional application of the circuit. Defaults to None.
        control_states (list[int] or int, optional): The control states for the control qubits (0 or 1). Defaults to None.

    Returns:
        Circuit: The compressed quantum circuit that block encodes the given matrix.
    """
    # Create a circuit object
    circuit = Circuit()

    n = int(np.log2(len(matrix)))

    # Compute rotation angles
    if is_real:
        norm_angles = anglecompute.rotation_angles_matrix(matrix, True)
    else:
        norm_angles, phase_angles = anglecompute.rotation_angles_matrix(matrix)

    # PREP_j
    circuit_PREP = Circuit()
    if not is_real:
        ur_circuit = qgates.compress_uniformly_rotation('RZ',
                                                        target_qubit=target_qubits[0],
                                                        control_qubits=target_qubits[n: 2 ** n],
                                                        rotation_angles=anglecompute.uniformly_rotation_angles(
                                                            phase_angles[0, :]),
                                                        epsilon=epsilon)
        circuit_PREP += ur_circuit
    angle_index = 0
    for layer in range(n):
        r_angles = norm_angles[angle_index: angle_index + 2 ** layer, :2 ** n].flatten()
        ur_angles = anglecompute.uniformly_rotation_angles(r_angles)
        ur_circuit = qgates.compress_uniformly_rotation('RY',
                                                        target_qubit=target_qubits[layer],
                                                        control_qubits=target_qubits[:layer] + target_qubits[n: 2 * n],
                                                        rotation_angles=ur_angles,
                                                        epsilon=epsilon)
        circuit_PREP += ur_circuit
        angle_index += 2 ** layer
    if not is_real:
        angle_index = 1
        for layer in range(n):
            r_angles = phase_angles[angle_index: angle_index + 2 ** layer, :].flatten()
            ur_angles = anglecompute.uniformly_rotation_angles(r_angles)
            ur_circuit = qgates.compress_uniformly_rotation('RZ',
                                                            target_qubit=target_qubits[layer],
                                                            control_qubits=target_qubits[:layer] + target_qubits[n: 2 * n],
                                                            rotation_angles=ur_angles,
                                                            epsilon=epsilon)
            circuit_PREP += ur_circuit
            angle_index += 2 ** layer
    circuit += circuit_PREP

    # SWAP
    for qubit in range(n):
        qgates.qgate('SWAP',
                     circuit,
                     target_qubit=[target_qubits[qubit], target_qubits[n + qubit]])

    # PREP_GLOBAL ^{dagger}
    circuit_GLOBAL = Circuit()
    if abs(norm_angles[0, -1]) > epsilon:
        qgates.qgate('RY',
                     circuit_GLOBAL,
                     target_qubit=target_qubits[0],
                     rotation_angle=-norm_angles[0, -1])
    angle_index = 1
    for layer in range(1, n):
        r_angles = - norm_angles[angle_index: angle_index + 2 ** layer, -1].flatten()
        ur_angles = anglecompute.uniformly_rotation_angles(r_angles)
        ur_circuit = qgates.compress_uniformly_rotation('RY',
                                                        target_qubit=target_qubits[layer],
                                                        control_qubits=target_qubits[:layer],
                                                        rotation_angles=ur_angles,
                                                        epsilon=epsilon)
        circuit_GLOBAL += ur_circuit
        angle_index += 2 ** layer
    circuit_GLOBAL.reverse()
    circuit += circuit_GLOBAL

    if control_qubits is not None:
        if not isinstance(control_qubits, list):
            control_qubits = [control_qubits]
        if not isinstance(control_states, list):
            control_states = [control_states]
        qubits_state0 = [control_qubits[index] for index, state in enumerate(control_states) if state == 0]
        circ = Circuit()
        for qubit in qubits_state0:
            circ += X.on(qubit)
        circ += controlled(circuit)(control_qubits)
        for qubit in qubits_state0:
            circ += X.on(qubit)
        return circ
    else:
        return circuit


def get_encoded_matrix(unitary, num_working_qubits):
    """
    Extracts the block-encoded matrix from a given unitary matrix.

    Args:
        unitary (numpy.array): The unitary matrix representing the quantum circuit.
        num_working_qubits (int): The number of working qubits used in the encoding.

    Returns:
        numpy.array: The block-encoded matrix.
    """
    unitary = tools.reverse_index_bits(unitary)
    matrix = unitary[: 2 ** num_working_qubits, : 2 ** num_working_qubits]

    return matrix