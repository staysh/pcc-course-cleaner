# Brightspace Course Package Cleaner

This is a basic python script that can perform the following bulk operations on an unzipped Brightspace Course Package
* Remove old style sheets
* Keep some stylesheets by keyword (like "bootstrap") for instance
* Insert the newest (or any) PCC Style Sheet
* Clean in-line style attributes from text content (skips layout modifying style on images for instance)

## Prerequisites
* An exported, downloaded and unzipped Brightspace Course Package
* Python ~3.9 (ish?)
* pip
* Beautiful Soup 4 (see instructions)

## Installation/Setup
Clone the repo or download it as a zip file and extract to somewhere you will remember.
```console
git clone https://github.com/staysh/pcc-course-cleaner.git
```
Navigate to the repo/folder in your terminal and create a virtual environment
```console
mkdir venv
python -m venv .
source .venv/bin/activate
```
Install requirements (Beautiful Soup 4)
```console
pip install -r requirements.txt
```
## Usage
To see the options for the script you can run the script with the --help argument
```console
python course-cleaner.py --help
```
* **--folder** or **-f** this argument should be followed by a path to your unzipped brightspace package
* **--sheet** or **-s** this argument should be followed by the path to a stylesheet
* **--keep** or **-k** follow with a keyword in a stylesheet url to keep like 'bootstrap' *Note:* using something like 'https' here will keep all external style sheets and remove those with relative urls
* **--links** or **-l** no argument, this flag will make all links open in a new window by adding `target="_blank"`
* **--clean** or **-c** no argument, this flag will remove non-layout inline style attributes
* **--debug** or **-d** runs and prints out way too much information about what it would do, but does not alter the files

## Updating the Course
* Zip the folder back up and rename it (like adding -cleaned) to the end
* There are two options for uploading
	* Reset theh course and import the cleaned zip course package
	* Import the cleaned zip and select overwrite files option

This is still rough around the edges, please feel free to email me with any questions. 
