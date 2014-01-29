# The class MUST call this class decorator at creation time
# doesn't instantiate it yet.
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)

import ast
from IPython.utils.timing import clock
import time
import os
import sqlite3
import pandas as pd


create_query = """
CREATE TABLE %s (
    userid VARCHAR(10),
    date VARCHAR(20),
    testid VARCHAR(10),
    filesize DOUBLE,
    time DOUBLE
);"""

@magics_class
class LogItMagic(Magics):
    table_name = 'logger'
    file_name = 'sqlite_logger.db'

    def __init__(self, shell):
        super(LogItMagic, self).__init__(shell)
        ## Remove file
        if not os.path.exists(self.file_name):
	        ## Create the table
	        self.execute(create_query%(self.table_name))
        
    def execute(self, query):
        """ Execute a command on the sqlite database """
        db = sqlite3.connect(self.file_name)
        c = db.cursor()
        c.execute(query)
        db.commit()
        c.close()

    @cell_magic
    def logit(self, line, cell):
        """Log the execution time and file size in a sqlite database

        %%logit testid, filename [, sql_type]

        """
        user_name = self.shell.user_ns['user_name']
    	extra = None
    	sql_type = None
        
        ## Extracting the testid and filename
        inputs = line.replace(' ','').split(',')
        if len(inputs) == 2:
        	testid, filename = inputs
        elif len(inputs) == 3:
        	testid, filename, extra = inputs

	        if extra == 'sql_type':
	        	## Get the sql_type from the shell and add it to the testid
	        	sql_type = self.shell.user_ns['sql_type']
	        	testid += '_' + sql_type
	        else: 
	        	testid += '_' + extra
        
        ## Current time
        ctime = time.strftime("%y-%m-%d %H:%M:%S", time.localtime())
        ns = {}
        t0 = clock()
        ## Execute the cell content
        exec(cell, self.shell.user_ns, ns)
        tc = clock() - t0
        
        if sql_type == 'mysql':
        	filesize = -1
        else:
	        if os.path.exists(self.file_name):
	            filesize = os.path.getsize(filename)/1024.**2
	        else:
	            filesize = -1

        ## Print the valuesi
        print testid,':'
        print ctime
        print 'File size:', filesize, 'MB'
        print 'Creation time:', tc, 'sec'

        ## Add the values to the log database
        self.execute("INSERT INTO %s VALUES ('%s', '%s', '%s', '%s', '%s')"%
                   (self.table_name, user_name, ctime, testid, filesize, tc))

        ## Adding the result of the cell back to the shell user_ns
        for k,v in ns.iteritems():
        	self.shell.user_ns[k] = v

def plot_stats():
	"""Plot the statistics"""
	db = sqlite3.connect('sqlite_logger.db')
	df = pd.io.sql.frame_query('SELECT * FROM logger', db)
	df.groupby('testid').mean().plot(subplots=True,kind='bar')
	return df

def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(LogItMagic)

