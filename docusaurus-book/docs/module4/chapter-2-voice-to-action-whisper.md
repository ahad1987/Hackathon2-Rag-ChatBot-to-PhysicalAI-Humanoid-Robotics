---
title: "Chapter 2: Voice-to-Action with Whisper"
description: "Build a voice-controlled robot interface using OpenAI Whisper and ROS 2. Transcribe speech, integrate with robot actions, and handle edge cases."
slug: chapter-2-voice-to-action-whisper
sidebar_position: 3
---

# Chapter 2: Voice-to-Action with Whisper

## Overview

This chapter teaches you how to build a voice-controlled robot interface. You'll use OpenAI Whisper for speech-to-text, integrate it with ROS 2, and handle real-world challenges like noise and ambiguity.

**Duration**: 45–55 minutes | **Difficulty**: Intermediate

---

## Learning Objectives

By the end of this chapter, you will:

1. Understand how speech recognition works
2. Use OpenAI Whisper to transcribe audio
3. Integrate voice input with ROS 2 nodes
4. Handle noise and improve transcription accuracy
5. Build a voice command listener for robots

---

## Key Concepts

- **Speech-to-Text (STT)**: Converting spoken words into text
- **Whisper**: OpenAI's open-source speech recognition model
- **Acoustic Features**: Audio properties that Whisper uses for recognition
- **Confidence Score**: How confident the model is in its transcription
- **Latency**: Time from speech to text output
- **Streaming**: Real-time transcription vs. batch processing

---

## Section 1: Audio Processing Fundamentals

### What is Audio?

Audio is a time-series signal representing sound waves. Key properties:
- **Sample Rate**: How often audio is measured (typically 16 kHz)
- **Bit Depth**: Resolution of each sample (typically 16-bit)
- **Duration**: Length of audio recording

### Preprocessing

Before transcription, audio often needs:
- **Normalization**: Scaling amplitude
- **Filtering**: Removing background noise
- **Framing**: Dividing audio into chunks

---

## Section 2: OpenAI Whisper – Speech-to-Text

### What is Whisper?

Whisper is a robust speech recognition model trained on 680,000 hours of multilingual audio. It handles:
- Multiple languages
- Background noise
- Technical terminology
- Accents and dialects

### Model Variants

| Model | Size | Latency | Accuracy | Best For |
|-------|------|---------|----------|----------|
| Tiny | 39 M | Fast | 60% | Edge devices |
| Base | 74 M | Medium | 75% | Mobile |
| Small | 244 M | Medium | 85% | Standard |
| Medium | 769 M | Slow | 92% | High accuracy |
| Large | 1.5 B | Very Slow | 95% | Maximum accuracy |

---

## Section 3: ROS 2 Integration

### Architecture

```
Microphone Input
    ↓
Audio Capture Node (Module 2 camera node pattern)
    ↓
Whisper STT Node (New)
    ↓
ROS 2 Topic: /transcribed_text
    ↓
Robot Action Nodes (Module 1 pattern)
```

### ROS 2 Messages

Define a message for voice commands:

```python
# voice_command.msg
string transcription
float32 confidence
int32 timestamp
```

---

## Section 4: Real-World Voice Applications

### Apple Siri

On-device speech recognition for natural language commands on iPhones and smart speakers.

### Amazon Alexa

Cloud-based speech recognition enabling smart home control through voice.

### Tesla Voice Commands

In-car voice interface for navigation, climate control, and vehicle commands.

---

## Section 5: Handling Noise and Ambiguity

### Noise Challenges

- **Background noise**: Traffic, machinery, other speakers
- **Accent variability**: Different speakers, dialects
- **Homophones**: "to" vs. "two" vs. "too"

### Solutions

- **Whisper robustness**: Trained on diverse noisy data
- **Confidence scoring**: Only act on high-confidence transcriptions
- **Fallback to text**: Allow manual input if voice unclear
- **Retry logic**: Ask user to repeat

---

## Section 6: Hands-On Exercise – Build a Voice Command Listener

### Objectives

- Create a ROS 2 node that listens to microphone input
- Transcribe using Whisper
- Publish transcriptions to a topic
- Test with voice commands

### Step 1: Install Dependencies

```bash
pip install openai
sudo apt-get install python3-pyaudio
```

### Step 2: Create a Voice Input Node

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from openai import OpenAI
import pyaudio

class VoiceInputNode(Node):
    def __init__(self):
        super().__init__('voice_input_node')
        self.client = OpenAI()

    def capture_audio(self):
        # Capture audio from microphone
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=16000,
                       input=True, frames_per_buffer=2048)
        frames = []
        for _ in range(32):  # ~2 seconds
            data = stream.read(2048)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        return b''.join(frames)

    def transcribe(self, audio_data):
        # Use Whisper to transcribe
        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_data
        )
        return response.text

def main(args=None):
    rclpy.init(args=args)
    node = VoiceInputNode()

    print("Listening for voice command...")
    audio = node.capture_audio()
    transcription = node.transcribe(audio)
    print(f"You said: {transcription}")

    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Step 3: Test Your Voice Input

```bash
python3 voice_input_node.py
```

### Expected Output

```
Listening for voice command...
You said: move forward ten centimeters
```

---

## Section 7: Latency Optimization

### Streaming vs. Batch

**Batch Processing**: Send entire audio clip after recording
- **Pros**: Higher accuracy
- **Cons**: Higher latency (2–5 seconds)

**Streaming**: Process audio in real-time
- **Pros**: Lower latency (0.5–1 second)
- **Cons**: Slightly lower accuracy

---

## Section 8: Debugging & Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "No microphone detected" | Hardware issue | Check audio device: `arecord -l` |
| "Poor transcription accuracy" | Noisy environment | Use noise cancellation filter |
| "Timeout" | Whisper taking too long | Use smaller model (base/tiny) |
| "API rate limit" | Too many requests | Implement retry with backoff |
| "Confidence too low" | Unclear speech | Ask user to repeat or speak clearly |

---

## Section 9: Summary & Glossary

### Key Takeaways

- Whisper enables robust speech recognition with minimal setup
- ROS 2 integration follows standard publisher-subscriber patterns
- Confidence scoring and fallback strategies improve reliability
- Noise handling is critical for real-world deployments

### New Glossary Terms

- **Speech-to-Text (STT)**: Converting speech to text
- **Whisper**: OpenAI's speech recognition model
- **Confidence Score**: Model's certainty in transcription
- **Latency**: Delay between speech and transcription
- **Streaming**: Real-time audio processing
- **Acoustic Features**: Audio properties used for recognition

---

## What's Next?

Chapter 3 teaches you how to use LLMs to plan robot actions from transcribed voice commands, and how to validate those plans for safety.

**Next Chapter**: [Chapter 3: Cognitive Planning with LLMs](/docs/module4/chapter-3-cognitive-planning-llm)
