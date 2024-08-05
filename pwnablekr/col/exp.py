import angr, claripy

def main():
    def getFuncAddress(funcName, plt=None):
            found = [
                addr for addr,func in cfg.kb.functions.items()
                if funcName == func.name and (plt is None or func.is_plt == plt)
                ]
            if len( found ) > 0:
                print(f"Found {funcName}'s address at {hex(found[0])}!")
                return found[0]
            else:
                raise Exception(f"No address found for function : {funcName}")

    project = angr.Project('col', auto_load_libs = False)

    cfg = project.analyses.CFG(fail_fast=True)

    system_add = getFuncAddress("system")

    argv = [project.filename]

    input_len = 20
    flag_chars = [claripy.BVS('flag_%d' % i, 8) for i in range(input_len)]
    flag = claripy.Concat(*flag_chars)

    argv.append(flag)

    state = project.factory.entry_state(args=argv)

    # Use only writable chars for semplicity
    for k in flag_chars:
        state.solver.add(k < 0x7f)
        state.solver.add(k > 0x20)
    
    sm = project.factory.simulation_manager(state)

    sm = sm.explore(find=system_add)

    if sm.found:
        input_value = sm.found[0].solver.eval(flag,cast_to=bytes)
        print(f"Found value: {input_value}")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
