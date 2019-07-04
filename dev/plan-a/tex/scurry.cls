
% purpose:  LaTeX class definition for Hurry Scurry documents
% author:   albinre@kth.se
% date:     2016-11-18

\ProvidesClass{scurry}[2016/11/18 Hurry Scurry]
\NeedsTeXFormat{LaTeX2e}
\LoadClass[]{article}

% using geometry driver xetex
\usepackage[a6paper]{geometry}
\geometry{
    bottom=0em
}

\usepackage{scrextend}
\usepackage{tikz}

% color definitions

\usepackage{xcolor}

\definecolor{white}{RGB}{255,255,255}
\definecolor{lightgrey}{RGB}{211,211,211}
\definecolor{grey}{RGB}{128,128,128}
\definecolor{black}{RGB}{0,0,0}

\colorlet{title_bgcolor}{black}
\colorlet{spine_bgcolor}{grey}

\colorlet{title_fontcolor}{white}
\colorlet{spine_fontcolor}{white}
\colorlet{heading_fontcolor}{black}
\colorlet{textblock_fontcolor}{black}
\colorlet{id_fontcolor}{lightgrey}

% font definitions
% all used fonts should be located at ./fonts/

\usepackage[quiet]{fontspec}

\newfontfamily\titlefont[Path=fonts/]{SF-Distant-Galaxy.ttf}
\newfontfamily\spinefont[Path=fonts/]{nulshock-bd.ttf}

\newfontfamily\headingfont[Path=fonts/]{texgyreheros-bold.otf} %{Rajdhani-SemiBold.ttf}
\newfontfamily\textblockfont[Path=fonts/]{Rajdhani-SemiBold.ttf} %{texgyreheros-regular.otf}


% command for entering a new headning

\newcommand{\heading}[1]{
    \begin{addmargin}[7mm]{-2mm}
        \fontsize{8pt}{8pt}
        \color{heading_fontcolor}
        \headingfont
        {#1}
    \end{addmargin}
}

% command for entering a new text block

\newcommand{\textblock}[1]{
    \begin{addmargin}[7mm]{-2mm}
        \fontsize{10pt}{10pt}
        \color{textblock_fontcolor}
        \textblockfont
        {#1}
    \end{addmargin}
    \vspace{1em}
}

% command for entering the document's ID

\newcommand{\id}[1]{
    \begin{tikzpicture}[remember picture,overlay]
        \node [anchor=west] (name) at ([shift={(-35mm, -8mm)}] current page.north) {
            \fontsize{8pt}{8pt}
            \color{id_fontcolor}
            \textblockfont
            {#1}
        };
    \end{tikzpicture}
}

% command for adding the document's title bar

\newcommand{\titlebar}[1]{
    \begin{tikzpicture}[remember picture,overlay]
        \node [rectangle, fill=title_bgcolor, anchor=north, minimum width=80mm, minimum height=10mm] (box) at ([shift={(7mm, -10mm)}] current page.north){};
        \node [anchor=center] (name) at (box) {
            \fontsize{12pt}{12pt}
            \color{title_fontcolor}
            \titlefont
            {#1}
        };
    \end{tikzpicture}
    \vspace{1em}
}

% command for adding the document's spine

\usepackage{rotating}

\newcommand{\spine}[1]{
    \begin{tikzpicture}[remember picture,overlay]
        \node [rectangle, fill=spine_bgcolor, anchor=east, minimum width=10mm, minimum height=140mm] (box) at ([shift={(-90mm, 0mm)}]current page.east){};
        \node [anchor=center] (name) at (box) {
            \fontsize{20pt}{72pt}
            \color{spine_fontcolor}
            \spinefont
            \begin{turn}{90}
                {#1}
            \end{turn}
        };
    \end{tikzpicture}
}

% command for adding the document's rebel logo

\usepackage{graphicx}

\newcommand{\logo}[0]{
    \begin{tikzpicture}[overlay,remember picture]
        \node[anchor=north west] at ([shift={(1.3mm,-6.5mm)}]current page.north west){
            \includegraphics[width=15mm, height= 15mm]{rebel.png}
        };
    \end{tikzpicture}
}
