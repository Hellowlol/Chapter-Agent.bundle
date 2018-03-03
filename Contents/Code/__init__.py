import hashlib, os, time
import re

def Start():
  pass

def ValidatePrefs():
  pass


#class Mixin():
#  def update()


class ChapterAgent(Agent.Movies):

  name = 'Chapter Agent'
  languages = [Locale.Language.NoLanguage, Locale.Language.EN]
  primary_provider = True
  contributes_to = ['com.plexapp.agents.imdb', 'com.plexapp.agents.none']
  #contributes_to = ['com.plexapp.agents.none', 'com.plexapp.agents.thetvdb', 'com.plexapp.agents.thetvdb', 'com.plexapp.agents.plexmovies']

  def search(self, results, media, lang):

    results.Append(MetadataSearchResult(id = media.id, name = media.name, year = None, score = 100, lang = lang))

  def update(self, metadata, media, lang):
    Log.Debug('called update')
    #Log.Debug(metadata)
    #Log.Debug(media)
    #Log.Debug('ASS')
    #Log.Debug('%s' % len(metadata.chapters))
    merge = True

    part = media.items[0].parts[0]
    path = os.path.dirname(part.file)
    f, ex = os.path.splitext(part.file)
    root_file, ext = os.path.splitext(os.path.basename(part.file))
    edl_path = f + '.edl'
    ds_path = f + '.xml'
    Log.Debug('edl was %s' % edl_path)
    curr_chapters = []
    #if not os.path.exists(edl) or not os.path.exists(ds):
    #  return
    #Log.Debug(list(dir(metadata)))
    class PH():
      def __init__(self, start=0, end=0, title=''):
        self.start = start
        self.end = end
        self.title = title

    #x = True
    #if x:
      #for ii, ch in enumerate(metadata.chapters):
      #  Log.Debug('org chapter %s %s %s' % (ch.start_time_offset, ch.end_time_offset, ch.title))
      #  ph = PH(ch.start_time_offset, ch.end_time_offset, title=ch.title)
      #  curr_chapters.append(ph)

    #Log.Debug(curr_chapters)

    #for i in sorted([i for i in metadata.attrs.keys() if not i.startswith('_')]):
    #  Log.Debug('%s %s %s', i, getattr(metadata, i), type(getattr(metadata, i)))
    #Log.Debug(list(dir(media)))
    #Log.Debug(metadata.__dict__)

    #if True:
    #for ch in metadata.chapters:
    #    Log.Debug(ch)
        #Log(list(dir(ch)))
        #Log(help(ch))
        #Log(ch.edit())
        #Log(vars(ch))
    Log.Debug('Should have printed shit.')
    #return

    if Prefs['input'].strip() == 'edl':
      if os.path.exists(edl_path) and os.path.isfile(edl_path):
      #if os.path.isfile(os.path.join(path, root_file + '.edl')):
        Log.Debug('Has edl %s' % edl_path)
        data = Core.storage.load(edl_path)
        Log.Debug(data.splitlines())

        #duration = int(part.duration)
        #duration = int(long(getattr(media.items[0].parts[0], 'duration')))
        #Log.Debug('Duration is %s' % self.toTime(duration) / 1000)

        Log.Debug('Had len %s chapters' % len(metadata.chapters))
        metadata.chapters.clear()

        Log.Debug('Cleared chapters %s' % len(metadata.chapters))

        offset = 0
        cindex = 1
        ncindex = 1
        need_convert = 1

        title_map = {'0': 'Cut',
                     '1': 'Mute',
                     '2': 'Scene Marker',
                     '3': 'Commercial break'}

        for line in data.splitlines():
          if '#' in line:
            need_convert = 24 # get fps here.
            line = line.strip('#', '')


          parts = line.split()
          Log.Debug(parts)
          if len(parts) == 3:
              start = int(float(parts[0])) * need_convert
              end = int(float(parts[1])) * need_convert
              action = parts[2] or ''
              #if merge:
              n = PH(start, end, title=title_map.get(action, action))
              curr_chapters.append(n)

        if curr_chapters:
          #metadata.chapters.clear()
          for i, item in enumerate(sorted(curr_chapters, key=lambda k: k.end)):
            Log.Debug('%s %s %s' % (item.start, item.end, item.title))
            chapter = metadata.chapters.new()
            chapter.title = item.title or 'Chapter %s' % i
            chapter.start_time_offset = item.start * 1000
            chapter.end_time_offset = item.end * 1000
              #chapter.index = i
              #metadata.chapters.add(chapter)

          #Log.Debug(parts)
          #start = self.toTime(int(round(float(parts[0]))))
          #end = self.toTime(int(round(float(parts[1]))))
          #action = parts[2]


          #if Prefs['commercial']:
          #  if offset > 0:
          #    chapter = metadata.chapters.new()
          #    chapter.title = 'Chapter %d' % ncindex
          #    chapter.start_time_offset = offset
          #    chapter.end_time_offset = int(round(float(parts[0]) * 1000))
          #    offset = 0
          #    ncindex += 1

            #if cindex == 1:
            #  if float(parts[0]) > 0.0:
            #    chapter = metadata.chapters.new()
            #    chapter.title = 'Chapter %d' % ncindex
            #    chapter.start_time_offset = offset
            #    chapter.end_time_offset = int(round(float(parts[0]) * 1000))
            #    offset = 0
            #    ncindex += 1

          #chapter = metadata.chapters.new()
          #if Prefs['commercial']:
          #  chapter.title = 'Commercial %d' % cindex
          #else:
          #  chapter.title = 'Chapter %d' % cindex
          #chapter.start_time_offset = int(round(float(parts[0]) * 1000))
          #chapter.end_time_offset = int(round(float(parts[1]) * 1000))
          #offset = int(round(float(parts[1]) * 1000))
          #cindex += 1

          #Log('Found chapter at %s - %s' % (start, end))

        #if Prefs['commercial']:
        #  if offset > 0:
        #    if offset < duration:
        #      chapter = metadata.chapters.new()
        #      chapter.title = 'Chapter %d' % ncindex
        #      chapter.start_time_offset = offset
        #      chapter.end_time_offset = duration

        #Log('Chapters loaded for %s' % root_file)
      #else:
      #  metadata.chapters.clear()
      #  Log('Chapters cleared for %s' % root_file)
      for iii in metadata.chapters:
        Log.Debug(iii)
      Log.Debug('len chapters %s' % len(metadata.chapters))

    if Prefs['input'].strip() == 'dvrmstb':
      if os.path.isfile(os.path.join(path, root_file + '.xml')):
        data = Core.storage.load(os.path.join(path, root_file + '.xml'))
        xml_data = XML.ElementFromString(data)

        duration = int(long(getattr(media.items[0].parts[0], 'duration')))
        Log('Duration is %s' % self.toTime(int(round(float(getattr(media.items[0].parts[0], 'duration')) / 1000))))
        metadata.chapters.clear()

        offset = 0
        cindex = 1
        ncindex = 1
        for region in xml_data.xpath('//commercial'):
          start = self.toTime(int(round(float(region.attrib['start']))))
          end = self.toTime(int(round(float(region.attrib['end']))))

          if Prefs['commercial']:
            if offset > 0:
              chapter = metadata.chapters.new()
              chapter.title = 'Chapter %d' % ncindex
              chapter.start_time_offset = offset
              chapter.end_time_offset = int(round(float(region.attrib['start']) * 1000))
              offset = 0
              ncindex += 1

            if cindex == 1:
              if int(round(float(region.attrib['start']))) > 0:
                chapter = metadata.chapters.new()
                chapter.title = 'Chapter %d' % ncindex
                chapter.start_time_offset = offset
                chapter.end_time_offset = int(round(float(region.attrib['start']) * 1000))
                offset = 0
                ncindex += 1

          chapter = metadata.chapters.new()
          if Prefs['commercial']:
            chapter.title = 'Commercial %d' % cindex
          else:
            chapter.title = 'Chapter %d' % cindex
          chapter.start_time_offset = int(round(float(region.attrib['start']) * 1000))
          chapter.end_time_offset = int(round(float(region.attrib['end']) * 1000))
          offset = int(round(float(region.attrib['end']) * 1000))
          cindex += 1

          Log('Found chapter at %s - %s' % (start, end))

        if Prefs['commercial']:
          if offset > 0:
            if offset < duration:
              chapter = metadata.chapters.new()
              chapter.title = 'Chapter %d' % ncindex
              chapter.start_time_offset = offset
              chapter.end_time_offset = duration

        Log('Chapters loaded for %s' % root_file)
      else:
        metadata.chapters.clear()
        Log('Chapters cleared for %s' % root_file)

  def toTime(self, seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

  def bts(self, duration, totalbytes, bytes):
    if bytes == 0.0:
      return int(bytes)
    else:
      bytes_per_ms = round(totalbytes / duration)
      ms = bytes / bytes_per_ms
      return int(round(ms))

  def dump(self, obj):
    for attr in dir(obj):
      Log('obj.%s = %s' % (attr, getattr(obj, attr)))
