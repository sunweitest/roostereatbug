import requests
import json
from generate_data import get_llm


class BugProcessor:
    """处理 bug 数据的类"""
    
    def __init__(self, api_url="http://127.0.0.1:8000/bugs/"):
        """初始化 API URL"""
        self.api_url = api_url

    def fetch_bugs(self, module_name):
        """从模块名称获取并解析 JSON 格式的 bug 数据"""
        raw_bugs = get_llm(module_name)
        
        # 去除多余的字符，确保是有效的 JSON 字符串
        stripped_bugs = raw_bugs.strip("```json\n").strip("```")
        
        try:
            parsed_data = json.loads(stripped_bugs)
            print(f"Data successfully parsed for module '{module_name}':", parsed_data)
            return parsed_data
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON for module '{module_name}':", e)
            return None

    def post_bug_to_api(self, bug_data):
        """将单个 bug 数据发送到 API"""
        try:
            response = requests.post(self.api_url, json=bug_data)
            response.raise_for_status()  # 检查 HTTP 请求是否成功
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to post bug data to API: {e}")
            return None

    def process_module(self, module_name):
        """处理单个模块，提取 bug 并发送到 API"""
        data = self.fetch_bugs(module_name)
        if not data or "buglist" not in data:
            print(f"No valid buglist found for module '{module_name}'")
            return
        
        bug_list = data["buglist"]
        # print(f"Bug list for module '{module_name}':", bug_list)
        print(f"Number of bugs: {len(bug_list)}")
        
        for bug in bug_list:
            api_response = self.post_bug_to_api(bug)
            if api_response:
                print(f"API response for bug: {api_response}")
            else:
                print(f"Failed to post bug: {bug}")

    def process_modules(self, modules):
        """处理模块列表"""
        for module in modules:
            self.process_module(module)


if __name__ == "__main__":
    # 初始化 BugProcessor 实例
    bug_processor = BugProcessor()
    # 定义模块列表
    modules = ["支付功能", "充值功能", "提现功能"]
    # 处理模块
    bug_processor.process_modules(modules)
