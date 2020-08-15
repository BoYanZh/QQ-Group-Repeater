# -*- coding: utf-8 -*-
import json
import time
import requests


class DueHelper:
    def __init__(self, token):
        self.sess = requests.Session()
        self.baseurl = 'https://umjicanvas.com/api/v1'
        self.token = token
        self.courses = self.getCourseID()

    def getCourseID(self):
        res = {}
        page = 1
        while True:
            url = f"{self.baseurl}/courses?" + \
                    f"access_token={self.token}&" + \
                    f"page={page}"
            courses = self.sess.get(url).json()
            if not courses:
                break
            for course in courses:
                # print(course)
                res[course['id']] = course.get('course_code', course.get('name'))
            page += 1
        return res

    def getDue(self):
        re = []
        for courseID, courseName in self.courses.items():
            url = f"{self.baseurl}/courses/{courseID}/assignments" + \
                  f"?access_token={self.token}&bucket=upcoming"
            dues = self.sess.get(url).json()
            for due in dues:
                if type(due) != dict or due.get('due_at') is None:
                    continue
                timeStamp = time.mktime(
                    time.strptime(due['due_at'], "%Y-%m-%dT%H:%M:%SZ"))
                re.append([courseName, due['name'].strip(), timeStamp])
        return sorted(re, key=lambda item: item[2])

    def getDueStr(self):
        re = []
        dues = self.getDue()
        length = str(max([len(due[1]) for due in dues]))
        fmt = "{:6s} {:" + length + "s} Due Time"
        re.append(fmt.format("ID", "Name"))
        fmt = "{:6s} {:" + length + "s} {}"
        for due in dues:
            timeStr = time.strftime("%m/%d %H:%M",
                                    time.localtime(due[2] + 8 * 60 * 60))
            re.append(fmt.format(due[0], due[1], timeStr))
        return '\n'.join(re)


# print(DueHelper(token).getDueStr())
