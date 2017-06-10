
'''
Test the simulation calls
'''

# TODO: we need better tests, asyncio would be helpful

import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    from misc import lg
    lg.config_logging()

    from simcubes.simcore import cSimEnvironment
    from levelgenerator.plain import generate_simple_conveyor_system
    from simcubes.basebehaviour import iter_threads_in_holders
    from misc.exec import realtime_batch_simulation_cycle, one_time_simulation


    # create simulation schedule
    env = cSimEnvironment()
    # spawn a blooming grass plane
    level = generate_simple_conveyor_system()
    # activate the threads in the environment
    for thr_i in iter_threads_in_holders(level.iter_over_blocks()):
        env.start_a_thread(thr_i)
    # Start a simulation cycle with batch ticks
    # Two variants implemented:

    realtime_batch_simulation_cycle(env, 10)
    # one_time_simulation(env, 4)








