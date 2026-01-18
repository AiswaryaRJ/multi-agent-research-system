from planner import planner_agent
from search_agent import search_agent
from writer_agent import writer_agent

class PlannerTool:
    @staticmethod
    def run(topic: str):
        return planner_agent(topic)

class SearchTool:
    @staticmethod
    def run(question: str):
        return search_agent(question)

class WriterTool:
    @staticmethod
    def run(topic: str, search_results: list, batch_size: int = 3):
        # batch_size can be used if you want to process in chunks
        return writer_agent(topic, search_results)

planner_tool = PlannerTool()
search_tool = SearchTool()
writer_tool = WriterTool()
