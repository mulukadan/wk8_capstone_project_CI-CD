import sys

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT),
)


from logistics_mcp_versioned import get_server_info

EXPECTED_MCP_VERSION = "1.2.0"

REQUIRED_TOOLS = {
    "check_stock",
    "plan_delivery_route",
    "get_delivery_eta",
}


def main():

    print()
    print("=" * 70)
    print("AFYAPLUS MCP HEALTH CHECK")
    print("=" * 70)

    info = get_server_info()

    server_name = info.get("name")

    version = info.get("version")

    tools = set(info.get("tools", []))

    print(f"Server: {server_name}")

    print(f"Version: {version}")

    print(f"Tools found: " f"{sorted(tools)}")

    print()

    # -----------------------------------
    # VERSION CHECK
    # -----------------------------------

    if version != EXPECTED_MCP_VERSION:

        print("MCP HEALTH: FAILED")

        print(f"Expected version: " f"{EXPECTED_MCP_VERSION}")

        print(f"Actual version: " f"{version}")

        sys.exit(1)

    # -----------------------------------
    # REQUIRED TOOL CHECK
    # -----------------------------------

    missing_tools = REQUIRED_TOOLS - tools

    if missing_tools:

        print("MCP HEALTH: FAILED")

        print("Missing required tools:")

        for tool in sorted(missing_tools):
            print(f"- {tool}")

        sys.exit(1)

    print("MCP HEALTH: PASSED")

    print("All required tools are available.")

    sys.exit(0)


if __name__ == "__main__":
    main()
