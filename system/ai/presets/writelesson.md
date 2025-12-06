# Preset: WriteLesson

## Purpose
Single lesson section workflow (~400-600 words + 1 code example) for adding a focused, self-contained lesson that fits within a chapter.

## Subagents Called
1. **BookWriter** — Generates lesson content (intro, learning objectives, theory, code example, real-world application, exercise, summary)
2. **CodeAgent** — Writes and validates one Python+rclpy code example with expected output
3. **QualityGuard** — Reviews lesson for brand voice and pedagogical clarity
4. **ContentValidator** — Checks glossary and cross-module references

## Skills Used
1. **VisionaryTone** — Maintains visionary, accessible tone for lesson intro
2. **ExplainSimple** — Breaks complex concept into beginner-friendly language
3. **ROS2Example** — Generates single production-quality code example
4. **CleanMarkdown** — Applies Markdown formatting standards
5. **GlossaryIntegration** — Identifies and integrates new technical terms
6. **CrossModuleReference** — Links to prerequisite material if needed

## Input Signature
```yaml
chapter_path: string    # Path to parent chapter (e.g., docs/module4/chapter-2-*.md)
lesson_title: string    # Lesson section title (e.g., "Whisper: Automatic Speech Recognition")
concept: string         # Core concept to teach (2-3 sentence summary)
target_words: integer   # Target word count (400-600)
code_example: string    # Brief description of what code should demonstrate
prior_knowledge: list   # Modules/concepts learner should know (optional)
```

## Output Format
```yaml
lesson_markdown: string     # Full lesson text with Markdown formatting
word_count: integer         # Actual word count generated
code_block: string          # Python code example (< 30 lines)
expected_output: string     # Sample output when code runs
glossary_terms: list        # New terms bolded and defined
estimated_read_time: string # "10-15 minutes"
validation_passed: boolean  # All checks passed?
issues: list                # Any issues found
```

## Safety Rules

1. **Keep lesson focused** — One core concept per lesson, ~400-600 words max
2. **Code examples are optional but recommended** — If included, must be < 30 lines and runnable
3. **Don't skip glossary integration** — Every technical term must be bolded on first mention
4. **Validate prerequisites** — If lesson assumes prior knowledge, create prerequisite callout
5. **Avoid forward references** — Never link to chapters/content not yet written

## Workflow Steps

### Step 1: Preparation
- QualityGuard confirms lesson concept fits within chapter scope
- ContentValidator checks for glossary conflicts with existing terms

### Step 2: Content Writing
- BookWriter writes lesson introduction (50-75 words) that hooks learner interest
- BookWriter writes learning objectives (2-3 testable outcomes)
- BookWriter writes theory section (200-300 words) with clear, progressive explanation
- ExplainSimple reviews theory for accessibility (uses analogies, short sentences, concrete examples)
- BookWriter writes 1-2 real-world applications (50-100 words total)

### Step 3: Code & Examples
- CodeAgent writes one focused Python+rclpy example (max 30 lines) if applicable
- CodeAgent provides expected output showing realistic results
- CodeAgent documents 1 common error and fix

### Step 4: Formatting & Integration
- CleanMarkdown applies Markdown standards to heading hierarchy, code blocks, links
- GlossaryIntegration bolds all new terms and suggests glossary entries
- CrossModuleReference adds prerequisite callouts if needed

### Step 5: Quality Review & Output
- QualityGuard checks for brand voice, pedagogical clarity, appropriate difficulty
- ContentValidator verifies no broken links or glossary conflicts
- Output complete lesson Markdown ready to insert into chapter

## Example Invocation

### Command
```
WriteLesson --chapter_path docs/module4/chapter-2-voice-to-action-whisper.md --lesson_title "Whisper: Automatic Speech Recognition" --concept "Whisper is OpenAI's neural network for converting speech audio to text. It processes raw audio waves and outputs predicted text tokens, similar to how LLMs predict word sequences." --code_example "ROS 2 subscriber that listens to /audio_input and publishes recognized text to /transcription" --prior_knowledge ["Module 1: ROS 2 Subscriptions","Module 3: Neural Network Basics"]
```

### Expected Output
```yaml
lesson_markdown: |
  ### Whisper: Automatic Speech Recognition

  Imagine speaking a command to your robot: "Pick up the coffee cup." How does the robot understand those words? **Automatic Speech Recognition (ASR)** is the AI technology that converts your voice into text, similar to how autocomplete predicts your next word on a smartphone.

  **Whisper** is OpenAI's neural network trained on 680,000 hours of multilingual audio. When you speak into a microphone, Whisper processes the audio waveform and predicts **tokens**—small units of text—one at a time, building your transcription word by word.

  #### Learning Objectives
  - [ ] Understand how Whisper converts audio to text
  - [ ] Implement a ROS 2 subscriber that uses Whisper for speech recognition
  - [ ] Debug common audio input issues

  #### How Whisper Works

  Whisper's process mirrors language models but operates on audio:
  1. **Input**: Raw audio waveform (44kHz or 48kHz)
  2. **Feature Extraction**: Convert audio to spectral features
  3. **Token Prediction**: Neural network predicts next token (word/subword)
  4. **Output**: Transcribed text

  #### Code Example: Whisper Subscriber Node

  \`\`\`python
  import rclpy
  from std_msgs.msg import String
  import whisper

  def main():
      rclpy.init()
      node = rclpy.create_node('whisper_transcriber')

      model = whisper.load_model("base")

      def audio_callback(msg):
          # msg.data contains path to audio file
          result = model.transcribe(msg.data)
          transcription = result["text"]
          pub.publish(String(data=transcription))

      sub = node.create_subscription(String, '/audio_input', audio_callback, 10)
      pub = node.create_publisher(String, '/transcription', 10)
      rclpy.spin(node)

  if __name__ == '__main__':
      main()
  \`\`\`

  **Expected Output:**
  ```
  Received audio file: /tmp/audio_001.wav
  Transcription: "Pick up the coffee cup"
  Published to /transcription
  ```

  **Common Error & Fix:**
  - **Error**: "Whisper model not found; model download failed"
  - **Fix**: Run `whisper-cli --download-model base` before starting node, or add error handling: `try: model = whisper.load_model("base") except Exception as e: node.get_logger().error(f"Load failed: {e}")`

  #### Real-World Application

  Tesla's voice command system ("Summon") uses ASR to interpret driver commands without requiring eyes on the road. Whisper's multilingual capability makes it ideal for global robotics applications.

  #### Summary

  You now understand how **Whisper** converts voice to text, and can build a ROS 2 node that processes audio input. In the next section, we'll combine Whisper with an **LLM** to create a robot that understands intent, not just words.

word_count: 428
code_block: "import rclpy..."
expected_output: "Transcription: \"Pick up the coffee cup\""
glossary_terms:
  - "ASR (Automatic Speech Recognition)"
  - "Whisper"
  - "Token"
estimated_read_time: "12 minutes"
validation_passed: true
issues: []
```

## Quality Checks
- ✅ Is the lesson focused on one core concept?
- ✅ Are learning objectives testable?
- ✅ Is content understandable for someone with Modules 1-3 knowledge?
- ✅ If code is included, is it < 30 lines and runnable?
- ✅ Are all new terms bolded and defined in context?
- ✅ Are prerequisite callouts included if needed?
- ✅ Does estimated read time match word count (~100 words per minute)?

---

**Implementation Note:** WriteLesson is ideal for expanding existing chapters with new focused lessons. Use WriteChapter for complete 5-7 section chapters. After writing a lesson, insert it into the chapter file and run ValidateCrossModule to check for broken references.
