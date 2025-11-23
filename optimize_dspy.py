import dspy
from dspy.teleprompt import BootstrapFewShot
from agent.dspy_signatures import GenerateSQL
from agent.tools.sqlite_tool import SQLiteTool

def optimize_sql_generator():
    # Configure LM
    lm = dspy.OllamaLocal(
        model="llama3.1:8b"
    )
    dspy.settings.configure(lm=lm)

    # Create training examples
    # In a real scenario, these would be carefully curated.
    examples = [
        dspy.Example(
            question="Total revenue from Beverages",
            schema="Table: Products\n - ProductID (INTEGER)\n - ProductName (TEXT)\n - CategoryID (INTEGER)\n\nTable: Categories\n - CategoryID (INTEGER)\n - CategoryName (TEXT)\n\nTable: Order Details\n - UnitPrice (FLOAT)\n - Quantity (INTEGER)\n - Discount (FLOAT)\n - ProductID (INTEGER)",
            constraints="",
            sql="SELECT SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) FROM \"Order Details\" od JOIN Products p ON od.ProductID = p.ProductID JOIN Categories c ON p.CategoryID = c.CategoryID WHERE c.CategoryName = 'Beverages'"
        ).with_inputs("question", "schema", "constraints"),
        dspy.Example(
            question="Top 3 products by price",
            schema="Table: Products\n - ProductID (INTEGER)\n - ProductName (TEXT)\n - UnitPrice (FLOAT)",
            constraints="",
            sql="SELECT ProductName, UnitPrice FROM Products ORDER BY UnitPrice DESC LIMIT 3"
        ).with_inputs("question", "schema", "constraints")
    ]

    # Define metric
    def validate_sql(example, pred, trace=None):
        return pred.sql.upper().startswith("SELECT")

    # Optimize
    teleprompter = BootstrapFewShot(metric=validate_sql, max_bootstrapped_demos=2, max_labeled_demos=2)
    optimized_program = teleprompter.compile(dspy.Predict(GenerateSQL), trainset=examples)
    
    # Save optimized program (in a real app, we'd save this to disk)
    print("Optimization complete.")
    # For this task, we just show it runs. In a real system, we'd replace the module in the agent.

if __name__ == "__main__":
    optimize_sql_generator()
