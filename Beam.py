from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import numpy as np
import odbAccess
import os
from driverUtils import executeOnCaeStartup
import xyPlot
mdb.models['Model-1'].PartFromInputFile(
    inputFileName='C:/Users/Saadiq Ahmed/OneDrive - Coventry University/University/4th Year Work/Final Indiviual/Model.inp')
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p1 = mdb.models['Model-1'].parts['PART-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
mdb.models['Model-1'].Material(name='AI')
mdb.models['Model-1'].materials['AI'].Density(table=((2.71e-09, ), ))
mdb.models['Model-1'].materials['AI'].Elastic(table=((69000.0, 0.3), ))
mdb.models['Model-1'].HomogeneousShellSection(name='Section-1', 
    preIntegrate=OFF, material='AI', thicknessType=UNIFORM, thickness=1.0, 
    thicknessField='', nodalThicknessField='', 
    idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
    thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
    integrationRule=GAUSS, numIntPts=3)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['Model-1'].parts['PART-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['Model-1'].parts['PART-1']
e = p.elements
elements = e.getSequenceFromMask(mask=('[#ffffffff:4032 #1ffff ]', ), )
region = p.Set(elements=elements, name='Set-1')
p = mdb.models['Model-1'].parts['PART-1']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
    constraints=ON, connectors=ON, engineeringFeatures=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=OFF, 
    constraints=OFF, connectors=OFF, engineeringFeatures=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['PART-1']
a.Instance(name='PART-1-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
mdb.models['Model-1'].FrequencyStep(name='Step-1', previous='Initial', 
    description='ModalFrequency', limitSavedEigenvectorRegion=None, 
    numEigen=26)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=OFF)
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.Job(name='Job-2', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)
mdb.jobs['Job-2'].writeInput(consistencyChecking=OFF)
mdb.jobs['Job-2'].submit(consistencyChecking=OFF)
mdb.jobs['Job-2'].waitForCompletion()
#: The job input file "Job-2.inp" has been submitted for analysis.
#: Job Job-2: Analysis Input File Processor completed successfully.
#: Job Job-2: Abaqus/Standard completed successfully.
#: Job Job-2 completed successfully.
def Open_ODB_and_Write_NodeSet_data_to_text(model,step_name,variable_name,set_name,Variable_component):
    # open ODB file - ABAQUS Result file
    odb = session.openOdb(str(model)+'.odb')

    # list for the VARIABLE you want to evaluate
    Variable_v = []

    # analysis step for your VARIABLE
    lastStep=odb.steps[step_name]

    #loop over all increments of the analysis step and save VARIABLE information from each increment
    for x in range(len(lastStep.frames)):
        lastFrame = lastStep.frames[x]
        Variable = lastFrame.fieldOutputs[variable_name]
        center = odb.rootAssembly.nodeSets[set_name]
        centerRForce = Variable.getSubset(region=center)
       
        # loop over the VARIABLE and save component (x,y,z - 0,1,2) to list
        for i in centerRForce.values:
            Variable_vr = [i.data[Variable_component]]
            Variable_v = Variable_v + Variable_vr  
            
    # write VARIABLE - component to text file

    np.savetxt(str(variable_name)+'_'+str("frequency_analysis")+'.txt',Variable_v)
def Write_Variable_to_text(variable,variable_name):

    # list for the VARIABLE you want to evaluate
    Variable_v = [variable]
      
    # write VARIABLE - component to text file

    np.savetxt(str(variable_name)+'_'+str("frequency_analysis")+'.txt',Variable_v) 
if os.path.isfile("C:/Temp/Job-2.odb"):
    Open_ODB_and_Write_NodeSet_data_to_text("Job-2","Step-1","Mode","Assembly ASSEMBLY",2)
    Write_Variable_to_text("Mode","Eigenfrequency: EIGFREQ for Whole Model")
