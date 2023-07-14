import datetime
import pm4py
import pandas as pd

# log = pm4py.write_ocel2_sqlite(ocel, '<path_to_export_to>')

class Event:
    """
    A Class for storing information about a single event.
    """
    def __init__(self, event_id, timestamp, activity, duration, summary, items_text, items_image) -> None:
        self.event_id = event_id
        self.timestamp = timestamp
        self.activity = activity
        self.duration = duration
        self.summary = summary
        self.items_text = items_text
        self.items_image = items_image
        

class EventLog:
    """
    A Class for storing the event log information, creating the OCEL and exporting to CSV.
    """
    def __init__(self):
        self.events = []
    
    def add_event(self, event: Event):
        self.events.append(event)
    
    def remove_event(self, event_id):
        self.events = [event for event in self.events if event.event_id != event_id]
     
    def get_events(self):
        return self.events
    
    def create_dataframe(self):
        """
        Returns a DataFrame for creating the OCEL using pm4py
        """
        event_ids = []
        timestamps = []
        activities = []
        durations = []
        summaries = []
        items_texts = []
        items_images = []
        for ev in self.events:
            event_ids.append(ev.event_id)
            timestamps.append(ev.timestamp)
            activities.append(ev.activity)
            durations.append(ev.duration)
            summaries.append(ev.summary)
            items_texts.append(ev.items_text)
            items_images.append(ev.items_image)
        df = pd.DataFrame(data={'ocel:eid':event_ids , 'time:timestamp':timestamps, 'ocel:activity':activities, 'duration':durations, 'summary':summaries, 
                       'items_text':items_texts, 'items_image':items_images})
        # print(df)
        return df
    
    def create_ocel(self):
        # pm4py.convert.convert_log_to_ocel(log: Union[EventLog, EventStream, DataFrame], activity_column: str = 'concept:name', timestamp_column: str = 'time:timestamp', 
#                                   object_types: Optional[Collection[str]] = None, 
#                                   obj_separator: str = ' AND ', additional_event_attributes: Optional[Collection[str]] = None) → OCEL
        return pm4py.convert.convert_log_to_ocel(log = self.create_dataframe(), activity_column = 'ocel:activity', timestamp_column = 'time:timestamp', 
                                    object_types = ['items_text', 'items_image'], 
                                    obj_separator = ' AND ', additional_event_attributes = ['ocel:eid','duration','summary'])
        

    def save_OCEL_standard(self, file_name='ocel_test_33.csv'):
        """
        Writes to CSV
        """
        pm4py.write.write_ocel_csv(self.create_ocel(), f'./logs/events/{file_name}', f'./logs/objects/{file_name}')
        # pm4py.write.write_ocel_csv(self.create_ocel(), 'ocel_test.csv', 'ocel_test_cd.csv')




# ev = Event(1,'4.56','making',8,'good text', 'text2', 'text1')

# log = EventLog()
# log.add_event(ev)
# obj = log.create_ocel()
# print(obj)
# print(obj.get_extended_table())
# log.save_OCEL_standard()
# print(log.save_OCEL_standard())
