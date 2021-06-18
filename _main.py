# https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-get

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests

from jql_requester import jira_jql_request
from jql_requester import jira_status_checker
from requests.auth import HTTPBasicAuth
from task_parser import jira_task
import pandas as pd


###################

'Зададим парамтеры'

jira_host = "https://jira.crpt.ru"
rest_api_path = "/rest/api/latest"
auth = HTTPBasicAuth("login", "password")
headers = {"Accept": "application/json"}
payload = {
              "expand": [
              ],
              "jql": "project = KAT AND component = \"Внесение изменений\"",
              "maxResults": 400,
              "fields": [
                "key"
              ],
              "startAt": 0
            }
folder_path = 'downloads/' # сюда будут сохранены вложения из тасок
######################################################

"проверим статус"

x = jira_status_checker(url=jira_host, headers=headers, auth=auth)
print('Response status:', x)

######################################################

'сделаем запрос на получение всех тасок'

# запрос выполнен успешно, поэтому закоментим, чтоб не тратить времени

jql_resp = jira_jql_request(jira_host=jira_host,
                                rest_api_path=rest_api_path,
                                params=payload,
                                headers=headers,
                                auth=auth)


#####################

'получим список тасок'

task_list = jql_resp.tasklist()
print('список тасок получен')


#######################

'получим массив названий-ссылок'
# закоментим этот фрагмент, т.к. уже массив получен и сохранен в

full_attachment_array = []
for issue in task_list:
    print('current issue =', issue)

    current_task = jira_task(jira_host=jira_host, rest_api_path=rest_api_path, issue_id=issue, headers=headers, auth=auth)
    current_attachments_array = current_task.attachment(extension_list=['.xlsx', '.xls'])
    for pair in current_attachments_array:
        full_attachment_array.append(pair)

#print(full_attachment_array)


##########################################
'сохраним все файлы из полученного предварительно сохраненного файла'
'''
with open('full_attachment_array.txt', 'r', encoding='UTF-8') as file:
    full_attachment_array = file.read()
    #print(full_attachment_array)
'''



for pair in full_attachment_array:
    file_name = pair[0]

    index_of_dot = pair[1].rfind('.')
    total_length = len(pair[1])
    file_extension = pair[1][index_of_dot:total_length]

    full_name = folder_path + file_name + file_extension
    link = pair[1]

    print('file {} is created \n'.format(full_name))


    resp = requests.get(link, auth=auth)  # делаем запрос
    with open(full_name, "wb") as output:  # открываем файл для записи, в режиме wb)
        output.write(resp.content)  # записываем содержимое в файл