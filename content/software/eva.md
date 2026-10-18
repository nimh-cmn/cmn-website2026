Title: EVA: EEG Viewer and Analysis
Slug: eva
Group: cmn
External_url: https://github.com/pmolfese/EVA
Summary: A native macOS application for viewing, cleaning, and analyzing EEG recordings
Maintainer: Peter Molfese
Weight: 5

EVA is a native macOS application for opening, viewing, cleaning, and exploring electroencephalography (EEG) recordings. Short for **Electrophysiology Viewer and Analysis**, EVA keeps the signal visible while researchers inspect processing decisions, review data quality, and move from continuous recordings toward analysis-ready data.

![EVA waveform view with channels, events, and analysis tools](/images/software/eva-waveform-overview.png)

The central waveform view brings channels, events, processing history, and commonly used tools into one workspace. Researchers can hide or mark bad channels, interpolate channels, apply bandpass and notch filters, use average referencing, browse events, add markers, and inspect sensor topographies without losing sight of the underlying recording.

EVA also supports broader EEG cleaning and analysis workflows, including simultaneous EEG/fMRI gradient-artifact correction, user-defined artifact detection and cleaning, independent component analysis with Core ML ICLabel support, epoching, category averages, butterfly plots, and single-trial peak and amplitude measurements. Explainable channel- and segment-health scores show the metrics behind a quality assessment rather than presenting a black-box label.

The application reads EGI/MagStim MFF recordings, BrainVision, EDF/EDF+, Persyst, and BESA average or multiplexed files. Processed continuous, epoched, and averaged recordings can be exported to MFF, while health metrics can be saved as JSON for review and future model development.

Built with SwiftUI, Accelerate/vDSP, Core ML, and Swift concurrency, EVA is designed to feel at home on macOS while keeping computationally intensive work responsive. It is intended as an open, inspectable addition to an EEG laboratory's toolbox and complements established projects such as MNE-Python, FieldTrip, and EEGLAB.
