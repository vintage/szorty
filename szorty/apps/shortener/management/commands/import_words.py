import os
import string

from django.core.management import base
from szorty.apps.shortener import models


AVAILABLE_CHARS = string.lowercase + string.digits


class Command(base.BaseCommand):
    help = 'Import keywords from file into database.'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    @staticmethod
    def get_words(words_path):
        with open(words_path) as words:
            for word in words:
                yield word.strip()

    @staticmethod
    def format_word(word):
        return ''.join([
            c for c in word.lower() if c in AVAILABLE_CHARS
        ])

    def handle(self, *args, **options):
        unique_words = set()
        file_path = str(options['file'])

        if not os.path.isfile(file_path):
            raise base.CommandError('Invalid file path provided')

        for word in self.get_words(file_path):
            word = self.format_word(word)
            unique_words.add(word)

        models.Word.objects.all().delete()
        models.Word.objects.bulk_create([
            models.Word(name=w) for w in unique_words
        ])

        self.stdout.write(
            'Successfully imported {} words into database'.format(
                len(unique_words)
            )
        )