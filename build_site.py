"""Build the static website from the published dataset, without network access."""
import csv
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ['account', 'id', 'date', 'views', 'likes', 'reposts', 'replies', 'quotes', 'bookmarks', 'url', 'text']


def build(source):
    payload = {key: source[key] for key in ['start', 'end', 'days', 'collected_at', 'accounts']}
    payload['coverage'] = {account: {'complete': info['complete']} for account, info in source.get('coverage', {}).items()}
    payload['posts'] = [{field: post.get(field) for field in FIELDS} for post in source['posts']]
    posts = payload['posts']
    if len({p['id'] for p in posts}) != len(posts):
        raise ValueError('Duplicate publication IDs')
    for post in posts:
        stamp = datetime.fromisoformat(post['date'])
        if stamp.utcoffset() is None or stamp.utcoffset().total_seconds() != 0:
            raise ValueError(f'Expected UTC timestamp: {post["id"]}')
        if not payload['start'] <= post['date'][:10] < payload['end']:
            raise ValueError(f'Publication outside the date range: {post["id"]}')
        if post['account'] not in payload['accounts']:
            raise ValueError(f'Unknown account: {post["account"]}')
        for field in ['views', 'likes', 'reposts', 'replies', 'quotes', 'bookmarks']:
            value = post[field]
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                raise ValueError(f'Invalid {field}: {post["id"]}')
    data_dir = ROOT / 'data'
    data_dir.mkdir(exist_ok=True)
    (data_dir / 'stats.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    with (data_dir / 'posts.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(posts)
    template = (ROOT / 'dashboard.template.html').read_text(encoding='utf-8')
    embedded = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c')
    html = template.replace('__DATA__', embedded)
    for name in ['index.html', 'statistiques-30-jours.html']:
        (ROOT / name).write_text(html, encoding='utf-8')
    output = ROOT / '_site'
    output.mkdir(exist_ok=True)
    (output / 'index.html').write_text(html, encoding='utf-8')
    (output / '.nojekyll').touch()
    print(f'Built _site/index.html: {len(posts)} publications checked.')


def main():
    build(json.loads((ROOT / 'data' / 'stats.json').read_text(encoding='utf-8')))


if __name__ == '__main__':
    main()
