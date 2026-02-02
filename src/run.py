import os

from ydata_profiling import ProfileReport
import sweetviz as sv
from json2args import get_parameter

from lib import load_data, LOGO, extract_associations_thumbnail

# parse parameters
parameter = get_parameter(typed=True)

# check if a toolname was set in env
toolname = os.environ.get('TOOL_RUN', 'profile').lower()

def main():
    if toolname != 'profile':
        raise ValueError("This toolbox only supports the 'profile' tool")

    name, df = load_data()

    profile = df.profile_report(
        title=parameter.title,
        dataset={
            "description": "This profiling report was generated using: https://github.com/vforwater/tool_dataset_profiler",
            "copyright_holder": "V-FOR-WaTer",
            "copyright_year": 2026,
            "url": "https://portal.vforwater.de"
        }
    )
    profile.config.html.style.logo = LOGO

    # generate the output
    profile.to_file(f"/out/{name}_report.html")
    js = profile.to_json()

    with open(f"/out/{name}_report.json", 'w') as f:
        f.write(js)

    # create the sweetviz report
    report = sv.analyze(df)
    stats_path = f"/out/{name}_stats.html"
    report.show_html(stats_path, layout='vertical', open_browser=False)

    # extract Associations heatmap as THUMBNAIL.png
    extract_associations_thumbnail(stats_path, "/out/THUMBNAIL.png")

if __name__ == "__main__":
    main()