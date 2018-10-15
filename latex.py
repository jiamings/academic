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
        workshops = 'Abridged version in ' + ', '.join([textit(s) for s in pub['workshops']]) + '.'
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


if __name__ == '__main__':
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
