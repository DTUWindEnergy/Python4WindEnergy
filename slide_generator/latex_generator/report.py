from __future__ import unicode_literals
import commands
import re

tag_dic = {
    'end*':'\\end{itemize}',
    'begin*':'\\begin{itemize}',
    'end-':'\\end{itemize}',
    'begin-':'\\begin{itemize}',
    'begin+':'\\begin{block}',
    'end+':'\\end{block}'
}

def md2tex(instr):
    """ Detect itemize in a markdown way.
    * - indicate an item
    + indicate a block
    """
    outstr = ""
    dic={}
    for l in instr.split('\n'):
        sps = re.findall('^\s*[*+-]',l)
        #print sps
        if len(sps)>0:
            sp = sps[0]
            dk = dic.keys()
            lens = map(len, dk)
            z1 = zip(lens, dk)
            z1.sort(key = lambda t: t[0], reverse=True)
            #print dic, z1            
            for le, i in z1:
                if len(i) > len(sp):
                    outstr += i[:-1] + tag_dic['end'+i[-1]] + '\n'
                    dic.pop(i)
            if sp in dic and (sp[-1] == '*' or sp[-1] == '-'):
                outstr += sp[:-1] + '  \\item ' + l[len(sp):] + '\n'
                dic[sp] += 1
            else:
                dic[sp] = 0
                if sp[-1] == '*' or sp[-1] == '-':
                    outstr += sp[:-1] + tag_dic['begin'+sp[-1]] + '\n'  
                    outstr += sp[:-1] + '  \\item ' + l[len(sp):] + '\n'
                if sp[-1] == '+':
                    outstr += sp[:-1] + tag_dic['begin'+sp[-1]] + '{' + l[len(sp):] + '}\n'                    
        else:
            dk = dic.keys()
            lens = map(len, dk)
            z1 = zip(lens, dk)
            z1.sort(key = lambda t: t[0], reverse=True)
            #print dic, z1
            for le, i in z1:
                if len(i) > len(re.findall('^\s*',l)[0]):
                    outstr += i[:-1] + tag_dic['end'+i[-1]] + '\n'
                    dic.pop(i)
            outstr += l + '\n'
    return outstr

def formi(input_string, dico):
    """
    Parsing function. Find all the #tags# in the string and
    replace them by the equivalent key in the dico.
    Replace the markdown keys by latex equivalent (using md2tex function).
    return the modified string.
    
    Tag pattern: any string composed of characters underscores and numbers surrounded by #
    Example: 
    - OK:  #resolution#, #Resolution_min1#
    - NOT OK: #text with spaces#
              #text with a
               return character \n
              #
              #text with those characters 

    """
    string = tostr(input_string)
    tag_pattern = '#[a-z_A-Z_0-9]*#'
    tag_list = re.findall(tag_pattern, string)
    for t in tag_list:
        key = t.split('#')[1]
        if key in dico:
        #print key + "=" + tostr(dico[key])
# This bugs with \begin \b chars!        
#        string = re.sub(t, unicode(dico[key]), string)
            if isinstance(dico[key], list):
                value = ''.join([tostr(i) for i in dico[key]])
            else:
                value = tostr(dico[key])
            string = string.replace(t, tostr(value))
        else:
            string = string.replace(t, '----'+key.upper()+'----')
    return md2tex(string)


def tostr(input_string):
    """ Change a list of strings into a multiline string """
    if isinstance(input_string, list):
        return '\n'.join([tostr(i) for i in input_string])
    else: 
        return str(input_string)        


def load_tostr(filename):
    with open(filename, 'r') as f: 
        return f.read()

def write_tostr(filename, string):
    with open(filename, 'w') as f: 
        f.write(string)

class latex_element(object):
    template = "#doc_main#"
    doc_main = []

    def __init__(self, doc_main= [], **kwargs):
        #print 'init', self.__class__.__name__
        ### Fill up the frame with the parameters
        if not isinstance(doc_main, list):
            self.doc_main = [doc_main]
        else:
            self.doc_main = doc_main[:]
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        #print self.doc_main

    def build_dic(self):
        dic = self.__dict__
        for k in dir(self):
            if k not in dic and k[:2] != '__':
                dic[k] = getattr(self, k)
        return dic

    def formi(self, string):
        return formi(string, self.build_dic(self.__class__))        
            
    def __str__(self):
        """
        Transform the object into a string. It also remplaces the #tags# 
        using the relevant object 
        """
        return formi(self.template, self.build_dic())            
    
    def add(self, string, **kwargs):
        """ Add a string to the doc_main.
        usage:
        rep.add(my_string, format1=str, format2=str...).
        """
        if kwargs:
            self.doc_main.append(string.format(**kwargs))
        else:
            self.doc_main.append(tostr(string))
        
    def addl(self, string):
        """ Add a line """
        self.add(string)
        self.endl()
        
    def endl(self):
        """ Add a end of line char"""
        self.doc_main.append('\n')
        
    def fig(self, path, label=None, width='9cm', caption=None):
        """ Add a figure """
        self.begin('figure')
        self.begin('center')
        self.addl('   \\includegraphics[width=' + width + ']{' + path + '}')
        if label:
            self.label(label)
        if caption:
            self.caption(caption)
        self.end('center')
        self.end('figure')

    def label(self, string):
        """ Add a label """
        self.addl("\\label{"+ string +"}")

    def caption(self, string):
        """ Add a caption"""
        self.addl("\\caption{"+ string +"}")
        
    def begin(self, string):
        self.addl('\\begin{' + string + '}')
        
    def end(self, string):
        self.addl('\\end{' + string + '}')
                        
    def section(self, long_name, short_name='', label=None):
        """
        Add a section equation
        """
        if short_name == '':
            short_name = long_name

        self.endl()
        #self.add("\Section["+short_name+"]{"+long_name+"}")
        self.add("\\section{"+long_name+"}")
        if label:
            self.label(label)
        self.endl()

    def subsection(self, long_name, short_name='', label=None):
        """
        Add a section equation
        """
        if short_name == '':
            short_name = long_name

        self.endl()
        #self.add("\Subsection["+short_name+"]{"+long_name+"}")
        self.add("\\subsection{"+long_name+"}")
        if label:
            self.label(label)
        self.endl()        

    def eq(self, string, label=None):
        """
        Add an equation
        """
        self.begin('equation')
        self.addl(string)
        if label:
            self.label(label)
        self.end('equation')

    def fig(self, filename, width='\\textwidth'):
        self.addl('\\begin{center}')
        self.addl('\\includegraphics[width='+width+']{'+filename+'}')
        self.addl('\\end{center}')
            

class report(latex_element):
    """
    Class to create a latex document.

    example:
    ---------
    rep = report()
    rep.section('Introduction')
    rep.add('hello.')
    rep.add(\""" EllipSys has run within {minutes} minutes over {ncpu}
    CPUs using the server called {srvname}.
    \""", minutes=10.0, srvname=inp['servername'], ncpu=72)
    rep.fig(inp['surf01.grd.png'], caption='This is fabulous!', label='fig:fabfig')
    rep.eq(r'x^2 = \int_a^b \ln{x} d x', label='eq:crazy_eq')
    rep.addl(r'\subsection{My section}')
    rep.addl(r'Look at Eq.\ref{eq:crazy_eq} and Fig.\ref{fig:fabfig} if you are not convinced.')
    """

    template_filename = 'template/template_simple_article.tex'

    template = ""

    def __init__(self, tex_filename='report.tex', **kwargs):
        super(report, self).__init__(**kwargs)
        self.template = load_tostr(self.template_filename)        
        self.tex_filename = tex_filename
        self.pdf_filename = tex_filename[:-3] + 'pdf'
      
    def save(self):
        write_tostr(self.tex_filename, tostr(self))
            
    def compile(self):
        self.save()
        for i in range(3):
            # commands.getoutput('xterm -e pdflatex ' + self.tex_filename)
            commands.getoutput('pdflatex ' + self.tex_filename)
            #commands.getoutput('open '+self.pdf_filename)
    

def cfig(filename, width='\\textwidth'):
    return centered(fig(filename, width=width))

def fig(filename, width='\\textwidth'):
    return '\\includegraphics[width='+width+']{'+filename+'}'



class table(latex_element):
    template =  """
\\begin{tabular}{#alignement#}
\\hline
#doc_main#
\\end{tabular}
"""
    def __init__(self, matrix, **kwargs):
        self.alignement = None
        self.ylabel = None
        super(table, self).__init__(**kwargs)
        ncol = matrix.shape[1]
        self.doc_main = []
        if self.ylabel:
            ncol += 1
            y0 = ' & '
            self.ylabel = [y + ' & ' for y in self.ylabel]
        else: 
            y0 = ''
            self.ylabel = ['']*matrix.shape[0]
        if self.xlabel:
            self.add(y0 + ' & '.join([str(e) for e in self.xlabel]))
            self.addl('\\\\ \\hline ')
        if not self.alignement:
            self.alignement = '| ' +  ' | '.join(['c' for i in range(ncol)]) + ' |'
        for r in range(matrix.shape[0]):
            self.add(self.ylabel[r] + ' & '.join([str(e) for e in matrix[r,:]]))
            self.addl('\\\\ \\hline ')



def itemize(items, order=[]):
    """ Generate the items, the order is not compulsary
    ex: 
    itemize(['item1', 'item2'], ['1-','2-']):
    \begin{itemize}
    \item<1-> item1
    \item<2-> item2
    \end{itemize}

    itemize(['item1', 'item2']):
    \begin{itemize}
    \item item1
    \item item2
    \end{itemize}
    """
    if len(order)>0:
        return(env_latex('itemize', ['\\item<%s> %s'%(o, tostr(i)) for i, o in zip(items, order)]))
    else:
        return(env_latex('itemize', ['\\item %s'%(tostr(i)) for i in items]))

def env_latex(env, string):
    """ Create an environment.
    Example:
    print env_latex('center', [text','to','center'])
    
    \begin{center}
    text
    to
    center
    \end{center}
    """
    return '\\begin{' + env + '}' + '\n' + tostr(string) + '\n' + '\\end{' + env + '}' + '\n'

eq = lambda string: env_latex('equation', string)
centered = lambda string: env_latex('center', string)
ceq = lambda string: centered(eq(string))
          