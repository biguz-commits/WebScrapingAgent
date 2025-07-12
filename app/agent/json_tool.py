from pathlib import Path
from typing import List, Optional
from langchain.tools import tool
from pydantic import BaseModel, ValidationError
import json

class UnicattEntry(BaseModel):
    """Schema for a single Unicatt article entry."""
    title: str
    pretitle: Optional[str] = None
    text: Optional[str] = None

@tool
def get_unicatt_json(args_schema=None) -> dict:
    """
    Reads and validates the contents of the data/unicatt.jsonl file.
    Returns a dictionary in 'content_and_artifact' format, where 'content' is a textual summary
    and 'artifact' contains the full validated entries.

    Each entry must include 'title', and may optionally include 'pretitle' and 'text'.
    This tool is useful for retrieving academic news and institutional content from Università Cattolica.
    """
    json_path = Path(__file__).parent / "data" / "unicatt.jsonl"
    if not json_path.exists():
        return {
            "content": "The file data/unicatt.jsonl does not exist.",
            "artifact": []
        }

    validated_entries: List[UnicattEntry] = []
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                try:
                    raw = json.loads(line)
                    entry = UnicattEntry(**raw)
                    validated_entries.append(entry)
                except ValidationError as ve:
                    return {
                        "content": f"Validation error at line {i}: {ve}",
                        "artifact": []
                    }

        summary = f"Loaded {len(validated_entries)} Unicatt entries successfully."
        artifact = [entry.dict() for entry in validated_entries]

        return {
            "content": summary,
            "artifact": artifact
        }

    except Exception as e:
        return {
            "content": f"Unexpected error reading the file: {e}",
            "artifact": []
        }
