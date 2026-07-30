import datetime as dt
import os
import re
from pathlib import Path

from pelican import signals
from pelican.readers import MarkdownReader


COLLECTIONS = {
    "groups": {"dir": "groups", "template": "group", "url": "groups/{slug}/index.html"},
    "people": {"dir": "people", "template": "person", "url": "people/{slug}/index.html"},
    "projects": {"dir": "projects", "template": "project", "url": "projects/{slug}/index.html"},
    "publications": {
        "dir": "publications",
        "template": "publication",
        "url": "publications/{slug}/index.html",
    },
    "talks": {"dir": "recent_talks", "template": "talk", "url": "talks/{slug}/index.html"},
    "posts": {"dir": "workshops", "template": "post", "url": "posts/{slug}/index.html"},
    "series": {"dir": "series", "template": "series_detail", "url": "talks/{slug}/index.html"},
    "resources": {"dir": "resources", "template": "resource", "url": "resources/{slug}/index.html"},
    "collaborators": {
        "dir": "collaborators",
        "template": "collaborator",
        "url": "collaborators/{slug}/index.html",
    },
    "software": {
        "dir": "software",
        "template": "software_detail",
        "url": "software/{slug}/index.html",
    },
    "datasets": {
        "dir": "dsst/datasets",
        "template": "dataset",
        "url": "dsst/datasets/{slug}/index.html",
    },
}


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _parse_links(value):
    links = []
    for raw in _as_list(value):
        for label, href in LINK_RE.findall(str(raw)):
            links.append({"label": label.strip(), "href": href.strip()})
    return links


def _speaker_value(values, index):
    if index >= len(values):
        return ""
    return str(values[index]).strip()


def _clean_speaker_description(value):
    return re.sub(r"\s*View Talk\s*$", "", value).strip()


def _clean_talk_title(value):
    value = re.sub(r"^\s*Talk Title\s*:\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", "", value)
    return value.strip().strip(".").strip().strip('"').strip()


def _build_speakers(metadata):
    names = _as_list(metadata.get("speakers_name"))
    titles = _as_list(metadata.get("speakers_title"))
    affiliations = _as_list(metadata.get("speakers_affiliation"))
    talk_titles = _as_list(metadata.get("speakers_talk_title"))
    images = _as_list(metadata.get("speakers_images"))
    links = _as_list(metadata.get("speakers_link"))
    descriptions = _as_list(metadata.get("speakers_description"))
    speakers = []

    for index, name in enumerate(names):
        clean_name = str(name).strip()
        if not clean_name:
            continue
        raw_title = _speaker_value(titles, index)
        raw_affiliation = _speaker_value(affiliations, index)
        raw_talk_title = _speaker_value(talk_titles, index)
        is_talk_title = raw_title.lower().startswith("talk title:")
        affiliation = raw_affiliation or ("" if is_talk_title else raw_title)
        talk_title = raw_talk_title or (
            _clean_talk_title(raw_title) if (is_talk_title or raw_affiliation) else ""
        )
        speakers.append(
            {
                "name": clean_name,
                "title": raw_title,
                "affiliation": affiliation,
                "talk_title": talk_title,
                "image": _speaker_value(images, index),
                "link": _speaker_value(links, index),
                "description": _clean_speaker_description(_speaker_value(descriptions, index)),
            }
        )
    return speakers


def _date_key(item):
    for field, fmt in (
        ("talk_month", "%B %Y"),
        ("workshop_time", "%B %Y"),
        ("date", None),
    ):
        value = item.get(field)
        if not value:
            continue
        if fmt:
            try:
                return dt.datetime.strptime(str(value), fmt)
            except ValueError:
                continue
        if hasattr(value, "date"):
            return value
    return dt.datetime.min


def _person_sort_key(person):
    title = str(person.get("title", "")).strip()
    last_name = str(person.get("last_name", "")).strip()
    if not last_name and title:
        parts = title.replace(".", "").split()
        suffixes = {"jr", "sr", "ii", "iii", "iv"}
        while parts and parts[-1].lower().strip(",") in suffixes:
            parts.pop()
        last_name = parts[-1] if parts else title
    return (last_name.lower(), title.lower())


def _dataset_sort_key(dataset):
    status_order = {"processed": 0, "downloaded": 1, "not started": 2}
    status = str(dataset.get("status", "")).strip().lower()
    title = str(dataset.get("title", "")).strip().lower()
    return (status_order.get(status, 99), title)


def _series_slug(label):
    slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    if slug == "the-machine-learning-in-brain-imaging-series":
        return "machine-learning-in-brain-imaging"
    if slug == "cmn-presentation-series":
        return "cmn-presentation-series"
    return slug


def _read_collection(generator, collection_name, spec):
    source_dir = Path(generator.settings["PATH"]) / spec["dir"]
    reader = MarkdownReader(generator.settings)
    items = []

    if not source_dir.exists():
        return items

    for path in sorted(source_dir.glob("*.md")):
        content, metadata = reader.read(str(path))
        slug = str(metadata.get("slug") or path.stem).strip("/")
        output_save_as = spec["url"].format(slug=slug)
        item_url = "/" + output_save_as.removesuffix("index.html")
        item = {
            **metadata,
            "content": content,
            "slug": slug,
            "collection": collection_name,
            "url": item_url,
        }
        if collection_name == "groups" and metadata.get("legacy_slug"):
            item["url"] = f"/{metadata['legacy_slug']}/"
        item["links"] = _parse_links(metadata.get("links"))
        item["part_of_links"] = _parse_links(metadata.get("part_of"))
        if collection_name == "talks":
            item["series_labels"] = [link["label"] for link in item["part_of_links"]]
            item["series_slugs"] = [_series_slug(label) for label in item["series_labels"]]
        if collection_name == "posts":
            item["speakers"] = _build_speakers(metadata)
        items.append(item)

    if collection_name in {"talks", "posts", "publications"}:
        items.sort(key=_date_key, reverse=True)
    elif collection_name == "groups":
        items.sort(key=lambda item: int(item.get("weight", 99)))
    elif collection_name == "collaborators":
        items.sort(key=lambda item: str(item.get("title", "")).lower())
    elif collection_name == "software":
        items.sort(
            key=lambda item: (
                int(item.get("weight", 99)),
                str(item.get("title", "")).lower(),
            )
        )
    elif collection_name == "datasets":
        items.sort(key=_dataset_sort_key)
    elif collection_name == "people":
        items.sort(key=_person_sort_key)
    else:
        items.sort(key=lambda item: str(item.get("title", "")).lower())

    return items


def _write_page(generator, template_name, output_save_as, context):
    output_path = os.path.join(generator.output_path, output_save_as)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    template = generator.get_template(template_name)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(template.render(context))


def build_collections(generator):
    collections = {}
    for name, spec in COLLECTIONS.items():
        collections[name] = _read_collection(generator, name, spec)

    people_by_slug = {str(person.get("slug")): person for person in collections["people"]}
    groups_by_slug = {str(group.get("slug")): group for group in collections["groups"]}
    groups_by_key = {}
    for group in collections["groups"]:
        for key in (group.get("slug"), group.get("legacy_slug")):
            if key:
                groups_by_key[str(key)] = group

    for group in collections["groups"]:
        aliases = {key for key in (group.get("slug"), group.get("legacy_slug")) if key}
        group["people"] = [
            person
            for person in collections["people"]
            if person.get("team_link") in aliases
            and person.get("place") == "Member"
            and person.get("employee_status", "").lower() != "alumni"
        ]
        group["people"].sort(
            key=lambda person: (
                int(person.get("sort_order", 50)),
                _person_sort_key(person),
            )
        )
        group["former_people"] = [
            person
            for person in collections["people"]
            if person.get("team_link") in aliases
            and person.get("place") == "Former Team Members"
        ]
        group["former_people"].sort(key=_person_sort_key)
        group["projects"] = [
            project
            for project in collections["projects"]
            if project.get("group") in aliases
        ]
        group["series"] = [
            series
            for series in collections["series"]
            if series.get("group") in aliases
        ]
        group["software"] = [
            tool
            for tool in collections["software"]
            if tool.get("group") in aliases
        ]
        group["software"].sort(
            key=lambda tool: (
                int(tool.get("weight", 99)),
                str(tool.get("title", "")).lower(),
            )
        )
        group["publications"] = [
            publication
            for publication in collections["publications"]
            if publication.get("group") in aliases
        ]
        group["publication_sections"] = {
            "preprint": [
                publication
                for publication in group["publications"]
                if publication.get("publication_type") == "preprint"
            ],
            "methods": [
                publication
                for publication in group["publications"]
                if publication.get("publication_type") == "methods"
            ],
            "applications": {
                "neuroscience": [
                    publication
                    for publication in group["publications"]
                    if publication.get("publication_type") == "applications"
                    and publication.get("application_category") == "neuroscience"
                ],
                "psychiatry": [
                    publication
                    for publication in group["publications"]
                    if publication.get("publication_type") == "applications"
                    and publication.get("application_category") == "psychiatry"
                ],
                "cognitive": [
                    publication
                    for publication in group["publications"]
                    if publication.get("publication_type") == "applications"
                    and publication.get("application_category")
                    == "cognitive psychology/neuroscience"
                ],
            },
        }

    for person in collections["people"]:
        person["group"] = groups_by_slug.get(str(person.get("team_link")))

    people_filter_groups = []
    for group in collections["groups"]:
        aliases = {key for key in (group.get("slug"), group.get("legacy_slug")) if key}
        count = sum(
            1
            for person in collections["people"]
            if person.get("team_link") in aliases
            and person.get("employee_status") in {"Active", "Alumni"}
        )
        if count:
            people_filter_groups.append(
                {
                    "slug": group.get("legacy_slug") or group.get("slug"),
                    "label": group.get("short_name") or group.get("title"),
                    "count": count,
                }
            )

    for publication in collections["publications"]:
        publication["group_info"] = groups_by_key.get(str(publication.get("group", "")))
        if publication["group_info"]:
            publication["group_abbreviation"] = publication["group_info"].get(
                "short_name", publication.get("group", "")
            )
        elif publication.get("group"):
            publication["group_abbreviation"] = str(publication.get("group")).upper()
        publication["people"] = [
            people_by_slug.get(str(author_id))
            for author_id in _as_list(publication.get("people"))
            if people_by_slug.get(str(author_id))
        ]

    publication_years = []
    seen_years = set()
    for publication in collections["publications"]:
        if not publication.get("date"):
            continue
        year = publication["date"].strftime("%Y")
        if year not in seen_years:
            publication_years.append(year)
            seen_years.add(year)

    talk_series_counts = {}
    talk_series_filters = []
    for talk in collections["talks"]:
        for label in talk.get("series_labels", []):
            slug = _series_slug(label)
            if slug not in talk_series_counts:
                talk_series_counts[slug] = {"slug": slug, "label": label, "count": 0}
                talk_series_filters.append(talk_series_counts[slug])
            talk_series_counts[slug]["count"] += 1

    dataset_status_counts = {}
    for dataset in collections["datasets"]:
        status = str(dataset.get("status", "Unspecified")).strip() or "Unspecified"
        dataset_status_counts[status] = dataset_status_counts.get(status, 0) + 1

    generator.context.update(
        {
            "cmn_collections": collections,
            "cmn_groups": collections["groups"],
            "people": collections["people"],
            "people_filter_groups": people_filter_groups,
            "projects": collections["projects"],
            "publications": collections["publications"],
            "publication_years": publication_years,
            "talks": collections["talks"],
            "talk_series_filters": talk_series_filters,
            "posts_list": collections["posts"],
            "series_list": collections["series"],
            "resources": collections["resources"],
            "collaborators": collections["collaborators"],
            "software": collections["software"],
            "datasets": collections["datasets"],
            "dataset_status_counts": dataset_status_counts,
            "SITEURL": generator.settings.get("SITEURL", ""),
        }
    )

    for name, spec in COLLECTIONS.items():
        for item in collections[name]:
            context = {**generator.context, **item, "item": item}
            _write_page(generator, spec["template"], spec["url"].format(slug=item["slug"]), context)

    _write_page(
        generator,
        "datasets",
        "dsst/datasets/index.html",
        {**generator.context, "item": {"title": "DSST Curated Datasets"}},
    )

    # Keep the old short URLs for the two teams while the new group URLs settle in.
    for group in collections["groups"]:
        legacy_slug = group.get("legacy_slug")
        if legacy_slug:
            context = {**generator.context, **group, "item": group}
            _write_page(generator, "group", f"{legacy_slug}/index.html", context)


def register():
    signals.article_generator_finalized.connect(build_collections)
