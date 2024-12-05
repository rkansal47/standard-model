from bs4 import BeautifulSoup
from pathlib import Path
import re


def edit_file(file_path: Path, edit_function: callable):
    with file_path.open('r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        edit_function(soup)
    
    with file_path.open('w') as file:
        file.write(str(soup))


def edit_main(soup: BeautifulSoup):
    # move the title and abstract inside the main content
    maketitle_div = soup.find('div', {'class': 'maketitle'})
    date_div = maketitle_div.find('div', {'class': 'date'})  # remove the date
    date_div.decompose()
    
    abstract_section = soup.find('section', {'class': 'abstract'})
    main_content_main = soup.find('main', {'class': 'main-content'})
    main_content_main.insert(0, maketitle_div)
    main_content_main.insert(1, abstract_section)
    
    # Remove the weird default "Next" link
    last_paragraph = main_content_main.find_all('p')[-1]
    last_paragraph.decompose()
    
    # Add the same type of "Next" as in all the other pages:
    next_nav = soup.new_tag('nav')
    next_nav['class'] = 'crosslinks-bottom'
    next_nav.append(soup.new_tag('a', href='contentsname.html'))
    next_nav.a.string = 'Next'
    main_content_main.insert(2, next_nav)


def edit_footnotes(soup: BeautifulSoup):
    """Move footnotes inside the maincontent div and add a copyright footer"""
    main_content_main = soup.find('main', {'class': 'main-content'})
    if not main_content_main:
        return

    footnotes_div = soup.find('div', {'class': 'footnotes'})
    if footnotes_div:
        main_content_main.append(footnotes_div)
        
    footer_div = soup.new_tag('div', **{'class': 'footer'})
    footer_p = soup.new_tag('p')
    footer_p.string = 'Copyright © 2024 Raghav Kansal. All rights reserved.'
    footer_div.append(footer_p)
    main_content_main.append(footer_div)
    

def edit_toc(soup: BeautifulSoup):
    """Add logo to the Table of Contents"""
    toc_nav = soup.find('nav', {'class': 'TOC'})
    if toc_nav:
        main_toc_span = soup.new_tag('span', **{'class': 'mainToc'})
        main_toc_link = soup.new_tag('a', href='main.html')
        main_toc_img = soup.new_tag('img', src='logo.png', alt='Symmetries, QFT, & The Standard Model', width='100%')
        main_toc_link.append(main_toc_img)
        main_toc_span.append(main_toc_link)
        toc_nav.insert(0, main_toc_span)


def slashedsubscript_fix(file: Path):
    """Workaround for bug with MathML code for subscripts / superscripts with \cancel{}"""
    with file.open('r') as f:
        content = f.read()
    
    # Apply regex to move <msub|...> tag outside of <menclose> tag
    content = re.sub(r'<menclose notation="updiagonalstrike"><(msub|msup|msubsup)>', r'<\1><menclose notation="updiagonalstrike">', content)
    
    with file.open('w') as f:
        f.write(content)
        

if __name__ == "__main__":
    # Edit the main content
    edit_file(Path('main.html'), edit_main)
    
    # # Edit footnotes for all HTML files in the directory
    html_files = Path('.').glob('*.html')
    for html_file in html_files:
        edit_file(html_file, edit_footnotes)
        edit_file(html_file, edit_toc)
        # slashedsubscript_fix(html_file)
    
    # edit_file(Path("Electroweakinteractions.html"), edit_footnotes)