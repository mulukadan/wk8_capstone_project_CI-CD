import json
from pathlib import Path

MCP_VERSION = "1.2.0"

PROJECT_ROOT = Path(__file__).resolve().parent
CLINICS_FILE = PROJECT_ROOT / "clinics.json"


VALID_ITEMS = {
    "amoxicillin",
    "ors_sachets",
    "malaria_kits",
}


def load_clinics():
    """
    Load clinic stock and logistics data.

    For the capstone this remains a local fixture.
    """

    if not CLINICS_FILE.exists():
        return []

    with open(
        CLINICS_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def check_stock(
    clinic_name: str,
    item: str,
):
    """
    Check whether a supported item is available
    at the requested clinic.
    """

    if item not in VALID_ITEMS:
        return {
            "ok": False,
            "error": "unsupported_item",
            "mcp_version": MCP_VERSION,
        }

    clinics = load_clinics()

    for clinic in clinics:

        if clinic["name"].lower() == clinic_name.lower():

            quantity = clinic.get("stock", {}).get(
                item,
                0,
            )

            return {
                "ok": True,
                "clinic": clinic["name"],
                "item": item,
                "quantity": quantity,
                "mcp_version": MCP_VERSION,
            }

    return {
        "ok": False,
        "error": "clinic_not_found",
        "mcp_version": MCP_VERSION,
    }


def get_server_info():
    """
    Return version and required tool names.

    The CI health probe will use this.
    """

    return {
        "name": "afyaplus-logistics-mcp",
        "version": MCP_VERSION,
        "tools": [
            "check_stock",
            "plan_delivery_route",
            "get_delivery_eta",
        ],
    }


def plan_delivery_route(
    clinic_name: str,
):
    return {
        "ok": True,
        "clinic": clinic_name,
        "route": "stub-route",
        "mcp_version": MCP_VERSION,
    }


def get_delivery_eta(
    clinic_name: str,
):
    return {
        "ok": True,
        "clinic": clinic_name,
        "eta_minutes": 45,
        "mcp_version": MCP_VERSION,
    }


if __name__ == "__main__":

    print(
        json.dumps(
            get_server_info(),
            indent=2,
        )
    )
