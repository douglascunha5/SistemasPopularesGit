import requests
import pandas as pd

def run_query(json, headers): # A simple function to use requests.post to make the API call.

    request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}. {}"
                        .format(request.status_code, json['query'],
                                json['variables']))

query = """
query example{
  search(query: "stars:>100", type: REPOSITORY, first: 100{AFTER}) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        name
      }
    }
  }
}
"""

finalQuery = query.replace("{AFTER}", "")

json = {
    "query":finalQuery, "variables":{}
}

token = '519489a5a0de36e2f22f708adc923eba673b5797' #insert your personal token here
headers = {"Authorization": "Bearer " + token}

result = run_query(json, headers)

ans = result['data']['search']['nodes']

if(result['data']['search']['pageInfo']['hasNextPage']):
    finalQuery = query.replace("{AFTER}", ", after:" + result['data']['search']['pageInfo']['endCursor'])
    result = run_query(json, headers)
    ans += result['data']['search']['nodes']

df = pd.DataFrame(result['data']['search']['nodes'], columns=['name'])
df.to_csv("balalaika2.csv", sep="\t", line_terminator="\n")
print(result['data']['search']['nodes'])