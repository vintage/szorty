import os

from django.core.management import call_command
from django.core.management import base
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils.six import StringIO

from . import models
from . import forms
from .management.commands.import_words import Command as ImportCommand


class ImportCommandTestCase(TestCase):
    file_path = '/tmp/words.txt'

    def setUp(self):
        super(ImportCommandTestCase, self).setUp()

        with open(self.file_path, 'w+') as word_file:
            word_file.write('first\n')
            word_file.write('second\n')
            word_file.write('third')

    def tearDown(self):
        os.remove(self.file_path)

    def test_missing_file_arg(self):
        out = StringIO()
        self.assertRaises(base.CommandError,
                          call_command,
                          'import_words',
                          stdout=out)

    def test_file_no_exist(self):
        out = StringIO()
        self.assertRaises(base.CommandError,
                          call_command,
                          'import_words',
                          '/tmp/oczko.txt',
                          stdout=out)

    def test_check_words(self):
        words = list(ImportCommand.get_words(self.file_path))

        self.assertEqual(['first', 'second', 'third'], words)

    def test_format_words(self):
        def _check(raw, word):
            self.assertEqual(word, ImportCommand.format_word(raw))

        _check('alibaba', 'alibaba')
        _check('10th', '10th')
        _check('sa`k', 'sak')
        _check('yan%g', 'yang')
        _check('UPPER1', 'upper1')
        _check('!@#$%^&*(', '')

    def test_valid_call(self):
        out = StringIO()
        call_command('import_words', self.file_path, stdout=out)
        self.assertIn(
            'Successfully imported 3 words into database', out.getvalue())


class ShortcutFormTestCase(TestCase):
    def setUp(self):
        super(ShortcutFormTestCase, self).setUp()

        self.first = models.Word.objects.create(name='first')
        self.second = models.Word.objects.create(name='second')
        self.third = models.Word.objects.create(name='third')

    def test_words_empty(self):
        models.Word.objects.all().delete()
        form = forms.ShortcutCreateForm({
            'target_url': 'http://google.pl'
        })
        self.assertFalse(form.is_valid())

    def test_invalid_target_url(self):
        form = forms.ShortcutCreateForm({
            'target_url': 'not a url'
        })
        self.assertFalse(form.is_valid())

    def test_missing_target_url(self):
        form = forms.ShortcutCreateForm()
        self.assertFalse(form.is_valid())

    def test_empty_target_url(self):
        form = forms.ShortcutCreateForm({
            'target_url': ''
        })
        self.assertFalse(form.is_valid())

    def test_for_existing_word(self):
        form = forms.ShortcutCreateForm({
            'target_url': 'http://o.com/first/'
        })
        self.assertTrue(form.is_valid())

        instance = form.save()
        self.assertEqual(instance.word, self.first)

    def test_reserved_word(self):
        # Reserve word for some shortcut
        forms.ShortcutCreateForm({
            'target_url': 'http://o.com/first/'
        }).save()

        # Try to create new shortcut for the same word
        form = forms.ShortcutCreateForm({
            'target_url': 'http://dot.eu/arg-first/'
        })
        instance = form.save()

        self.assertNotEqual(instance.word, self.first)

    def test_all_words_reserved(self):
        # Reserve all words
        forms.ShortcutCreateForm({
            'target_url': 'http://o.com/second/'
        }).save()

        forms.ShortcutCreateForm({
            'target_url': 'http://o.com/third/'
        }).save()

        forms.ShortcutCreateForm({
            'target_url': 'http://o.com/first/'
        }).save()

        # Try to create new shortcut when all words are used
        form = forms.ShortcutCreateForm({
            'target_url': 'http://dot.eu/any-new/'
        })
        instance = form.save()

        self.assertEqual(instance.word, self.second)

    def test_for_not_existing_word(self):
        form = forms.ShortcutCreateForm({
            'target_url': 'http://o.com/fourth/'
        })
        self.assertTrue(form.is_valid())

        instance = form.save()
        self.assertIsNotNone(instance.word)


class ShortcutDetailViewTestCase(TestCase):
    def setUp(self):
        super(ShortcutDetailViewTestCase, self).setUp()

        self.client = Client()

        self.word = models.Word.objects.create(name='first')
        self.shortcut = models.Shortcut.objects.create(
            target_url='http://localhost', word=self.word)

    def test_not_found(self):
        url = reverse('shortcut_detail', args=[self.shortcut.slug])
        self.shortcut.delete()
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_using_pk(self):
        url = reverse('shortcut_detail', args=[self.shortcut.pk])
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_detail_valid(self):
        url = reverse('shortcut_detail', args=[self.shortcut.slug])
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)


class ShortcutRedirectViewTestCase(TestCase):
    def setUp(self):
        super(ShortcutRedirectViewTestCase, self).setUp()

        self.client = Client()

        self.word = models.Word.objects.create(name='first')
        self.shortcut = models.Shortcut.objects.create(
            target_url='http://localhost', word=self.word)

    def test_not_found(self):
        url = reverse('shortcut_redirect', args=[self.word.name])
        self.word.delete()
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_word_without_shortcut(self):
        word = models.Word.objects.create(name='second')
        url = reverse('shortcut_redirect', args=[word.name])
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_using_pk(self):
        url = reverse('shortcut_redirect', args=[self.word.pk])
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_redirect_valid(self):
        url = reverse('shortcut_redirect', args=[self.word.name])
        response = self.client.get(url)

        self.assertEqual(302, response.status_code)
        self.assertEqual(
            1,
            models.Shortcut.objects.get(pk=self.shortcut.pk).redirection_count
        )

    def test_redirect_multiple_times(self):
        url = reverse('shortcut_redirect', args=[self.word.name])
        self.client.get(url)
        self.client.get(url)
        response = self.client.get(url)

        self.assertEqual(302, response.status_code)
        self.assertEqual(
            3,
            models.Shortcut.objects.get(pk=self.shortcut.pk).redirection_count
        )