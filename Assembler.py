def assemble(code):
    
    # Split the code into lines.
    lines = code.split("\n")

    # Create a list to store the machine code.
    machine_code = []

    # Iterate over the lines of code.
    for line in lines:
        # Remove any comments.
        line = line.split("//")[0]

        # If the line is empty, skip it.
        if not line.strip():
            continue

        # Split the line into tokens.
        tokens = line.split(",")

        # Remove leading and trailing whitespaces from tokens.
        tokens = [token.strip() for token in tokens]

        # Get the opcode and operands.
        instruction_parts = tokens[0].split()
        opcode = instruction_parts[0].lower()
        operands = instruction_parts[1:]

        # Assemble the instruction.
        machine_code.append(assemble_instruction(opcode, operands))

    # Return the machine code.
    return machine_code


def assemble_instruction(opcode, operands):
    """Assembles a single 8051 assembler instruction.

    Args:
        opcode: The opcode of the instruction.
        operands: A list of operands for the instruction.

    Returns:
        A byte containing the machine code for the instruction.
    """
    # Get the opcode value.
    opcode_value = opcodes[opcode]

    # Get the operand values.
    operand_values = []
    for operand in operands:
        operand_values.append(assemble_operand(operand))

    # Assemble the instruction.
    machine_code = opcode_value << 4  # Shift the opcode value to the left by 4 bits
    for operand_value in operand_values:
        machine_code |= operand_value

    # Return the machine code.
    return machine_code


def assemble_operand(operand):
    """Assembles a single 8051 assembler operand.

    Args:
        operand: The operand to assemble.

    Returns:
        A byte containing the machine code for the operand.
    """
    # If the operand is a register, return the register value.
    if operand in registers:
        return registers[operand]

    # If the operand is a memory address, split it into operand and address parts
    elif operand.endswith('h'):  # Memory operand like 50h
        operand = operand[:-1]  # Remove the 'h' suffix
        return 0x80 | int(operand, 16)  # Set the MSB to 1 for memory operand and return the address

    # If the operand is a number, return the number value.
    elif operand.isdigit():
        return int(operand)

    # Otherwise, raise an error.
    else:
        raise ValueError("Invalid operand: {}".format(operand))


# Opcode table.
opcodes = {
    "mov": 0x01,
    "add": 0x02,
    "sub": 0x03,
    "mul": 0x04,
    "div": 0x05,
    "and": 0x06,
    "or": 0x07,
    "xor": 0x08,
    "not": 0x09,
    "jmp": 0x0A,
    "call": 0x0B,
    "ret": 0x0C,
    "reti": 0x0D,
    "int": 0x0E,
    "iret": 0x0F,
}

# Register table.
registers = {
    "a": 0x00,
    "b": 0x01,
    "c": 0x02,
    "d": 0x03,
    "e": 0x04,
    "h": 0x05,
    "l": 0x06,
    "sp": 0x07,
    "pc": 0x08,
}

# Example code.
code = """
mov f 5
mov b 10
add c b
mov 50h a
and a 42h
jmp 42h
"""

# Assemble the code.
machine_code = assemble(code)

# Print the machine code.
for byte in machine_code:
    print(hex(byte))