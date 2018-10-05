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
    if len(pub['url']) > 0:
        paper = href(pub['url'], pub['name'])
    else:
        paper = pub['name']

    if 'workshops' in pub.keys() and len(pub['workshops']) > 0:
        workshops = '\\\\Abridged version in ' + ', '.join([textit(s) for s in pub['workshops']]) + '.'
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

    conference = appear + ' ' + textit(pub['conference']) + '. '
    if 'additional' in pub.keys():
        conference += pub['additional'] + '.'

    return command('cventry', [
        '\\footnotesize ' + date,
        '\\bfseries ' + paper,
        '', '', '',
        '\\normalfont ' + ', '.join(authors) + '.\\\\' + conference + workshops
    ])


if __name__ == '__main__':
    with open('publications.yml', 'r') as f:
        d = yaml.load(f.read())

    ss = []
    for pub in d['publications']:
        s = create_cventry_publication(pub, d['collaborators'])
        ss.append(s)

    ss = '\n'.join(ss)
    with open('publications.tex', 'w') as f:
        f.write(ss)
