import re

def extract_cpu_idle(command_output):
    match = re.search(r'%Cpu\(s\):\s*(\d+\.\d+).*?(\d+\.\d+)\sid', command_output)
    if match:
        idle_percentage = float(match.group(2))
        return idle_percentage
    return 0.0

def extract_memory_usage(mem_lines):
    for line in mem_lines:
        if "MiB Mem :" in line:
            return extract_memory_usage_from_line(line)

def extract_memory_usage_from_line(mem_line):
    match = re.search(r'MiB Mem :\s*(\d+\.\d+)\s*total,\s*(\d+\.\d+)\s*free,\s*(\d+\.\d+)\s*used', mem_line)
    if match:
        total = float(match.group(1))
        used = float(match.group(3))
        memory_usage_percentage = (used / total) * 100
        return memory_usage_percentage
    return 0


def extract_used_memory(df_output):
    used_memory = 0
    lines = df_output.splitlines()
    for line in lines:
        if line.startswith('tmpfs') or line.startswith('/dev'):
            columns = line.split()
            used_space = columns[2]
            if used_space.endswith('M'):
                used_memory += float(used_space[:-1]) / 1024
            elif used_space.endswith('G'):
                used_memory += float(used_space[:-1])
    return used_memory
