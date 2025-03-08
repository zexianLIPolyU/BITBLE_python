# BITBLE
Binary Tree Block encoding for quantum circuits


## Install Python

1. Download and install [Anaconda](https://www.anaconda.com/download)

2. Create a virtual environment with Python 3.9.11 as an example

   ```
   conda create -n quantum python=3.9.11 -y
   conda activate quantum
   ```

## Install Python packages

```
pip install numpy
```

```
pip install mindquantum
```

```
pip install pyqpanda
```

## Note

Put the folder "BITBLE" under the root directory of your project

## pyqpanda - implementation


### State Preparation ###

1. Real amplitude state preparation
 ```
    from pyqpanda import *
    from ble.qpanda import statepreparation

    n = 3
    epsilon = 0
    state = np.random.randn(2 ** n)
    state = state / np.linalg.norm(state)

    circuit = statepreparation.compressed_state_preparation(state, list(range(n)), is_real=True, epsilon=epsilon)
    print(circuit)

    unitary = circuit.matrix()
    res_state = statepreparation.get_prepared_state(unitary)

    print('The prepared state (s):')
    print(res_state)
    print('')
    print('The state to be prepared (s0):')
    print(state)
    print('')
    print('||s - s0||_F:')
    print(np.linalg.norm(res_state - state))
```
Output:
```
--------Real state preparation--------
          ┌──┐                                             
q_0:  |0>─┤RY├ ─■─ ──── ─■─ ─── ──── ─■─ ──── ─── ──── ─■─ 
          ├──┤ ┌┴┐ ┌──┐ ┌┴┐           │                 │  
q_1:  |0>─┤RY├ ┤X├ ┤RY├ ┤X├ ─■─ ──── ─┼─ ──── ─■─ ──── ─┼─ 
          ├──┤ └─┘ └──┘ └─┘ ┌┴┐ ┌──┐ ┌┴┐ ┌──┐ ┌┴┐ ┌──┐ ┌┴┐ 
q_2:  |0>─┤RY├ ─── ──── ─── ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ 
          └──┘              └─┘ └──┘ └─┘ └──┘ └─┘ └──┘ └─┘ 
 c :   / ═
          


The prepared state (s):
[ 0.38460008+0.j -0.22085312+0.j  0.10700528+0.j -0.70755671+0.j
  0.26296034+0.j  0.12902675+0.j  0.09317466+0.j  0.44355664+0.j]

The state to be prepared (s0):
[ 0.38460008 -0.22085312  0.10700528 -0.70755671  0.26296034  0.12902675
  0.09317466  0.44355664]

||s - s0||_F:
4.918300529807393e-16
```
2. Complex amplitude state preparation
```
    from pyqpanda import *
    from ble.qpanda import statepreparation

    n = 3
    epsilon = 0
    state = np.random.randn(2 ** n) + 1j * np.random.randn(2 ** n)
    state = state / np.linalg.norm(state)

    circuit = statepreparation.compressed_state_preparation(state, list(range(n)), epsilon=epsilon)
    print(circuit)

    unitary = circuit.matrix()
    res_state = statepreparation.get_prepared_state(unitary)

    print('The prepared state (s):')
    print(res_state)
    print('')
    print('The state to be prepared (s0):')
    print(state)
    print('')
    print('||s - s0||_F:')
    print(np.linalg.norm(res_state - state))
```
Output:
```
--------Complex state preparation--------

          ┌──┐ ┌──┐                                             ┌──┐                                             
q_0:  |0>─┤RZ├ ┤RY├ ─■─ ──── ─■─ ─── ──── ─■─ ──── ─── ──── ─■─ ┤RZ├ ─■─ ──── ─■─ ─── ──── ─■─ ──── ─── ──── ─■─ 
          ├──┤ └──┘ ┌┴┐ ┌──┐ ┌┴┐           │           ┌──┐  │  └──┘ ┌┴┐ ┌──┐ ┌┴┐           │                 │  
q_1:  |0>─┤RY├ ──── ┤X├ ┤RY├ ┤X├ ─■─ ──── ─┼─ ──── ─■─ ┤RZ├ ─┼─ ──── ┤X├ ┤RZ├ ┤X├ ─■─ ──── ─┼─ ──── ─■─ ──── ─┼─ 
          ├──┤      └─┘ └──┘ └─┘ ┌┴┐ ┌──┐ ┌┴┐ ┌──┐ ┌┴┐ ├──┤ ┌┴┐ ┌──┐ └─┘ └──┘ └─┘ ┌┴┐ ┌──┐ ┌┴┐ ┌──┐ ┌┴┐ ┌──┐ ┌┴┐ 
q_2:  |0>─┤RY├ ──── ─── ──── ─── ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RZ├ ─── ──── ─── ┤X├ ┤RZ├ ┤X├ ┤RZ├ ┤X├ ┤RZ├ ┤X├ 
          └──┘                   └─┘ └──┘ └─┘ └──┘ └─┘ └──┘ └─┘ └──┘              └─┘ └──┘ └─┘ └──┘ └─┘ └──┘ └─┘ 
 c :   / ═
          


The prepared state (s):
[-0.27644244+0.1610026j  -0.01573856-0.34984595j -0.44353131+0.19808173j
  0.06034424+0.23572727j -0.20606243-0.10696451j  0.49705746+0.21671312j
  0.05255242-0.03075348j  0.20549343+0.29322989j]

The state to be prepared (s0):
[-0.27644244+0.1610026j  -0.01573856-0.34984595j -0.44353131+0.19808173j
  0.06034424+0.23572727j -0.20606243-0.10696451j  0.49705746+0.21671312j
  0.05255242-0.03075348j  0.20549343+0.29322989j]

||s - s0||_F:
3.7789906771029953e-16
```

### Block Encoding ###

**QPanda**: test_blockencoding_pyqpanda.py
1. Real matrix encoding
 ```
    from pyqpanda import *
    from ble.qpanda import blockencoding
    import numpy as np

    n = 3
    epsilon = 0
    matrix = np.random.randn(2 ** n, 2 ** n)
    matrix = matrix / np.linalg.norm(matrix)

    num_qubits = 2 * n
    init(QMachineType.CPU)
    qubits = qAlloc_many(num_qubits)
    cbits = cAlloc_many(num_qubits)
    circuit = blockencoding.compress_qcircuit(matrix, qubits, is_real=True, epsilon=epsilon)
    print(circuit)

    unitary = get_unitary(circuit)
    unitary = np.array(unitary).reshape(2 ** num_qubits, 2 ** num_qubits)
    res_matrix = blockencoding.get_encoded_matrix(unitary, n)

    print('The encoded matrix (A):')
    print(res_matrix)
    print('')
    print('The matrix to be encoded (A0):')
    print(matrix)
    print('')
    print('||A - A0||_F:')
    print(np.linalg.norm(res_matrix - matrix))
```
Output:
```
--------Real matrix--------
          ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐                                                          >
q_0:  |0>─┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├─── ─── ──── ─── ──── ─■─ ──── ─── ──── ─── ──── ─── ──── >
          ├──┤ └┬┘ └──┘ └┬┘ └──┘ └┬┘ ├─┬┘ └┬┼──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌┴┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ >
q_1:  |0>─┤RY├ ─┼─ ──── ─┼─ ──── ─┼─ ┤X├─ ─┼┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ >
          └──┘  │        │        │  └┬┘   │└──┘ └┬┘ └──┘ └┬┘ └──┘ └─┘ └──┘ └┬┘ └──┘ └┬┘ └──┘ └┬┘ └──┘ >
q_2:  |0>───── ─┼─ ──── ─■─ ──── ─┼─ ─┼── ─■──── ─■─ ──── ─┼─ ──── ─── ──── ─┼─ ──── ─■─ ──── ─┼─ ──── >
                │                 │   │                    │                 │                 │       >
q_3:  |0>───── ─■─ ──── ─── ──── ─■─ ─■── ────── ─── ──── ─■─ ──── ─── ──── ─■─ ──── ─── ──── ─■─ ──── >
                                                                                                       >
 c :   / ═
          

                                 ┌──────┐ 
q_0:  |0>─■─ X─ ─■─ ──────── ─■─ ┤RY.dag├ 
         ┌┴┐ │  ┌┴┐ ┌──────┐ ┌┴┐ ├──────┤ 
q_1:  |0>┤X├ ┼X ┤X├ ┤RY.dag├ ┤X├ ┤RY.dag├ 
         └─┘ ││ └─┘ └──────┘ └─┘ └──────┘ 
q_2:  |0>─── X┼ ─── ──────── ─── ──────── 
              │                           
q_3:  |0>─── ─X ─── ──────── ─── ──────── 
                                          
 c :   / 
         


The encoded matrix (A):
[[-0.28255199+0.j -0.17499563+0.j  0.05215907+0.j -0.2713498 +0.j]
 [-0.15682983+0.j -0.07541978+0.j  0.19680222+0.j  0.01425079+0.j]
 [-0.32159963+0.j  0.2243003 +0.j -0.33002954+0.j -0.19212792+0.j]
 [-0.03625142+0.j  0.44664007+0.j  0.12867116+0.j  0.47649168+0.j]]

The matrix to be encoded (A0):
[[-0.28255199 -0.17499563  0.05215907 -0.2713498 ]
 [-0.15682983 -0.07541978  0.19680222  0.01425079]
 [-0.32159963  0.2243003  -0.33002954 -0.19212792]
 [-0.03625142  0.44664007  0.12867116  0.47649168]]

||A - A0||_F:
4.838852477487593e-16
```
2. complex matrix encoding
```
    from pyqpanda import *
    from ble.qpanda import blockencoding
    import numpy as np

    n = 3
    epsilon = 0
    matrix = np.random.randn(2 ** n, 2 ** n) + 1j * np.random.randn(2 ** n, 2 ** n)
    matrix = matrix / np.linalg.norm(matrix)

    num_qubits = 2 * n
    init(QMachineType.CPU)
    qubits = qAlloc_many(num_qubits)
    cbits = cAlloc_many(num_qubits)
    circuit = blockencoding.compress_qcircuit(matrix, qubits, epsilon=epsilon)
    print(circuit)

    unitary = get_unitary(circuit)
    unitary = np.array(unitary).reshape(2 ** num_qubits, 2 ** num_qubits)
    res_matrix = blockencoding.get_encoded_matrix(unitary, n)

    print('The encoded matrix (A):')
    print(res_matrix)
    print('')
    print('The matrix to be encoded (A0):')
    print(matrix)
    print('')
    print('||A - A0||_F:')
    print(np.linalg.norm(res_matrix - matrix))

```
Output:
```
--------Complex matrix--------

          ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐                      >
q_0:  |0>─┤RZ├ ┤X├ ┤RZ├ ┤X├ ┤RZ├ ┤X├ ┤RZ├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├─── ─── ──── ─── ──── >
          ├──┤ └┬┘ └──┘ └┬┘ └──┘ └┬┘ └──┘ └┬┘ └──┘ └┬┘ └──┘ └┬┘ └──┘ └┬┘ ├─┬┘ └┬┼──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ >
q_1:  |0>─┤RY├ ─┼─ ──── ─┼─ ──── ─┼─ ──── ─┼─ ──── ─┼─ ──── ─┼─ ──── ─┼─ ┤X├─ ─┼┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ >
          └──┘  │        │        │        │        │        │        │  └┬┘   │└──┘ └┬┘ └──┘ └┬┘ └──┘ >
q_2:  |0>───── ─┼─ ──── ─■─ ──── ─┼─ ──── ─■─ ──── ─┼─ ──── ─■─ ──── ─┼─ ─┼── ─■──── ─■─ ──── ─┼─ ──── >
                │                 │                 │                 │   │                    │       >
q_3:  |0>───── ─■─ ──── ─── ──── ─■─ ──── ─── ──── ─■─ ──── ─── ──── ─■─ ─■── ────── ─── ──── ─■─ ──── >
                                                                                                       >
 c :   / ═
          

                                                 ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐                 >
q_0:  |0>─■─ ──── ─── ──── ─── ──── ─── ──── ─■─ ┤RZ├ ┤X├ ┤RZ├ ┤X├ ┤RZ├ ┤X├ ┤RZ├ ┤X├─── ─── ──── ─── >
         ┌┴┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌┴┐ ├──┤ └┬┘ └──┘ └┬┘ └──┘ └┬┘ ├─┬┘ └┬┼──┐ ┌─┐ ┌──┐ ┌─┐ >
q_1:  |0>┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RY├ ┤X├ ┤RZ├ ─┼─ ──── ─┼─ ──── ─┼─ ┤X├─ ─┼┤RZ├ ┤X├ ┤RZ├ ┤X├ >
         └─┘ └──┘ └┬┘ └──┘ └┬┘ └──┘ └┬┘ └──┘ └─┘ └──┘  │        │        │  └┬┘   │└──┘ └┬┘ └──┘ └┬┘ >
q_2:  |0>─── ──── ─┼─ ──── ─■─ ──── ─┼─ ──── ─── ──── ─┼─ ──── ─■─ ──── ─┼─ ─┼── ─■──── ─■─ ──── ─┼─ >
                   │                 │                 │                 │   │                    │  >
q_3:  |0>─── ──── ─■─ ──── ─── ──── ─■─ ──── ─── ──── ─■─ ──── ─── ──── ─■─ ─■── ────── ─── ──── ─■─ >
                                                                                                     >
 c :   / 
         

                                                                          ┌──────┐ 
q_0:  |0>──── ─■─ ──── ─── ──── ─── ──── ─── ──── ─■─ X─ ─■─ ──────── ─■─ ┤RY.dag├ 
         ┌──┐ ┌┴┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌─┐ ┌──┐ ┌┴┐ │  ┌┴┐ ┌──────┐ ┌┴┐ ├──────┤ 
q_1:  |0>┤RZ├ ┤X├ ┤RZ├ ┤X├ ┤RZ├ ┤X├ ┤RZ├ ┤X├ ┤RZ├ ┤X├ ┼X ┤X├ ┤RY.dag├ ┤X├ ┤RY.dag├ 
         └──┘ └─┘ └──┘ └┬┘ └──┘ └┬┘ └──┘ └┬┘ └──┘ └─┘ ││ └─┘ └──────┘ └─┘ └──────┘ 
q_2:  |0>──── ─── ──── ─┼─ ──── ─■─ ──── ─┼─ ──── ─── X┼ ─── ──────── ─── ──────── 
                        │                 │            │                           
q_3:  |0>──── ─── ──── ─■─ ──── ─── ──── ─■─ ──── ─── ─X ─── ──────── ─── ──────── 
                                                                                   
 c :   / 
         


The encoded matrix (A):
[[ 0.0717925 -0.29259169j -0.15164446+0.14305347j -0.07978028+0.04929215j
  -0.06278604+0.0579586j ]
 [-0.09443328-0.02357717j -0.26869318+0.06971573j -0.29271985+0.07387712j
  -0.10569737-0.17675179j]
 [ 0.06225808-0.35331841j  0.20143416+0.1131481j  -0.13867982+0.00457545j
  -0.00672616+0.29886571j]
 [ 0.26427384+0.11476363j -0.04505902+0.10454406j  0.10836367-0.36276957j
   0.04147132+0.31281208j]]

The matrix to be encoded (A0):
[[ 0.0717925 -0.29259169j -0.15164446+0.14305347j -0.07978028+0.04929215j
  -0.06278604+0.0579586j ]
 [-0.09443328-0.02357717j -0.26869318+0.06971573j -0.29271985+0.07387712j
  -0.10569737-0.17675179j]
 [ 0.06225808-0.35331841j  0.20143416+0.1131481j  -0.13867982+0.00457545j
  -0.00672616+0.29886571j]
 [ 0.26427384+0.11476363j -0.04505902+0.10454406j  0.10836367-0.36276957j
   0.04147132+0.31281208j]]

||A - A0||_F:
4.637263367040817e-16
```



