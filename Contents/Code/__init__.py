import os
import time
import re

class PH():
    def __init__(self, start=0, end=0, title=''):
        self.start = start
        self.end = end
        self.title = title


def Start():
    pass


def ValidatePrefs():
    pass


def dump(obj):
    for attr in dir(obj):
        Log.Debug('obj.%s = %s' % (attr, getattr(obj, attr)))


class Mixin():
    def search(self, results, media, lang):
        results.Append(MetadataSearchResult(id=media.id, name=media.name, year=None, score=100, lang=lang))

    def update(self, metadata, media, lang):
        # Should we just loop seasons or episodes.
        dump(metadata)
        ALL_PARTS = []

        title_map = {'0': 'Cut',
                     '1': 'Mute',
                     '2': 'Scene Marker',
                     '3': 'Commercial break'
        }

        # Is this a tvshow..?
        # This does not work as the metadata obj for  tvshow class does not support
        # chapters.. I wish i had tested this sooner. Anyway.. Atleast it should be ready.
        if hasattr(media, 'seasons') or hasattr(media, 'episodes'):
            ids = metadata.guid.split('://')[1].split('?')[0].split('/')
            ep_grandparent_key = -1
            ep_season = -1
            ep_ep = -1

            if len(ids) == 3:
                ep_grandparent_key, ep_season, ep_ep = ids
                ALL_PARTS.extend(media.seasons[str(ep_season)].episodes[str(ep_ep)].all_parts())

            if len(ids) == 2:
                ep_grandparent_key, ep_season = ids
                ALL_PARTS.extend(media.seasons[ep_season].all_parts())

            if len(ids) == 1:
                ep_grandparent_key = ids[0]
                ALL_PARTS.extend(media.all_parts())
                Log.Debug('Cant add chapters to TV_Shows')
                return

        else:
            # this is a movie..
            #part = media.items[0].parts[0]
            ALL_PARTS.extend(media.all_parts())


        for part in ALL_PARTS:
            Log.Debug('Checking part %s' % part.file)
            try:
                fps = part.steams[0].frameRate
            except:
                # This for for comskip shitty frames.
                Log.Debug('Defaulting to 24 fps')
                fps = 24

            filename_without_ext, ext = os.path.splitext(part.file)
            edl = filename_without_ext + '.edl'
            comskip = filename_without_ext + '.txt'
            edl_like_ext = ('edl', 'txt')

            curr_chapters = []

            # Prefer edl.
            for typ in [edl, comskip]:
                if os.path.isfile(typ):
                    # https://kodi.wiki/view/Edit_decision_list#MPlayer_EDL
                    if typ.endswith('edl') or typ.endswith('txt'):
                        need_convert = 1
                        data = Core.storage.load(typ)

                        # Lets try to parse the damn thing.
                        for line in data.splitlines():
                            if '#' in line or typ.endswith('txt'):
                                need_convert = fps  # get fps here.
                                line = line.strip('#', '')

                            parts = line.split()
                            start = int(float(parts[0])) * need_convert
                            end = int(float(parts[1])) * need_convert
                            #
                            try:
                                action = parts[2]
                            except IndexError:
                                action = '3'

                            n = PH(start, end, title=title_map.get(action, action))
                            curr_chapters.append(n)

                        if curr_chapters:
                            Log.Debug('Clearing chapters')
                            metadata.chapters.clear()
                            for i, item in enumerate(sorted(curr_chapters, key=lambda k: k.end)):
                                Log.Debug('%s %s %s' % (item.start, item.end, item.title))
                                chapter = metadata.chapters.new()
                                chapter.title = item.title or 'Chapter %s' % i
                                chapter.start_time_offset = item.start * 1000
                                chapter.end_time_offset = item.end * 1000

                            Log.Debug('Finished doing edl for %s', part.file)



class ChapterAgentShows(Mixin, Agent.TV_Shows):
    name = 'Chapter Agent TV Show'
    languages = [Locale.Language.NoLanguage]
    primary_provider = False
    contributes_to = ['com.plexapp.agents.thetvdb', 'com.plexapp.agents.none']


class ChapterAgentMovie(Mixin, Agent.Movies):
    name = 'Chapter Agent Movies'
    languages = [Locale.Language.NoLanguage]
    primary_provider = False
    contributes_to = ['com.plexapp.agents.imdb', 'com.plexapp.agents.none']




