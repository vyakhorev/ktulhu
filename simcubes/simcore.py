
from heapq import heappush, heappop

import logging
logger = logging.getLogger(__name__)

class cSimEnvironment:
    '''
    Our environment consists of connected asyncronious threads (behaviours).
    This class manages these threads: iterates over them to gather simulation schedule,
    activates and deactives them.
    '''

    def __init__(self):
        #self._threads = {}
        self.schedule = cSimSchedule()

    def get_the_schedule(self):
        '''
        Game engine gets the reference to the schedule from here
        and opererates directly with apply_next_tick method.
        :return: the cSimSchedule instance
        '''
        return self.schedule

    def start_a_thread(self, async_thread):
        '''
        Do the first step and schedule the first event.
        All the rest events would be scheduled with like
        a chain reaction.
        '''
        # TODO I should add something for "no more events" and "deactivate event"
        #logger.info("Starting a thread " + async_thread.__repr__())
        async_thread.set_environment(self)
        async_thread.first_step()  # this would call cSimSchedule.schedule_event


class cSimSchedule:
    '''
    Activates the scheduled events in the correct order.
    Game Engine should synchronise it's ticks with this
    schedule.
    '''

    def __init__(self):
        self._heap = []  # a heap to hold the events
        self._recent_events = []  # these eventes just happened and not visible in the game yet
        self._now = 0.0

    def get_time(self):
        return self._now

    def peek_next_event(self):
        '''
        :return: a tuple (event_time, event_priority, event_reference)
        (unpack for destoying a reference to the actual schedule)
        '''
        T, P, an_event = self._heap[0]
        return T, P, an_event

    def peek_next_timestamp(self):
        return self._heap[0][0]

    def schedule_event(self, ev):
        '''
        Schedule an event with a
        :param ev: some event with known duration
        '''
        heappush(self._heap, (self._now + ev.duration, ev.priority, ev))

    def apply_next_tick(self, until_T):
        '''
        Game engine should call this method frequently (each 0.1 seconds).
        This call 'reserves' all the events up to the moment until_T. They
        will be activated right at the moment of the call, however the game
        should synchronise them with graphical representation.
        :param until_T: simulation time, we reserve the events up to this moment.
        :return: a list with activated events (so that game engine can easily
                find all the corresponding cubes).

        ..warning:
            If some of the threads produce only zero duration events, this call
            may never end.

        ..note:
            Game engine is reponsible to INCREF and DECREF for events, they'll be
            garbage collected on the next tick, when we empty self._recent_events.

        ..note:
            Game engine should read the states from the blocks after this call,
            before the next call.
        '''

        # There can be a lot of additional things here - like events cancellations

        self._recent_events = []  # free the references
        while self.peek_next_timestamp() <= until_T:
            self._now, P, an_event = heappop(self._heap)
            #logger.info("Simulation time is incremented up to " + str(self._now))
            if not an_event.cancelled:
                # applies an event and schedules the next one
                # so after this process_step() call new events
                # are heappuched inside self._heap.
                an_event.process_step()
                self._recent_events += [an_event]
        return self._recent_events

    def apply_event_after_event(self):
        '''
        Iterative call to apply events until forced to be stoped.
        '''
        while True:
            self._now, P, an_event = heappop(self._heap)
            logger.info("Simulation time is incremented up to " + str(self._now))
            if not an_event.cancelled:
                an_event.process_step()
            yield self._now


class cAsyncThread:
    '''
    Event generator for environment, a process. May be active and
    inactive. In latter case there should be no events from this
    thread in the simulation.
    '''

    thread_count = 0

    def __init__(self):
        self.env = None  # to be set upon cSimEnvironment.start_a_thread
        self.do_schedule = None  # to be set upon cSimEnvironment.start_a_thread
        self.generator_state = None  # to be set after

    def set_environment(self, env):
        self.env = env
        self.do_schedule = lambda ev: env.schedule.schedule_event(ev)

    def run(self):
        '''
        Write logic here, generate events in any order under any rules.
        Behaviours implement state-dependent activity with external
        switch calls from events.
        '''
        is_active = True
        while is_active:
            # yield any cEvent here, timeout is obligatory
            raise NotImplemented

    def first_step(self):
        '''
        Environment does the first step, events do the rest steps.
        '''
        self.generator_state = self.run()
        self.step()

    def step(self):
        '''
        A technical call to schedule the next event. First time it is called from the
        environment to schedule the first event. After that this is called
        from event upon finishig.
        '''
        # TODO: error catching
        # print(next(self.generator_state))
        self.do_schedule(next(self.generator_state))


# Events

class cEvent:
    '''
    Base event class. Useful aslo as a timeout.
    All the priorities should be diffrent, depending on the
    event class. The lower the value, the higher is the priority.
    This sets execution order.
    '''

    priority = 10

    def __init__(self, beh, duration):
        self.beh = beh
        self.duration = duration
        # a way to cancel events (after block destruction for example)
        self.cancelled = False

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def process_step(self):
        '''
        This thing is call from the schedule to complete an event.
        Behaviour inherits cAsyncThread. It has a generator run()
        that produce events. As soon as this event is applied
        we should step further and schedule next event (afterwards,
        this event would be garbage collected and new event would
        do the same in it's turn.

        So the next event is scheduled right after the previous one
        is applied
        '''
        self.apply()
        self.beh.step()

    def apply(self):
        '''
        Change the self.beh state here. ?Or pass a callback here.
        '''
        pass