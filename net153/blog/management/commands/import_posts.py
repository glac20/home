from pathlib import Path
import datetime
import re
from django.core.management.base import BaseCommand
from net153.blog.models import Post


class Command(BaseCommand):
    help = "Migrate from bloxsom markdown files"
    entries_index = {}

    def _set_entries_index(self):
        with open('old_data/oldblog/.entries_index.index', 'r') as f:
            self.entries_index = {k.strip(): int(v.strip()) for k, v in list(
                map(lambda x: x.split('=>'), f.readlines()))}

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
        p = Post(**d)
        p.save()
        p.tags.add(*tags)

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        pass

    def handle(self, *args, **options):
        self._set_entries_index()

        directory = Path('old_data/oldblog')
        for file in directory.iterdir():
            if file.is_file() and re.search(r'\.txt$', file.name, re.I):
                self._create_post(file.parent.as_posix(), file.name)
