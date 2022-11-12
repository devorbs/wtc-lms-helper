import os
import subprocess
import sys


def start_project():
    '''
    when command is start, this function will execute the sequence to start a project
    '''
    #get project name and start the project
    project_uiid = input('Enter the project uiid: ').lower().strip()
    start_results = subprocess.run(['wtc-lms', 'start', project_uiid], stdout=subprocess.PIPE, text=True)

    if start_results.returncode == 0:
        #get information to create a directory for storing the project
        print('\nProject successfully started, where to clone it?')
        project_name = input("Project name (e.g. Mastermind): ").strip()
        iteration = input('Which iteration? (1 - for iteration 1, 2 - for iteration 2, etc..): ').strip()

        #set up the necessary folders 
        iteration = f'iteration{iteration}'
        home = os.path.expanduser('~')
        os.chdir(home) 
        cwd = os.getcwd() + '/problems'
        directory = os.path.join(cwd,project_name,iteration)

        #get the project gitlab link and clone to the appropriate folder
        link_dump = start_results.stdout
        link_pos = link_dump.find('git')
        commands_list = link_dump[link_pos:].strip().split()  

        clone_results = subprocess.run([commands_list[0], commands_list[1], commands_list[2], directory],
                                         stdout= subprocess.PIPE , text=True)

        if clone_results.returncode != 0:
            print("\nDirectory already exists and it's not empty.")
            print("\nThe directory will be opened with VS Code shortly..")

        #change to the folder and open it with vs code
        os.chdir(directory)
        #subprocess.run(['code', directory])
    
    else:
        print('\nFailed to start project. Please check the project uiid.')

def start_review():
    review_results = subprocess.run(['wtc-lms', 'reviews'],  stdout= subprocess.PIPE, text=True)
    list_of_reviews= review_results.stdout.split('\n')

    for review in list_of_reviews:
        if review.find('[') > 0:
            start_pos = review.find('[')
            end_pos = review.find(']')
            keyword = review[start_pos+1: end_pos]

            if keyword == 'Assigned':
                start_pos = review.find('(')
                end_pos = review.find(')')
                clone_name = review[start_pos+1: end_pos]
                
                clone_link_dump = subprocess.run(['wtc-lms','accept', clone_name],
                                         stdout=subprocess.PIPE, text=True)

                if clone_link_dump.returncode == 0:
                    reviewee_info = subprocess.run(['wtc-lms', 'review_details', clone_name],
                                            stdout=subprocess.PIPE, text=True)

                    clone_link = clone_link_dump[clone_link_dump.find('git'):].strip()
                    words_list = review.split('>')
                    another_words_list = words_list[2].split('-')
                    project_name = another_words_list[0].strip()
                    iteration = f'iteration{another_words_list[1].split()[0].strip().split()[0]}'
                    username = reviewee_info.stdout[reviewee_info.stdout.find('Submission'):].split('\n')[0].split(':')[1]
                    username = username[:username.find('@')].strip()


                    home = os.path.expanduser('~')
                    os.chdir(home)
                    cwd = os.getcwd() + '/reviews'
                    directory = os.path.join(cwd, project_name, iteration, username)

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
                        

def check_login():
    '''
    This function will check if the user is logged in on the wtc-lms
    '''
    check_login = subprocess.run(['wtc-lms', 'problems'], stdout=subprocess.PIPE, text=True)

    if check_login.returncode != 0:
        #get the user to login 
        print("Seems like you're not logged in. Let's get you logged in first..\n")
        logged = subprocess.run(['wtc-lms' ,'login'], stdout=subprocess.PIPE , text = True)

        return True if logged.returncode == 0 else False

    return True

def varify_command(command):
    '''
    check if user entered the required command,
    ask until user enters required command
    '''
    while command not in ['start', 'submit', 'review']:
        print('Please command helper to do something( start - to start a project, review - to review  a project, submit - to submit a project)')
        command = input('-- ').lower().strip()
    return command

def match_command(command):
    '''
    check command and call appropriate function based on command
    '''
    if command == 'start':
        start_project()
    elif command == 'review':
        start_review()
    elif command == 'submit':
        submit_project()

def get_command():
    '''
    after user logs in , run this function to get command
    '''
    print('Successfully Logged in, now checking commands...\n')

    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print('Please command helper to do something( start - to start a project, review - to review  a project, submit - to submit a project)')
        command = input('-- ').lower().strip()
        command = varify_command(command)
        match_command(command) 

    else:
        command = sys.argv[2]

        command = varify_command(command)
        match_command(command)


if __name__ == "__main__":
 
    if check_login():
        get_command()
    else:
        print('Login failed. Please check your password and try again.')

