"""type stubs for js functions"""

def get_selected_isa() -> str: ...
def get_pipeline_mode() -> str: ...
def get_hazard_detection() -> bool: ...
def update_register_table(reg: int, representations: tuple, abi_name: str) -> None: ...
def update_single_register(reg: int, val: int) -> None: ...
def update_memory_table(address: str, val: str) -> None: ...
def update_single_memory_address(address: str, val: str) -> None: ...
def update_instruction_table(address, val, stage) -> None: ...
def clear_memory_table() -> None: ...
def highlight(position: int, str: str) -> None: ...
def remove_all_highlights() -> None: ...
def highlight_cmd_table(position: int) -> None: ...
def remove_cmd_table_highlights() -> None: ...
def update_IF_Stage(
    mnemonic, instruction, address_of_instruction, pc_plus_instruction_length
) -> None: ...
def update_ID_Stage(
    mnemonic,
    register_read_addr_1,
    register_read_addr_2,
    register_read_data_1,
    register_read_data_2,
    imm,
    write_register,
    pc_plus_instruction_length,
    address_of_instruction,
    control_unit_signals,
) -> None: ...
def update_EX_Stage(
    mnemonic,
    alu_in_1,
    alu_in_2,
    register_read_data_1,
    register_read_data_2,
    imm,
    result,
    write_register,
    comparison,
    pc_plus_imm,
    pc_plus_instruction_length,
    address_of_instruction,
    control_unit_signals,
) -> None: ...
def update_MA_Stage(
    mnemonic,
    memory_address,
    result,
    memory_write_data,
    memory_read_data,
    write_register,
    comparison,
    comparison_or_jump,
    pc_plus_imm,
    pc_plus_instruction_length,
    imm,
    control_unit_signals,
) -> None: ...
def update_WB_Stage(
    mnemonic,
    register_write_data,
    write_register,
    memory_read_data,
    alu_result,
    pc_plus_instruction_length,
    imm,
    control_unit_signals,
) -> None: ...
def update_visualization(
    pc_plus_imm_or_pc_plus_instruction_length,
    pc_plus_imm_or_pc_plus_instruction_length_or_ALU_result,
) -> None: ...
def clear_register_table() -> None: ...
def clear_instruction_table() -> None: ...
def set_output(str: str) -> None: ...
