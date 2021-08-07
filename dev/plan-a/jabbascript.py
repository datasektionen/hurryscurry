#!/usr/bin/env python

import re
import os
import sys
import shutil
import signal
import argparse
import jsonschema
import simplejson as json
from datetime import datetime
from termcolor import colored, cprint
from subprocess import Popen, PIPE, TimeoutExpired, CalledProcessError

#
# utility methods
#

"""
Loads the JSON file specified by the passed path
Captures no exceptions
"""
def load_JSONfile(path):
    with open(path) as datafile:
        return json.load(datafile)

"""
Returns a composite path from the passed components
"""
def filepath(*components):
    return '/'.join(components)

"""
Returns an indexed id string from the passed super-id and index
"""
def id_str(super_id, index, separator=':'):
    return '%s%s%s' % (super_id, separator, index)

"""
Returns a super-id and index from the passed composite id string
"""
def breakup_id(id_str):
    return id_str.split(':')[:2]

"""
Finds all files in the passed directory.
User may also specify a required filename suffix for the search
"""
def list_files(dir_path, suffix=None):
    files = ['%s/%s' % (dir_path, src) for src in os.listdir(dir_path)]
    if suffix:
        files = list(filter(lambda src: src[-len(suffix):] == suffix, files))
    return files

"""
Logs the passed message in the logfile specified by the passed suffix.
Creates a new logfile if there was none before
"""
def log(suffix, where, message):
    # create a logs/ dir if it doesn't already exist
    log_dir = filepath(__path_to_logs)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # load the content of any existing logfile
    log_path = '%s/log.%s' % (log_dir, suffix)
    with open(log_path, mode='a+') as logfile:
        logfile.write('\n')
        logfile.write('%s\n' % ('>'*80))
        logfile.write('%s timestamp: %s\n' % ('>'*5 , str(datetime.now())))
        logfile.write('%s where: %s\n' % ('>'*5 , where))
        logfile.write('%s\n' % message)

"""
Prints a summary of the results from *some* operation
"""
def print_summary(passed, failed, errors):
    summary = list()
    # only present stats > 0
    if passed > 0: summary.append(colored('Passed: %s' % passed, 'green', attrs=['bold']))
    if failed > 0: summary.append(colored('Failed: %s' % failed, 'red', attrs=['bold']))
    if errors > 0: summary.append(colored('Errors: %s' % errors, 'yellow', attrs=['bold']))
    pretty_print.important('Summary: [ %s ]' % (', '.join(summary)))
    pretty_print.important('Logfiles can be found at logs/')

"""
Returns a dictionary containing all JSON resources in the resources/rpu/data/ directory tree.
"""
def load_resources(missions=False, events=False, drifters=False, characters=False):
    payload = {}
    try:

        if missions:
            # load the JSON file for each mission
            print('Loading %s into memory ... ' % (colored(__path_to_missions['title'], attrs=['bold'])), end='')
            missions = dict()
            for filepath in list_files(__path_to_missions['data.d'], suffix='.json'):
                mission = load_JSONfile(filepath)
                missions[mission['id']] = mission
            payload['missions'] = missions
            pretty_print.ok()

        if events:
            # load the JSON file for each event category
            print('Loading %s into memory ... ' % (colored(__path_to_events['title'], attrs=['bold'])), end='')
            events = dict()
            for filepath in list_files(__path_to_events['data.d'], suffix='.json'):
                event_category = load_JSONfile(filepath)
                for event in event_category['events']:
                    events[id_str(event_category['id'], event['id'])] = event
            payload['events'] = events
            pretty_print.ok()

        if drifters:
            # load the JSON file for drifters
            print('Loading %s into memory ... ' % (colored(__path_to_drifters['title'], attrs=['bold'])), end='')
            drifters = dict()
            for filepath in list_files(__path_to_drifters['data.d'], suffix='.json'):
                drifter_file = load_JSONfile(filepath)
                for drifter_mission in drifter_file['missions']:
                    drifters[drifter_mission['id']] = drifter_mission
            payload['drifters'] = drifters
            pretty_print.ok()

        if characters:
            # load the JSON file for each character
            print('Loading %s into memory ... ' % (colored(__path_to_characters['title'], attrs=['bold'])), end='')
            characters = dict()
            for filepath in list_files(__path_to_characters['data.d'], suffix='.json'):
                character = load_JSONfile(filepath)
                characters[character['id']] = character
            payload['characters'] = characters
            pretty_print.ok()

    except json.JSONDecodeError:
        pretty_print.fatal()
        pretty_print.critical('Error in JSON syntax')
        pretty_print.critical('Please run the JSON parser and fix all errors that appear')
        sys.exit(1)

    else:
        return payload

#
# Utility classes
#

class pretty_print:
    """ Simple class for organizing pretty print outputs """
    def ok():
        cprint('OK', 'green', attrs=['bold'])
    def fail():
        cprint('FAIL', 'red', attrs=['bold'])
    def error():
        cprint('ERROR', 'yellow', attrs=['bold'])
    def fatal():
        cprint(' FATAL ', 'red', attrs=['bold', 'reverse'])
    def na():
        cprint('N/A', 'grey', attrs=['bold'])
    def important(text):
        prompt = colored(' > ', 'green', attrs=['bold', 'reverse'])
        print('%s %s' % (prompt, text))
    def critical(text):
        prompt = colored(' > ', 'red', attrs=['bold', 'reverse'])
        print('%s %s' % (prompt, text))

#
# path constants
#

__path_to_logs = './logs'
__path_to_resources = './../../resources'
__path_to_tex_temp = './tex/temp.tex'
__path_to_tex_templates = './tex/templates'

__path_to_data = filepath(__path_to_resources, 'rpu/data')
__path_to_schemas = filepath(__path_to_resources, 'rpu/schemas')
__path_to_pdfs = filepath(__path_to_resources, 'tryck/pdf')

__path_to_events = {
    'title': 'events',
    'swedish': 'händelse',
    'data.d': filepath(__path_to_data, 'events'),
    'schema': filepath(__path_to_schemas, 'schema.events.json'),
    'template': filepath(__path_to_tex_templates, 'event.tex')
}
__path_to_missions = {
    'title': 'missions',
    'swedish': 'uppdrag',
    'data.d': filepath(__path_to_data, 'missions'),
    'schema': filepath(__path_to_schemas, 'schema.missions.json'),
    'template': filepath(__path_to_tex_templates, 'mission.tex')
}
__path_to_drifters = {
    'title': 'drifters',
    'swedish': 'drifvare',
    'data.d': filepath(__path_to_data, 'drifters'),
    'schema': filepath(__path_to_schemas, 'schema.drifters.json'),
    'template': filepath(__path_to_tex_templates, 'event.tex')
}
__path_to_characters = {
    'title': 'characters',
    'swedish': 'karaktär',
    'data.d': filepath(__path_to_data, 'characters'),
    'schema': filepath(__path_to_schemas, 'schema.characters.json'),
    'template': filepath(__path_to_tex_templates, 'character.tex')
}

#
# Main method for the jabbascript program
#

def main():

    # Parse all command line options
    parser = argparse.ArgumentParser(description='Tools for monitoring and generating hurryscurry data')
    parser.add_argument('-P' ,'--parse-json', help='parse each json file in the project', action='store_true', default=argparse.SUPPRESS)
    parser.add_argument('-V' ,'--validate-json', help='validates the json files in the project', action='store_true', default=argparse.SUPPRESS)
    parser.add_argument('-S' ,'--sanity-check', help='performs a sanity check on the json resources', action='store_true', default=argparse.SUPPRESS)
    parser.add_argument('-G' ,'--generate-all', help='generates all resources of the project', action='store_true', default=argparse.SUPPRESS)
    parser.add_argument('-m' ,'--generate-missions', help='generates the missions of the project', action='store_true', default=argparse.SUPPRESS)
    parser.add_argument('-e' ,'--generate-events', help='generates the events of the project', action='store_true', default=argparse.SUPPRESS)
    parser.add_argument('-d' ,'--generate-drifters', help='generates the drifter missions of the project', action='store_true', default=argparse.SUPPRESS)
    parser.add_argument('-c' ,'--generate-characters', help='generates the characters descriptions of the project', action='store_true', default=argparse.SUPPRESS)

    # Run the commands associated with each passed command line option
    methods = globals().copy()
    methods.update(locals())
    for option in vars(parser.parse_args()):
        command = methods.get(option)
        if not command:
             raise NotImplementedError('Whoops, option %s is not implemented ¯\_(ツ)_/¯' % option)
        else:
            command()
            pretty_print.important('Press any key to continue ...')
            input()

#
# Tool implementations
#

"""
Parses all JSON files in the project's resources/rpu/data/ directory tree
"""
def parse_json():
    pretty_print.important('Running %s ...' % colored(' JSON Parser ', 'blue', attrs=['bold', 'reverse']))

    # parse all JSON files in the following directories
    json_dirs = [
        __path_to_events,
        __path_to_missions,
        __path_to_drifters,
        __path_to_characters
    ]
    # record parse results
    passed = 0
    failed = 0
    errors = 0

    for directory in json_dirs:
        jsonfiles = list_files(directory['data.d'], suffix='.json') + [directory['schema']]
        print('%s (%s files)' % (colored(directory['title'], attrs=['bold']), len(jsonfiles)))
        print('Root at: %s/' % directory['data.d'])

        # parse each JSON file in this category
        for filepath in jsonfiles:
            print('\tFile: %s ... ' % colored(filepath, 'magenta', attrs=['bold']), end='')
            try:
                load_JSONfile(filepath)
            except json.JSONDecodeError as e:
                log(suffix='parser.failed', where=filepath, message=str(e))
                pretty_print.fail()
                failed += 1
            except Exception as e:
                log(suffix='parser.errors', where=filepath, message=str(e))
                pretty_print.error()
                errors += 1
            else:
                pretty_print.ok()
                passed += 1

    print_summary(passed=passed, failed=failed, errors=errors)

"""
Validates all JSON files in the project's resources/rpu/data/ directory tree.
Enforces the JSON schemas defined in resources/rpu/schemas/
"""
def validate_json():
    pretty_print.important('Running %s ...' % colored(' JSON Schema Enforcer ', 'blue', attrs=['bold', 'reverse']))

    # validate all JSON files in the following directories
    json_dirs = [
        __path_to_events,
        __path_to_missions,
        __path_to_drifters,
        __path_to_characters
    ]
    # record validation results
    passed = 0
    failed = 0
    errors = 0

    try:
        for directory in json_dirs:
            jsonfiles = list_files(directory['data.d'], suffix='.json')
            print('%s (%s files)' % (colored(directory['title'], attrs=['bold']), len(jsonfiles)))
            print('Root at: %s/' % directory['data.d'])

            # load the schema
            try:
                schema = load_JSONfile(directory['schema'])
            except:
                pretty_print.critical('Missing JSON schema: %s' % directory['schema'])
                pretty_print.critical('Please restore the schema file and run this procedure again')
                sys.exit(1)
            else:
                 print('Using JSON schema: %s' % directory['schema'])

            # validate each JSON file in this category
            for filepath in jsonfiles:
                print('\tFile: %s ... ' % colored(filepath, 'magenta', attrs=['bold']), end='')
                try:
                    jsonschema.validate(load_JSONfile(filepath), schema)
                except jsonschema.ValidationError as e:
                    log(suffix='validation.failed', where=filepath, message=str(e))
                    pretty_print.fail()
                    failed += 1
                except IOError as e:
                    log(suffix='validation.errors', where=filepath, message=str(e))
                    pretty_print.error()
                    errors += 1
                else:
                    pretty_print.ok()
                    passed += 1

    except json.JSONDecodeError:
        pretty_print.fatal()
        pretty_print.critical('Error in JSON syntax')
        pretty_print.critical('Please run the JSON parser and fix all errors that appear')
        sys.exit(1)

    print_summary(passed=passed, failed=failed, errors=errors)

"""
Perform a sanity check on all JSON resources in the resources/rpu/data/ directory tree.
"""
def sanity_check():
    pretty_print.important('Running %s ...' % colored(' Reference sanity-check ', 'blue', attrs=['bold', 'reverse']))

    data = load_resources(missions=True, events=True, drifters=True, characters=True)
    # record results of the sanity check
    passed = 0
    failed = 0
    errors = 0

    # check foreign key validity for the missions
    print('Checking foreign key validity for %s' % colored(__path_to_missions['title'], attrs=['bold']))
    # define some help functions for local pretty printing of missions
    mission_prompt_1 = lambda x: print('\t%s %s' % ('checking', colored(x, 'magenta', attrs=['bold'])))
    mission_prompt_2 = lambda x: print('\t%s%s %s ... ' % (' '*9, colored('+', 'magenta', attrs=['bold']), x), end='')

    # Checking main mission
    for mission_id, mission in sorted(data['missions'].items()):
        mission_prompt_1(mission_id)

        # check every clue in the current mission
        for clue in mission['clues']:
            clue_id = id_str(mission_id, clue['id'])
            mission_prompt_2(clue_id)

            try:
                if not clue['characters']:
                    # character lookup is not applicable
                    raise AttributeError
                for character in clue['characters']:
                    if character not in data['characters']:
                        # character id did not refer to an existing character
                        raise LookupError('Invalid character id: %s' % character)
                    if clue_id not in [m['id'] for m in data['characters'][character]['missions']]:
                        # the specified character makes no mention of the current mission
                        raise AssertionError('Character (%s) has no entry for clue: %s' % (character, clue_id))

            except LookupError as e:
                pretty_print.error()
                log(suffix='sanity.errors', where=clue_id, message=str(e))
                errors += 1
            except AssertionError as e:
                pretty_print.fail()
                log(suffix='sanity.failed', where=clue_id, message=str(e))
                failed += 1
            except AttributeError:
                pretty_print.na()
            else:
                pretty_print.ok()
                passed += 1

    # Checking foreign key validity in all events
    print('Checking foreign key validity for %s' % colored(__path_to_events['title'], attrs=['bold']))

    for event_id, event in sorted(data['events'].items()):
        print('\t%s %s ... ' % ('checking', colored(event_id, 'magenta', attrs=['bold'])), end='')
        try:
            if not event['characters']:
                # character lookup is not applicable
                raise AttributeError
            for character in event['characters']:
                if character not in data['characters']:
                    # character id did not refer to an existing character
                    raise LookupError('Invalid character id: %s' % character)
                if event_id not in [e['id'] for e in data['characters'][character]['events']]:
                    # the specified character makes no mention of the current mission
                    raise AssertionError('Character (%s) has no entry for mission: %s' % (character, event_id))

        except LookupError as e:
            pretty_print.error()
            log(suffix='sanity.errors', where=event_id, message=str(e))
            errors += 1
        except AssertionError as e:
            pretty_print.fail()
            log(suffix='sanity.failed', where=event_id, message=str(e))
            failed += 1
        except AttributeError:
            pretty_print.na()
        else:
            pretty_print.ok()
            passed += 1

    # Checking foreign key validity in all characters' mission and event lists
    print('Checking foreign key validity for %s' % colored(__path_to_characters['title'], attrs=['bold']))

    for char_id, character in sorted(data['characters'].items()):
        mission_prompt_1(char_id)

        # check the character's registered missions
        mission_prompt_2('missions')
        try:
            if not character['missions']:
                # the character has no missions registered
                raise AttributeError
            for mission in character['missions']:
                mission_id, clue_id = breakup_id(mission['id'])
                clues = {c['id'] : c['characters'] for c in data['missions'][mission_id]['clues']}

                if not data['missions'][mission_id]:
                    # mission id did not refer to an existing mission
                    raise LookupError('Invalid mission id: %s' % mission['id'])
                if clue_id == '0':
                    # if the clue ID is 0 the mission as a whole is just referenced, which is alright.
                    continue
                if char_id not in clues[clue_id]:
                    # the specified mission makes no mention of the current character
                    raise AssertionError('Mission (%s) has no entry for character: %s' % (mission['id'], char_id))

        except LookupError as e:
            pretty_print.error()
            log(suffix='sanity.errors', where=char_id, message=str(e))
            errors += 1
        except AssertionError as e:
            pretty_print.fail()
            log(suffix='sanity.failed', where=char_id, message=str(e))
            failed += 1
        except AttributeError:
            pretty_print.na()
        else:
            pretty_print.ok()
            passed += 1

        # check the character's registered events'
        mission_prompt_2('events')
        try:
            if not character['events']:
                # the character has no events registered
                raise AttributeError

            for event in character['events']:
                if event['id'] not in data['events']:
                    # event id did not refer to an existing event
                    raise LookupError('Invalid event id: %s' % event['id'])
                if char_id not in data['events'][event['id']]['characters']:
                    # the specified event makes no mention of the current character
                    raise AssertionError('Event (%s) has no entry for character: %s' % (event['id'], char_id))

        except LookupError as e:
            pretty_print.error()
            log(suffix='sanity.errors', where=char_id, message=str(e))
            errors += 1
        except AssertionError as e:
            pretty_print.fail()
            log(suffix='sanity.failed', where=char_id, message=str(e))
            failed += 1
        except AttributeError:
            pretty_print.na()
        else:
            pretty_print.ok()
            passed += 1

    print_summary(passed=passed, failed=failed, errors=errors)

"""
Generates all resources of the project, i.e. missions, events, drifter-missions and character descriptions
"""
def generate_all():
    generate_missions()
    generate_events()
    generate_drifters()
    # generate-characters()


def json2pdf(template_path, destination, log_suffix, data):
    print('\tGenerating: %s ... ' % colored(destination, 'magenta', attrs=['bold']), end='')
    sys.stdout.flush()

    jobname = 'tex/autogen'
    cmd = [
    'latexmk',
    '-gg',
    '-cd',
    '-quiet',
    '-xelatex',
    '-jobname=%s' % jobname,
    __path_to_tex_temp
    ]

    try:
        # load the template file
        with open(template_path, 'r') as myfile:
            template=myfile.read()

        # replace tags with the appropriate data
        with open(__path_to_tex_temp, mode='w+') as out:
            for tag, value in data.items():
                template = re.sub(r'{{%s}}' % tag, value, template)
            out.write(template)

        # run latexmk to generate the pdf
        FNULL = open(os.devnull, 'w')
        with Popen(cmd, stdout=FNULL, stderr=FNULL, preexec_fn=os.setsid) as process:
            try:
                process.communicate(timeout=30)
            except TimeoutExpired as e:
                os.killpg(process.pid, signal.SIGINT)
                process.communicate()
                raise Exception(e)
            else:
                if not os.path.exists(os.path.dirname(destination)):
                    os.makedirs(os.path.dirname(destination))
                shutil.copy2('./%s.pdf' % jobname, destination)

    except IOError as e:
        pretty_print.error()
        log(suffix='%s.errors' % log_suffix, where=destination, message='%s' % str(e))
    except Exception as e:
        pretty_print.error()
        log(suffix='%s.errors' % log_suffix, where=destination, message=str(e))
    else:
        pretty_print.ok()

"""
Generates the mission resources, as well as their respective clues, as pdf documents
"""
def generate_missions():
    pretty_print.important('Running %s ...' % colored(' Generate missions ', 'blue', attrs=['bold', 'reverse']))
    mission_log_suffix = 'generate.%s' % __path_to_missions['title']
    missions = load_resources(missions=True)['missions']

    for mission_id, mission in missions.items():

        mission_dest = '%s/missions/%s.pdf' % (__path_to_pdfs, mission['id'])
        json2pdf(__path_to_missions['template'], mission_dest, mission_log_suffix, {
            'type': __path_to_missions['swedish'],
            'id': mission['id'],
            'title': mission['main']['title'],
            'background': mission['main']['background'],
            'goal': mission['main']['goal'],
            'reward': mission['main']['reward'],
            'hint': mission['main']['hint']
        })

        for clue in mission['clues']:
            clue_dest = '%s/missions/%s.clues/%s.pdf' % (__path_to_pdfs, mission['id'], id_str(mission['id'], clue['id'], '_'))
            clue_log_suffix = 'generate.clues'

            json2pdf(filepath(__path_to_tex_templates,'event.tex'), clue_dest, clue_log_suffix, {
                'type': 'ledtråd',
                'id': id_str(mission['id'], clue['id']),
                'title': mission['main']['title'],
                'text': clue['text']
            })

"""
Generates the event resources as pdf documents
"""
def generate_events():
    pretty_print.important('Running %s ...' % colored(' Generate events ', 'blue', attrs=['bold', 'reverse']))
    event_log_suffix = 'generate.%s' % __path_to_events['title']
    events = load_resources(events=True)['events']

    for event_id, event in events.items():
        event_dest = '%s/events/%s.pdf' % (__path_to_pdfs, re.sub(':', '_', event_id))
        json2pdf(__path_to_events['template'], event_dest, event_log_suffix, {
            'type': __path_to_events['swedish'],
            'id': event_id,
            'title': event['title'],
            'text': event['text'],
        })

"""
Generates the drifter-mission resources as pdf documents
"""
def generate_drifters():
    pretty_print.important('Running %s ...' % colored(' Generate drifters ', 'blue', attrs=['bold', 'reverse']))
    drifter_log_suffix = 'generate.%s' % __path_to_drifters['title']
    drifters = load_resources(drifters=True)['drifters']

    for drifter_id, drifter in drifters.items():
        drifter_dest = '%s/drifters/%s.pdf' % (__path_to_pdfs, re.sub(':', '_', drifter_id))
        json2pdf(__path_to_drifters['template'], drifter_dest, drifter_log_suffix, {
            'type': __path_to_drifters['swedish'],
            'id': drifter_id,
            'title': drifter['name'],
            'text': drifter['goal'],
        })

"""
Generates the character resources as pdf documents
"""
def generate_characters():
    pretty_print.important('Running %s ...' % colored(' Generate characters ', 'blue', attrs=['bold', 'reverse']))
    character_log_suffix = 'generate.%s' % __path_to_characters['title']
    characters = load_resources(characters=True)['characters']

    for character_id, character in characters.items():
        missions_tex_blob = formatted_tex_blob(character['missions']) or 'Deltar inte i något uppdrag'  # hack
        events_tex_blob = formatted_tex_blob(character['events']) or 'Deltar inte i någon händelse'     # hack

        character_dest = '%s/characters/%s.pdf' % (__path_to_pdfs, re.sub(':', '_', character_id))
        json2pdf(__path_to_characters['template'], character_dest, character_log_suffix, {
            'id': tex_escape_underscores(character_id),
            'name': tex_escape_underscores(character['name']),
            'persona': tex_escape_underscores(character['persona']),
            'area': tex_escape_underscores(character['area']),
            'location': tex_escape_underscores(character['location']),
            'props': tex_escape_underscores(character['props']),
            'missions': missions_tex_blob,
            'events': events_tex_blob
        })

# Note: this is a POC and should not have hard-coded text in the source code
def formatted_tex_blob(listing):
    """Returns a formatted TeX-blob listing the items of the passed list"""
    sections = list()
    for item in listing:
        lines = list()
        lines.append(r'\\subsection{{ {} }}'.format(item['id']))
        lines.append(r'\\textbf{{Bakgrund:}} {} \\\\'.format(item['comment']))
        lines.append(r'\\textbf{{Reaktion:}} {}'.format(item['response']))
        sections.append('\n'.join(lines))
    return '\n'.join(sections)

def tex_escape_underscores(text):
    """Escape underscores so that TeX interpret them correctly"""
    return text.replace('_', '\_')

if __name__ == "__main__":
    main()
