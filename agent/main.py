from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
import uuid
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from agent.tools.rag import VectorStoreRetriever, load_data
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from agent.agent import Assistant, State
from agent.utils import create_tool_node_with_fallback, _print_event


from agent.tools.bookings import BookingManager
import openai
from langchain_core.tools import tool

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph.message import AnyMessage, add_messages


docs = load_data("static/plumber.txt")

retriever = VectorStoreRetriever.from_docs(docs, openai.Client())

@tool
def lookup_policy(query: str) -> str:
        """Consult the company policies to check whether certain options are permitted.
        Use this before making any booking changes performing other 'write' events.
        You can also get information about FAQs, services offered by the company along with their pricing details and other general information
        """
        docs = retriever.query(query, k=2)
        return "\n\n".join([doc["page_content"] for doc in docs])


booking_manager = BookingManager("business_bookings.db")



llm = ChatGroq(model="llama3-groq-70b-8192-tool-use-preview", temperature=0.3)

primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful customer support assistant for {company_name}. "
            " Use the provided tools to make and manage a user's bookings, search company services, faqs and policies, and other information to assist the user's queries. "
            " When searching, be persistent. Expand your query bounds if the first search returns no results. "
            " If a search comes up empty, expand your search before giving up."
            "\n\nCurrent user:\n<User>\n{user_info}\n</User>"
            "\nCurrent time: {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

part_1_tools = [
    TavilySearchResults(max_results=1),
    lookup_policy,
    booking_manager.fetch_user_bookings,
    booking_manager.create_booking,
    booking_manager.update_booking_status,
    booking_manager.update_booking_date,
    booking_manager.update_booking_service,
    booking_manager.cancel_booking,
]
part_1_assistant_runnable = primary_assistant_prompt | llm.bind_tools(part_1_tools)

builder = StateGraph(State)


# Define nodes: these do the work
builder.add_node("assistant", Assistant(part_1_assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(part_1_tools))
# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
memory = SqliteSaver.from_conn_string(":memory:")
part_1_graph = builder.compile(checkpointer=memory)



thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        # The passenger_id is used in our flight tools to
        # fetch the user's flight information
        "booking_id": 2,
        "company_name": "Bob the Builder Warehouses",
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}

_printed = set()

# while True:
#     question = input("User: ")
#     if question == "exit":
#         break
#     events = part_1_graph.stream(
#         {"messages": ("user", question)}, config, stream_mode="values"
#     )
#     for event in events:
#         _print_event(event, _printed)