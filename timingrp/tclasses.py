import csv
import datetime as dt
from __future__ import division, print_function
import numpy as np


def print_time(seconds):
    sec = dt.timedelta(seconds=int(seconds))
    d = dt.datetime(1,1,1) + sec
    print("%d hours, %d minutes and %d seconds" % (d.hour, d.minute, d.second))

class tevent:
    def __init__(self,v):
        self.app = v[0]
        self.path = v[1]
        self.start_date = v[2]
        self.day = int(v[2][:2])
        self.month = int(v[2][3:5])
        self.year = int(v[2][6:8])
        self.end = v[3]
        self.hour = int(v[2][9:11])
        self.duration = int(v[4])
        self.project = v[5]
        self.date = dt.date(2000+self.year,self.month,self.day)



class tlogevents:
    def __init__(self,file_name):
        #open the cvs file, example file_name='lastweek.cvs'
        self._cvsrawfile = open(file_name, 'rt')
        #builds a reader. ATTENTION it doesn't always work, don't know why
        self._cvsreader = csv.reader(self._cvsrawfile, delimiter=',')

        #fucking hack
        self._a=[]
        for row in self._cvsreader:
            self._a.append(row)
        
        #creates a list of tevent class objects. Skips the first element because it's just labels.
        self.events = []
        for row in self._a[1:]:
            self.events.append(tevent(row))
        self.start_date = self.events[0].date
        self.end_date = self.events[-1].date
        self.num_of_days = (self.end_date - self.start_date).days + 1
        
        #lazy stuff
        self._num_of_inactive_days = None
        self._total_seconds = None
        self._daily_usage_vector = None
        self._busiest_day = None

        self.daily_average_seconds = self.total_seconds / self.num_of_days
        self.daily_average_seconds_disc = self.total_seconds / (self.num_of_days - self.num_of_inactive_days)
        
    @property
    def num_of_inactive_days(self):
        if self._num_of_inactive_days is None:
            count = 0
            last_day = self.start_date
            for event in self.events:
                if (event.date - last_day).days >1:
                    count += (event.date - last_day).days - 1
                last_day = event.date
            self._num_of_inactive_days = count
        return self._num_of_inactive_days

    @property
    def total_seconds(self):
        if self._total_seconds is None:
            count = 0
            for event in self.events:
                count+=event.duration
            self._total_seconds = count
        return self._total_seconds

    @property
    def hour_usage_matrix(self):
        if _hour_usage_matrix is None:
            mat = np.zeros((self.num_of_days,24))
            for event in self.events:
                mat[event.date - self.start_date][event.hour]+=event.duration
            _hour_usage_matrix = mat
        return _hour_usage_matrix

    @property
    def daily_usage_vector(self):
        if self._daily_usage_vector is None:
            vect = [0]*self.num_of_days
            for event in self.events:
                vect[(event.date-self.start_date).days]+=event.duration
            self._daily_usage_vector = vect
        return self._daily_usage_vector

    @property 
    def busiest_day(self):
        if self._busiest_day is None:
            self._busiest_day =  self.start_date + dt.timedelta(days=self.daily_usage_vector.index(max(self.daily_usage_vector)))
        return self._busiest_day

    def hour_heat_map(self):
        imshow(self.hour_usage_matrix)

    def daily_usage_plot(self):
        plot(range(self.num_of_days),self.daily_usage_vector)
    def print_analysis(self):
        print ("START DATE")
        print (self.start_date)
        print ("END DATE")
        print (self.end_date)
        print ("NUMBER OF DAYS OF ANALYSIS")
        print (self.num_of_days)
        print ("TOTAL TIME SPENT ON THE COMPUTER")
        print_time(self.total_seconds)
        print ("DAILY AVERAGE")
        print_time(self.daily_average_seconds)
        print ("NUMBER OF INACTIVE DAYS")
        print (self.num_of_inactive_days)
        print ("DAILY AVERAGE (DISCOUNTED)")
        print_time(self.daily_average_seconds_disc)
        print ("BUISIES DAY")
        print (self.busiest_day)