# Novel Accessibility Interventions for Video (TV, Online Video)

## Overview

This project focuses on developing accessibility interventions for the aphasic community, specifically to enhance their experience of watching videos on TV or online. The goal is to address challenges faced by aphasia patients, such as difficulties with subtitles, context misinterpretation, and word retrieval, by providing a software application with enhanced accessibility features.

## Project Description

This thesis presents a website application that includes:
- **Concise Summaries**: Simplified versions of video content, retaining meaning without distortion.
- **Textual and Pictorial Descriptions**: Explanations of complex words used in the summaries.
- **Customizable Audio Playback**: Adjustable playback speed for generated summaries.

The aim is to address challenges like ephemeral screen-time of subtitles, misinterpretation of context, and issues with sentence comprehension and word retrieval.

## Code Versions

### Python Code

- **version1.py**: Contains the original logic for the functionalities described.
- **version2.py**: Modified version after usability testing. Features updated return types and a shift from tooltips to popup boxes.

### HTML Code

- **Version 1:**
  - `vertical.html`: Frontend code for the vertical layout, including HTML, CSS, and JS.
  - `horizontal.html`: Frontend code for the horizontal layout, including HTML, CSS, and JS.

- **Version 2:**
  - `modified.html`: Modified frontend code after usability testing, featuring popup boxes instead of tooltips.

## Running the Flask Application

1. **For Version 1:**
   - Use `version1.py` and choose between `vertical.html` or `horizontal.html` depending on the layout you want to test.
   - **Vertical Layout:** Modify `version1.py` to refer to `vertical.html` by updating:
     - Line 100 in `index()` function: `return render_template('vertical.html')`
     - Line 129 in `process_video()` function: `return render_template('vertical.html', transcript=text, video_url=url_for('static', filename=f'uploads/Documentaries/{video_filename}'))`
   - **Horizontal Layout:** Modify `version1.py` to refer to `horizontal.html` similarly.

2. **For Version 2:**
   - Use `version2.py`. This version automatically refers to `modified.html` and requires no further changes.

## Application Interface Guidelines

1. **Choose a Video:**
   - Click the "Choose Video" button to select a video file (`vid1.mp4` or `vid2.mp4`) from your device.
   - Click the "Upload" button to load the video into the application.

2. **Summarization:**
   - After uploading, click the "Summarise" button. It is recommended to do this before starting the video to reduce waiting time.

3. **Interacting with the Summary:**
   - **Previously (before changes):** Hover over highlighted words to see tooltips.
   - **Presently (after changes):** Click on highlighted words to see popup boxes.
   - For tablets, touch highlighted words to trigger tooltips (previously) or popup boxes (presently).

4. **Handling Popup Boxes:**
   - **Previously:** Tooltips retracted when hovering away.
   - **Presently:** Click the "X" button to close popup boxes.

5. **Audio Playback Controls:**
   - **Start Playing / Start from Beginning:** Click to start the summary audio playback from the beginning.
   - **Pause:** Pauses the summary audio playback.
   - **Resume:** Resumes playback from where it was paused.

