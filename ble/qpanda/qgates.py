from pyqpanda import *
from ble import tools


def qgate(gate, circuit, target_qubit, control_qubits=None, control_states=None, rotation_angle=None):
    """
    Simulate a quantum gate on a quantum circuit, including single-qubit gates and controlled gates.

    Applies a quantum gate to a target qubit, optionally controlled by one or more control qubits.
    The gate is applied only when the control qubits are in the specified states.

    Args:
        gate (str): The type of quantum gate to apply ('X', 'Y', 'Z', 'H', 'SWAP', 'RX', 'RY', 'RZ').
        circuit (QCircuit): The quantum circuit to which the gate will be added.
        target_qubit (Qubit or list[Qubit]): The target qubit(s) for the gate.
        control_qubits (Qubit or list[Qubit], optional): A single qubit or a list of control qubit(s) for the gate. Defaults to None.
        control_states (int or list[int], optional): A single state or a list of state(s) of the control qubit(s) that trigger the gate. Defaults to None.
        rotation_angle (float, optional): The angle of rotation for RX, RY, RZ gates. Defaults to None.

    Returns:
        None

    Raises:
        ValueError: If the specified gate is not supported.

    Note:
        The function assumes that the quantum circuit and qubits are properly initialized.
        The target_qubit and control_qubits must be of type pyqpanda.pyQPanda.Qubit or a list of such types.

    See Also:
        pyqpanda.Qubit: The class representing a quantum bit in pyqpanda.
    """
    # Perform gate if it has no control qubits
    if control_qubits is None or control_qubits == []:
        if gate == 'X':
            circuit << X(target_qubit)
        elif gate == 'Y':
            circuit << Y(target_qubit)
        elif gate == 'Z':
            circuit << Z(target_qubit)
        elif gate == 'H':
            circuit << H(target_qubit)
        elif gate == 'SWAP':
            circuit << SWAP(target_qubit[0], target_qubit[1])
        elif gate == 'RX':
            circuit << RX(target_qubit, rotation_angle)
        elif gate == 'RY':
            circuit << RY(target_qubit, rotation_angle)
        elif gate == 'RZ':
            circuit << RZ(target_qubit, rotation_angle)
        else:
            raise ValueError(gate + ' is not supported.')
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
            circuit << X(qubit)

        # Perform controlled gates
        if gate == 'X':
            circuit << X(target_qubit).control(control_qubits)
        elif gate == 'Y':
            circuit << Y(target_qubit).control(control_qubits)
        elif gate == 'Z':
            circuit << Z(target_qubit).control(control_qubits)
        elif gate == 'H':
            circuit << H(target_qubit).control(control_qubits)
        elif gate == 'SWAP':
            circuit << SWAP(target_qubit[0], target_qubit[1]).control(control_qubits)
        elif gate == 'RX':
            circuit << RX(target_qubit, rotation_angle).control(control_qubits)
        elif gate == 'RY':
            circuit << RY(target_qubit, rotation_angle).control(control_qubits)
        elif gate == 'RZ':
            circuit << RZ(target_qubit, rotation_angle).control(control_qubits)
        else:
            raise ValueError(gate + ' is not supported')

        # Perform X gates on the control qubits with control states being 0
        for qubit in qubits_state0:
            circuit << X(qubit)


def compressed_uniformly_rotation(gate, target_qubit, control_qubits, rotation_angles, epsilon=None, gate_ctrl_qubits=None, gate_ctrl_states=None):
    """
    Constructs a compressed quantum circuit that implements the decomposition of a uniformly controlled rotation.

    Args:
        gate (str): The type of rotation gate, such as "Rx", "Ry", or "Rz".
        target_qubit (Qubit): The target qubit.
        control_qubits (Qubit or list[Qubit]): A single qubit or a list of qubit(s) for the control qubits.
        rotation_angles (float or list[float] or numpy.array): A single rotation angle or a list of rotation angles for rotation gate(s).
        gate_ctrl_qubits (Qubit or list[Qubit], optional): Additional control qubit(s) for the entire gate sequence. Defaults to None.
        gate_ctrl_states (int or list[int], optional): The state(s) of the additional control qubit(s) that trigger the gate sequence. Defaults to None.

    Returns:
        QCircuit: The constructed quantum circuit object.

    Raises:
        TypeError: If the input argument types are incorrect.

    Note:
        This function assumes that the length of the rotation angles list matches the number of control qubits.
    """

    # Create a QCircuit object
    circuit = QCircuit()

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
                circuit << X(target_qubit).control(control_qubits[qubit])
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
            circuit << X(target_qubit).control(control_qubits[qubit])
        cnot_gate_ctrl_qubits.clear()

    if gate_ctrl_qubits is not None:
        if not isinstance(gate_ctrl_qubits, list):
            gate_ctrl_qubits = [gate_ctrl_qubits]
        if not isinstance(gate_ctrl_states, list):
            gate_ctrl_states = [gate_ctrl_states]
        gate_ctrl_qubits_state0 = [gate_ctrl_qubits[index] for index, state in enumerate(gate_ctrl_states) if state == 0]
        circ = QCircuit()
        for qubit in gate_ctrl_qubits_state0:
            circ << X(qubit)
        circ << circuit.control(gate_ctrl_qubits)
        for qubit in gate_ctrl_qubits_state0:
            circ << X(qubit)

        return circ

    else:
        return circuit