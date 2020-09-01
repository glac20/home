from collections import namedtuple
from datetime import datetime
import re
from django.core.management.base import BaseCommand
from net153.journal.models import Entry


class Command(BaseCommand):
    help = "Migrate from text file journal"

    def _create_post(self, path, file):
        full_path = path + '/' + file
        d = {}
        tags = ''
        with open(full_path, 'r') as f:
            d['title'] = f.readline()
            tags = [
                i.strip() for i in f.readline().replace(
                    'Tags:', '').strip().split(',')]
            d['body'] = f.read().strip()
            d['creator_id'] = 1
            d['created'] = datetime.datetime.fromtimestamp(
                self.entries_index.get(file))
        p = Entry(**d)
        p.save()
        p.tags.add(*tags)

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        pass

    def handle(self, *args, **options):
        last_date = datetime.strptime('01/01/22', '%m/%d/%y')
        lines = []
        Line = namedtuple('Line', ['date', 'entry'])
        with open('old_data/journal.txt', 'r') as j:
            date = ''
            while ln := j.readline():
                ln = ln.strip()
                if ln == '':
                    continue
                if re.match(r'^\d+/\d', ln):
                    date = datetime.strptime(ln, '%m/%d/%y')
                else:
                    assert(last_date > date), f'{last_date} > {date}?'
                    last_date = date
                    lines.append(Line(date=date, entry=ln))

        lines.reverse()
        for i in lines:
            p = Entry(date=i.date, body=i.entry)
            p.save()
