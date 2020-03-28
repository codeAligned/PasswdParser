Author: 
	Name: Nainy Jain
	Email: jain0193@umn.edu

Language used: Python
Version used: Python 3.6.5 

Instuctions to run PasswdParser::
	Run the following command in the terminal:
		python PasswdParser.py [passwd_path] [group_path]

		Here passwd_path and group_path are arguments with default value as '/etc/passwd' and '/etc/group' respectively.

	Example command to run with system arguments:
		python PasswdParser.py /etc/passwd /etc/group

	Example command to run without system arguments:
		python PasswdParser.py

Result:
	After running the above command, desired result is printed in the CLI. Also, a JSON file is created (if permitted) in the current directory naming "passwd_parser.json"

Assumptions:
	- The argument for passwd and group file is assumed to be full path, till the file name. Example, '/etc/passwd'.
	- The passwd and group files have 2 types of lines, one is comment (starting with #) and other one is valid user details with 7 and 4 colons (:) for passwd and group file respectively. Any other entry is considered to be malformed and a warning is shown if such line is found.
	- If files are not present in the paths provided, an error is thrown and code exits.
	- If user do not have permission to open/read the files, code exits after throeing error.