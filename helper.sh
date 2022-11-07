#! /usr/bin/bash
#get info for creating a path and getting the clone from gitlab

echo -n "What's the project name? (e.g. Mastermind): "
read project
echo -n "What iteration? (Enter '1' for iteration 1.. etc): "
read iteration_number

iteration='iteration'$iteration_number
project_uiid=$1

if [ -z "$project_uiid" ]; 
then
	echo "Enter the project uiid"
	read project_uiid
fi
	DIR=~/problems/$project/$iteration/$project_name
	wtc-lms start $project_uiid > gitlab_link.txt;
	link=$(grep "git" "gitlab_link.txt");
	if [ -d "$DIR" ]; 
	then 
		cd $DIR;
		echo "Directory already exists.";
		code $DIR;
		$SHELL;
	else
		$link $DIR;
		cd $DIR;
		code $DIR;
		$SHELL
	fi


