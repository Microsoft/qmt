# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from qmt.task_framework import Task
from qmt.geometry import Geo1DData, Geo2DData, Geo3DData


class Geometry1D(Task):
    def __init__(self, options=None, name='geometry_1d_task'):
        """
        Builds a geometry in 1D.
        :param dict options: The dictionary specifying parts, of the form
        {"part_name":(start_coord,stop_coord)}
        :param str name: The name of this task.
        """
        super(Geometry1D, self).__init__([], options, name)

    def _solve_instance(self, input_result_list, current_options):
        """
        :param list input_result_list: This is an empty list.
        :param dict current_options: The dictionary specifying parts from above.
        :return geo_1d: A Geo1DData object.
        """
        geo_1d = Geo1DData()
        for part_name in current_options:
            geo_1d.add_part(part_name, current_options[part_name][0], current_options[part_name][1])
        return geo_1d


class Geometry2D(Task):
    def __init__(self, options=None, name='geometry_2d_task'):
        """
        Builds a geometry in 2D.
        :param dict options: The dictionary holding parts and edges. It should be of the form:
        {'parts':{'part_name':Polygon}, 'edges':{'edge_name':LineString}, where Polygon and
        LineString are instances of shapely.geometry.
        "part_name":Part3D}
        :param str name: The name of this task.
        """
        super(Geometry2D, self).__init__([], options, name)

    def _solve_instance(self, input_result_list, current_options):
        """
        :param list input_result_list: This is an empty list.
        :param dict current_options: The dictionary specification from above.
        :return: geo_2d: A Geo2DData object.
        """
        geo_2d = Geo2DData()
        for part_name in current_options['parts']:
            geo_2d.add_part(part_name, current_options['parts'][part_name])
        for edge_name in current_options['edges']:
            geo_2d.add_edge(edge_name, current_options['edges'][edge_name])
        return geo_2d


class Geometry3D(Task):
    def __init__(self, options=None, name='geometry_3d_task'):
        """
        Builds a geometry in 3D.
        :param dict options: The dictionary specifying parts and and FreeCAD infromation. It should
        be of the form {"fcname":path_to_freeCAD_file,"parts_dict":parts_dict}, where parts_dict
        is a dictionary of the form
        {part_name:Part3D}.
        :param str name: The name of this task.
        """
        super(Geometry3D, self).__init__([], options, name)
        # assert type(options["fcname"]) is str
        # assert type(options["parts_dict"]) is dict
        # for partDirective in options["part_dict"]:
        #     assert type(options["part_dict"][partDirective]) is Part3D

    def _solve_instance(self, input_result_list, current_options):
        """
        :param list input_result_list: This is an empty list.
        :param dict current_options: The dictionary specifying parts from above.
        :return geo_3d: A Geo3DData object.
        """
        pyenv = current_options['pyenv'] if 'pyenv' in current_options else 'python2'
        geo = Geo3DData()
        # fill geo with parts
        # ~ for part_name in ret['serial_parts']:
            # ~ geo.add_part(part_name, ret['serial_parts'][part_name])
        from qmt.geometry.freecad_wrapper import fcwrapper
        ret = fcwrapper(pyenv, 'build3d',
                        {'input_result_list': input_result_list,
                         'current_options': current_options})
        return geo
