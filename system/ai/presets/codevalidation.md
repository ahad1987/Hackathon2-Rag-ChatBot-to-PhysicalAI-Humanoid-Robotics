# Preset: CodeValidation

## Purpose
Test all Python+rclpy code examples in a chapter or module. Verify code runs, produces expected output, handles common errors, and follows ROS 2 patterns.

## Subagents Called
1. **CodeAgent** — Executes code examples, validates output, tests error handling
2. **MarkdownCleaner** — Scans chapter for code blocks, extracts examples
3. **QualityGuard** — Reviews code quality, compliance with patterns

## Skills Used
1. **ROS2Example** — Validates code follows rclpy patterns, max 30 lines, runnable in isolation
2. **CleanMarkdown** — Ensures code blocks have language tags, proper formatting
3. **ConsistencyCheck** — Verifies code matches Module 1 pattern conventions

## Input Signature
```yaml
scope: string               # "module" | "chapter" | "file" (e.g., "module4" or specific file path)
test_mode: string          # "syntax_only" | "run_examples" | "full_validation"
ros_environment: string    # "docker" | "system" | "mock" (how to run code)
max_execution_time: integer # Timeout per example in seconds (default: 30)
```

## Output Format
```yaml
scope_tested: string                    # What was tested
total_code_examples: integer            # Count of code blocks found
examples_passed: integer                # Count of successful runs
examples_failed: integer                # Count of failures
examples_skipped: integer               # Code examples not executable (pseudocode, etc.)
test_results: list                      # Detailed results per code block
syntax_issues: list                     # Syntax errors found
output_issues: list                     # Unexpected output issues
validation_passed: boolean              # All testable examples passed?
test_duration: string                   # Total test time
```

## Safety Rules

1. **Never execute untrusted code** — Verify code context before running; examples should be from known curriculum
2. **Isolate execution environment** — Use Docker or sandbox to prevent side effects
3. **Timeout all executions** — Max 30 seconds per example to prevent hangs
4. **Capture output safely** — Don't expose system information in error messages
5. **Skip non-executable examples** — Pseudocode and diagrams shouldn't block validation

## Workflow Steps

### Step 1: Extraction
- MarkdownCleaner scans target file(s) for code blocks (triple backtick format)
- Extract all blocks marked as Python with language tag `python` or `python\n`
- Associate each block with its chapter/section for reporting

### Step 2: Syntax Validation
- CodeAgent parses each example for Python syntax errors
- Report syntax issues with line numbers and suggestions
- Flag examples that import non-standard libraries (must be rclpy only)

### Step 3: Semantic Check
- ROS2Example validates code follows rclpy patterns:
  - Uses `rclpy.init()`, `rclpy.create_node()`, `rclpy.spin()`
  - Subscriptions/publishers follow standard format
  - Max 30 lines per example
- ConsistencyCheck verifies matches Module 1 patterns

### Step 4: Execution (if test_mode != "syntax_only")
- CodeAgent sets up test environment (Docker/system/mock based on ros_environment parameter)
- Execute each example with timeout
- Capture stdout, stderr, return code
- Compare actual output against expected output (if documented)

### Step 5: Error Testing (if test_mode == "full_validation")
- CodeAgent attempts to trigger documented "common errors" (e.g., missing node, bad topic)
- Verify error handling works as documented
- Confirm error messages are helpful

### Step 6: Report Generation
- Aggregate results by severity (passed, warning, failed, skipped)
- Provide detailed output for each code example
- Suggest fixes for failed examples

## Example Invocation

### Command
```
CodeValidation --scope module4/chapter-2 --test_mode full_validation --ros_environment docker --max_execution_time 30
```

### Expected Output
```yaml
scope_tested: docs/module4/chapter-2-voice-to-action-whisper.md
total_code_examples: 2
examples_passed: 2
examples_failed: 0
examples_skipped: 0
validation_passed: true

test_results:
  - example_id: chapter2_code1
    section: "Code Example: Whisper Subscriber Node"
    language: python
    line_range: "142-158"
    size: "17 lines"
    status: PASSED

    syntax_validation: PASSED
    pattern_compliance: PASSED (matches Module 1 rclpy pattern)
    max_lines_check: PASSED (17 < 30)

    execution_test: PASSED
    timeout: 5.2 seconds
    expected_output_match: PASSED

    actual_output: |
      Received audio file: /tmp/audio_001.wav
      Transcription: "Pick up the coffee cup"
      Published to /transcription

    error_handling_test: PASSED
    - Tested missing audio file error: ✓ Caught, logged appropriately
    - Tested invalid model error: ✓ Caught, logged appropriately

    notes: "Excellent example. Clear variable names, proper error handling."

  - example_id: chapter2_code2
    section: "Code Example: Voice Command Handler"
    language: python
    line_range: "201-215"
    size: "15 lines"
    status: PASSED

    syntax_validation: PASSED
    pattern_compliance: PASSED
    max_lines_check: PASSED (15 < 30)

    execution_test: PASSED
    timeout: 4.8 seconds
    expected_output_match: PASSED

    actual_output: |
      Voice command received: "move forward"
      Publishing to /cmd_vel: linear.x=0.5

    error_handling_test: PASSED
    - Tested unrecognized command error: ✓ Caught, published warning

    notes: "Code is clean and idiomatic. Consider adding timeout for user commands (optional enhancement)."

syntax_issues: [] (no syntax errors found)

output_issues: [] (all outputs match expected)

recommendations: []

validation_summary: |
  ✓ All 2 code examples passed validation
  ✓ Syntax: Valid Python 3.10+ code
  ✓ Patterns: All examples follow Module 1 rclpy conventions
  ✓ Execution: All examples run successfully and produce expected output
  ✓ Error Handling: All documented error cases caught correctly

  Chapter 2 is ready for publication.
```

### Command (Syntax Only)
```
CodeValidation --scope module4 --test_mode syntax_only
```

### Expected Output
```yaml
scope_tested: module4 (4 chapters: chapter-1.md, chapter-2.md, chapter-3.md, chapter-4.md)
total_code_examples: 8
examples_passed: 7
examples_failed: 1
examples_skipped: 0
validation_passed: false

test_results:
  - example_id: chapter1_code1
    status: PASSED
    syntax: Valid Python 3.10+
    imports: rclpy, geometry_msgs.msg (all valid)

  - example_id: chapter1_code2
    status: PASSED
    syntax: Valid Python 3.10+

  - example_id: chapter2_code1
    status: PASSED

  - example_id: chapter2_code2
    status: PASSED

  - example_id: chapter3_code1
    status: FAILED
    syntax_error: "Invalid syntax at line 8: unexpected EOF while parsing"
    code: |
      def callback(msg):
          print(f"Received: {msg}")
          # Missing closing brace or incorrect indentation

    suggestion: |
      def callback(msg):
          print(f"Received: {msg}")
          # Add missing code or fix indentation

    file: docs/module4/chapter-3-cognitive-planning-llm.md
    line: 267

  - example_id: chapter3_code2
    status: PASSED

  - example_id: chapter4_code1
    status: PASSED

  - example_id: chapter4_code2
    status: PASSED

syntax_issues:
  - severity: critical
    file: docs/module4/chapter-3-cognitive-planning-llm.md
    line: 267
    issue: "Invalid Python syntax in code example"
    code_snippet: "def callback(msg):\n    print(f\"Received: {msg}\")\n    #Missing closing"
    suggestion: "Fix indentation or complete the function"

validation_summary: |
  ✓ 7 of 8 code examples have valid syntax
  ✗ 1 syntax error in chapter-3 requires fixing

  Action Required:
  1. Fix syntax error in chapter-3 (line 267)
  2. Re-run CodeValidation to confirm all examples are valid
```

## Quality Checks
- ✅ Do all code examples have Python language tags?
- ✅ Is all code syntactically valid Python 3.10+?
- ✅ Do all examples follow rclpy patterns (Module 1 style)?
- ✅ Are all examples under 30 lines?
- ✅ Do examples produce expected output when executed?
- ✅ Are documented error cases handled correctly?
- ✅ Do all imports use rclpy only (no external libs)?

---

**Implementation Note:** CodeValidation should be run before publishing chapters to ensure all code examples are correct and runnable. For modules with ROS 2 dependencies, use `--ros_environment docker` to test in isolated environment. Results can be integrated into CI/CD pipeline for automated validation on every commit.
