#! /usr/bin/python3

import os
import subprocess
import sys

def setup():
    """
    create a script file that will setup helper to be run as [helper start]
    """
    #when the script is run it should run the python file
    home = os.path.expanduser('~')

    #create helper-config folder
    config_path = os.path.join(home, 'helper-config')
    os.makedirs(config_path, exist_ok=True)
    cwd = os.getcwd()

    #copy the helper.py to home/wethinkcode/helper-config folder
    subprocess.run(['cp', f'{cwd}/helper.py', config_path])

    #change the script permission to +x
    subprocess.run(['chmod','+x',f'{config_path}/helper.py'])
    os.system(f'ln {config_path}/helper.py {home}/.local/bin/helper') #link for file to bin folder

    print("\n\nSetup complete!\n")


def start_project():
    '''
    when command is start, this function will execute the sequence to start a project
    '''
    #get project name and start the project
    project_uiid = input( "Enter the project uiid: " ).lower().strip()
    start_results = subprocess.run( ['wtc-lms', 'start', project_uiid] ,
                                     stdout=subprocess.PIPE, text=True )

    if start_results.returncode == 0:
        #get information to create a directory for storing the project
        print( "\nProject successfully started, where to clone it?" )
        project_name = input( "Project name (e.g. Mastermind): " ).strip()
        iteration = input( "Which iteration? (1 - for iteration 1, 2 - for iteration 2, etc..): " ).strip()

        #set up the necessary folders 
        iteration = f'iteration{ iteration }'
        home = os.path.expanduser('~')
        os.chdir(home) 
        cwd = os.getcwd()
        directory = os.path.join(cwd, 'problems', project_name, iteration)
        config_folder = os.path.join(home,'helper-config', 'paths')
        os.mkdir(config_folder)

        #get the project gitlab link and clone to the appropriate folder
        link_dump = start_results.stdout
        link_pos = link_dump.find('git')
        commands_list = link_dump[ link_pos: ].strip().split()  

        clone_results = subprocess.run( [commands_list[0], commands_list[1], commands_list[2], directory] ,
                                         stdout= subprocess.PIPE , text=True )

        if clone_results.returncode != 0:
            print( "\nDirectory already exists and it's not empty." )
            print( "\nThe directory will be opened with VS Code shortly.." )
        helper_path = os.path.join(directory, 'helper-info')
        os.mkdir(helper_path)

        os.system(f'echo "{directory}" >> {helper_path}/{project_uiid}.txt')
        os.system(f'ln {helper_path}/{project_uiid}.txt {config_folder}/{project_uiid}')

        #change to the folder and open it with vs code
        os.chdir(directory)
        subprocess.run(['code', directory])
    
    else:
        print( "\nFailed to start project. Please check the project uiid." )

def start_review():
    '''
    This function will execute when the user chooses the 'review' command for helper
    '''
    review_results = subprocess.run(['wtc-lms', 'reviews'],  stdout= subprocess.PIPE, text=True)
    list_of_reviews= review_results.stdout.split('\n')


    for review in list_of_reviews:
        #look for '[' in that line, only take lines with '[]' in them
        if review.find('[') > 0:
            start_pos = review.find('[')
            end_pos = review.find(']')
            keyword = review[start_pos+1: end_pos] #the word between the [] should be 'Invited'

            if keyword == 'Invited':
                start_pos = review.find('(')
                end_pos = review.find(')')
                clone_name = review[start_pos+1: end_pos] #get the uiid for the project on gitlab
                
                clone_link_dump = subprocess.run(['wtc-lms','accept', clone_name],
                                         stdout=subprocess.PIPE, text=True)

                if clone_link_dump.returncode == 0:
                    reviewee_info = subprocess.run(['wtc-lms', 'review_details', clone_name],
                                            stdout=subprocess.PIPE, text=True)

                    clone_link = clone_link_dump[clone_link_dump.find('git'):].strip() #get the gitlab link from the dump
                    words_list = review.split('>') #separate the lines by '>' character
                    another_words_list = words_list[2].split('-') #take string from words_list[2] and separate them further
                    project_name = another_words_list[0].strip() #the first el in another_worlds_list is the project name
                    iteration = f'iteration{another_words_list[1].split()[0].strip().split()[0]}'
                    username = reviewee_info.stdout[reviewee_info.stdout.find('Submission'):].split('\n')[0].split(':')[1] #get username 
                    #from the reviewee_info_dump on a line that starts with Submission
                    username = username[:username.find('@')].strip()


                    home = os.path.expanduser('~')
                    os.chdir(home)
                    cwd = os.getcwd()
                    directory = os.path.join(home, 'reviews', project_name, iteration, username)

                    cloning_results = subprocess.run([clone_link, directory], stdout=subprocess.PIPE, text=True)

                    if cloning_results.returncode == 0:
                        print("\nReview started. Review info will be stored in the review folder.")

                        with open(f'{directory}/review_info.txt', 'a') as file:
                            file.write(reviewee_info.stdout)
                        
                        #subprocess.run(['echo', f'"{cloning_results.stdout}"', '>', f'{directory}/review_info.txt'])

                        os.chdir(directory)
                        subprocess.run(['code', directory], stdout=subprocess.PIPE, text=True)

                        is_comment = input("\nDo you want to add a comment now?(yes/no): ").lower().strip()

                        if is_comment == 'yes' or is_comment == 'y':
                            comment = input("Enter your comment: ").strip()

                            subprocess.run(['wtc-lms', 'add_comment', clone_name, comment])

                            complete_review = input("\nComplete Review? (yes/no): ").lower.strip()

                            if complete_review == 'yes' or complete_review == 'y':
                                subprocess.run(['wtc-lms', 'complete_review', clone_name])
                            
                        next_review = input("\nGo to the next review? (yes/no): ").lower().strip()

                        if next_review == 'yes' or next_review == 'y':
                            continue
                        else:
                            exit()                       

def submit_project():

    home = os.path.expanduser('~')
    config_folder = os.path.join(home,'helper-config', 'paths')

    project_uiid = input("\nPlease enter the project uiid for the project you want to submit: ")
    file_name = ''

    with open(f'{config_folder}/{project_uiid}') as file:
        file_name = file.readlines()

    files = input('\nEnter the file names you want to push separated by a space: ').strip().split(" ")
    file_path = file_name[0].strip()

    os.chdir(file_path)  
    #os.system(f'git add {files}')
    for file in files:
        add_results = subprocess.run(['git', 'add', file], stdout=subprocess.PIPE, text=True)
        if add_results.returncode == 0:
            continue
        else:
            print('\nSomething wrong with the files you entered.')

    commit_message = ''
    if add_results.returncode ==0:
        commit_message = input("What's your commit message?: ")

    subprocess.run(['git','commit','-m',f'"{commit_message}"'])

    subprocess.run(['git', 'push'])

    print("\nProject successfully pushed to gitlab..")

    subprocess.run(['wtc-lms', 'grade', project_uiid])

    subprocess.run(['wtc-lms', 'history', project_uiid])

def check_login():
    '''
    Check if user is logged in on the wtc-lms
    '''
    check_login = subprocess.run(['wtc-lms', 'problems'], stdout=subprocess.PIPE, text=True)

    if check_login.returncode != 0:
        #Prompt the user to login before continuing
        print("Seems like you're not logged in. Let's get you logged in first..\n")
        logged = subprocess.run(['wtc-lms' ,'login'], stdout=subprocess.PIPE , text = True)

        return True if logged.returncode == 0 else False

    return True

def varify_command(command):
    '''
    Check if the command is known, if not get the user to enter a known command to helper
    '''
    while command not in ['start', 'submit', 'review', 'setup']:
        print( "Please command helper to do something( start - to start a project, review - to review  a project, submit - to submit a project, setup - to set up helper")
        command = input('-- ').lower().strip()
    return command

def match_command(command):
    '''
    match the command with it's function and call the function
    '''
    if command == 'start':
        start_project()
    elif command == 'review':
        start_review()
    elif command == 'submit':
        submit_project()
    elif command == 'setup':
        setup()

def get_command():
    '''
    When the user is logged in, check for the command-line argument 
    if it's there, run it through check
    otherwise get it from user
    '''
    print( "Successfully Logged in, now checking commands...\n" )

    if len(sys.argv) != 2: #when there's more than or less than 3 arguments, argument wasnt entered
        command = ''
        command = varify_command(command)
        match_command(command) 

    else:
        command = sys.argv[1] #the third elem in the command line should be the command
        

        command = varify_command(command)
        match_command(command)


if __name__ == "__main__":
 
    if check_login():
        get_command()
    else:
        print('Login failed. Please check your password and try again.')

