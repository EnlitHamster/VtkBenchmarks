from vtk import *
from time import perf_counter
from Introspector import Introspector

import os

# str -> long
time_execution_data = {}


def timed_execution(name, func, args = ()):
    t_start = perf_counter()
    r = func(*args)
    time_execution_data[name] = perf_counter() - t_start
    return r


def main():
    introspector = timed_execution("introspector_inst", Introspector)

    reader = timed_execution("reader_inst", introspector.createVtkObject, ("vtkStructuredGridReader",))
    timed_execution("reader_setfile", introspector.setVtkObjectAttribute, (reader, "FileName", "s", "density.vtk"))
    timed_execution("reader_update", introspector.updateVtkObject, (reader,))

    seeds = timed_execution("seeds_inst", introspector.createVtkObject, ("vtkPointSource",))
    timed_execution("seeds_setradius", introspector.setVtkObjectAttribute, (seeds, "Radius", "f", 3.0))
    output = timed_execution("reader_getoutput", introspector.vtkInstanceCall, (reader, "GetOutput", ()))
    center = timed_execution("reader_getcenter", introspector.genericCall, (output, "GetCenter", ()))
    timed_execution("seeds_setcenter", introspector.setVtkObjectAttribute, (seeds, "Center", "f3", introspector.outputFormat(center)))
    timed_execution("seeds_setnumberofpoints", introspector.setVtkObjectAttribute, (seeds, "NumberOfPoints", "d", 100))

    streamer = timed_execution("streamer_inst", introspector.createVtkObject, ("vtkStreamTracer",))
    reader_port = timed_execution("reader_getoutputport", introspector.getVtkObjectOutputPort, (reader,))
    seeds_port = timed_execution("seeds_getoutputport", introspector.getVtkObjectOutputPort, (seeds,))
    timed_execution("streamer_setinputconn", introspector.vtkInstanceCall, (streamer, "SetInputConnection", (reader_port,)))
    timed_execution("streamer_setsourceconn", introspector.vtkInstanceCall, (streamer, "SetSourceConnection", (seeds_port,)))
    timed_execution("streamer_setmaxpropagation", introspector.setVtkObjectAttribute, (streamer, "MaximumPropagation", "d", 1000))
    timed_execution("streamer_setinitialintegstep", introspector.setVtkObjectAttribute, (streamer, "InitialIntegrationStep", "f", .1))
    timed_execution("streamer_setintegdirboth", introspector.vtkInstanceCall, (streamer, "SetIntegrationDirectionToBoth", ()))

    outline = timed_execution("outline_inst", introspector.createVtkObject, ("vtkStructuredGridOutlineFilter",))
    timed_execution("outline_setinputconn", introspector.vtkInstanceCall, (outline, "SetInputConnection", (reader_port,)))


if __name__ == '__main__':
    timed_execution("main", main)

    dump_exists = os.path.isfile("./dump_introspection_py.csv")
    

    with open("dump_introspection_py.csv", "a" if dump_exists else "w") as f:
        if not dump_exists:
            for name in time_execution_data:
                f.write(name + ",")
            f.write("\n")
            f.flush()

        for name in time_execution_data:
            f.write(f"{time_execution_data[name]},")
        f.write("\n")
        f.flush()
        f.close()