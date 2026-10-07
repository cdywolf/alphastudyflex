import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    load=lambda n:json.loads((ROOT/'content'/f'{n}.json').read_text(encoding='utf-8'))
    sources=load('sources');questions=load('questions');curriculum=load('curriculum');rules=load('pedagogy')
    ids={s['id']:s for s in sources}
    pilots=[c for c in curriculum['chapters'] if c['state']=='pilot']
    skill_chapter={s['id']:c['id'] for c in pilots for s in c['skills']};skills=set(skill_chapter)
    assert len(ids)==len(sources)==18
    assert len(skill_chapter)==sum(len(c['skills']) for c in pilots),'identifiants de compétences dupliqués entre chapitres'
    assert len({l['id'] for c in pilots for l in c['lessons']})==sum(len(c['lessons']) for c in pilots)
    for c in pilots:
        assert {l['skill'] for l in c['lessons']}=={s['id'] for s in c['skills']}
        for s in c['skills']:
            for ref in s['sources']:assert ref['id'] in ids and 1<=ref['pdf_page']<=ids[ref['id']]['pages']
    assert len({q['id'] for q in questions})==len(questions)
    for q in questions:
        assert q['skill'] in skills and q['sources'] and q['criteria'] and q['chapter']==skill_chapter[q['skill']]
        if q['mode']=='practice':assert q['hints'],q['id']
        assert q['dimension'] in ['expression','outils','methodologie']
        if q['kind']=='choice':assert type(q['answer']) is int and 0<=q['answer']<len(q['choices'])
        for ref in q['sources']:
            assert ref['id'] in ids and ids[ref['id']]['level']=='2AC'
            assert 1<=ref['pdf_page']<=ids[ref['id']]['pages']
    for r in rules:
        assert r['sources']
        for ref in r['sources']:assert ref['id'] in ids
    for mode in ['diagnostic','final']:
        assert {s:sum(q['mode']==mode and q['skill']==s for q in questions) for s in skills}=={s:2 for s in skills}
    print(f'{len(sources)} sources, {len(pilots)} chapitres pilotes, {len(questions)} questions, {len(rules)} règles : structure cohérente.')
if __name__=='__main__':main()
