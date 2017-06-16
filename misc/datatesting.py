'''
These classes help to log data during simulation. Very handy for testing.
'''

import pandas as pd

from simcubes.simcore import cAsyncThread, cEvent


class cSimPeriodicObserver(cAsyncThread):
    '''
    A separate async thread that logs something specific.
    '''

    def __init__(self, target, sim_results, period=1):
        super().__init__()
        self.period = period
        self.target = target
        self.target_repr = str(target)
        self.sim_results = sim_results  # a link to cSimulationResultsContainer

    def full_name(self):
        return self.target_repr

    def run(self):
        while True:
            self.observe_data()
            yield cEvent(self, self.period)

    def observe_data(self):
        ts_name = "abstract"
        ts_value = 0
        self.record_data(ts_name, ts_value)
        raise NotImplementedError("implement please (you may record multiple time series here)")

    def record_data(self, ts_name, ts_value):
        # Do not record the same data twice - they are aggregated in pandas, though.. Never tested.
        self.sim_results.add_ts_point(self.full_name(), ts_name, self.get_time(), ts_value)


class cSimulationResultsContainer:
    def __init__(self):
        self.ts_dict = {}

    def __repr__(self):
        s = "c_simulation_results_container:" + "\n"
        for k_obs_i in self.ts_dict.keys():
            s += "--data from " + k_obs_i + "\n"
            ts_i = self.ts_dict[k_obs_i]
            for k_ts_i in ts_i.keys():
                s += "----data of " + k_ts_i + "\n"
                s += ts_i[k_ts_i].__repr__()
        return s

    def add_ts_point(self, observer_name, ts_name, timestamp, value):
        '''
        Entry point for observer

        :param observer_name: observer's name
        :param ts_name: the name of timeseries we are evaluating
        :param timestamp: timestamp of simulation
        :param value: value of the timeseries
        '''
        if not (observer_name in self.ts_dict):
            self.ts_dict[observer_name] = dict()
        if not (ts_name in self.ts_dict[observer_name]):
            self.ts_dict[observer_name][ts_name] = cFastTS()
        self.ts_dict[observer_name][ts_name].add_obs(timestamp, value)

    def get_sim_results(self, observer_name, ts_name):
        try:
            return self.ts_dict[observer_name][ts_name]
        except KeyError:
            return None

    def get_available_names(self):
        my_keys = []
        for k1 in self.ts_dict.keys():
            for k2 in self.ts_dict[k1]:
                my_keys.append([k1, k2])
        return my_keys

    def get_dataframe(self, observer_name, variable_name):
        datas_4_pandas = {}
        datas_4_pandas[observer_name + "->" + variable_name] = self.get_sim_results(observer_name, variable_name).return_series()
        df = pd.DataFrame(datas_4_pandas)
        return df

    def do_plot(self):
        import matplotlib
        for obs_name, var_name in self.get_available_names():
            df = self.get_dataframe(obs_name, var_name)
            df.plot()
        matplotlib.pyplot.show()


class cFastTS:
    '''
    Simulation runtime data accumulator with transformation into pandas series
    '''
    def __init__(self):
        self.timestamps = []
        self.values = []

    def __repr__(self):
        s = "c_fast_ts:" + "\n"
        for k in range(0, len(self.timestamps)):
            s += str(self.timestamps[k]) + " : " + str(self.values[k]) + "\n"
        return s

    def __len__(self):
        return len(self.timestamps)

    def add_obs(self, timestamp, value):
        self.timestamps.append(timestamp)
        self.values.append(value)

    def return_series(self):

        tempdict = {}
        for k in range(0, len(self.values)):

            d = self.timestamps[k]
            if d in tempdict:
                tempdict[d] += self.values[k]
            else:
                tempdict[d] = self.values[k]
        panda_series = pd.Series(tempdict)
        return panda_series