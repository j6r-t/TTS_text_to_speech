Here is a comprehensive **Project Design Report (PDR)** for the Text-to-Speech application using Microsoft Edge TTS.

---

# Project Design Report (PDR)
**Project Title:** Edge-TTS Synthesizer
**Version:** 1.0
**Date:** October 26, 2023

---

## 1. Executive Summary
The **Edge-TTS Synthesizer** is a software application designed to convert written text into lifelike spoken audio using the Microsoft Edge Text-to-Speech API. Unlike standard robotic TTS engines, this project leverages the advanced neural voices available in the Microsoft Edge browser. The application will provide users with granular control over audio output, specifically allowing for real-time adjustments of speech rate and pitch using a normalized integer scale (where 0 represents default values).

## 2. Project Objectives
*   **Primary Objective:** Develop a cross-platform tool to convert text strings into audio files (MP3/WAV).
*   **Secondary Objective:** Provide a user-friendly interface to manipulate audio parameters (Rate and Pitch) dynamically.
*   **Cost Efficiency:** Utilize the unofficial Edge TTS API to provide high-quality voice synthesis without the costs associated with official Azure Cognitive Services subscriptions.

## 3. Scope

### 3.1 In-Scope
*   **Text Input:** Support for raw text input (and potentially .txt file uploads).
*   **Voice Selection:** Ability to select from available Microsoft Edge neural voices (e.g., Jenny, Guy, Aria).
*   **Audio Controls:**
    *   **Rate Adjustment:** Modify speaking speed.
    *   **Pitch Adjustment:** Modify voice tone.
*   **Output:** Audio playback and saving to disk (MP3 format).
*   **Interface:** Graphical User Interface (GUI) for desktop or web.

### 3.2 Out-of-Scope
*   Real-time voice streaming (latency minimization for live conversations).
*   SSML (Speech Synthesis Markup Language) advanced tags (focus is on simple parameter sliders).
*   Voice training or custom voice cloning.

## 4. Functional Requirements

| ID | Requirement | Description |
| :--- | :--- | :--- |
| **FR-01** | **Text Input** | The system shall accept a text string of at least 1,000 characters. |
| **FR-02** | **Voice Selection** | The system shall allow the user to select a specific voice gender and locale (e.g., en-US). |
| **FR-03** | **Rate Control** | The system shall allow adjustment of the speech rate.<br>**Logic:** Integer input where `0` is default. Positive integers increase speed; negative integers decrease speed. |
| **FR-04** | **Pitch Control** | The system shall allow adjustment of the voice pitch.<br>**Logic:** Integer input where `0` is default. Positive integers raise pitch; negative integers lower pitch. |
| **FR-05** | **Audio Export** | The system shall generate a downloadable audio file (e.g., .mp3) containing the synthesized speech. |

## 5. Non-Functional Requirements
*   **Performance:** Audio generation for a standard paragraph (approx. 100 words) should complete within 5 seconds, dependent on internet speed.
*   **Usability:** The interface must clearly indicate that "0" is the baseline setting for controls.
*   **Dependencies:** The application requires an active internet connection to communicate with the Microsoft Edge TTS endpoints.

## 6. Technical Architecture

### 6.1 Technology Stack
*   **Language:** Python 3.x (Recommended for rapid development and library support).
*   **Core Library:** `edge-tts` (An asynchronous Python module that allows you to use Microsoft Edge's online text-to-speech service).
*   **Audio Handling:** `ffmpeg` (for handling audio stream conversion) or `pydub`.
*   **User Interface:** `Streamlit` (for Web) or `CustomTkinter` (for Desktop GUI).

### 6.2 Data Flow
1.  **User Input:** User enters text and adjusts sliders for Rate/Pitch in the UI.
2.  **Parameter Processing:** The application maps the integer inputs (e.g., +5, -2) to the string format required by the API (e.g., `+5%`, `-2Hz` or relative rate tags).
3.  **API Request:** The `edge-tts` module sends an HTTP POST request to the Edge Communicator endpoint.
4.  **Stream Processing:** The API returns an audio stream. The application reads the stream asynchronously.
5.  **Output:** The stream is saved to a temporary buffer and played for the user or written to a permanent file.

## 7. Detailed Design: Parameter Logic

This section details the implementation of the specific requirement: *"0 is default, positive values increase, negative values decrease."*

### 7.1 Rate (Speed)
The Edge TTS API expects a `rate` string.
*   **Input:** Integer $R$ (User input).
*   **Logic:**
    *   If $R = 0$, API string = `'+0%'` (Default).
    *   If $R > 0$, API string = `'+' + str(R) + '%'` (e.g., Input 10 becomes `'+10%'`).
    *   If $R < 0$, API string = `str(R) + '%'` (e.g., Input -5 becomes `'-5%'`).
*   **Range:** Suggested limit -50 (slowest) to +100 (fastest).

### 7.2 Pitch
The Edge TTS API expects a `pitch` string.
*   **Input:** Integer $P$ (User input).
*   **Logic:**
    *   If $P = 0$, API string = `'+0Hz'` (Default).
    *   If $P > 0$, API string = `'+' + str(P) + 'Hz'` (e.g., Input 5 becomes `'+5Hz'`).
    *   If $P < 0$, API string = `str(P) + 'Hz'` (e.g., Input -5 becomes `'-5Hz'`).
*   **Range:** Suggested limit -50 (lowest) to +50 (highest).

## 8. User Interface (UI) Mockup Description

**Main Window:**
*   **Top:** Text Area ("Enter text here...").
*   **Middle Left:** Dropdown Menu for "Select Voice" (populated dynamically via API).
*   **Middle Right:** Control Panel.
    *   Slider: **Speech Rate** [Scale: -10 to +10]. Default: 0.
    *   Slider: **Pitch** [Scale: -10 to +10]. Default: 0.
*   **Bottom:** Action Buttons.
    *   [Play Audio] (Preview)
    *   [Save to MP3]

## 9. Implementation Plan

1.  **Phase 1: Environment Setup**
    *   Install Python, `edge-tts`, and GUI libraries.
    *   Verify connectivity to the Edge TTS endpoint.
2.  **Phase 2: Core Logic Development**
    *   Write the function to convert text to audio stream.
    *   Implement the integer-to-string mapping logic for Rate and Pitch.
3.  **Phase 3: UI Development**
    *   Build the input forms and sliders.
    *   Connect UI events to the core logic functions.
4.  **Phase 4: Testing & Debugging**
    *   Test edge cases (empty text, extreme pitch values).
    *   Ensure file saving works correctly.
5.  **Phase 5: Deployment**
    *   Package the application (e.g., using PyInstaller for desktop).

## 10. Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| **API Change** | Medium | High | Microsoft may change the internal API URL, breaking the library. Mitigation: Use the widely-maintained `edge-tts` library which updates frequently. |
| **Dependency Issues** | Low | Medium | `ffmpeg` may not be installed on the user's system. Mitigation: Include a check on startup to prompt the user to install ffmpeg or bundle it. |

