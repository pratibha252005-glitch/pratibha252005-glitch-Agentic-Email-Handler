# Agent Instructions: The Ponytail Philosophy

> *"The best code is the code you never wrote."*

When modifying or extending this codebase, every agent MUST evaluate solutions using the **7-Rung Ladder of Laziness** sequentially before writing new code:

1. **Rung 1: Does this need to exist at all? (YAGNI)**
   - Reject speculative abstractions, dead imports, and unused dependencies.
2. **Rung 2: Is it already in this codebase? (Reuse)**
   - Reuse existing clients, toolkits, and functions instead of re-instantiating.
3. **Rung 3: Does the standard library do it? (Stdlib first)**
   - Use built-in Python constructs (`set`, `dict.get()`, `split(..., 2)`) before pulling in packages or custom classes.
4. **Rung 4: Does a native framework feature cover it?**
   - Use native LangGraph graph primitives and CrewAI task/agent structures without redundant OOP wrappers.
5. **Rung 5: Does an already-installed dependency solve it?**
   - Use existing LangChain / CrewAI utilities before adding new packages.
6. **Rung 6: Can it be done in one line?**
   - Prefer concise expressions and pure functions over multi-line class scaffolding.
7. **Rung 7: Only then write minimal code.**
   - Write the strict minimum code necessary that is correct, secure, and preserves error boundaries.

### Guardrails (Lazy, never negligent)
- Always protect security, authentication, and trust boundaries.
- Ensure graceful handling of missing environment variables and state keys.
- Preserve backward-compatibility for existing public module interfaces.
