# Test Writing

## Description
This skill enables Pallas to write comprehensive, maintainable tests for any function, module, or system. It covers unit tests, integration tests, edge cases, and the appropriate use of mocks and fixtures — with the goal of tests that actually catch real bugs.

## When to Use
- When the user asks for tests for a function or module they've just written
- When adding a new feature and TDD-style test-first development is appropriate
- When a bug is fixed and a regression test should be added
- When improving coverage on an existing codebase

## Instructions
You are writing tests that will be read, maintained, and relied upon by a team. Prioritize clarity, correctness, and real coverage over raw line coverage percentages.

**Before Writing — Understand the Contract**
For each function or module under test, establish:
- What are the valid inputs and their types?
- What are the expected outputs or side effects for each input class?
- What are the documented error conditions?
- What external dependencies exist (DB, HTTP, filesystem, time)?

**Test Structure — Follow AAA**
Every test should follow Arrange-Act-Assert:
```python
def test_create_user_returns_id_on_success():
    # Arrange
    db = MockDatabase()
    service = UserService(db)

    # Act
    result = service.create_user(name="Alice", email="alice@example.com")

    # Assert
    assert result["id"] is not None
    assert db.users[result["id"]]["email"] == "alice@example.com"
```

**Coverage Checklist — write tests for each:**
1. Happy path — the typical, expected use case
2. Empty / zero / null inputs — what happens with nothing?
3. Boundary values — min, max, off-by-one
4. Invalid type or format inputs — should raise or return error, not crash silently
5. Large inputs — performance and memory behavior
6. Concurrent or repeated calls — idempotency if relevant
7. Each documented error condition — does it actually raise the right exception?

**Mocking Rules**
- Mock external I/O (HTTP, DB, filesystem, time) — never make real network calls in unit tests
- Do not mock the unit under test itself
- Do not over-mock: if two real classes work together correctly, let them — that is integration coverage
- Use `pytest` fixtures for reusable setup; avoid code duplication across test functions

**Test Naming**
Name tests as: `test_[function]_[scenario]_[expected_outcome]`
Example: `test_divide_by_zero_raises_value_error`

**Integration Tests**
When writing integration tests:
- Use a real (but ephemeral) database, not a mock
- Test the full call chain end-to-end
- Clearly separate them from unit tests (different directory or marker)

**Output Format**
Provide all tests in a single file. Include a brief comment above each test group explaining what aspect is being tested. Do not pad coverage with trivial assertions.

## Examples
- "Write unit tests for this `parse_config` function."
- "Add regression tests for the bug I just fixed in the payment processor."
- "Write integration tests for the user registration endpoint."
