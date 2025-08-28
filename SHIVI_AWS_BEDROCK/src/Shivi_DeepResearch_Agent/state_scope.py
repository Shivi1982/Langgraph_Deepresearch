# using writefile which is a jupyter magic command to write the contents of the cell to a file. 
# the benefit is that we can call this function from any notebook. so state.py is the file
#  that is created in src/Shivi_DeepResearch_Agent/ & can be imported from any notebook. 

"""State Definitions and Pydantic Schemas for Research Scoping.

This defines the state objects and structured schemas used for
the research agent scoping workflow, including researcher state management and output schemas.
"""

import operator
from typing_extensions import Optional, Annotated, List, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

# ===== STATE DEFINITIONS =====

class AgentInputState(MessagesState):
    """What the agent receives initially (just user conversation).
    Only messages from user interaction"""
    pass

class AgentState(MessagesState):
    """
    Main state for the full multi-agent research system.
    
    Everything accumulated during the research process
    Note: Some fields are duplicated across different state classes for proper
    state management between subgraphs and the main workflow.
    """

    # The focused research question generated from user input from AgentInputState above 
    research_brief: Optional[str]
    # Messages exchanged with the supervisor agent for coordination. Internal agent-to-agent communication, this means each
    #call is a new call to an LLM 
    supervisor_messages: Annotated[Sequence[BaseMessage], add_messages]
    # Raw unprocessed research notes collected during the research phase
    raw_notes: Annotated[list[str], operator.add] = []
    # Processed and structured notes ready for report generation
    notes: Annotated[list[str], operator.add] = []
    # Final formatted research report
    final_report: str

# ===== STRUCTURED OUTPUT SCHEMAS =====

class ClarifyWithUser(BaseModel):
    """Schema for user clarification decision and questions."""
    
    need_clarification: bool = Field(
        description="Whether the user needs to be asked a clarifying question.",
    )
    question: str = Field(
        description="A question to ask the user to clarify the report scope",
    )
    verification: str = Field(
        description="Verify message that we will start research after the user has provided the necessary information.",
    )

class ResearchQuestion(BaseModel):
    """Schema for structured research brief generation, this is how the output should be generated."""
    
    research_brief: str = Field(
        description="A research question that will be used to guide the research.",
    )
