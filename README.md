
# Novel Accessibility Interventions for Video (TV, Online Video)

## Overview

This project focuses on developing accessibility interventions for the aphasic community, specifically to enhance their experience of watching videos on TV or online. The goal is to address challenges faced by aphasia patients, such as difficulties with subtitles, context misinterpretation, and word retrieval, by providing a software application with enhanced accessibility features.

## Project Description

The application includes:
- **Concise Summaries:** Simplified versions of video content, retaining meaning without distortion.
- **Textual and Pictorial Descriptions:** Explanations of complex words used in the summaries.
- **Customizable Audio Playback:** Adjustable playback speed for generated summaries.

The aim is to address challenges like ephemeral screen-time of subtitles, misinterpretation of context, and issues with sentence comprehension and word retrieval.

## Folder Structure

The folder structure of the submitted Supplemental zip file is as follows:

```
├── __pycache__
├── other background files (.txt, .PKL, .PICKLE, and .CONLLU) (non executable)
├── version1.py
├── version2.py
├── README.txt
├── templates
│   ├── vertical.html
│   ├── horizontal.html
│   └── modified.html
├── static
│   ├── JSON files (non executable)
│   └── icon-images used in the frontend
├── uploads
│   └── Documentaries
│       ├── vid_1.mp4
│       └── vid2.mp4
```

## Downloading and Running

To run the Flask application, follow these steps:

1. Download the project folder from the submitted executable files or clone the project from the GitHub repository linked in the thesis report.
2. Move to the location of the python files in the folder. For example, if the downloaded project folder is saved in `Documents`, use the command:
    ```
    cd Documents/project_folder
    ```
3. Run the `.py` files which reference the required files and programs automatically. There are 2 python files - `version1.py` and `version2.py` and 3 HTML files - `vertical.html`, `horizontal.html`, and `modified.html` as described below.

## Code Versions

### A. Python Code

- **version1.py:** Contains the original logic for the functionalities described.
- **version2.py:** Modified version after usability testing. Features updated return types and a shift from tooltips to popup boxes.

### B. HTML Code

**Version 1:**

- **vertical.html:** Frontend code for the vertical layout, including HTML, CSS, and JS.
- **horizontal.html:** Frontend code for the horizontal layout, including HTML, CSS, and JS.

**Version 2:**

- **modified.html:** Modified frontend code after usability testing, featuring popup boxes instead of tooltips, bigger size of static visual elements, in vertical layout.

## Running the Flask Application

### For Version 1 (initial version before user testing):

Use `version1.py` and choose between `vertical.html` or `horizontal.html` depending on the layout you want to test.

- **Vertical Layout:** Modify `version1.py` to refer to `vertical.html` by updating the HTML file name in Line 19 as follows:
    ```python
    html_filename = 'vertical.html'
    ```

- **Horizontal Layout:** Modify `version1.py` to refer to `horizontal.html` similarly:
    ```python
    html_filename = 'horizontal.html'
    ```

[Initially by default, ‘vertical.html’ is set in Line 19.]

### For Version 2 (modified version after user testing):

Use `version2.py`. This version automatically refers to `modified.html` and requires no further changes. Simply run `version2.py`.

## Application Interface Guidelines

### Choose a Video:

1. Click the "Choose Video" button to select a video file (`vid1.mp4` or `vid2.mp4`) from the device.
2. Click the "Upload" button to load the video into the application.
3. While running the python code, refer to the original video transcript returned to the terminal (optional).

### Summarization:

After uploading, click the "Summarise" button. It is recommended to do this before starting the video to reduce waiting time.

### Interacting with the Summary:

- **Running with `version1.py` (before changes):** Hover over highlighted words to see tooltips.
- **Running with `version2.py` (after changes):** Click on highlighted words to see popup boxes.

For tablets, touch highlighted words to trigger tooltips (`version1.py`) or popup boxes (`version2.py`).

### Handling Popup Boxes:

- **Running with `version1.py` (before changes):** Tooltips retracted when hovering away in laptop or clicking anywhere on screen other than tooltip area for tablets.
- **Running with `version2.py` (after changes):** Click the "X" button to close popup boxes.

### Audio Playback Controls:

- **Start Playing / Start from Beginning:** Click to start the summary audio playback from the beginning.
- **Pause:** Pauses the summary audio playback.
- **Resume:** Resumes playback from where it was paused.

---

