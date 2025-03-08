from mindquantum import *
from BITBLE.mindquantum import qgates
from BITBLE import anglecompute, tools
import numpy as np


def state_preparation(state, target_qubits, is_real=False, control_qubits=None, control_states=None):
    """
    Prepares a quantum state using a series of rotation gates.

    Args:
        state (numpy.array): The input state vector to be prepared.
        target_qubits (list[int]): The list of target qubits on which the state will be prepared.
        is_real (bool, optional): Whether the state is real-valued. If True, only RY gates are used. Defaults to False.
        control_qubits (list[int] or int, optional): Additional control qubits for conditional state preparation. Defaults to None.
        control_states (list[int] or int, optional): The control states for the control qubits (0 or 1). Defaults to None.

    Returns:
        Circuit: The quantum circuit that prepares the desired state.

    Raises:
        ValueError: If the input state is not a valid state vector or if the control qubits/states are inconsistent.
    """
    # Create a circuit object
    circuit = Circuit()

    # The number of target qubits
    n = len(target_qubits)

    # Compute rotation angles
    if is_real:
        norm_angles = anglecompute.binarytree_vector(state, 'norm', True)
    else:
        state_norm = np.abs(state)
        state_phase = np.angle(state)
        norm_angles = anglecompute.binarytree_vector(state_norm, 'norm')
        phase_angles = anglecompute.binarytree_vector(state_phase, 'phase')

        qgates.qgate('RZ',
                     circuit,
                     target_qubit=target_qubits[0],
                     rotation_angle=phase_angles[0])
    qgates.qgate('RY',
                 circuit,
                 target_qubit=target_qubits[0],
                 rotation_angle=norm_angles[0])
    angle_index = 1
    for layer in range(1, n):
        for i in range(2 ** layer):
            qgates.qgate('RY',
                         circuit,
                         target_qubit=target_qubits[layer],
                         control_qubits=target_qubits[:layer],
                         control_states=tools.binary_list(i, layer),
                         rotation_angle=norm_angles[angle_index + i])
        angle_index += 2 ** layer
    if not is_real:
        qgates.qgate('RZ',
                     circuit,
                     target_qubit=0,
                     rotation_angle=phase_angles[1])
        angle_index = 2
        for layer in range(1, n):
            for i in range(2 ** layer):
                qgates.qgate('RZ',
                             circuit,
                             target_qubit=layer,
                             control_qubits=target_qubits[:layer],
                             control_states=tools.binary_list(i, layer),
                             rotation_angle=phase_angles[angle_index + i])
            angle_index += 2 ** layer

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


def compressed_state_preparation(state, target_qubits, is_real=False, epsilon=0, control_qubits=None,
                                 control_states=None):
    """
    Prepares an arbitrary quantum state using compressed circuit.

    Args:
        state (numpy.array): The input state vector to be prepared. It must be a normalized vector
            with a length that is a power of 2.
        target_qubits (list[int]): The list of target qubits on which the state will be prepared.
        is_real (bool, optional): Whether the state is real-valued. If True, only RY gates are used.
            Defaults to False.
        epsilon (float, optional): The threshold for filtering out small rotation angles. Defaults to 0.
        control_qubits (list[int] or int, optional): Additional control qubits for conditional state preparation.
            Defaults to None.
        control_states (list[int] or int, optional): The control states for the control qubits (0 or 1). Defaults to None.

    Returns:
        Circuit: The compressed quantum circuit that prepares the desired state.

    Raises:
        ValueError: If the input state is not a valid state vector, or if the control qubits/states are inconsistent.
    """
    # Create a circuit object
    circuit = Circuit()

    # The number of target qubits
    n = len(target_qubits)

    # Compute rotation angles
    if is_real:
        norm_angles = anglecompute.binarytree_vector(state, 'norm', True)
    else:
        state_norm = np.abs(state)
        state_phase = np.angle(state)
        norm_angles = anglecompute.binarytree_vector(state_norm, 'norm')
        phase_angles = anglecompute.binarytree_vector(state_phase, 'phase')

        if abs(phase_angles[0]) > epsilon:
            qgates.qgate('RZ',
                         circuit,
                         target_qubit=target_qubits[0],
                         rotation_angle=phase_angles[0])
    if abs(norm_angles[0]) > epsilon:
        qgates.qgate('RY',
                     circuit,
                     target_qubit=target_qubits[0],
                     rotation_angle=norm_angles[0])
    angle_index = 1
    for layer in range(1, n):
        ur_angles = anglecompute.uniformly_rotation_angles(norm_angles[angle_index: angle_index + 2 ** layer])
        ur_circuit = qgates.compress_uniformly_rotation('RY',
                                                        target_qubit=target_qubits[layer],
                                                        control_qubits=target_qubits[:layer],
                                                        rotation_angles=ur_angles.flatten(),
                                                        epsilon=epsilon)
        circuit += ur_circuit
        angle_index += 2 ** layer
    if not is_real:
        if abs(phase_angles[1]) > epsilon:
            qgates.qgate('RZ',
                         circuit,
                         target_qubit=target_qubits[0],
                         rotation_angle=phase_angles[1])
        angle_index = 2
        for layer in range(1, n):
            ur_angles = anglecompute.uniformly_rotation_angles(phase_angles[angle_index: angle_index + 2 ** layer])
            ur_circuit = qgates.compress_uniformly_rotation('RZ',
                                                            target_qubit=target_qubits[layer],
                                                            control_qubits=target_qubits[:layer],
                                                            rotation_angles=ur_angles,
                                                            epsilon=epsilon)
            circuit += ur_circuit
            angle_index += 2 ** layer

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


def get_prepared_state(unitary):
    """
    Retrieves the prepared state from a given unitary matrix.

    This function extracts the first column of the unitary matrix, which represents the prepared state,
        and then reverses the index bits of the state to obtain the correct qubit ordering.

    Args:
        unitary (numpy.array): The unitary matrix representing the quantum circuit.

    Returns:
        numpy.array: The prepared state vector.
    """
    state = unitary[:, 0].flatten()
    state = tools.reverse_index_bits(state)

    return state