from mindquantum import *
from ble import tools


# Simulate controlled gate
def qgate(gate, circuit, target_qubit, control_qubits=None, control_states=None, rotation_angle=None):
    """
    Simulate a quantum gate on a quantum circuit, including single-qubit gates and controlled gates.

    Args:
        gate (str): The type of quantum gate to apply. Supported gates include 'X', 'Y', 'Z', 'H', 'SWAP', 'RX', 'RY', 'RZ'.
        circuit: The quantum circuit to which the gate will be added.
        target_qubit: The target qubit on which the gate will be applied.
        control_qubits (list, optional): The control qubits for conditional gate application. Defaults to None.
        control_states (list, optional): The control states for the control qubits (0 or 1). Defaults to None.
        rotation_angle (float, optional): The rotation angle for rotation gates (RX, RY, RZ). Defaults to None.

    Returns:
        None: The function modifies the input circuit in place.

    Raises:
        ValueError: If the specified gate is not supported.

    Note:
        - The `control_qubits` and `control_states` must be provided together if used.
        - The length of `control_qubits` and `control_states` must match.
        - The function assumes that the input circuit is a valid quantum circuit object.
        - The function modifies the input circuit in place.

    See Also:
        mindquantum.circuit.gates: The quantum gates used in this function (X, Y, Z, H, SWAP, RX, RY, RZ).
    """
    # Perform gate if it has no control qubits
    if control_qubits is None:
        if gate == 'X':
            circuit += X.on(target_qubit)
        elif gate == 'Y':
            circuit += Y.on(target_qubit)
        elif gate == 'Z':
            circuit += Z.on(target_qubit)
        elif gate == 'H':
            circuit += H.on(target_qubit)
        elif gate == 'SWAP':
            circuit += SWAP.on(target_qubit)
        elif gate == 'RX':
            circuit += RX(rotation_angle).on(target_qubit)
        elif gate == 'RY':
            circuit += RY(rotation_angle).on(target_qubit)
        elif gate == 'RZ':
            circuit += RZ(rotation_angle).on(target_qubit)
        else:
            raise ValueError(gate + ' is not supported')
    # Perform gate if it has control qubits
    else:
        # Ensure "control_qubits" and "control_states" be lists
        if not isinstance(control_qubits, list):
            control_qubits = [control_qubits]
        if not isinstance(control_states, list):
            control_states = [control_states]

        # Select control qubits with control states being 0
        qubits_state0 = [control_qubits[index] for index, state in enumerate(control_states) if state == 0]

        # Perform X gates on the control qubits with control states being 0
        for qubit in qubits_state0:
            circuit += X.on(qubit)

        # Perform controlled gates
        if gate == 'X':
            circuit += X.on(target_qubit, control_qubits)
        elif gate == 'Y':
            circuit += Y.on(target_qubit, control_qubits)
        elif gate == 'Z':
            circuit += Z.on(target_qubit, control_qubits)
        elif gate == 'H':
            circuit += H.on(target_qubit, control_qubits)
        elif gate == 'SWAP':
            circuit += SWAP.on(target_qubit, control_qubits)
        elif gate == 'RX':
            circuit += RX(rotation_angle).on(target_qubit, control_qubits)
        elif gate == 'RY':
            circuit += RY(rotation_angle).on(target_qubit, control_qubits)
        elif gate == 'RZ':
            circuit += RZ(rotation_angle).on(target_qubit, control_qubits)
        else:
            raise ValueError(gate + ' is not supported')

        # Perform X gates on the control qubits with control states being 0
        for qubit in qubits_state0:
            circuit += X.on(qubit)


def compress_uniformly_rotation(gate, target_qubit, control_qubits, rotation_angles, epsilon=None, gate_ctrl_qubits=None, gate_ctrl_states=None):
    """
    Constructs a compressed quantum circuit that implements the decomposition of a uniformly controlled rotation.

     Args:
        gate (str): The type of rotation gate to apply (e.g., 'RX', 'RY', 'RZ').
        target_qubit (int): The target qubit on which the rotation gates will be applied.
        control_qubits (list or int): The control qubits used for the Gray code compression.
        rotation_angles (numpy.ndarray): The uniformly distributed rotation angles.
        epsilon (float, optional): The threshold for filtering out small rotation angles. Defaults to 0.
        gate_ctrl_qubits (list or int, optional): Additional control qubits for the entire circuit. Defaults to None.
        gate_ctrl_states (list or int, optional): The control states for the additional control qubits. Defaults to None.

    Returns:
        Circuit: The compressed quantum circuit with the specified rotation gates.

    Raises:
        ValueError: If the input gate type is not supported or if the control qubits/states are inconsistent.

    Note:
        This function assumes that the length of the rotation angles list matches the number of control qubits.

    """

    # Create a circuit object
    circuit = Circuit()

    if epsilon is None:
        epsilon = 0
    if not isinstance(control_qubits, list):
        control_qubits = [control_qubits]

    rotation_angles = rotation_angles.flatten()

    # Perform single qubit controlled rotation gates and CNOT gates
    cnot_gate_ctrl_qubits = []
    for i in range(len(rotation_angles)):
        if abs(rotation_angles[i]) > epsilon:
            for qubit in cnot_gate_ctrl_qubits:
                circuit += X.on(target_qubit, control_qubits[qubit])
            cnot_gate_ctrl_qubits.clear()
            qgate(gate,
                  circuit,
                  target_qubit=target_qubit,
                  rotation_angle=rotation_angles[i])
        # The control qubit of CNOT gate is up to the index of different bits between the gray codes of i and i+1
        # The control qubit of the last CNOT gate is the top one of "control_qubits"
        if i != len(rotation_angles) - 1:
            ctrl_qubit = tools.different_gray_codes_index(i, i + 1, len(control_qubits))
        else:
            ctrl_qubit = 0
        if ctrl_qubit not in cnot_gate_ctrl_qubits:
            cnot_gate_ctrl_qubits.append(ctrl_qubit)
        else:
            cnot_gate_ctrl_qubits.remove(ctrl_qubit)
    if cnot_gate_ctrl_qubits is not None:
        for qubit in cnot_gate_ctrl_qubits:
            circuit += X.on(target_qubit, control_qubits[qubit])
        cnot_gate_ctrl_qubits.clear()

    if gate_ctrl_qubits is not None:
        if not isinstance(gate_ctrl_qubits, list):
            gate_ctrl_qubits = [gate_ctrl_qubits]
        if not isinstance(gate_ctrl_states, list):
            gate_ctrl_states = [gate_ctrl_states]
        gate_ctrl_qubits_state0 = [gate_ctrl_qubits[index] for index, state in enumerate(gate_ctrl_states) if state == 0]
        circ = Circuit()
        for qubit in gate_ctrl_qubits_state0:
            circ += X.on(qubit)
        circ += controlled(circuit)(gate_ctrl_states)
        for qubit in gate_ctrl_qubits_state0:
            circ += X.on(qubit)

        return circ

    else:
        return circuit

