# Program reads Google Chrome bookmark html file (bookmarks_xx.xx.xxxx.html)
# and then generate Markdown format file with list of links (with description)

import glob
import re

def main():
# looking for bookmark files
    file_mask = "bookmarks_*.*.*.html"

    bookmark_files = glob.glob(file_mask)

    if not bookmark_files:
        print("files matching to the mask \"{mask}\" not found".format(mask=file_mask))
        exit = input("Press enter to exit...")
        return

# for found files
    for file in bookmark_files:
    
    # open
        html_file_body = open(file, encoding='utf-8').read()
    
    # parse: looking for links URLs and descriptions
        link_regex    = re.compile(r"<A HREF=\"(.+?)\".+>(.+)</A>")
        list_of_links = re.findall(link_regex, html_file_body)

    # generate data for Markdown file
        md_data={}

        domain_regex = r"http[s]?://(\S+?)/"

        for url, description in list_of_links:
            try:
                domain = re.match(domain_regex, url).group(1)
            except:
                print("something wrong with url:{url}".format(url=url))
                print("that url will be skipped")
                print()
                continue_execution = input("Press enter to continue...")
                continue

            if domain not in md_data:
                md_data[domain] = []

            md_data[domain].append((url,description))

    # prepare Markdown formatted text from data
        md_file_body = []

        md_title  = "# Bookmarks: {count} links in total\n".format(count = len(list_of_links))
        md_file_body.append(md_title)

        # hack: push habrahabr and geektimes to top
        for domain in 'habrahabr.ru', 'geektimes.ru':
            md_file_body.append(bake_domain_links_to_md(md_data, domain))
            del md_data[domain]
        
        for domain in md_data.keys():
            md_file_body.append(bake_domain_links_to_md(md_data, domain))

        md_file_body = '\n\n'.join(md_file_body)

    # save output Markdown file
        # "bookmarks_*.*.*.html"[:-5] -> "bookmarks_*.*.*"
        md_file = open(file[:-5]+".md", 'w', encoding='utf-8')
        md_file.write(md_file_body)


def bake_domain_links_to_md(md_data, domain):
    tmp = []

    md_header = "### {domain}".format(domain=domain)
    tmp.append(md_header)

    # just improves output result appearance
    md_data[domain].sort()

    for link in md_data[domain]:
        tmp.append("[{description}]({url})".format(description=link[1],
                                                   url        =link[0]))
    return '\n\n'.join(tmp)

# ----------------------------------------------------------------------------

if __name__ == '__main__':
    main()