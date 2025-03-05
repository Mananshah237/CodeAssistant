from analyzer import analyze_code

if __name__ == "__main__":
    sample_file = "test_code/sample.py"
    with open(sample_file, "r") as f:
        code = f.read()
    result = analyze_code(code)
    print(result)