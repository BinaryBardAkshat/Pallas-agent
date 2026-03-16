import pytest
from tools.file_tools import FileTool
import tempfile
import os


@pytest.fixture
def tmp_path_str(tmp_path):
    return str(tmp_path)


def test_file_write_and_read(tmp_path_str):
    tool = FileTool()
    path = os.path.join(tmp_path_str, "test.txt")
    write_result = tool(action="write", path=path, content="hello pallas")
    assert "Written" in write_result

    content = tool(action="read", path=path)
    assert content == "hello pallas"


def test_file_list(tmp_path_str):
    tool = FileTool()
    tool(action="write", path=os.path.join(tmp_path_str, "a.txt"), content="a")
    tool(action="write", path=os.path.join(tmp_path_str, "b.txt"), content="b")
    listing = tool(action="list", path=tmp_path_str)
    assert "a.txt" in listing
    assert "b.txt" in listing


def test_file_not_found(tmp_path_str):
    tool = FileTool()
    result = tool(action="read", path=os.path.join(tmp_path_str, "missing.txt"))
    assert "not found" in result.lower()


def test_terminal_tool_safe():
    from tools.file_tools import TerminalTool
    tool = TerminalTool()
    out = tool(command="echo pallas_ok")
    assert "pallas_ok" in out


def test_terminal_tool_blocked():
    from tools.file_tools import TerminalTool
    tool = TerminalTool()
    out = tool(command="rm -rf /")
    assert "Blocked" in out
