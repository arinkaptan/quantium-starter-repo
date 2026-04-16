import pytest
import os
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session", autouse=True)
def add_chromedriver_to_path():
    """Automatically download chromedriver and add it to PATH."""
    chromedriver_path = ChromeDriverManager().install()
    chromedriver_dir = os.path.dirname(chromedriver_path)
    os.environ["PATH"] = chromedriver_dir + os.pathsep + os.environ.get("PATH", "")