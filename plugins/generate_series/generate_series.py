import datetime
import os
import re
from pelican import signals
from pelican.readers import MarkdownReader
import json


def generate_series(generator):
    """Generate custom pages for people based on their articles."""
    # Loop over all articles and filter for 'People' category (optional)
    series_dir = os.path.join(generator.settings["PATH"], "series")

    series_list = []

    for filename in os.listdir(series_dir):
        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(series_dir, filename)
        reader = MarkdownReader(generator.settings)
        content, metadata = reader.read(file_path)

        context = {
            **metadata,
            "content": content,
        }

        series_list.append(context)

    # Sort talks by 'Talk_month' in descending order
    series_list.sort(key=lambda x: x.get("name", ""))
    generator.context["series_list"] = series_list


def register():
    """Register the plugin to Pelican's signal system."""
    signals.article_generator_finalized.connect(generate_series)
