from openwpm import task_manager
from openwpm.commands.utils.webdriver_utils import parse_neterror
from openwpm.utilities import db_utils

from .openwpmtest import OpenWPMTest


def test_parse_neterror():
    text = (
        "selenium.common.exceptions.WebDriverException: "
        "Message: Reached error page: "
        "about:neterror?e=dnsNotFound&u=http%3A//medmood.it/&c=UTF-8&"
        "f=regular&d=We%20can%E2%80%99t%20"
        "connect%20to%20the%20server%20at%20medmood.it."
    )
    assert parse_neterror(text) == "dnsNotFound"


class TestCustomFunctionCommand(OpenWPMTest):
    def get_config(self, data_dir=""):
        return self.get_test_config(data_dir)

    def test_parse_neterror_integration(self):
        manager_params, browser_params = self.get_config()
        manager = task_manager.TaskManager(manager_params, browser_params)
        manager.get("http://website.invalid")
        manager.close()

        get_command = db_utils.query_db(
            manager_params.database_name,
            "SELECT command_status, error FROM crawl_history WHERE command = \"<class 'openwpm.commands.types.GetCommand'>\"",
            as_tuple=True,
        )[0]

        assert get_command[0] == "neterror"
        assert get_command[1] == "dnsNotFound"
