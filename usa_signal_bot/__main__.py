
import sys

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "dry-admission-info":
        print("Paper-Mode Dry Admission Rehearsal Module")
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1].startswith("dry-admission"):
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1].startswith("write-lock"):
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1].startswith("human"):
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1].startswith("approval"):
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1].startswith("no-write"):
        sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
