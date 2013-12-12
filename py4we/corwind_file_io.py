# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 10:04:28 2013

@author: pmau
"""
import numpy as np
from we_file_io import WEFileIO
import matplotlib.ticker as ticker
from matplotlib import dates
import datetime

class CorwindFileIO(WEFileIO):
    __header = [];
    __dates = [];
    __values = [];
    __filename = ''
    __delimiter = ','
    __dateTimeFormat = '%d/%m/%Y %H:%M:%S'
    __alternativeDateTimeFormat = '%d/%m/%Y'
        
    def __init__(self, filename=None):        
        WEFileIO.__init__(self, filename)
        self.__filename = filename
                
    def _read(self):
        f = open(self.filename,"r")
        contents = f.readlines()                
        f.close()
        lastHeaderLine = 0
        isHeader=1
        i=0
        arrayInitialized = 0;
        for row in contents:
            parts = row.rstrip('\n').split(self.__delimiter)
            i=i+1
            try:                                
                dateTime = datetime.datetime.strptime(parts[0], self.__dateTimeFormat)                
                isHeader = 0;
            except ValueError:
                try:
                    dateTime = datetime.datetime.strptime(parts[0], self.__alternativeDateTimeFormat)
                    isHeader = 0;
                except ValueError:
                    lastHeaderLine=i;                
                    dateTime = None 
            if (isHeader == 1):
                self.__header.append(parts[1:])
            else:
                if (arrayInitialized==0):
                    arrayInitialized=1;
                    self.__values=np.zeros((len(contents)-lastHeaderLine, len(parts) - 1))
                for j in range(0,len(parts)-1):
                    self.__values[i-lastHeaderLine - 1, j] = float(parts[j+1])
                self.__dates.append(dateTime)    
    
    def _plot(self, fig):
        ax = fig.add_subplot(1,1,1)    
        
        def format_date(x, pos=None):                         
            #return dates.num2date(x).strftime('%d.%m.%Y %H:%M')
            return dates.num2date(x).strftime('%d.%m.%Y') + '\n' + dates.num2date(x).strftime('%H:%M:%S')
                        
        for j in range(0,np.size(self.__values, 1)):
            ax.plot(self.__dates, self.__values[:,j],'-')
                            
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date)) # custom format
        
        #for tl in ax.xaxis.get_ticklabels():            
        #    tl.set_rotation(0)            
        
        ax.legend(self.__header[len(self.__header) - 1], loc='upper left', fancybox=True, shadow=True, ncol=1)        
        ax.set_xlabel('date/time')        
        ax.set_title(self.__filename)        
        
    def _write(self):
        f = open(self.filename, 'w')
        for i in range(0, len(self.__header)):            
            for j in range (0, len(self.__header[i])):
                f.write(self.__delimiter)
                f.write(self.__header[i][j])
            f.write('\n')
                
        for i in range(0, len(self.__dates)):             
            f.write(datetime.datetime.strftime(self.__dates[i], self.__dateTimeFormat))
            for j in range(0, np.size(self.__values, 1)):
                f.write(self.__delimiter)
                f.write(str(self.__values[i, j]))
            f.write('\n')        
        
        f.close()

    def getHeader(self):
        return self.__header;

    def setHeader(self, header):
        self.__header = header;
        
    def getDateTimes(self):
        return self.__dates;

    def setDateTimes(self, datetimes):
        self.__dates = datetimes;

    def getValues(self):
        return self.__values;

    def setValues(self, values):
        self.__values = values;

#corwindData=CorwindFileIO('test\\corwind\\ws_individual.csv')
#headerRows=corwindData.getHeader();
#dateTimes=corwindData.getDateTimes();
#values=corwindData.getValues()
#corwindData.write('test\\corwind\\new.csv')
#corwindData.plot()

