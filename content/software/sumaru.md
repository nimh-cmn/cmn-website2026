Title: Sumaru
Slug: sumaru
Group: cmn
External_url: https://github.com/pmolfese/sumaru/
Summary: A surface viewer written in Rust with AFNI/SUMA compatibility
Maintainer: Peter Molfese
Weight: 6

Sumaru is an experimental Rust-based viewer for inspecting SUMA-style neuroimaging data in a lightweight, native application. The project is designed around compatibility with common AFNI/SUMA workflows, including GIFTI surfaces, `.spec` scenes, `.niml.dset` and `.gii.dset` overlays, `.niml.roi` regions, and NIfTI volume data.

![Sumaru viewing an inflated cortical surface with a statistical overlay](/images/software/sumaru-hero-surface-overlay.png)

The viewer supports interactive surface visualization, statistical overlays, region-of-interest inspection, paired-hemisphere layouts, and orthogonal volume slice planes. This makes it useful for practical quality-control questions that arise during multimodal neuroimaging work, such as checking surface-volume alignment, verifying overlay placement, and inspecting values at specific cortical locations.

Sumaru is also a scientific software experiment in building a testable neuroimaging viewer architecture. Its Rust data model keeps file parsing, coordinate handling, overlays, ROI state, and AFNI/SUMA interoperability separate from the graphical interface, making core behavior easier to validate and extend. Rendering is powered by `wgpu`, allowing responsive interaction with surface and volume scenes.

The project is research software and remains under active development. It is intended for investigators and developers who want a compact native viewer, a transparent codebase for experimenting with neuroimaging visualization methods, or a complementary tool for inspecting AFNI/SUMA-compatible datasets.
