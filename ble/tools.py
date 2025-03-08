import copy
import numpy as np


def gray_code(x):
    """
    Get the Gray code of the input number.

    Args:
        x (int): A non-negative integer.

    Returns:
        int: Gray code of the input number.
    """
    return x ^ (x >> 1)


def different_gray_codes_index(number1, number2, length):
    """
    Get the index of the different bit between the gray codes of number1 and number2

    Args:
        number1 (int): A non-negative integer.
        number2 (int): A non-negative integer.
        length (int): The length of the gray codes.

    Returns:
        int: The index of the different bit between the gray codes of number1 and number2.
    """
    gray_code_number1 = gray_code(number1)
    gray_code_number2 = gray_code(number2)
    diff = gray_code_number1 ^ gray_code_number2    # Calculate XOR of the two Gray codes
    index = length - 1 - int(np.log2(diff))

    return index


def phase_angle_matrix_inverse(N):
    """
    Generate a matrix which computes phase_angles from phase

    This function constructs a matrix that can be used to calculate phase angles from phase values.
    The matrix is built recursively by combining smaller matrices.

    Args:
        N (int): The dimension of the matrix. It must be a power of two.

    Returns:
        np.array: A NumPy array representing the matrix which computes phase angles.
    """
    matrix = [[-1, -1], [-1, 1]]
    if N != 2:
        k = 2
        while k != N:
            leftward = np.kron(matrix, [1/2, 1/2])
            rightward = np.kron(np.eye(k), [-1, 1])
            matrix = np.vstack([leftward, rightward])
            k = 2 * k

    return np.array(matrix)


def mikko_matrix(n):
    """
    Generate the Mikko matrix, which computes rotation angles for the decomposition of a uniformly controlled rotation.

    The Mikko matrix is a tool used in control theory to decompose a rotation into a series of simpler rotations.
    This function constructs the Mikko matrix using the binary and Gray code representations of numbers.

    The main logic of the function involves the following steps:
    1. Generate a vector of binary numbers from 0 to (2^n) - 1.
    2. Convert these binary numbers to their corresponding Gray code representation.
    3. Compute the bitwise AND between the binary and Gray code representations.
    4. Use the result to build the Mikko matrix through a series of bitwise XOR operations.

    Args:
        n (int): The logarithm of the dimension of the Mikko matrix. This means the matrix will be of size (2^n) x (2^n).

    Returns:
        np.array: A NumPy array representing the Mikko matrix.
    """
    vec = np.arange(2 ** n).reshape(-1, 1)
    vec_gray = np.array([gray_code(x) for x in vec]).reshape(1, -1)
    binary_times_gray = np.bitwise_and(vec_gray, vec)
    mikko_matrix = np.zeros((2 ** n, 2 ** n), dtype=int)
    for i in range(n):
        mikko_matrix = np.bitwise_xor(
            mikko_matrix, np.bitwise_and(binary_times_gray,
                                         np.ones((2 ** n, 2 ** n), dtype=int))
        )
        binary_times_gray = binary_times_gray >> 1
    mikko_matrix = -1 * mikko_matrix + (mikko_matrix == 0)

    return mikko_matrix


def sfwht(input_array):
    """
    Computes the Scaled Fast Walsh-Hadamard Transform (SFWHT) of a given array.

    Args:
        input_array (numpy.array): The input array to be transformed. It can
            be a 1D column vector or a 2D square matrix with dimensions that are
            a power of 2.

    Returns:
        numpy.array: The transformed array after applying the SFWHT.
    """
    n = input_array.shape[0]
    k = int(np.log2(n))

    for h in range(1, k + 1):
        for i in range(1, n + 1, 2 ** h):
            for j in range(i, i + 2 ** (h - 1)):
                # Create a deep copy of the array to avoid modifying the original array
                temp = copy.deepcopy(input_array)
                # Extract the current element/row and the corresponding element/row to be combined
                x = temp[j - 1, :]
                y = temp[j + 2 ** (h - 1) - 1, :]
                # Update the array with the combined values according to the slant structure
                input_array[j - 1, :] = (x + y) / 2
                input_array[j + 2 ** (h - 1) - 1, :] = (x - y) / 2

    return input_array


def gray_permutation(input_array):
    """
    Reorders the rows of the input array according to the Gray code permutation.

    Args:
        input_array (numpy.array): The input array to be reordered. It can be
            a 1D column vector or a 2D matrix.

    Returns:
        numpy.array: The reordered array with rows permuted according to the
            Gray code sequence.
    """
    n = input_array.shape[0]
    new_array = np.zeros_like(input_array)

    for i in range(n):
        # Compute the Gray code for the current index
        gray_index = gray_code(i)
        # Reorder the rows based on the Gray code sequence
        new_array[i, :] = input_array[gray_index, :]

    return new_array


def binary_list(num, length=None):
    """
    Generate the binary list of the input number with the specified length.

    This function converts an integer into its binary representation as a list of integers.
    If the length parameter is provided, the binary representation will be padded with zeros to reach the specified length.

    Args:
        num (int): The number to convert to binary.
        length (int, optional): The desired length of the binary list. Defaults to None.

    Returns:
        list: A list of binary numbers (0s and 1s) representing the input number.
    """
    if length == 0:
        return []
    num_binary = bin(num)[2:]
    if length is not None:
        num_binary = num_binary.zfill(length)

    return [int(bit) for bit in num_binary]


def reverse_index_bits(arr):
    """
    Reverse the binary index of the input array for all dimensions.

    This function takes an input array and returns a new array with the same values
    but with indices reversed in binary representation for each dimension.
    It works by recursively reversing the binary index for each dimension,
    starting from the last dimension and moving towards the first.

    Args:
        arr (np.ndarray): The input array with any number of dimensions.

    Returns:
        np.array: A new array with the same values as the input array but with reversed binary indices for all dimensions.

    Raises:
        ValueError: If the input is not a NumPy array.
    """
    if not isinstance(arr, np.ndarray):
        raise ValueError("Input must be a NumPy array.")

    def _reverse_dim(arr, dim):
        """
        Reverse the binary index for a specific dimension of the array.

        Args:
            arr (np.ndarray): The input array.
            dim (int): The dimension to reverse the binary index for.

        Returns:
            np.ndarray: A new array with the binary index reversed for the specified dimension.
        """
        n = int(np.log2(arr.shape[dim]))
        new_arr = np.empty_like(arr)

        # Iterate over all indices in the current dimension
        for index in range(arr.shape[dim]):
            new_index_bin = '0b' + bin(index)[2:].zfill(n)[::-1]
            new_index = int(new_index_bin, 2)

            # Construct the full index tuple for the new and original arrays
            index_tuple = [slice(None)] * arr.ndim
            index_tuple[dim] = new_index
            index_tuple_original = [slice(None)] * arr.ndim
            index_tuple_original[dim] = index

            # Copy the values from the original array to the new array at the reversed index position
            new_arr[tuple(index_tuple)] = arr[tuple(index_tuple_original)]
        return new_arr

    # Start from the last dimension and move towards the first
    for dim in range(arr.ndim - 1, -1, -1):
        arr = _reverse_dim(arr, dim)

    return arr