import base64
import re
from pathlib import Path

import pandas as pd
from json2args.data import get_data_paths


LOGO = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPIAAACFCAYAAABhT6XdAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAG5pJREFUeNrsnT1sG0mWgMvGDBa4RKSjw+IAcTiHScWBJlcbkIHDAQdrAjlc04kdHYaOpIuGjk6Khg7txNQlB1jB0FjgEgswlW1gYajwBjCHSu4HBwwpYLHYuZ+Zq8d5JT2Vqrqrq7u6m9R7QJsyf7qrq+t7f/W6+tYvv/wiWFiqJIfjnxrypUW2mtw2HH9+jK9DuU3kNtpu/mZEv/D97GfY5xZ+PsG3Z5/Vbo8Wtc9uMcgsFQC3hmBF+LoS4DDHCPdQgj2UMNfI8egxzxBu+C6APZSAzxhkFhY7wG2E6H7Bhz5HUAewSbBnEmwF9EPD90/l1keoRwwyC8P7q9sMAHcCWV4fqAHoPrHUqn2rMVD3q2SpGWSWIt3nnsXiVUXAre5KoPsYSwPQXQvQIAdwTlWw0gwySxEQdytkgV2tNCidHrrdSUBD/N2VQA8ZZJZlBDhCN3R1QU/hHC10D13uToJCAqA7ZVhoBpklFMRg0b5aktMBl7uNMXQDlVPcdNhztNAzBpllUQGGgQ7Jo7UlPL03CDS42x10t1dirHlbwjxgkFkWDWIotBguUCzs624DzAO0zklK6w0CHdQ63+bhx5ITxG358t2SQyzw/L6V59s//fF/oBqsha60TWCOfCKhjxhklkWA+NUNO22YRhuCFyJhBjf7UQL87yTMXXatWRji6rvaLqFFEFebQWYpGmJV8zxRm4RgYtg3TPe08L/gljZw26hodzyCQhJHmKE6bEvCPGGQWcqGGOB65/DVUxzYUNM8zPHY6g6mKoH9FOecXWAGSx7lNefMILP4gJQ0UGHeFbK5PWVtf/t2quBrEEu7kTDQ1SAfofUe/du9+tBguSNhv+GhaDmQ59wuGmYGmSUtxDUcoGsWtxngHUhwlcWMAljNY1QUQwn2SGsbHLMjyp3Hfib7oFskzAwyS1qQ+wbLN681/urDn2AwtoX9zqEQAtYf2tSXUE8097tbouutYmaXECQzzAwySxqIwdp9q0HUlgBPEJqyXVvICPeo+42VZv2SgP4Ss9mg3F6FhJlBZknjUk+Im/hMAtxD6/t1xZp7ikD3NQvdK9jlnsMJSw1JmPsOig4UY8tnaopBZknrUsPg3JIQ19DSVbmSC4DuaBY6qUY6hOvfwvrskYMiOUXLnApmruxicYE4QohP/+unn/9OQtxGF7vq5ZgAzbvfvp1C8g1cbAHTQ+LXrPlxQW1YRYUnMH9w7tDmHltklhAgg0Wr/f4///t3R3/8338Si3ln0/zeYmmde5p1/"

def load_data() -> tuple[str, pd.DataFrame]:
    # get the paths
    data_paths = get_data_paths()
    
    # extract the dataframe path
    df_path = data_paths['dataframe']

    # check the extension
    ext = Path(df_path).suffix.lower()

    if ext == '.csv':
        data = pd.read_csv(df_path)
    elif ext == '.parquet':
        data = pd.read_parquet(df_path)

    return Path(df_path).stem, data


ASSOC_HEATMAP_CSS_PATTERN = re.compile(
    r"span\.association-graph-source::before\s*\{\s*content:\s*url\(data:image/png;base64,([A-Za-z0-9+/=]+)\)"
)


def extract_associations_thumbnail(html_path: str, out_path: str) -> bool:
    """Extract the Associations heatmap from a sweetviz HTML report and save as PNG."""
    try:
        html = Path(html_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    m = ASSOC_HEATMAP_CSS_PATTERN.search(html)
    if not m:
        return False
    try:
        raw = base64.b64decode(m.group(1))
    except Exception:
        return False
    try:
        Path(out_path).write_bytes(raw)
    except OSError:
        return False
    return True
