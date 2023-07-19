# Automated CLI Tool for WeThinkCode Students (WTC-LMS Helper)

## Overview
The Automated CLI Tool for WeThinkCode Students is a powerful command line application that simplifies project management tasks for WeThinkCode students. It automates the process of project initiation, submission, and peer reviews, providing a streamlined workflow and enhancing overall efficiency.

This tool seamlessly integrates with the WeThinkCode command line tool (wtc-lms) and leverages technologies such as Python3, the subprocess module, and the os module to deliver a user-friendly and automated experience.

## Features
- **Project Initialization**: Effortlessly start a project for the current iteration using the `start` command.
- **Submission Automation**: Submit your completed project to a GitLab repository created by WTC_ with a single command.
- **Peer Review Initiator**: Initiate review sessions for other students, fostering collaboration and knowledge sharing.
- **Seamless Integration**: The tool seamlessly integrates with the WeThinkCode command line tool (wtc-lms) for a cohesive experience.
- **Efficient File Operations**: The os module facilitates efficient file handling, such as directory creation and file compression.

## Technologies and Libraries Used
- Python3: The core programming language used for development.
- Subprocess Module: Enables integration with the WeThinkCode command line tool (wtc-lms).
- os Module: Facilitates efficient file and directory operations.

## Usage
1. Clone the repository: `git clone https://github.com/devorbs/wtc-lms-helper.git`
2. Navigate to the project directory: `cd wtc-lms-helper`
4. Run the tool setup command: `python main.py setup`

## Examples
- Start a project: `helper start <project_uiid>`
- Submit a project: `helper submit <project_uiid>`
- Initiate a peer review: `helper review`

## About the Author
This tool is developed and maintained by [Bokang Makibinye](https://github.com/devorbs).
