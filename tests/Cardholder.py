from pyquery import PyQuery as pq

from foo.pojo.studeninfo import StudentInfo


if __name__ == '__main__':
    doc = pq(filename="../.idea/httpRequests/2022-04-04T105236.200.html")

    studentInfo = StudentInfo(doc)
    print(studentInfo.__dict__)
