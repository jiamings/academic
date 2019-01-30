import yaml
import datetime


def find_collaborator(colabs, name):
    for colab in colabs:
        if colab['name'] == name:
            return colab
        else:
            return None


def command(name, values):
    return '\\' + name + '{' + '}{'.join(values) + '}'


def href(url, text):
    return command('href', [url, text])


def textit(text):
    return command('textit', [text])


def create_cventry_publication(pub, colabs):
    authors = []
    for author in pub['authors']:
        colab = find_collaborator(colabs, author)
        if colab is not None:
            authors.append(href(colab['url'], colab['name']))
        else:
            authors.append(author)
    if 'url' in pub.keys() and len(pub['url']) > 0:
        paper = href(pub['url'], pub['name'])
    else:
        paper = pub['name']

    if 'workshops' in pub.keys() and len(pub['workshops']) > 0:
        workshops = 'Abridged in ' + ', '.join([textit(s) for s in pub['workshops']]) + '.'
    else:
        workshops = ''

    if 'date' in pub.keys():
        now = datetime.datetime.now()
        date = datetime.datetime.strptime(pub['date'], '%m/%d/%Y')
        if date < now:
            appear = 'In '
        else:
            appear = 'To appear in '
        date = date.strftime('%B %Y')
    else:
        appear = ''
        date = ''

    if 'conference' in pub.keys():
        conference = appear + ' ' + textit(pub['conference']) + '. '
        if 'additional' in pub.keys() and len(pub['additional']) > 0:
            conference += pub['additional'] + '.'
    else:
        conference = ''

    if 'locations' in pub.keys() and len(pub['locations']) > 0:
        locations = 'In ' + ', '.join([textit(s) for s in pub['locations']]) + '.'
    else:
        locations = ''

    return command('cventry', [
        '\\footnotesize ' + date,
        '\\bfseries ' + paper,
        '', '', '',
        '\\normalfont ' + ', '.join(authors) + '.\\\\' +
        '\\\\'.join([s for s in [conference, locations, workshops] if len(s) > 0])
    ])


def latex_main():
    with open('publications.yml', 'r') as f:
        d = yaml.load(f.read())

    ss = ['\\section{' + 'Publications' + '}\n\n']
    for pub in d['publications']:
        s = create_cventry_publication(pub, d['collaborators'])
        ss.append(s)
    ss += ['\n\n\\section{' + 'Workshop Papers and Manuscripts' + '}\n\n']
    for pub in d['preprints']:
        s = create_cventry_publication(pub, d['collaborators'])
        ss.append(s)

    ss = '\n'.join(ss)
    with open('cv/src/publications.tex', 'w') as f:
        f.write(ss)


def html_href(url, text):
    if len(text) == 0:
        return ''
    else:
        return r"""<a href="{}" target="_blank">{}</a>""".format(url, text)


def html_b(text):
    return "<b>{}</b>".format(text)


def html_i(text):
    return "<i>{}</i>".format(text)


def create_html_publication(pub, colabs):
    authors = []
    for author in pub['authors']:
        colab = find_collaborator(colabs, author)
        if colab is not None:
            if 'Jiaming Song' in colab['name']:
                authors.append(html_b(colab['name']))
            else:
                authors.append(colab['name'])
        else:
            authors.append(author)
    
    authors = ', '.join(authors)
    
    if 'url' in pub.keys() and len(pub['url']) > 0:
        paper = html_href(pub['url'], pub['name'])
    else:
        paper = pub['name']

    paper = html_b(paper)

    if 'date' in pub.keys():
        now = datetime.datetime.now()
        date = datetime.datetime.strptime(pub['date'], '%m/%d/%Y')
        if date < now:
            appear = 'In '
        else:
            appear = 'To appear in '
        date = date.strftime('%B %Y')
    else:
        appear = ''
        date = ''

    if 'conference' in pub.keys():
        conference = appear + ' ' + html_i(pub['conference']) + '. '
        if 'additional' in pub.keys() and len(pub['additional']) > 0:
            conference += pub['additional'] + '.'
    else:
        conference = ''

    if 'code' in pub.keys():
        code = html_href(pub['code'], '[code]')
    else:
        code = ''

    if 'slides' in pub.keys():
        slides = html_href(pub['slides'], '[slides]')
    else:
        slides = ''

    if 'blog' in pub.keys():
        blog = html_href(pub['blog'], '[blog]')
    else:
        blog = ''
    
    if 'workshops' in pub.keys() and len(pub['workshops']) > 0:
        workshops = 'Abridged in ' + ', '.join([html_i(s) for s in pub['workshops']]) + '.'
    else:
        workshops = ''
    
    if 'locations' in pub.keys() and len(pub['locations']) > 0:
        locations = 'In ' + ', '.join([html_i(s) for s in pub['locations']]) + '.'
    else:
        locations = ''

    if len(conference) > 0:
        conference = ' '.join([s for s in [conference, code, slides, blog] if len(s) > 0])
    elif len(locations) > 0:
        locations = ' '.join([s for s in [locations, code, slides, blog] if len(s) > 0])
    cwl = '<br/>'.join([s for s in [conference, workshops, locations] if len(s) > 0])

    return """
    <p style="line-height: 1.5; margin-top: 1px; margin-bottom: 1px; font-size: 16px;">
        {}
    </p>
    <p style="line-height: 1.5; margin-top: 0; margin-bottom: 0;">
        {}
        <br/>
        {}
    </p>
    <hr style="margin-top: 10px; margin-bottom: 10px;" />
    """.format(paper, authors, cwl) 


def html_main():
    with open('publications.yml', 'r') as f:
        d = yaml.load(f.read())

    ss = r'''
    <div class="panel panel-default" style="line-height: 1.5; margin-top: 0;">
    <div class="panel-heading" id="publications">
        <h4 style="line-height: 1.5; margin-top: 0; margin-bottom: 0;">Publications</h4>
    </div>
    <div class="panel-body" style="padding-top: 5px; margin-top: 0; margin-bottom: 0;">
    '''

    for pub in d['publications']:
        s = create_html_publication(pub, d['collaborators'])
        ss += s

    ss += "\n</div></div>\n"
    
    ss += r'''

    <div class="panel panel-default" style="line-height: 1.5; margin-top: 0;">
    <div class="panel-heading" id="publications">
        <h4 style="line-height: 1.5; margin-top: 0; margin-bottom: 0;">Workshop Papers and Manuscripts</h4>
    </div>
    <div class="panel-body" style="padding-top: 5px; margin-top: 0; margin-bottom: 0;">
    '''

    for pub in d['preprints']:
        s = create_html_publication(pub, d['collaborators'])
        ss += s

    ss += "\n</div></div>\n"

    with open('../tsong.me/_includes/publications.html', 'w') as f:
        f.write(ss)
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--latex', action='store_true')
    parser.add_argument('--html', action='store_true')

    args = parser.parse_args()
    if args.latex:
        latex_main()

    if args.html:
        html_main()