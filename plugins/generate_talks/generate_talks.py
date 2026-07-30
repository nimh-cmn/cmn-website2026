import datetime
import os
import re
from pelican import signals
from pelican.readers import MarkdownReader
import json


def get_speaker_info(generator):
    people_dir = os.path.join(generator.settings["PATH"], "people")
    people_info = {}
    for filename in os.listdir(people_dir):
        if not filename.endswith(".md"):
            continue
        file_path = os.path.join(people_dir, filename)
        reader = MarkdownReader(generator.settings)
        _, metadata = reader.read(file_path)
        # metadata["date"] = ""
        # if not metadata["image"]:
        #     metadata["image"] = "event.jpg"

        # Prepare context for each person's page
        slug = metadata.get("slug")

        people_info[slug] = metadata

    return people_info


def generate_talks(generator):
    """Generate custom pages for people based on their articles."""
    # Loop over all articles and filter for 'People' category (optional)
    people_dir = os.path.join(generator.settings["PATH"], "recent_talks")
    talks_list = []

    people_info = get_speaker_info(generator)

    
    cmnpres_talks = []
    mltalks_talks = []
    for filename in os.listdir(people_dir):
        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(people_dir, filename)
        reader = MarkdownReader(generator.settings)
        content, metadata = reader.read(file_path)

        # Regular expression to match text inside [] and ()
        pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        part_of_list = []

        for entry in metadata.get("part_of", "").split(","):
            # Extract the parts using re.search
            match = re.search(pattern, entry)

            if match:
                text = match.group(1)  # Text inside []
                link = match.group(2)  # Text inside ()
                part_of_list.append((text, link))
                

        links = []
        for entry in metadata.get("links", "").split(","):
            # Extract the parts using re.search
            match = re.search(pattern, entry)

            if match:
                text = match.group(1)  # Text inside []
                link = match.group(2)  # Text inside ()
                links.append((text, link))

        context = {
            **metadata,
            "content": content,
            "part_of": part_of_list,
            "links": links,
            "speaker": people_info.get(metadata.get("speaker_slug")),
        }

        talks_list.append(context)

        if part_of_list:
            link = part_of_list[0][1]
            if link == "/cmnpres":
                cmnpres_talks.append(context)
            elif link == "/mltalks":
                mltalks_talks.append(context)



    # Sort talks by 'Talk_month' in descending order
    talks_list.sort(key=lambda x: datetime.datetime.strptime(x.get("talk_month", ""), "%B %Y"), reverse=True)
    generator.context["talks_list"] = talks_list
    generator.context["talks_dict"] = generate_talks_dict(talks_list)

    # Sort series talks by 'Talk_month' in descending order
    cmnpres_talks.sort(key=lambda x: datetime.datetime.strptime(x.get("talk_month", ""), "%B %Y"), reverse=True)

    mltalks_talks.sort(key=lambda x: datetime.datetime.strptime(x.get("talk_month", ""), "%B %Y"), reverse=True)

    generator.context["series_talks"] = {"cmnpres": cmnpres_talks, "mltalks": mltalks_talks}

def generate_talks_dict(talks_list):
    talks_dict = {}
    for article in talks_list:
        slug = str(article["slug"])
        talks_dict[slug] = article
    return talks_dict

def register():
    """Register the plugin to Pelican's signal system."""
    signals.article_generator_finalized.connect(generate_talks)
