from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData
import time


def process_agent_data(agent_data: AgentData) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
    agent_data (AgentData): Agent data that contains accelerometer, GPS, and timestamp.
    Returns:
    processed_data (ProcessedAgentData): Processed data containing the classified state of
    the road surface and agent data.
    """
    state = "incorrectly entered data"
    if agent_data.accelerometer.z >= 17000:
        state = "good"
    elif 16000 < agent_data.accelerometer.z <= 17000:
        state = "within limits"
    elif agent_data.accelerometer.z <= 16000:
        state = "bad"
    time.sleep(1)
    return ProcessedAgentData(road_state=state,
                              agent_data=AgentData(accelerometer=agent_data.accelerometer,
                                                   gps=agent_data.gps,
                                                   timestamp=agent_data.timestamp))
