import subprocess
import os

# Configuration
MMATA_SCRIPT = "mmata.py"
TESTS_FOLDER = "tests"
LANGUAGE = "setswana"  # Can be changed to zulu, sotho, etc.

def run_ml_script(script_path):
    """Run a .ml file using mmata.py and return its output."""
    result = subprocess.run(
        ["python", MMATA_SCRIPT, script_path, LANGUAGE],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def load_expected_outputs():
    """Read expected outputs from tests/expected_outputs.txt"""
    outputs = {}
    path = os.path.join(TESTS_FOLDER, "expected_outputs.txt")
    if not os.path.exists(path):
        print("❌ expected_outputs.txt not found.")
        return outputs

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = content.strip().split("---")
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 2:
            filename = lines[0].strip()
            expected_output = "\n".join(lines[1:]).strip()
            outputs[filename] = expected_output
    return outputs

def main():
    expected_outputs = load_expected_outputs()
    test_files = [
        f for f in os.listdir(TESTS_FOLDER)
        if f.endswith(".ml") and f in expected_outputs
    ]

    print("🔎 Running Mmata Language Tests...\n")
    all_passed = True

    for test_file in test_files:
        script_path = os.path.join(TESTS_FOLDER, test_file)
        actual_output = run_ml_script(script_path)
        expected_output = expected_outputs[test_file]

        print(f"🧪 Test: {test_file}")
        if actual_output == expected_output:
            print("✅ Passed\n")
        else:
            print("❌ Failed")
            print(f"Expected:\n{expected_output}")
            print(f"Actual:\n{actual_output}\n")
            all_passed = False

    if all_passed:
        print("🎉 All tests passed successfully!")
    else:
        print("🚨 Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
