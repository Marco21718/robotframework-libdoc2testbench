#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os.path
import enum
from datetime import datetime

from robot.utils import WINDOWS, XmlWriter, unicode


class Element_Types(enum.Enum):
    subdivision = 'subdivision'
    datatype = 'datatype'
    interaction = 'interaction'
    condition = 'condition'


class Project_States(enum.Enum):
    planned = 'planned'
    active = 'active'
    finished = 'finished'
    closed = 'closed'


class PK_Generator():
    def __init__(self, pk_start: int = 230):
        self.pk_counter = pk_start
    # TODO: maybe insert here logic to get pk for specific objects

    def get_pk(self):
        self.pk_counter += 1
        return str(self.pk_counter)


class Element():
    all_elements = {}

    def __init__(self, pk_generator: PK_Generator, element):
        self.pk = pk_generator.get_pk()
        self.name = element.name
        self.desc = element.doc
        self.hmtl_desc = self.desc
        Element.all_elements[self.name] = self.pk

class Data_Type(Element):

    def __init__(self, pk_generator: PK_Generator, data_type):
        super().__init__(pk_generator, data_type)
        self.members = data_type.members
        self.type = data_type.type
        # self.equivalence_classes = self._get_equivalence_classes()



class Libdoc2TestBenchWriter:
    pk_generator = PK_Generator()

    project_name = 'RF Import'
    testobject_name = 'RF Import'
    testobject_state = Project_States.active.value
    testobject_desc = "RF import generated via Libdoc2TestBench.py"
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z") + \
        ' +0100'

    project_settings = {
        'overwrite-exec-responsible': 'false',
        'optional-checkin': 'false',
        # 'hide-exec-auto-checkin': 'false',
        'filter-sync-interval': '30',
        'ignore-not-edited': 'false',
        'ignore-not-planned': 'true',
        'designers-may-manage-baselines': 'false',
        'designers-may-import-baselines': 'false',
        'only-admins-manage-udfs': 'false',
        'variants-management-enabled': 'false'
    }

    def write(self, libdoc, outfile):
        writer = XmlWriter(outfile, usage='Libdoc spec')
        self._write_start(libdoc, writer)
        self._write_testobjectversion(libdoc, writer)
        self._write_data_types(libdoc.data_types, writer)
        self._write_interactions(libdoc.keywords, writer)
        # self._write_keywords('inits', 'init', libdoc.inits, libdoc.source, writer)
        # self._write_keywords('keywords', 'kw', libdoc.keywords, libdoc.source, writer)
        # self._write_data_types(libdoc.data_types, writer)
        self._write_end(writer)

    def _write_start(self, libdoc, writer):
        # generated = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
        # attrs = {'name': libdoc.name,
        #          'type': libdoc.type,
        #          'format': libdoc.doc_format,
        #          'scope': libdoc.scope,
        #          'generated': generated,
        #          'specversion': '3'}
        # self._add_source_info(attrs, libdoc, writer.output)

        # TODO: Values for attributes
        writer.start('project-dump', {
            'version': "2.6.1",
            'build-number': "201215/dcee",
            'repository': "itba"
        })
        writer.start('details')
        writer.element('name', self.project_name)
        writer.element('id', '')
        writer.element('testobjectname', self.testobject_name)
        writer.element('state', self.testobject_state)
        for tag in ['customername', 'customeradress', 'contactperson', 'testlab', 'checklocation', 'startdate', 'enddate']:
            writer.element(tag, '')
        writer.element('status', self.testobject_state)
        writer.element('description', self.testobject_desc)
        writer.element('html-description', '')
        writer.element('testingIntelligence', 'false')
        writer.element('createdTime', self.created_time)
        writer.start('settings')
        for key, value in self.project_settings.items():
            writer.element(key, value)
        writer.end('settings')
        for tag in ['requirement-repositories', 'requirement-projects', 'requirement-udfs']:
            writer.element(tag, '')
        writer.end('details')

        writer.element('userroles', '')
        writer.element('keywords', '')  # TODO: XSD?
        # TODO xsd <-> tb more strict public/private needs to be there
        writer.start('labels')
        for tag in ['public', 'private']:
            writer.element(tag, '')
        writer.end('labels')
        writer.element('references', '')  # TODO XSD?
        writer.start('testobjectversions')

    def _write_testobjectversion(self, libdoc, writer):
        testobjectversion_tags = {
            'pk': '38243',
            'id': 'RF Import',
            'startdate': '2021-03-01',
            'enddate': '',
            'status': self.testobject_state,
            'createdTime': self.created_time,
            'description': 'Robot Framework import',
            'html-description': '',
            'testingIntelligence': 'false',
            'baselines': '',
            'placeholders': '',
            'variantsDefinitions': '',
            'variantsMarkers': '',
            'placeholderValues': '',
            'testcycles': '',
            'testthemes': ''
        }

        writer.start('testobjectversion')
        for key, value in testobjectversion_tags.items():
            writer.element(key, value)

        writer.start('test-elements')
        writer.start('element', {'type': Element_Types.subdivision.value})
        writer.element('pk', self.pk_generator.get_pk())
        writer.element('name', 'RF')
        #writer.element('uid', 'itba-SD-221')
        writer.element('locker', '')
        writer.element('description', 'Robot Framework test elements import')
        writer.element('html-description', '')
        writer.element('historyPK', '221')
        writer.element('identicalVersionPK', '-1')
        writer.element('references', '')  # min occurs = 0

        writer.start('element', {'type': Element_Types.subdivision.value})
        writer.element('pk', self.pk_generator.get_pk())
        writer.element('name', libdoc.name)
        #writer.element('uid', 'itba-SD-222')
        writer.element('locker', '')
        writer.element('description', libdoc.doc)
        writer.element('html-description', '')
        writer.element('historyPK', '-1')
        writer.element('identicalVersionPK', '-1')
        writer.element('references', '')

    def _write_interactions(self, keywords, writer):
        # TODO: Keywords -> Interactions
        keyword = keywords[1]
        attris = vars(keyword)
        #print(', '.join("%s: %s" % item for item in attris.items()))

        for keyword in keywords:
            writer.start('element', {'type': Element_Types.interaction.value})
            writer.element('pk', self.pk_generator.get_pk())
            writer.element('name', keyword.name)
            writer.element('locker', '')
            writer.element('description', keyword.doc)
            writer.element('html-description', '')
            writer.element('historyPK', '-1')
            writer.element('identicalVersionPK', '-1')
            writer.element('references', '')
            writer.end('element')

    def _write_data_types(self, data_types, writer):
        # TODO
        datatype = data_types.enums[0]
        attris = vars(datatype)
        print(', '.join("%s: %s" % item for item in attris.items()))

        for data_type in data_types.enums:
            Data_Type(self.pk_generator, data_type)

    def _add_source_info(self, attrs, item, outfile, lib_source=None):
        if item.source and item.source != lib_source:
            attrs['source'] = self._format_source(item.source, outfile)
        if item.lineno > 0:
            attrs['lineno'] = str(item.lineno)

    def _format_source(self, source, outfile):
        if not os.path.exists(source):
            return source
        source = os.path.normpath(source)
        if not (hasattr(outfile, 'name')
                and os.path.isfile(outfile.name)
                and self._on_same_drive(source, outfile.name)):
            return source
        return os.path.relpath(source, os.path.dirname(outfile.name))

    def _on_same_drive(self, path1, path2):
        if not WINDOWS:
            return True
        return os.path.splitdrive(path1)[0] == os.path.splitdrive(path2)[0]

    def _get_old_style_scope(self, libdoc):
        if libdoc.type == 'RESOURCE':
            return ''
        return {'GLOBAL': 'global',
                'SUITE': 'test suite',
                'TEST': 'test case'}[libdoc.scope]

    # def _write_keywords(self, list_name, kw_type, keywords, lib_source, writer):
    #     writer.start(list_name)
    #     for kw in keywords:
    #         attrs = self._get_start_attrs(kw, lib_source, writer)
    #         writer.start(kw_type, attrs)
    #         self._write_arguments(kw, writer)
    #         writer.element('doc', kw.doc)
    #         writer.element('shortdoc', kw.shortdoc)
    #         if kw_type == 'kw' and kw.tags:
    #             self._write_tags(kw.tags, writer)
    #         writer.end(kw_type)
    #     writer.end(list_name)

    def _write_tags(self, tags, writer):
        writer.start('tags')
        for tag in tags:
            writer.element('tag', tag)
        writer.end('tags')

    def _write_arguments(self, kw, writer):
        writer.start('arguments', {'repr': unicode(kw.args)})
        for arg in kw.args:
            writer.start('arg', {'kind': arg.kind,
                                 'required': 'true' if arg.required else 'false',
                                 'repr': unicode(arg)})
            if arg.name:
                writer.element('name', arg.name)
            for type_repr in arg.types_reprs:
                writer.element('type', type_repr)
            if arg.default is not arg.NOTSET:
                writer.element('default', arg.default_repr)
            writer.end('arg')
        writer.end('arguments')

    def _get_start_attrs(self, kw, lib_source, writer):
        attrs = {'name': kw.name}
        if kw.deprecated:
            attrs['deprecated'] = 'true'
        self._add_source_info(attrs, kw, writer.output, lib_source)
        return attrs

    # def _write_data_types(self, data_types, writer):
    #     writer.start('datatypes')
    #     if data_types.enums:
    #         writer.start('enums')
    #         for enum in data_types.enums:
    #             writer.start('enum', {'name': enum.name})
    #             writer.element('doc', enum.doc)
    #             writer.start('members')
    #             for member in enum.members:
    #                 writer.element('member', attrs=member)
    #             writer.end('members')
    #             writer.end('enum')
    #         writer.end('enums')
    #     if data_types.typed_dicts:
    #         writer.start('typeddicts')
    #         for typ_dict in data_types.typed_dicts:
    #             writer.start('typeddict', {'name': typ_dict.name})
    #             writer.element('doc', typ_dict.doc)
    #             writer.start('items')
    #             for item in typ_dict.items:
    #                 if item['required'] is None:
    #                     item.pop('required')
    #                 elif item['required']:
    #                     item['required'] = 'true'
    #                 else:
    #                     item['required'] = 'false'
    #                 writer.element('item', attrs=item)
    #             writer.end('items')
    #             writer.end('typeddict')
    #         writer.end('typeddicts')
    #     writer.end('datatypes')

    def _write_end(self, writer):
        writer.end('element')  # close Library Subdivision
        writer.end('element')  # close RF Subdivision
        writer.end('test-elements')
        writer.end('testobjectversion')
        writer.end('testobjectversions')
        writer.element('requirements', '')
        writer.start('referenced-user-names')
        writer.end('referenced-user-names')
        writer.element('errors', '')
        writer.element('warnings', '')
        writer.end('project-dump')
        writer.close()
