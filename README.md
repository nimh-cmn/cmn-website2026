# CMN Website 2026

Pelican site for the Center for Multimodal Neuroimaging.

The site keeps the legacy CMN content but reorganizes it around simple Markdown collections inspired by the SFIM site:

- `content/groups`: CMN, Machine Learning Core, and Data Science and Sharing Team.
- `content/people`: one Markdown file per person, copied from the legacy site.
- `content/projects`: one Markdown file per project.
- `content/publications`: one Markdown file per publication.
- `content/recent_talks`: copied talk records from the legacy site.
- `content/workshops`: copied workshop records from the legacy site.
- `content/resources`: PDFs and shared resources with lightweight landing pages.
- `content/collaborators`: collaborative cores and teams shown on the front page.
- `content/software`: tools and software shown on the front page and group pages.

## Local Build

```bash
make build
```

## Local Preview

Use the explicit settings/content form instead of bare `pelican -r -l`.
With Pelican 4.12, bare autoreload/listen can miss `pelicanconf.py` and crash
with `TypeError: expected str, bytes or os.PathLike object, not NoneType`.

```bash
make serve
```

Then open `http://127.0.0.1:8000`.

## Front-Page Collaborator Image

The composite image is generated from `content/collaborators` and the existing
brain image:

```bash
make image
make build
```

## Adding Content

Add a new Markdown file to the relevant collection folder. Pelican metadata goes at the top as `Field: value`, followed by normal Markdown content.

Publication starter:

```markdown
Title: Example Paper Title
Slug: example-paper-title
Date: 2026-01-01
Citation: First Author; Second Author.
Venue: Journal or conference
Group: mlc
Publication_type: methods
DOI: 10.0000/example
Paper_url: https://example.org/paper
Data_url: https://example.org/data
Code_url: https://github.com/example/repo

Abstract or notes go here.
```

For Machine Learning Core publications, use:

- `Publication_type: preprint`
- `Publication_type: methods`
- `Publication_type: applications`

For applications, add one of:

- `Application_category: neuroscience`
- `Application_category: psychiatry`
- `Application_category: cognitive psychology/neuroscience`

Project starter:

```markdown
Title: Project Name
Slug: project-name
Group: cmn
Summary: One sentence summary used in lists.
People: Peter Molfese, 48

Full project description goes here.
```

The optional `People:` field connects a project to person profile pages. Use a
comma- or semicolon-separated list of person names or legacy numeric slugs.

Talk starter:

```markdown
Title: Talk Title
Date: 2026-01-01
Talk_month: January 2026
Slug: talk-title
Speaker_Slug: 48
Part_of: [CMN Presentation Series](/talks/cmn-presentation-series/)
External_url: https://example.org/talk

Talk summary or abstract goes here.
```

Talks appear on person profile pages when `Speaker_Slug:`, `Speaker:`, or
`Speakers:` matches a person name or legacy numeric slug. Use `External_url:`,
`Talk_url:`, or `Video_url:` when the profile/talks-list card should link to
another website instead of the local generated talk page.

Person profile section links:

Profile pages automatically show top anchor links for any sections that exist:
`Projects`, `Talks`, `Publications`, and `Software`.

These relationships are driven by metadata:

- Projects: `People:` on project files.
- Talks: `Speaker_Slug:`, `Speaker:`, or `Speakers:` on talk files.
- Publications: `People:` on publication files.
- Software: `Maintainer:` on software files.

# cmn-website2026
