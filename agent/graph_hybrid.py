import dspy
from typing import TypedDict, List, Dict, Any, Literal
from langgraph.graph import StateGraph, END
from agent.rag.retrieval import Retriever
from agent.tools.sqlite_tool import SQLiteTool
from agent.dspy_signatures import RouteQuery, GenerateSQL, SynthesizeAnswer, Planner

# Initialize tools
retriever = Retriever()
sqlite_tool = SQLiteTool()

# Define State
class AgentState(TypedDict):
    question: str
    format_hint: str
    route: str
    rag_results: List[Dict]
    sql_query: str
    sql_results: Dict
    constraints: str
    final_answer: Any
    citations: List[str]
    errors: List[str]
    repair_count: int
    confidence: float

# Nodes

def router_node(state: AgentState):
    print("DEBUG: Entering router_node")
    """Classifies the query."""
    predictor = dspy.Predict(RouteQuery)
    result = predictor(question=state["question"])
    print(f"DEBUG Router: {result}")
    route = getattr(result, "route", "hybrid").split()[0].lower() # Handle extra text
    if route not in ["rag", "sql", "hybrid"]:
        route = "hybrid"
    return {"route": route}

def retriever_node(state: AgentState):
    print("DEBUG: Entering retriever_node")
    """Retrieves documents."""
    results = retriever.retrieve(state["question"], top_k=3)
    return {"rag_results": results}

def planner_node(state: AgentState):
    print("DEBUG: Entering planner_node")
    """Extracts constraints from RAG results for SQL generation."""
    if state["route"] == "sql":
        return {"constraints": ""}
    
    context = "\n\n".join([r["content"] for r in state.get("rag_results", [])])
    predictor = dspy.Predict(Planner)
    result = predictor(question=state["question"], rag_results=context)
    print(f"DEBUG Planner: {result}")
    constraints = getattr(result, "constraints", "")
    return {"constraints": constraints}

def sql_generator_node(state: AgentState):
    print("DEBUG: Entering sql_generator_node")
    """Generates SQL query."""
    schema = sqlite_tool.get_schema()
    constraints = state.get("constraints", "")
    
    predictor = dspy.Predict(GenerateSQL)
    result = predictor(question=state["question"], schema=schema, constraints=constraints)
    return {"sql_query": getattr(result, "sql", "")}

def sql_executor_node(state: AgentState):
    print("DEBUG: Entering sql_executor_node")
    """Executes SQL query."""
    query = state["sql_query"]
    result = sqlite_tool.execute_sql(query)
    
    if result["error"]:
        return {"sql_results": result, "errors": [result["error"]]}
    
    return {"sql_results": result}

def synthesizer_node(state: AgentState):
    print("DEBUG: Entering synthesizer_node")
    """Synthesizes the final answer."""
    rag_context = "\n\n".join([f"[{r['id']}] {r['content']}" for r in state.get("rag_results", [])])
    sql_context = str(state.get("sql_results", {}))
    
    predictor = dspy.Predict(SynthesizeAnswer)
    result = predictor(
        question=state["question"],
        format_hint=state["format_hint"],
        rag_results=rag_context,
        sql_results=sql_context
    )
    
    citations = getattr(result, "citations", [])
    if isinstance(citations, str):
        citations = [c.strip() for c in citations.split(',')]
        
    confidence = 0.8
    
    return {
        "final_answer": getattr(result, "answer", "Error generating answer"),
        "citations": citations,
        "confidence": confidence
    }

def repair_node(state: AgentState):
    print("DEBUG: Entering repair_node")
    current_repairs = state.get("repair_count", 0)
    return {"repair_count": current_repairs + 1}

# Conditional Edges

def route_decision(state: AgentState):
    return state["route"]

def check_sql_error(state: AgentState):
    if state.get("sql_results", {}).get("error"):
        if state.get("repair_count", 0) < 2:
            return "repair"
        else:
            return "synthesizer" # Give up and try to answer or fail gracefully
    return "synthesizer"

# Graph Construction

workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("retriever", retriever_node)
workflow.add_node("planner", planner_node)
workflow.add_node("sql_generator", sql_generator_node)
workflow.add_node("sql_executor", sql_executor_node)
workflow.add_node("synthesizer", synthesizer_node)
workflow.add_node("repair", repair_node)

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "rag": "retriever",
        "sql": "sql_generator",
        "hybrid": "retriever"
    }
)

workflow.add_edge("retriever", "planner")

def planner_router(state: AgentState):
    if state["route"] == "rag":
        return "synthesizer"
    return "sql_generator"

workflow.add_conditional_edges(
    "planner",
    planner_router,
    {
        "synthesizer": "synthesizer",
        "sql_generator": "sql_generator"
    }
)

workflow.add_edge("sql_generator", "sql_executor")

workflow.add_conditional_edges(
    "sql_executor",
    check_sql_error,
    {
        "repair": "repair",
        "synthesizer": "synthesizer"
    }
)

workflow.add_edge("repair", "sql_generator") # Retry SQL generation
workflow.add_edge("synthesizer", END)

# from langgraph.checkpoint.memory import MemorySaver

# checkpointer = MemorySaver()
app = workflow.compile()
