from bs4 import BeautifulSoup
from pathlib import Path

# Edit main.html
with Path('main.html').open('r') as file:
    soup = BeautifulSoup(file, 'html.parser')

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
    

with Path('main.html').open('w') as file:
    file.write(str(soup))