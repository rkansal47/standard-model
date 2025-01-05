from bs4 import BeautifulSoup
from pathlib import Path
import re


headerlinks = [
    {
        "href": "https://github.com/rkansal47/standard-model",
        "src": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        "alt": "GitHub Repository",
        "style": "width: 32px; height: 32px;",
        "astyle": "top: 10px; right: 44px;",
        "target": "_blank",
    },
    {
        "href": "https://github.com/rkansal47/standard-model/blob/gh-pages/standard-model.pdf?raw=true",
        "src": "assets/download.png",
        "alt": "Download PDF",
        "style": "width: 25px; height: 25px;",
        "astyle": "top: 13px; right: 85px;",
        "target": "_blank",
    },
    {
        "href": "https://www.raghavkansal.com",
        "src": "assets/icon.png",
        "alt": "My website",
        "style": "width: 26px; height: 26px;",
        "astyle": "top: 13px; right: 12px;",
        "target": "_blank",
    },
    {
        "href": "#mainToc",
        "src": "assets/sidebar.png",
        "alt": "Table of Contents",
        "style": "width: 32px; height: 32px;",
        "astyle": "top: 11px; left: 150px;",
        "astylemain": "top: 11px; left: 14px;",  # closer to edge for main.html
        "class": "smallscreenhide",
        "target": "_self",  # same tab
    },
]


def edit_file(file_path: Path, edit_function: callable, **kwargs):
    with file_path.open("r") as file:
        soup = BeautifulSoup(file, "html.parser")
        edit_function(soup, **kwargs)

    with file_path.open("w") as file:
        file.write(str(soup))


def edit_main(soup: BeautifulSoup):
    # move the title and abstract inside the main content
    maketitle_div = soup.find("div", {"class": "maketitle"})
    date_div = maketitle_div.find("div", {"class": "date"})  # remove the date
    date_div.decompose()

    abstract_section = soup.find("section", {"class": "abstract"})
    main_content_main = soup.find("main", {"class": "main-content"})
    main_content_main.insert(0, maketitle_div)
    main_content_main.insert(1, abstract_section)

    # Remove the weird default "Next" link
    last_paragraph = main_content_main.find_all("p")[-1]
    last_paragraph.decompose()

    # Add the same type of "Next" as in all the other pages:
    next_nav = soup.new_tag("nav")
    next_nav["class"] = "crosslinks-bottom"
    next_nav.append(soup.new_tag("a", href="contentsname.html"))
    next_nav.a.string = "⭢"
    main_content_main.insert(2, next_nav)


def edit_header(soup: BeautifulSoup, file_name: str):
    main_content_main = soup.find("main", {"class": "main-content"})
    if not main_content_main:
        return

    for i, link in enumerate(headerlinks):
        header_link = soup.new_tag(
            "a",
            href=link["href"],
            **{
                "class": "header-link " + link.get("class", ""),
                "target": link["target"],
                "rel": "noopener noreferrer",
                "style": (
                    link["astyle"]
                    if not file_name == "main.html"
                    else link.get("astylemain", link["astyle"])
                ),
            },
        )
        header_img = soup.new_tag(
            "img",
            src=link["src"],
            alt=link["alt"],
            **{"class": "header-icon", "style": link["style"]},
        )
        header_link.append(header_img)
        main_content_main.insert(0, header_link)


def edit_footnotes(soup: BeautifulSoup):
    """Move footnotes inside the maincontent div and add a copyright footer"""
    main_content_main = soup.find("main", {"class": "main-content"})
    if not main_content_main:
        return

    footnotes_div = soup.find("div", {"class": "footnotes"})
    if footnotes_div:
        main_content_main.append(footnotes_div)

    footer_div = soup.new_tag("div", **{"class": "footer"})
    footer_p = soup.new_tag("p")
    footer_p.string = "Copyright © 2024 Raghav Kansal. All rights reserved."
    footer_div.append(footer_p)
    main_content_main.append(footer_div)


def edit_toc(soup: BeautifulSoup):
    """Add logo to the Table of Contents"""
    toc_nav = soup.find("nav", {"class": "TOC"})
    if toc_nav:
        main_toc_span = soup.new_tag("span", **{"class": "mainToc", "id": "mainToc"})
        main_toc_link = soup.new_tag("a", href="index.html")
        main_toc_img = soup.new_tag(
            "img", src="assets/logo.png", alt="Symmetries, QFT, & The Standard Model", width="100%"
        )
        main_toc_link.append(main_toc_img)
        main_toc_span.append(main_toc_link)
        toc_nav.insert(0, main_toc_span)


def regex_fixes(file: Path):
    with file.open("r") as f:
        content = f.read()

    # Apply regex to move <msub|...> tag outside of <menclose> tag
    content = re.sub(r"main.html", r"index.html", content)

    # Remove the weird invisible function character
    content = content.replace("⁡", "")

    with file.open("w") as f:
        f.write(content)


if __name__ == "__main__":
    outdir = Path("out")

    html_files = list(outdir.glob("*.html"))
    main_file = outdir / "main.html"

    # This has to be done first, otherwise the html parsing will be messed up
    for html_file in html_files:
        regex_fixes(html_file)

    # Edit the main content
    edit_file(main_file, edit_main)

    # Edit footnotes for all HTML files in the directory
    for html_file in html_files:
        file_name = html_file.name
        edit_file(html_file, edit_header, file_name=file_name)
        edit_file(html_file, edit_footnotes)
        edit_file(html_file, edit_toc)

    # Rename main.html to index.html
    main_file.rename(outdir / "index.html")
