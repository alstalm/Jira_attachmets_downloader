import requests
import json
from requests.auth import HTTPBasicAuth


####################################################################################
class jira_task(object):
    """Полный объект по запрошеной таске"""

    def __init__(self, jira_host, rest_api_path, issue_id, headers, auth):
        """Constructor"""
        self.jira_host = jira_host
        self.rest_api_path = rest_api_path
        self.issue_id = issue_id
        self.headers = headers
        self.auth = auth

        request_issue = "/issue/" + issue_id
        url = jira_host + rest_api_path + request_issue
        #pint('url =', url)
        headers = headers
        auth = auth

        response = requests.request(method="GET",
                                    url=url,
                                    headers=headers,
                                    auth=auth)
        self.answer = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

    def response(self):
        """
        Полная информация по таске в виде словаря, но формат ответа - str
        """
        return self.answer

    def attachment(self, extension_list=None):
        """
        Список ссылок вложений
        """

        answer_body = json.loads(self.answer)

        attachment_array = []
        task = self.issue_id

        i = 0

        for attachment_element_number in range(len(answer_body['fields']['attachment'])):
            link = answer_body['fields']['attachment'][attachment_element_number]['content']
            for extension in extension_list:
                extension_index = link.find(extension)
                link_length = len(link)
                if extension_index != -1 and link_length - extension_index == len(extension): # проверяем есть ли вхождение расширения в названии ссылки

                    link_curent_attachment_name_pair = []
                    curent_attachment_name = task + '_' + str(i)
                    i += 1

                    link_curent_attachment_name_pair.append(curent_attachment_name)
                    link_curent_attachment_name_pair.append(link)

                    attachment_array.append(link_curent_attachment_name_pair)

        return attachment_array


''' ниже проверка работы текущеего модуля '''

if __name__ == '__main__':
    jira_host = "https://jira.crpt.ru"
    rest_api_path = "/rest/api/latest"
    auth = HTTPBasicAuth("aleksandr.stalmakov", "TaNghetto2849")
    headers = {"Accept": "application/json"}
    issue_id = 'KAT-11756'

    KAT_11756 = jira_task(jira_host=jira_host, rest_api_path=rest_api_path, issue_id=issue_id,
                          headers=headers, auth=auth)


    x = KAT_11756.attachment(extension_list=['.xlsx', '.png'])


    print(x)
    '''
    y = KAT_11756.attachment()
    print(y)
    '''
    # x = jira_status_checker(url=jira_host, headers=headers, auth=auth)
    # print('Response status:', x)

    # y = jira_jql_requester(jira_host=jira_host, rest_api_path=rest_api_path, jql_request=jql_request,
    #                       headers=headers, auth=auth)
    # print(y)

    # z = jira_issue_requester(jira_host, rest_api_path, issue_id='KAT-11756', headers=headers, auth=auth)
    # print(z)
