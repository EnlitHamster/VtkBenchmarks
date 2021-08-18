from vtk import *
from time import perf_counter

import os

# str -> long
time_execution_data = {}


def timed_execution(name, func, args = ()):
    t_start = perf_counter()
    r = func(*args)
    time_execution_data[name] = perf_counter() - t_start
    return r


def main():
    reader = timed_execution("reader_inst", vtkStructuredGridReader)
    timed_execution("reader_setfile", reader.SetFileName, ("density.vtk",))
    timed_execution("reader_update", reader.Update)

    seeds = timed_execution("seeds_inst", vtkPointSource)
    timed_execution("seeds_setradius", seeds.SetRadius, (3.0,))
    output = timed_execution("reader_getoutput", reader.GetOutput)
    center = timed_execution("output_getcenter", output.GetCenter)
    timed_execution("seeds_setcenter", seeds.SetCenter, (center,))
    timed_execution("seeds_setnumberofpoints", seeds.SetNumberOfPoints, (100,))

    streamer = timed_execution("streamer_inst", vtkStreamTracer)
    reader_port = timed_execution("reader_getoutputport", reader.GetOutputPort, (0,))
    seeds_port = timed_execution("seeds_getoutputport", seeds.GetOutputPort, (0,))
    timed_execution("streamer_setinputconn", streamer.SetInputConnection, (reader_port,))
    timed_execution("streamer_setsourceconn", streamer.SetSourceConnection, (seeds_port,))
    timed_execution("streamer_setmaxpropagation", streamer.SetMaximumPropagation, (1000,))
    timed_execution("streamer_setinitialintegstep", streamer.SetInitialIntegrationStep, (.1,))
    timed_execution("streamer_setintegdirboth", streamer.SetIntegrationDirectionToBoth)

    outline = timed_execution("outline_inst", vtkStructuredGridOutlineFilter)
    timed_execution("outline_setinputconn", outline.SetInputConnection, (reader_port,))


if __name__ == '__main__':
    timed_execution("main", main)

    dump_exists = os.path.isfile("./dump_native_py.csv")

    with open("dump_native_py.csv", "a" if dump_exists else "w") as f:
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