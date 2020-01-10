from bs4 import *
import requests
import re
from datetime import date
import datetime
import json


def crawler_1(user, contest_code, question_code):

    u =  'https://codeforces.com/api/contest.status?contestId='+contest_code+'&handle='+user

    r = requests.get(u)

    data = r.json()
    data = data['result']

    for submission in data:
        if submission['problem']['index']==question_code and submission['verdict']=='OK':
            u = 'https://codeforces.com/contest/'+contest_code+'/submission/'+str(submission['id'])
            code_page = requests.get(u).text
            soup_code = BeautifulSoup(code_page, 'lxml')
            return soup_code.find("pre", id="program-source-text").stripped_strings
    


def crawler_2(user):
    codeforces = 'http://codeforces.com/'
    contests = 'contests/with/'
    user_1_page = requests.get(codeforces + contests + user_1).text
    user_2_page = requests.get(codeforces + contests + user_2).text
    soup_1 = BeautifulSoup(user_1_page, 'lxml')
    soup_2 = BeautifulSoup(user_2_page, 'lxml')
    contest_table_1 = soup_1.find_all("table", class_="tablesorter user-contests-table")
    contest_table_2 = soup_2.find_all("table", class_="tablesorter user-contests-table")
    contests_1 = []
    contests_2 = []
    rating_changes_1 = []
    rating_changes_2 = []
    for table_row in contest_table_1[0].tbody.find_all("tr"):
        contest_details = []
        for table_data in table_row.find_all("td"):
            contest_details.append(table_data)
        contests_1.append(contest_details)
        rating_changes_1.append(int(contest_details[4].span.string))
    for table_row in contest_table_2[0].tbody.find_all("tr"):
        contest_details = []
        for table_data in table_row.find_all("td"):
            contest_details.append(table_data)
        contests_2.append(contest_details)
        rating_changes_2.append(int(contest_details[4].span.string))
    max_change_1 = rating_changes_1[0]
    min_change_1 = rating_changes_1[0]
    avg_change_1 = 0
    for rating in rating_changes_1:
        if (rating >= max_change_1):
            max_change_1 = rating
        if (rating <= min_change_1):
            min_change_1 = rating
        avg_change_1 += rating
    avg_change_1 /= len(rating_changes_1)
    max_change_2 = rating_changes_2[0]
    min_change_2 = rating_changes_2[0]
    avg_change_2 = 0

    for rating in rating_changes_2:
        if (rating >= max_change_2):
            max_change_2 = rating
        if (rating <= min_change_2):
            min_change_2 = rating
        avg_change_2 += rating
    avg_change_2 /= len(rating_changes_2)
    return (max_change_1, min_change_1, avg_change_1, max_change_2, min_change_2, avg_change_2)
    """
    u = "https://codeforces.com/api/user.info?handles="+user
    r = requests.get(u)
    data = r.json()
    data = data['result'][0]
    return(data)
    """

def crawler_3(user):
    codeforces = 'http://codeforces.com/'
    submissions = 'submissions/'
    submissions_page = requests.get(codeforces + submissions + user + "/page/1").text
    soup = BeautifulSoup(submissions_page, 'lxml')
    page_list = soup.find_all("span", class_="page-index")
    page_list = page_list[len(page_list) - 1].find("a").contents
    pages = int(page_list[0])
    attempts = {}
    for page_index in range(1, pages + 1):
        submissions_page = requests.get(codeforces + submissions + user + "/page/" + str(page_index)).text
        soup = BeautifulSoup(submissions_page, 'lxml')
        submissions_table = soup.find_all("table", class_="status-frame-datatable")
        for table_row in submissions_table[0].find_all("tr"):
            for table_data in table_row.find_all("td", class_="status-small"):
                if (table_data.a != None):
                    problem = table_data.a.get("href")
                    problem = " ".join(problem.split("/"))
                    if problem not in attempts:
                        attempts[problem] = 1
                    else:
                        attempts[problem] += 1
    return attempts

def crawler_4(user):
    codeforces = 'https://www.codeforces.com/'
    contests = 'contests/'
    user_page = requests.get(codeforces + contests + 'with/' + user).text
    soup = BeautifulSoup(user_page, 'lxml')
    contest_table = soup.find_all("table", class_="tablesorter user-contests-table")
    contests_dict = {}
    for table_row in contest_table[0].tbody.find_all("tr"):
        if (table_row.a != None):
            contests_dict[table_row.a.get('href')] = 1
    contest_page = requests.get(codeforces + contests).text
    soup_contests = BeautifulSoup(contest_page, 'lxml')
    contest_table = soup_contests.find_all("table", class_="")
    past_contests = contest_table[1]
    contest_date_and_time = {}
    for table_row in past_contests.find_all("tr"):
        if (table_row.a != None):
            time_of_contest = table_row.find_all("span", class_="format-date")
            if (str(table_row.a.get('href')) in contests_dict):
                contest_date_and_time[table_row.a.get('href')] = time_of_contest[0].string
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
              'Nov': 11, 'Dec': 12}
    dates_of_contests = []
    for x in contest_date_and_time:
        dates = str(contest_date_and_time[x])
        month = months[dates[:3]]
        day = int(dates[4:6])
        year = int(dates[7:11])
        d = date(year, month, day)
        dates_of_contests.append(d)
    avg_contest_gap = 0
    for i in range(1, len(dates_of_contests) - 1):
        avg_contest_gap += (dates_of_contests[i - 1] - dates_of_contests[i]).days
    avg_contest_gap /= (len(dates_of_contests) - 1)
    return avg_contest_gap


def crawler_5(user1, user2, contest_code):
    codeforces = 'https://www.codeforces.com/'
    contest_page = requests.get(codeforces + 'contest/' + contest_code).text
    soup = BeautifulSoup(contest_page, 'lxml')
    problems_table = soup.find("table", class_="problems")
    problems = {}
    for table_row in problems_table.find_all("tr"):
        table_data = list(table_row.find_all("td"))
        if (len(table_data) > 2):
            code = table_data[0].a.string.strip()
            problems[code] = {}
            problems[code]['name'] = table_data[1].a.get_text()
            problems[code]['attempts1'] = 0
            problems[code]['attempts2'] = 0
            problems[code]['success1'] = 0
            problems[code]['success2'] = 0
            problems[code]['time1'] = 0
            problems[code]['time2'] = 0
    contest_page1 = requests.get(codeforces + 'submissions/' + user1 + '/contest/' + contest_code).text
    #contest_page1=requests.get('https://codeforces.com/submissions/sparsh2706/contest/1287').text
    contest_page2 = requests.get(codeforces + 'submissions/' + user2 + '/contest/' + contest_code).text
    soup1 = BeautifulSoup(contest_page1, 'lxml')
    soup2 = BeautifulSoup(contest_page2, 'lxml')
    contests_table1 = soup1.find("table" , class_="status-frame-datatable")
    contests_table2 = soup2.find("table", class_="status-frame-datatable")
    for table_row in contests_table1.find_all("tr"):
        table_data = table_row.find_all("td")
        if (len(table_data) > 0):
            code = list(table_data[3].a.get("href").split('/'))[-1]
            problems[code]['attempts1'] += 1
            if (table_data[5].span['submissionverdict'] == 'OK'):
                problems[code]['success1'] += 1
                problems[code]['time1'] = table_data[1].get_text().strip()
    for table_row in contests_table2.find_all("tr"):
        table_data = table_row.find_all("td")
        if (len(table_data) > 0):
            code = list(table_data[3].a.get("href").split('/'))[-1]
            problems[code]['attempts2'] += 1
            if (table_data[5].span['submissionverdict'] == 'OK'):
                problems[code]['success2'] += 1
                problems[code]['time2'] = table_data[1].get_text().strip()
    for A in problems:
        print(A, problems[A]['name'])
        print(user1, problems[A]['attempts1'], problems[A]['success1'], problems[A]['time1'])
        print(user2, problems[A]['attempts2'], problems[A]['success2'], problems[A]['time2'])
    return problems
   
def generate_heat_map(user):
    cf_api = requests.get('https://codeforces.com/api/user.status?handle=' + user)

    sub_json = cf_api.json()

    submissions = {}
    ref = datetime.date(2019, 1, 1)
    for t in sub_json["result"]:
        x = datetime.datetime.fromtimestamp(t["creationTimeSeconds"]).date()
        x = (x - ref).days
        if submissions.get(x) is None:
            submissions[x] = 1
        else:
            submissions[x] = submissions[x] + 1
    return submissions

def generate_pie_chart(user):
    cf_api = requests.get('https://codeforces.com/api/user.status?handle=' + user)
    sub_json = cf_api.json()
    tags = {}
    for keys in sub_json["result"]:
        for tag in keys["problem"]["tags"]:
            if tags.get(tag) is None:
                tags[tag] = 1
            else:
                tags[tag] += 1
    return tags

#print(crawler_3('seabreeze'))