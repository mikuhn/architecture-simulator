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
def get_riscv_visualization_loaded() -> bool: ...
def update_IF_Stage(parameters) -> None: ...
def update_ID_Stage(
    parameters,
    control_unit_signals,
) -> None: ...
def update_EX_Stage(
    parameters,
    control_unit_signals,
) -> None: ...
def update_MEM_Stage(
    parameters,
    control_unit_signals,
) -> None: ...
def update_WB_Stage(
    parameters,
    control_unit_signals,
) -> None: ...
def update_visualization(
    pc_plus_imm_or_pc_plus_instruction_length,
    pc_plus_imm_or_pc_plus_instruction_length_or_ALU_result,
) -> None: ...
def clear_register_table() -> None: ...
def clear_instruction_table() -> None: ...
def set_output(str: str) -> None: ...
def toyUpdateRegisters(
    accuRepresentations: tuple,
    pcRepresentations: tuple,
    irRepresentations: tuple,
    instruction: str,
) -> None: ...
def toyUpdateMemoryTable(
    address: str,
    value_representations: tuple,
    instruction_representation: str,
    cycle: str,
) -> None: ...
def toyClearMemoryTable() -> None: ...
def update_toy_visualization(
    update_values: list[tuple[str, str, str | bool]]
) -> None: ...
def get_toy_visualization_loaded() -> bool: ...
