# Retail Analytics Copilot - Execution Script

$python = ".\.venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Error "Python executable not found at $python. Please ensure the .venv is created."
    exit 1
}

Write-Host "Step 1: Installing dependencies..."
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { Write-Error "Dependency installation failed"; exit 1 }

Write-Host "`nStep 2: Creating Database Views..."
& $python create_views.py
if ($LASTEXITCODE -ne 0) { Write-Warning "View creation failed." }

Write-Host "`nStep 3: Running DSPy Optimization (This may take a moment)..."
& $python optimize_dspy.py
if ($LASTEXITCODE -ne 0) { Write-Warning "Optimization failed or skipped." }

Write-Host "`nStep 4: Running the Agent..."
& $python run_agent_hybrid.py --batch sample_questions_hybrid_eval.jsonl --out outputs_hybrid.jsonl

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSuccess! Results written to outputs_hybrid.jsonl"
}
else {
    Write-Error "`nAgent execution failed."
}
