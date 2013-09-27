%---------------------------------------------------------------------------
%Please  be  aware that the use of this LaTeX class file is governed by the
%following conditions:
%
% based on the original LaTeX ARTICLE DOCUMENT STYLE
% Copyright (C) 1988, 1989 by Leslie Lamport
%
% Copyright (c) 2010 John Wiley & Sons, Ltd, The Atrium, Southern Gate, Chichester,
% West Sussex, PO19 8SQ UK.   All rights reserved.
%
%Rules of Use
%
%% You are NOT ALLOWED to change this file.
%
%
%This class file is made available for use by authors who wish to prepare an
%article for publication in
%WIND ENERGY
%published by John Wiley & Sons Ltd. The user may not exploit any part of
%the class file commercially.
%
%This class file is provided on an `as is'  basis, without warranties of any
%kind, either expressed or implied, including but not limited to warranties of
%title, or  implied warranties of merchantablility or fitness for  a
%particular purpose. There will be no duty on the author[s] of the software
%or John Wiley & Sons Ltd to correct any errors or defects in the software.
%Any statutory rights you may have remain unaffected by your acceptance of
%these rules of use.
%---------------------------------------------------------------------------
%
% Created by Alistair Smith, Sunrise Setting Ltd, 17 June 2010
%
% weauth.cls --- For Wind Energ.

\def\update{2010/06/17 v1.00}

\newcommand{\journalname}{WIND ENERGY}
\newcommand{\journalnamelc}{Wind Energy}
\newcommand{\journalabb}{Wind Energ.}
\newcommand{\journalclass}{weauth.cls}
\newcommand{\journalclassshort}{weauth}
\newcommand{\DOI}{we}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{weauth}[\update\ \journalclass]

%\newcommand\hmmax{0}

\newif\if@timesfont
\DeclareOption{times}{%
\@timesfonttrue}

\newif\if@doublespace
\DeclareOption{doublespace}{%
\@doublespacetrue}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions
\LoadClass{article}
\if@timesfont
\RequirePackage{times}
\fi
\if@doublespace
\RequirePackage[onehalfspacing]{setspace}
\fi

\RequirePackage{graphicx}
\RequirePackage{pifont,latexsym,ifthen,rotating,calc,textcase,booktabs,color}
\RequirePackage{amsfonts,amssymb,amsbsy,amsmath,amsthm}
%\RequirePackage{bm}
\RequirePackage[errorshow]{tracefnt}

\@twosidetrue
\flushbottom
\frenchspacing

\textwidth 36.5pc
\textheight 641pt
%\setlength\columnsep{24pt}

%Trim sizes
\setlength\voffset{-1in}
\setlength\hoffset{-1in}
\topmargin -1mm
\setlength\oddsidemargin{33mm}%back margin on odd pages
\setlength\evensidemargin{33mm}%fore margin on even pages
\setlength\paperwidth{210mm}
\setlength\paperheight{276mm}
%Needed to set PDF page size
\special{papersize=210mm,276mm}

\parskip \z@
\parindent 1em
\headheight 50pt
\headsep    20pt 
\footskip 28pt 

\hyphenpenalty=1000
\pretolerance=8000
\tolerance=9500
\hbadness=8000
\vbadness=9000
\displaywidowpenalty=0
\clubpenalty=10000
\widowpenalty=10000
\lefthyphenmin=3%
\righthyphenmin=3%
\brokenpenalty=10000%

\thinmuskip = 3mu
\medmuskip = 4mu
\thickmuskip = 5mu

\setcounter{topnumber}{10}
\def\topfraction{1}
\setcounter{bottomnumber}{10}
\def\bottomfraction{0.8}
\setcounter{totalnumber}{10}
\def\textfraction{0}
\renewcommand{\floatpagefraction}{0.95}
\setcounter{dbltopnumber}{10}
\renewcommand{\dblfloatpagefraction}{0.95}
\renewcommand{\dbltopfraction}{1}

\renewcommand\normalsize{%
   \@setfontsize\normalsize\@ixpt{11pt}%
   \abovedisplayskip 10\p@ \@plus2\p@ \@minus5\p@
   \abovedisplayshortskip \z@ \@plus3\p@
   \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 6\p@ \@plus2\p@ \@minus2\p@
               \parsep 3\p@ \@plus2\p@ \@minus\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}
\normalsize

\renewcommand{\small}{\fontsize{7.5pt}{9.5pt}\selectfont}
\renewcommand{\footnotesize}{\fontsize{6.5pt}{8.5pt}\selectfont}
\renewcommand\scriptsize{\@setfontsize\scriptsize\@viipt{9.5}}
\renewcommand\tiny{\@setfontsize\tiny\@vpt\@viipt}
\renewcommand\large{\@setfontsize\large\@xipt{13}}
\renewcommand\Large{\@setfontsize\Large\@xivpt{18}}
\renewcommand\LARGE{\@setfontsize\LARGE\@xviipt{22}}
\renewcommand\huge{\fontsize{22pt}{24pt}\selectfont}
\renewcommand\Huge{\@setfontsize\Huge\@xxvpt{30}}

\newcommand{\numsize}{\fontsize{8pt}{10pt}\selectfont}
\newcommand{\titlesize}{\fontsize{15pt}{18pt}\selectfont}
\newcommand{\authorsize}{\fontsize{10pt}{12pt}\selectfont}
\newcommand{\absize}{\fontsize{11.5pt}{14pt}\selectfont}

\newbox\absbox
\def\abstract{\lrbox\absbox\minipage{\textwidth}%
  \normalfont%
  {\noindent\sffamily\bfseries\absize{ABSTRACT}}\par\vspace{10pt}\normalsize%
  }
\def\endabstract{\copyrightline\endminipage\endlrbox}

\def\keywords#1{%
  \gdef\@keywords{\small{\bfseries\sffamily KEYWORDS}\par\noindent\raggedright\noindent\sffamily{#1}}}
\let\@keywords\@empty

\skip\footins 22pt plus  8pt
%\gdef\footnoterule{}
\def\footnoterule{\kern-3\p@
  \hrule \@width 60pt \kern 2.6\p@}

\renewcommand{\thefootnote}{\fnsymbol{footnote}}
\long\def\@makefntext#1{\parindent 1em%
\noindent{$\m@th^{\@thefnmark}$}#1}

\def\corraddr#1{%
  \gdef\@corraddr{\small{\bfseries\sffamily Correspondence}\par\noindent\raggedright\noindent\sffamily{#1}}%
    }
\let\@corraddr\@empty
\def\corrauth{\footnotemark[1]}

\def\address#1{%
  \gdef\@address{{\small\sffamily #1}}}
\let\@address\@empty

\def\cgsn#1#2{%
\gdef\@cgsn{%
\small\noindent{\raggedright\bfseries\sffamily Contract/grant sponsor}\par\raggedright\noindent\sffamily{#1}\par\vspace{11pt}%
\small\noindent{\raggedright\bfseries\sffamily Contract/grant number}\par\raggedright\noindent\sffamily{#2}\par\vspace{5pt}}}

\def\cgs#1{%
\gdef\@cgs{%
\small\noindent{\raggedright\bfseries\sffamily Contract/grant sponsor}\par\raggedright\noindent\sffamily{#1}\par\vspace{5pt}}}

\let\@cgsn\@empty
\let\@cgs\@empty

\def\articletype#1{%
\gdef\@articletype{\authorsize\sffamily\noindent{#1}}}
\let\@articletype\@empty

\def\affilnum#1{${}^{#1}$}
\def\affil#1{${}^{#1}$}
\def\comma{${}^{\text{,}}$}

\renewcommand\maketitle{\par
  \begingroup
     \if@twocolumn
      \ifnum \col@number=\@ne
        \@maketitle
      \else
        \twocolumn[\@maketitle]%
       \fi
    \else
      \newpage
      \global\@topnum\z@   % Prevents figures from going at top of page.
      \@maketitle
    \fi
    \thispagestyle{title}\label{FirstPage}%\@corraddr\@cgs\@cgsn
  \endgroup
  %\setcounter{footnote}{0}%
  \global\let\address\relax
  \global\let\corraddr\relax
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\articletype\relax
  \global\let\@maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\@articletype\@empty
  \global\let\@address\@empty
  \global\let\@corraddr\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
}
\def\@maketitle{\vspace*{4pt}%
\null%
%\begin{center}
\@articletype\par
\vspace{9pt}
    {\raggedright\titlesize\sffamily\bfseries\noindent\@title \par}%
    \vskip 1.5em %
    \vskip -8pt
    {\large
      \lineskip .5em%
      \authorsize\sffamily\noindent\@author
      \par}%
      \vskip 7pt
{\small
      \lineskip .5em%
      %
        {\raggedright\sffamily\noindent\@address}
      \par}%
%\end{center}    
    \vskip 34pt%
    {\noindent\usebox\absbox\par}
      {\vspace{9pt}%
      {\noindent\@keywords}\par}
      {\vspace{5pt}%
      {\noindent\@corraddr}\par}
      {\vspace{5pt}%
      {\noindent\@cgs}}%
      {\noindent\@cgsn}%
      {% 
      {\noindent\small\sffamily Received \dots}\par}
      \vspace{12pt}
        \par%
  }
 
\def\startpage{\pageref{FirstPage}}
\def\endpage{\pageref{LastPage}}
\def\volumeyear{0000}
\def\volumenumber{00}

\gdef\copyrightline{Copyright \copyright\ \volumeyear\ John Wiley \& Sons, Ltd.}
\gdef\footercopyrightline{\copyright\ \volumeyear\ John Wiley \& Sons, Ltd.}
\def\runningheads#1#2{\markboth{{#1}}{{#2}}}

\def\ps@title{%
\def\@oddhead{%
\parbox[t]{\textwidth}{%
\mbox{}\hfill\begin{tabular}[t]{@{}r@{}}%
{\scriptsize\sffamily\journalname}\\[-1pt]
{\scriptsize\sffamily\emph{\journalabb} \volumeyear; \textbf{\volumenumber}:\startpage--\endpage}\\[-1pt]
{\scriptsize\sffamily DOI: 10.1002/\DOI}
\end{tabular}}}%
\let\@evenhead\@oddhead
\def\@oddfoot{\parbox[t]{\textwidth}{%
{\footnotesize\sffamily\copyrightline\hfill\numsize\textbf{\thepage}\\
\footnotesize\sffamily\textit{Prepared using \textsf{\journalclass} [Version: \update]\hfill}%
}}}
\let\@evenfoot\@oddfoot}

\def\ps@wpage{%
\let\@mkboth\@gobbletwo
\def\@evenhead{\small\sffamily{\rightmark}\hfill{\leftmark}}
\def\@oddhead{\small\sffamily{\leftmark}\hfill{\rightmark}}
\def\@evenfoot{\parbox[t]{\textwidth}{\sffamily\numsize\textbf{\thepage}\hfill%
\footnotesize \emph{\journalabb\ }\volumeyear; \textbf{\volumenumber}:\startpage--\endpage\ \footercopyrightline\\ %
\mbox{}\hfill DOI: 10.1002/\DOI\\
\mbox{}\hfill\footnotesize\textit{Prepared using \textsf{\journalclass}}}}
\def\@oddfoot{\parbox[t]{\textwidth}{\sffamily\footnotesize \emph{\journalabb\ }\volumeyear; \textbf{\volumenumber}:\startpage--\endpage\ \footercopyrightline%
\hfill\numsize\textbf{\thepage}\\%
\footnotesize DOI: 10.1002/\DOI\\
\textit{Prepared using \textsf{\journalclass}}}}%
}

\renewcommand{\@seccntformat}[1]{{\csname the#1\endcsname.}\hspace{0.5em}}

\newdimen\@bls                              
\@bls=\baselineskip

\renewcommand\section{\@startsection {section}{1}{\z@}%
                                   {2\@bls  plus .3\@bls minus .1\@bls}%
                                   {1\@bls\@afterindentfalse}%
                                   {\sffamily\bfseries\large\raggedright\protect\MakeTextUppercase}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                     {\@bls plus .3\@bls minus .1\@bls}%
                                     {6pt\@afterindentfalse}%
                                     {\sffamily\bfseries\normalsize\raggedright}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                     {\@bls plus .2\@bls}%
                                     {0.01pt}%
                                     {\sffamily\bfseries\normalsize\raggedright}}

\def\enumerate{\ifnum \@enumdepth >3 \@toodeep\else
      \advance\@enumdepth \@ne
      \edef\@enumctr{enum\romannumeral\the\@enumdepth}\list
      {\csname label\@enumctr\endcsname}{\usecounter
        {\@enumctr}\itemsep 0pt\parsep 0pt
         \def\makelabel##1{\hss\llap{##1}}}\fi}

\let\endenumerate =\endlist

\def\itemize{\ifnum \@itemdepth >3 \@toodeep\else \advance\@itemdepth \@ne
\edef\@itemitem{labelitem\romannumeral\the\@itemdepth}%
\list{\csname\@itemitem\endcsname}{\itemsep 0pt\parsep 0pt
\def\makelabel##1{\hss\llap{##1}}}\fi}

\let\enditemize =\endlist

\renewcommand{\thetable}{\Roman{table}}

\usepackage{caption}
\DeclareCaptionLabelSeparator{jwperiod}{.\hspace*{0.5ex}}
\captionsetup[figure]{font=small,labelfont={sf,bf},textfont=sf,labelsep=jwperiod,justification=centerlast,singlelinecheck=true}
\captionsetup[table]{font=small,labelfont={sf,bf},textfont=sf,labelsep=jwperiod,justification=centerlast,singlelinecheck=true}

\def\thmhead@plain#1#2#3{%
  \thmname{#1}\thmnumber{\@ifnotempty{#1}{ }{#2}}%
  \thmnote{ {\the\thm@notefont(#3)}}}

\newtheoremstyle{wiley}
{6pt plus 2pt minus 2pt}% space above
{6pt plus 2pt minus 2pt}% space below
{}% Body font
{}% Indent amount
{\itshape}% Theorem head font
{}% Punctuation after theorem head
{\newline}% Space after theorem head
{}% Theorem head spec

\renewenvironment{proof}[1][\proofname]{\par
  \pushQED{\qed}%
  \normalfont \topsep6\p@\@plus6\p@\relax
  \trivlist
  \item[\hskip\labelsep
        \itshape
    #1\@addpunct{}]\mbox{}\newline\ignorespaces
}{%
  \popQED\endtrivlist\@endpefalse
}

\theoremstyle{wiley}

\def\ack{\section*{ACKNOWLEDGEMENT}}
\def\acks{\section*{ACKNOWLEDGEMENTS}}

\renewcommand\refname{REFERENCES}

\renewenvironment{thebibliography}[1]{%
\section*{\refname}
\list{{\arabic{enumi}}}{\def\makelabel##1{\hss{##1.}}\topsep=0\p@\parsep=0\p@
\partopsep=0\p@\itemsep=0\p@
\labelsep=1ex\itemindent=0\p@
\settowidth\labelwidth{\normalsize[#1]}%
\leftmargin\labelwidth
\advance\leftmargin\labelsep
\advance\leftmargin -\itemindent
\usecounter{enumi}}\normalsize
\def\newblock{\ }
\sloppy\clubpenalty4000\widowpenalty4000
\sfcode`\.=1000\relax}{\endlist}

%\def\biog{\section*{Author's Biography}\small}
%\def\biogs{\section*{Authors' Biographies}\small}

\AtEndDocument{%
\label{LastPage}}

\hyphenation{com-mu-ni-ca-tions}

\pagestyle{wpage}
\normalsize
\sloppy
