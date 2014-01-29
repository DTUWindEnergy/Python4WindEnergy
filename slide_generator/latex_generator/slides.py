from report import *

class frame(latex_element):
    template = """%%%%%%%%%%%%%%%% FRAME #nb#: #title# %%%%%%%%%%%%%%%%%%%
\\frame{
\\frametitle{#title#}
#doc_main#
}"""
    title = ''
    nb = 1


class block(latex_element):
	template = """%%% BLOCK #order#: #title#  %%%%
\\begin{block}<#order#>{#title#}
#doc_main#
\\end{block}
"""
	title=''
	order='1-'

class minipage(latex_element):
    template="""
 \\begin{minipage}{#ratio#\\textwidth}
 #doc_main#
\\end{minipage}
"""
    ratio='0.49'

def anim(filename, ratio, frames):
    return formi("""
\\animategraphics[controls,autoplay,loop,width=#ratio#\\textwidth]{#nframes#}{#filename#}{#f1#}{#f2#}
""", dict(filename=filename, ratio=ratio, f1=frames[0], f2=frames[1], nframes=frames[1]-frames[0]))

class slides(report):  
    template_filename = 'template/slides_header_template.tex'
           
    def __init__(self, **kwargs):
        super(slides, self).__init__(**kwargs)
        self.doc_main = []
           
    def f(self, title, doc):
        """ Add a frame to the slideshow"""
        self.addl(frame(doc_main=doc, title=title))

    # def outline(self, title='Outline', section=None):
    #     if section:
    #         self.f(title, '\\tableofcontents[%s]'%(section))
    #     else:
    #         self.f(title, '\\tableofcontents')

    # def section(self, long_name, short_name='', label=None):
    #     super(slides, self).section(long_name, short_name, label)
    #     self.outline(section=long_name)

class columns(latex_element):
    template = """
\\begin{columns}[#position#]
#doc_main#
\\end{columns}    
"""
    position = 'c'
    c = []
    
    def __init__(self, c=[], widths=[], **kwargs):
    	if len(c)>0:
    		self.c = []
    		for i, e in enumerate(c):
  				if len(widths)>0:
  					w = widths[i]
  				else:
  					w = '%f\\textwidth'%(1.0/len(c) - 0.01)
  				self.c.append(_column(e, width=w, position=self.position))
    	else:
    		self.c = []
	        for w in widths:
	            self.c.append(column(width=w))
        super(columns, self).__init__(**kwargs)
            
    def __str__(self):
        self.doc_main = [''.join([tostr(c) for c in self.c])]
        return formi(self.template, self.build_dic())
        
    
    
class _column(latex_element):
    template = """
\\begin{column}[#position#]{#width#}
#doc_main#
\\end{column}    
"""
    width = '4.5cm'
    position = 'c'


