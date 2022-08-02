#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Simple tutorial for layout
"""
import layout_3d.optimization.voxel as voxel_opt
import layout_3d.voxel as voxel
import volmdlr as vm
import volmdlr.primitives3d as primitives3d
from dessia_api_client.users import PlatformUser
from pathlib import Path

DIR = Path(__file__).resolve().parent

bx0 = primitives3d.Block(
    vm.Frame3D(vm.Point3D(0, 0, 0), vm.Vector3D(0.3, 0, 0), vm.Vector3D(0, 0.3, 0), vm.Vector3D(0, 0, 0.3)),
    color=(0.5546875, 0.66015625, 0.85546875), alpha=0.6)

shell0 = vm.faces.ClosedShell3D(bx0.faces)
shell0.alpha = 0.3
shell0.color = (92 / 255, 124 / 255, 172 / 255)

bx1 = primitives3d.Block(
    vm.Frame3D(vm.Point3D(0, 0, 0), vm.Vector3D(0.17, 0, 0), vm.Vector3D(0, 0.17, 0), vm.Vector3D(0, 0, 0.17)),
    color=(0.1, 0.1, 0.1), alpha=0.6)
shell1 = vm.faces.ClosedShell3D(bx1.faces)
shell1.alpha = 0.3
shell1.color = (92 / 255, 124 / 255, 172 / 255)


# generer une g
available_box = voxel.AvailableBox(outer_primitive=shell0,
                                    inner_primitives=[shell1],
                                    number_level=2,
                                    number_block_x=5,
                                    number_block_y=3,
                                    number_block_z=3)

# print(dir(available_box))

P1 = vm.Frame3D(vm.Point3D(0, 0, 0), vm.Point3D(0.6, 0, 0), vm.Point3D(0, 0.6, 0), vm.Point3D(0, 0, 0.6))
P2 = vm.Frame3D(vm.Point3D(0, 0.6, 0), vm.Point3D(0.6, 0, 0), vm.Point3D(0, 0.6, 0), vm.Point3D(0, 0, 1.8))
block1 = primitives3d.Block(P1)
block2 = primitives3d.Block(P2)
block3 = block2.union(block1)
# block3[0].babylonjs()
# print(dir(block3[0]))

object = block3[0].frame_mapping(vm.Frame3D(vm.Point3D(0, 0, 0),
                                          vm.Vector3D(0.06, 0, 0),
                                          vm.Vector3D(0, 0.06, 0),
                                          vm.Vector3D(0, 0, 0.06)), 'old')

# print('frame_mapping :', (vm.faces.ClosedShell3D.frame_mapping).__doc__)
# object.babylonjs()
object.alpha = 0.3
object.color = (92 / 255, 124 / 255, 172 / 255)


# @créer un vol à partir de available_box(ext), comportant l'objet 'object'
component_box = voxel.ComponentBox(available_box=available_box,
                                    primitive_input=object)
# print(dir(component_box))

component_boxes = voxel.ComponentBoxes(component_boxes=[component_box])

generator = voxel_opt.Generator(available_box=available_box,
                                 combination_component_boxes=[component_boxes])

cluster_selections = generator.generate_all_cluster()


cluster_selections = generator.selection_clusters(cluster_combinations=cluster_selections)

for cluster_selection in cluster_selections:
    cluster_selection1 = generator.refine_all_cluster(cluster_combination=cluster_selection)


basis = voxel.AllBasis.genere()
for i, basic in enumerate(basis.all_basis[0:10]):
    component_box = voxel.ComponentBox(available_box=available_box,
                                       primitive_input=object,
                                       new_basis=basic)
    component_boxes = voxel.ComponentBoxes(component_boxes=[component_box])
    generator = voxel_opt.Generator(available_box=available_box,
                                    combination_component_boxes=[component_boxes])
    try:
        cluster_selections = generator.generate_all_cluster()
        cluster_selections = generator.selection_clusters(cluster_combinations=cluster_selections)

        for cluster_selection in cluster_selections:
            cluster_selection1 = generator.refine_all_cluster(cluster_combination=cluster_selection)
            #cluster_selection1.babylonjs()

            # print(dir(cluster_selection1))
            cluster_selection1.save_babylonjs_to_file(filename='file')
    except:
        print('no cluster for {} rotation'.format(i))


# c = PlatformUser(api_url='https://api.testing.dessia.ovh/')
# r = c.objects.create_object_from_python_object(available_box)





