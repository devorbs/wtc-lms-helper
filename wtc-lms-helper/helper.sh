#! /usr/bin/bash

helper_command=$1

if [ -z $helper_command ];
then

	echo "Please provide a command for helper ['helper start' - to start a project,\
'review' - for reviews, 'submit' - to submit a project]"

elif [ $helper_command == 'start' ];
then
	#get info for creating a path and getting the clone from gitlab

	echo -n "What's the project name? (e.g. Mastermind): ";
	read project;
	echo -n "What iteration? (Enter '1' for iteration 1.. etc): ";
	read iteration_number;

	#Set the iteration number and concat to path, get project name
	iteration='iteration'$iteration_number;
	project_uiid=$2

	#check if project name is not found from cli arguments
	if [ -z "$project_uiid" ]; 
	then
		#Prompt user for the project name
		echo "Enter the project uiid";
		read project_uiid;
	fi
	#set a directory path to save the clone into
	DIR=~/problems/$project/$iteration/$project_uiid;

	#command lms to start a project with project name, save to file
	#get the file and search for git clone command
	wtc-lms start $project_uiid > gitlab_link.txt
	link=$(grep "git" "gitlab_link.txt");

	if [ -z "$link" ];
	then
		echo "Please log in on wtc-lms using 'wtc-lms login' command"
	else

		#check if the directory to clone into exists
		if [ -d "$DIR" ]; 
		then 
			# move to that directory and open it with a code editor
			cd $DIR;
			echo "Directory already exists.";
			code $DIR;
			$SHELL; #opening child terminal
		else
		
			#clone from github into the directory then open with code editor
			$link $DIR;
			cd $DIR;
			code $DIR;
			$SHELL; #opening child terminal
		fi
	fi
elif [ $helper_command == 'review' ];
then
	
	wtc-lms reviews | grep "Invited" > reviews_list.txt

	python3 do_not_touch.py

elif [ $helper_command == 'submit' ];
then
	echo "submitting project"
else
	echo "unknown command"
fi
