import dspy

class RouteQuery(dspy.Signature):
    """Classify query as rag, sql, or hybrid.
    
    rag: Questions about policies, marketing calendars, definitions, or static text.
    sql: Questions requiring data aggregation, counting, or filtering from the database (orders, products, customers).
    hybrid: Questions requiring both database data and context from documents (e.g., "revenue during Summer 1997" where dates are in docs).
    """
    question = dspy.InputField()
    route = dspy.OutputField(desc="one of: rag, sql, hybrid")

class GenerateSQL(dspy.Signature):
    """Generate SQLite query from natural language using the provided schema and constraints."""
    question = dspy.InputField()
    schema = dspy.InputField(desc="Schema of available tables")
    constraints = dspy.InputField(desc="Specific constraints like date ranges or formulas extracted from docs")
    sql = dspy.OutputField(desc="Valid SQLite query. Use 'Orders', 'Order Details', 'Products', 'Customers', 'Categories' tables.")

class SynthesizeAnswer(dspy.Signature):
    """Produce a typed answer with citations based on RAG and SQL results."""
    question = dspy.InputField()
    format_hint = dspy.InputField(desc="Expected output format (e.g., int, float, dict)")
    rag_results = dspy.InputField(desc="Context from documents")
    sql_results = dspy.InputField(desc="Data from database execution")
    answer = dspy.OutputField(desc="Final answer matching the format_hint exactly")
    citations = dspy.OutputField(desc="List of sources used (table names and doc chunk IDs)")

class Planner(dspy.Signature):
    """Extract constraints and relevant information from retrieved documents to help generate SQL."""
    question = dspy.InputField()
    rag_results = dspy.InputField()
    constraints = dspy.InputField(desc="Extracted date ranges, formulas, or category names to be used in SQL")
