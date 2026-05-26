with open('usa_signal_bot/app/cli.py', 'r') as f:
    lines = f.readlines()

# It's highly likely I appended phase116_add_commands at the very end of the file AFTER main()
# Let's find def main(), and pull everything after if __name__ == '__main__': and before it to just before def main()

main_idx = -1
for i, line in enumerate(lines):
    if line.startswith("def main()"):
        main_idx = i
        break

if main_idx != -1:
    phase116_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("def phase116_add_commands(subparsers):"):
            phase116_idx = i
            break

    if phase116_idx > main_idx:
        # Move phase116 def before main
        # Find end of phase116_add_commands
        end_idx = phase116_idx
        while end_idx < len(lines):
            if lines[end_idx].startswith("def ") and end_idx != phase116_idx:
                break
            if lines[end_idx].startswith("if __name__"):
                break
            end_idx += 1

        phase116_lines = lines[phase116_idx:end_idx]

        # Remove from old position
        lines = lines[:phase116_idx] + lines[end_idx:]

        # Recalculate main_idx after removal
        for i, line in enumerate(lines):
            if line.startswith("def main()"):
                main_idx = i
                break

        # Insert before main
        lines = lines[:main_idx] + phase116_lines + lines[main_idx:]

        with open('usa_signal_bot/app/cli.py', 'w') as f:
            f.writelines(lines)
        print("Fixed CLI order")
