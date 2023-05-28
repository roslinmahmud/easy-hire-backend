import glob
import os

from pyresparser import ResumeParser

current_directory = os.path.dirname(os.path.abspath(__file__))
target_directory = os.path.join(current_directory, 'resumes')
file_paths = glob.glob(os.path.join(target_directory, '*'))

resume_data = []

# Process each file in a loop
for file_path in file_paths:
    print("Processing file:", file_path)
    resume_data.append(ResumeParser(file_path).get_extracted_data())
