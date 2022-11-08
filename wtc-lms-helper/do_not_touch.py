import os

# with open('reviews_list.txt') as file:
#     if file.read() == '':
#         os.system("echo file is empty.. try logging in the wtc-lms first")
#     else:
#         file_info = file.read()
#         print('file read')
#         print(file_info)

file = open('reviews_list.txt')

file_info = file.readline()

if not file_info:
    print("file is empty.. try logging in the wtc-lms first")
else:

        pos_start = file_info.find('(')
        pos_end = file_info.find(')')
        review_uiid = file_info[pos_start+1 : pos_end]

        os.system(f'wtc-lms accept {review_uiid}')
        os.system(f'wtc-lms review_details {review_uiid} > review_details.txt')


        