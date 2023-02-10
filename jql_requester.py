import requests

import json
from requests.auth import HTTPBasicAuth

def jira_status_checker(url, headers, auth):
    r = requests.request(method="GET",
                         url=url,
                         headers=headers,
                         auth=auth)
    if r.status_code != 200:
        print('Status code: ' + str(r.status_code))
        print('Login response: ' + str(r.json()))
        exit(1)

    print("waiting for response...\n")
    return(str(r.status_code))


class jira_jql_request(object):
    """Полный объект по запросу. Запрос формируется в строке запроса и копируется из адресной строки"""
    def __init__(self, jira_host, rest_api_path, params, headers, auth):
        """Constructor"""
        self.jira_host = jira_host
        self.rest_api_path = rest_api_path
        self.params = params
        self.headers = headers
        self.auth = auth

        url = jira_host + rest_api_path + '/search'
        payload = params #json.dumps(payload)
        headers = headers
        auth = auth

        response = requests.request(method="GET",
                                    url=url,
                                    headers=headers,
                                    params=payload,
                                    auth=auth)
        response = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

        self.answer = response

    def response(self):
        """
        Полная информация по таске в виде словаря, но формат ответа - str
        """
        return self.answer

    def tasklist(self):
        """
        Список задач по запросу
        """
        answer_body = json.loads(self.answer)

        task_list = []
        for issue_number in range(len(answer_body['issues'])):
            issue_url = answer_body['issues'][issue_number]['key']
            task_list.append(issue_url)

        return task_list




if __name__ == '__main__':

    jira_host = "https://jira.crpt.ru"
    rest_api_path = "/rest/api/latest"
    auth = HTTPBasicAuth("username", "password")
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

    # depricated
    #jql_request = "search?jql=project%20%3D%20KAT%20AND%20component%20%3D%20\"Внесение%20изменений\"%20ORDER%20BY%20updated%20DESC"

    x = jira_status_checker(url=jira_host, headers=headers, auth=auth)
    print('Response status:', x)


    jql_resp = jira_jql_request(jira_host=jira_host,
                                rest_api_path=rest_api_path,
                                params=payload,
                                headers=headers,
                                auth=auth)

    full_response = jql_resp.response()
    #print(full_response)

    # Запишем в файл
    full_response_textfile = open("full_response.txt", "w")
    a = full_response_textfile.write(full_response)
    full_response_textfile.close()

    # сохраним в список

    task_list = jql_resp.tasklist()
    print(task_list)



    #tasklist = jql_resp.tasklist()
    #print(len(tasklist))
