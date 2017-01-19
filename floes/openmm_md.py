from __future__ import unicode_literals
"""
Copyright (C) 2016 OpenEye Scientific Software
"""
from floe.api import WorkFloe, OEMolIStreamCube, FileOutputCube, DataSetInputParameter, FileInputCube
from OpenMMCubes.cubes import OpenMMComplexSetup, OpenMMSimulation

job = WorkFloe("RunOpenMMSimulation")

job.description = """
**Run a OpenMM Simulation**

Check out the awesome stuff at the [OpenMM website](http://openmm.org)
"""

job.classification = [
    ["OpenEye", "OpenMM"],
]
job.tags = [tag for lists in job.classification for tag in lists]

ifs = OEMolIStreamCube("ifs")
ifs.promote_parameter("data_in", promoted_name="ifs", description="complex pdb file")

md_sim = OpenMMSimulation('md_sim')
md_sim.promote_parameter('state', promoted_name='state')
md_sim.promote_parameter('system', promoted_name='system')
md_sim.promote_parameter('complex_pdb', promoted_name='complex_pdb')

state_save = FileOutputCube('state_save')
state_save.set_parameters(name="state.xml.xz")

ofs = FileOutputCube('ofs')
ofs.set_parameters(name='simulation.log')

job.add_cubes(ifs, md_sim, ofs, state_save)
ifs.success.connect(md_sim.intake)
md_sim.success.connect(ofs.intake)
md_sim.checkpoint.connect(state_save.intake)

if __name__ == "__main__":
    job.run()
